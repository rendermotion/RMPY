from maya.api import OpenMaya
from maya.api import OpenMayaAnim
import maya.cmds as cmds
import re
import pymel.core as pm
from math import isclose
class ApiComponents(object):
    def __init__(self):
        self.components_object = None
        self.selection_list = OpenMaya.MSelectionList()

    def set_selection_list(self, components):
        for closest_point_uv in components:
            print(closest_point_uv)
            other_list = OpenMaya.MSelectionList().add(closest_point_uv)
            self.selection_list.merge(other_list)
            print(self.selection_list.getDagPath(0))

        print(self.selection_list.length())
        print(self.selection_list.getDagPath(0))

    def index_list(self):
        for closest_point_uv in range(self.selection_list.length()):
            dag_path = self.selection_list.getDagPath(closest_point_uv)
            vertex_dag_path, vertex_object = self.selection_list.getComponent(closest_point_uv)

    def component_string_values(self, component_string):
        search_re = re.search("\\[(\d+)\\]", component_string)
        if search_re:
            return int(search_re.group(1))
        search_re = re.search("\\[(\d+):(\d+)\\]", component_string)
        if search_re:
            return {int(search_re.group(1)), int(search_re.group(2))}
        else:
            return None


class SmoothSkin(object):
    def __init__(self):
        self._mesh = None
        self._skin_cluster = None
        self._joint_list = []
        self._surface = None
        self._surface_name = None

    @property
    def skin_cluster(self):
        return self._skin_cluster

    @skin_cluster.setter
    def skin_cluster(self, skin_cluster):
        self._skin_cluster = self.getMFnSkinCluster(skin_cluster)

    @property
    def mesh(self):
        return self._mesh

    @mesh.setter
    def mesh(self, scene_transform):
        if cmds.objectType(scene_transform) == 'mesh':
            self._mesh = self.getMfnMesh(scene_transform)
        else:
            mesh_shape = cmds.listRelatives(scene_transform, shapes=True)
            self._mesh = self.getMfnMesh(mesh_shape[0])
    @property
    def surface(self):
        return self._surface

    @surface.setter
    def surface(self, nurbs_surface):
        if cmds.objectType(nurbs_surface) == 'nurbsSurface':
            self._surface = self.getMfnNurbs(nurbs_surface)
            self._surface_name =cmds.listRelatives(nurbs_surface, parent=True)[0]
        else:
            mesh_shape = cmds.listRelatives(nurbs_surface, shapes=True)
            self._surface_name = nurbs_surface
            self._surface = self.getMfnNurbs(mesh_shape[0])

    @property
    def joint_list(self):
        return self._joint_list

    @joint_list.setter
    def joint_list(self, string_joint_list):
        self._joint_list = []
        for closest_point_uv in string_joint_list:
            dag_path = self.getDagPath(closest_point_uv)
            self._joint_list.append(dag_path)

    def getDagPath(self, name):
        sel = OpenMaya.MSelectionList()
        try:
            sel.add(str(name))
        except RuntimeError as e:
            return e
        return sel.getDagPath(0)

    def getMObject(self, name):
        sel = OpenMaya.MSelectionList()
        try:
            sel.add(str(name))
        except RuntimeError as e:
            return e
        m_object = sel.getDependNode(0)
        return m_object

    def MDoubleArray(self, length=0, value=0):
        """
        Returns an MDouble Array initialized.
        keyword arguments
        _________________
        length: the number of elements on the array.
        value: the value at what all the elements on the array will be initialized.
        Returns
        _______
        return: The initialized MDoubleArray
        """
        double_array = OpenMaya.MDoubleArray()
        double_array.setLength(length)
        for each in range(length):
            double_array[each] = value
        return double_array
    def get_skincluster_from_mesh(self):
        for closest_point_uv in cmds.listHistory(self.mesh.name(), pruneDagObjects=True):
            if cmds.objectType(closest_point_uv) == 'skinCluster':
                self.skin_cluster = closest_point_uv

    def get_mesh_from_skin_cluster(self):
        for closest_point_uv in cmds.listHistory(self.skin_cluster.name(), future=True):
            if cmds.objectType(closest_point_uv) == 'mesh':
                self.mesh = closest_point_uv
    @classmethod
    def by_skin_cluster(cls, skin_cluster):
        new_instance = cls()
        new_instance.skin_cluster = skin_cluster
        new_instance.get_mesh_from_skin_cluster()

    @classmethod
    def by_geometry(cls, scene_transform):
        new_instance = cls()
        new_instance.mesh = scene_transform
        new_instance.get_skincluster_from_mesh()
        return new_instance

    def getMFnSkinCluster(self, name):
        m_object = self.getMObject(name)
        return OpenMayaAnim.MFnSkinCluster(m_object)

    def getMfnMesh(self, name):
        dagPath = self.getDagPath(name)
        return OpenMaya.MFnMesh(dagPath)

    def getMfnNurbs(self, name):
        surface_path = self.getDagPath(name)
        return OpenMaya.MFnNurbsSurface(surface_path.node())

    def getMfnTransform(self, name):
        surface_path = self.getDagPath(name)
        return OpenMaya.MFnTransform(surface_path.node())

    def get_max_weight_skinning(self, joints_list):
        full_index_list = self.get_index_of_points_affected_by_multiple_influences(*joints_list)
        max_weight_value = self.MDoubleArray(length=len(full_index_list))

        for each_joint in joints_list:
            vertex_indices, skin_weights = self.get_index_of_points_affected_by_influence(each_joint)
            for index, each_vertex_index in enumerate(vertex_indices):
                max_weight_value[full_index_list.index(each_vertex_index)] = max_weight_value[full_index_list.index(
                    each_vertex_index)] + skin_weights[index]
        return full_index_list, max_weight_value

    def unify_skinning(self, joints_list):
        """
        Moves the skin weights of a joints list provided to the first joint of the list.
        Arguments:
            joints_list:list
        """
        full_index_list, max_weight_value = self.get_max_weight_skinning(joints_list)

        # self.apply_skinning(full_index_list, max_value_weight, joints_list[0])
        for index, each_joint in enumerate(joints_list):
            if index == 0:
                self.apply_skinning(full_index_list, max_weight_value, each_joint)
            else:
                zero_values_weight = self.MDoubleArray(length=len(full_index_list))
                self.apply_skinning(full_index_list, zero_values_weight, each_joint)

                # self.skin_cluster.setWeights(self.mesh.dagPath(),  kobject_components, influence_indices, weights, normalize=False, returnOldWeights=False)
    def joints_to_indices(self, joint_list):
        if not type(joint_list) == list:
            joint_list = [joint_list]
        influence_indices = OpenMaya.MIntArray()
        for influence in joint_list:
            index_influence = self.skin_cluster.indexForInfluenceObject(self.getDagPath(influence))
            influence_indices.append(index_influence)
        return influence_indices

    def smooth(self, joints_list):
        full_index_list, max_weight_value = self.get_max_weight_skinning(joints_list)

        joint_weights = {}
        # creating a list per joint the lengt of the influence values
        for each_joint in joints_list:
            joint_weights[each_joint] = self.MDoubleArray(length=len(full_index_list))

        uv_values = self.closest_point_to_surface(full_index_list)
        for closest_point_uv, vertex_index in zip(uv_values, full_index_list):
            # print(vertex_index, closest_point_uv[1])
            for skin_value, joint in zip(*self.remap_value(closest_point_uv[1], joints_list)):
                #print(skin_value, joint)
                joint_weights[joint][full_index_list.index(vertex_index)] = \
                    joint_weights[joint][full_index_list.index(vertex_index)] + \
                    skin_value * max_weight_value[full_index_list.index(vertex_index)] / 6

        cmds.setAttr(f"{self.skin_cluster.name()}.normalizeWeights", 0)
        for each_joint in joint_weights:
            self.apply_skinning(full_index_list,
                                joint_weights[each_joint],
                                each_joint)
        cmds.setAttr(f"{self.skin_cluster.name()}.normalizeWeights", 1)
        #for index, uv_value in zip(fullset, uv_values):
        #     print(f'{index} , {uv_value[-2]:.2f}, {uv_value[-1]:.2f}')

    def get_index_of_points_affected_by_multiple_influences(self, *influences):
        """
        return: a list containing  vertices indices affected by all joint influences.
        """
        self.joint_list = influences
        vertex_index = []
        for each_joint in self.joint_list:
            selection_list, weights = self.skin_cluster.getPointsAffectedByInfluence(each_joint)
            # index_of_influence = self.skin_cluster.indexForInfluenceObject(each_joint)
            influence_list = []
            if not selection_list.isEmpty():
                scene_object, vertices = selection_list.getComponent(0)
                fn_vertices = OpenMaya.MFnSingleIndexedComponent(vertices)
                influence_list.extend(fn_vertices.getElements())
            vertex_index.append(influence_list)
        fullset = set()  # To save the full list of affected indices
        for set_list in vertex_index:
            fullset = fullset.union(set(set_list))
        full_index_list = list(fullset)
        full_index_list.sort()
        return full_index_list

    def get_index_of_points_affected_by_influence(self, influence):
        """
        Returns an index of points that are affected by a specific influence.
        this influence can be just a string with the name of the joint.
        It will return 2 lists, one containing the vertex indices, and another one containing the weights per vertex.
        """
        self.joint_list = [influence]
        selection_list, weights = self.skin_cluster.getPointsAffectedByInfluence(self.joint_list[0])
        influence_list = []
        if not selection_list.isEmpty():
            scene_object, vertices = selection_list.getComponent(0)
            fn_vertices = OpenMaya.MFnSingleIndexedComponent(vertices)
            influence_list.extend(fn_vertices.getElements())
        return influence_list, weights

    def closest_point_to_surface(self, index_list):
        # Returns a list of uv points of an specific index list of vertex.
        return_list = []
        points = self.mesh.getPoints(space=OpenMaya.MSpace.kWorld)
        surface_transform = self.getDagPath(self._surface_name)
        #  Getting the transform matrix of the surface
        surface_inclusive_matrix = surface_transform.inclusiveMatrix().inverse()
        for closest_point_uv_index in index_list:
            return_list.append(self.surface.closestPoint(points[closest_point_uv_index] * surface_inclusive_matrix))
        return return_list

    def apply_skinning(self, vertex_indices, weight_values, influences):
        influence_indices = self.joints_to_indices(influences)

        component_list = OpenMaya.MFnSingleIndexedComponent()
        kobject_components = component_list.create(OpenMaya.MFn.kMeshVertComponent)
        component_list.addElements(vertex_indices)

        weights = OpenMaya.MDoubleArray(weight_values)
        self.skin_cluster.setWeights(self.mesh.dagPath(),
                                     kobject_components,
                                     influence_indices,
                                     weights,
                                     normalize=False,
                                     returnOldWeights=False)

    def get_skinning(self, influence):
        if influence.__class__ == str:
            index_influence = self.skin_cluster.indexForInfluenceObject(self.getDagPath(influence))
        else:
            index_influence = influence

        influence_indices = OpenMaya.MIntArray([index_influence])
        empty_object = OpenMaya.MObject()
        skinweights = self.skin_cluster.getWeights(self.mesh.dagPath(), empty_object, influence_indices)
        return skinweights

    def remap_value(self, value, joint_list, print_value=False):
        u_knots_values = self.surface.knotsInU()
        for index, (min_value, max_value) in enumerate(zip(u_knots_values[:-1], u_knots_values[1:])):
            if min_value != max_value:
                if min_value <= value <= max_value or isclose(value, min_value) or isclose(value, max_value):
                    t_value = (value - min_value) / (max_value - min_value)
                    if t_value < 0:
                        t_value = 0
                    elif t_value > 1:
                        t_value = 1
                    output_list = [joint_list[0], joint_list[0]]
                    output_list.extend(joint_list)
                    output_list.append(joint_list[-1])
                    output_list.append(joint_list[-1])
                    if print_value:
                        print(t_value)
                    return self.nurbs_interpolation(t_value), output_list[index-1:index+3]
        print(f'value not in range = {value} , {u_knots_values}')
        raise

    def nurbs_interpolation(self, t_value):
        t_value_vector = OpenMaya.MFloatPoint(1, t_value, pow(t_value, 2), pow(t_value, 3))
        nurbs_matrix = OpenMaya.MFloatMatrix((1, 4, 1, 0, -3, 0, 3, 0, 3, -6, 3, 0, -1, 3, -3, 1))
        values = t_value_vector * nurbs_matrix
        return values


if __name__ == '__main__':
    selection = pm.ls(selection=True)[0]
    smooth_skin = SmoothSkin().by_geometry(str(selection))
    # index_list = smooth_skin.get_index_of_points_affected_by_multiple_influences('joint2', 'joint1')
    # print(index_list)
    smooth_skin.surface = 'C_smoothSurface00_Spine_nrb'

    # points_affected = smooth_skin.get_index_of_points_affected_by_influence('C_main02_Spine_sknjnt')
    # print(points_affected)

    smooth_skin.smooth(['C_main00_Spine_sknjnt', 'C_main01_Spine_sknjnt', 'C_main02_Spine_sknjnt', 'C_main03_Spine_sknjnt', 'C_main04_Spine_sknjnt'])

    # print(smooth_skin.surface)
    # print(smooth_skin.closest_point_to_surface(index_list[0]))
    # print(smooth_skin.mesh.numVertices)
    # smooth_skin.apply_skinning([4, 5, 6, 7, 1], [1, .75, .5, .25, 0], 'joint1')

    # print(smooth_skin.get_skinning('joint1'))
    # print(smooth_skin.get_index_of_points_affected_by_multiple_influences('joint1'))
    # selection_points_list, values = smooth_skin.get_index_of_points_affected_by_influence('joint1')
    # print(selection_points_list)
    # print(values)
    # print(selection_points_list.length())
    # smooth_skin.smooth(['joint1', 'joint2', 'joint3'])

    'C_main02_Spine_sknjnt'
    '''num_points = 50
    step= 1/50
    space_locators_groups = []
    for each in range(4):
        space_locators_groups.append(pm.group(empty=True))

    for each in range(num_points):
        values = smooth_skin.nurbs_interpolation(step*each)
        for index, value in enumerate(values):
            new_space_loc = pm.spaceLocator()
            new_space_loc.setParent(space_locators_groups[index])
            new_space_loc.translateX.set(step*each)
            new_space_loc.translateY.set(value)
    '''

    # selection = cmds.ls(selection=True)
    # components = ApiComponents()
    # components.set_selection_list(selection)
    # components.index_list()





