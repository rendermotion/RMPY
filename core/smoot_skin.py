from maya.api import OpenMaya
from maya.api import OpenMayaAnim
import maya.cmds as cmds
import re


class ApiComponents(object):
    def __init__(self):
        self.components_object = None
        self.selection_list = OpenMaya.MSelectionList()
    def set_selection_list(self, components):
        for each in components:
            print(each)
            other_list = OpenMaya.MSelectionList().add(each)
            self.selection_list.merge(other_list)
            print(self.selection_list.getDagPath(0))

        print(self.selection_list.length())
        print(self.selection_list.getDagPath(0))

    def index_list(self):
        for each in range(self.selection_list.length()):
            dag_path = self.selection_list.getDagPath(each)
            vertex_dag_path, vertex_object = self.selection_list.getComponent(each)


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
        else:
            mesh_shape = cmds.listRelatives(nurbs_surface, shapes=True)
            self._surface = self.getMfnNurbs(mesh_shape[0])

    @property
    def joint_list(self):
        return self._joint_list

    @joint_list.setter
    def joint_list(self, string_joint_list):
        self._joint_list = []
        for each in string_joint_list:
            dag_path = self.getDagPath(each)
            self._joint_list.append(dag_path)

    def get_index_of_points_affected_by_multiple_influences(self, *influences):
        self.joint_list = influences
        vertex_index = []
        for each_influence in self.joint_list:
            selection_list, weights = self.skin_cluster.getPointsAffectedByInfluence(each_influence)
            # index_of_influence = self.skin_cluster.indexForInfluenceObject(each_influence)
            influence_list = []
            scene_object, vertices = selection_list.getComponent(0)
            fn_vertices = OpenMaya.MFnSingleIndexedComponent(vertices)
            influence_list.extend(fn_vertices.getElements())
            vertex_index.append(set(influence_list))
        return vertex_index
    def get_index_of_points_affected_by_influence(self, influence):
        self.joint_list = [influence]
        return self.skin_cluster.getPointsAffectedByInfluence(self.joint_list[0])
    def closest_point_to_surface(self, index_list):
        # Returns a list of uv points of an specific index list of vertex.
        return_list = []
        points = self.mesh.getPoints()
        for each_index in index_list:
            return_list.append(self.surface.closestPoint(points[each_index]))
        return return_list
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

    def apply_skinning(self, vertex_indices, weight_values, influences):
        influence_indices = OpenMaya.MIntArray()
        if influences.__class__ == str:
            index_influence = self.skin_cluster.indexForInfluenceObject(self.getDagPath(influences))

        elif influences.__class__ == list:
            for each in influences:
                influence_indices.append(self.skin_cluster.indexForInfluenceObject(self.getDagPath(influences)))
        else:
            index_influence = influences

            influence_indices.append(index_influence)

        '''for each_index, each_value in zip(vertex_indices, weight_values):
            vertex_list = OpenMaya.MSelectionList()
            vertex_list.add(f'{self.mesh.dagPath()}.vtx[{each_index}]')
            vertex_dag_path, vertex_object = vertex_list.getComponent(0)
            print(vertex_object, vertex_object.__class__)
            weights = OpenMaya.MDoubleArray([each_value])
            self.skin_cluster.setWeights(self.mesh.dagPath(),
                                         vertex_object,
                                         influence_indices,
                                         weights,
                                         normalize=False,
                                         returnOldWeights=True)'''
        component_list = OpenMaya.MFnSingleIndexedComponent()
        kobject_components = component_list.create(OpenMaya.MFn.kMeshVertComponent)
        component_list.addElements(vertex_indices)
        weights = OpenMaya.MDoubleArray(weight_values)
        self.skin_cluster.setWeights(self.mesh.dagPath(),
                                     kobject_components,
                                     influence_indices,
                                     weights,
                                     normalize=False,
                                     returnOldWeights=True)
    def get_skinning(self, influence):
        if influence.__class__ == str:
            index_influence = self.skin_cluster.indexForInfluenceObject(self.getDagPath(influence))
        else:
            index_influence = influence

        influence_indices = OpenMaya.MIntArray([index_influence])
        empty_object = OpenMaya.MObject()
        skinweights = self.skin_cluster.getWeights(self.mesh.dagPath(), empty_object, influence_indices)
        return skinweights

    def get_skincluster_from_mesh(self):
        for each in cmds.listHistory(self.mesh.name(), pruneDagObjects=True):
            if cmds.objectType(each) == 'skinCluster':
                self.skin_cluster = each

    def get_mesh_from_skin_cluster(self):
        for each in cmds.listHistory(self.skin_cluster.name(), future=True):
            if cmds.objectType(each) == 'mesh':
                self.mesh = each

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


if __name__ == '__main__':
    smooth_skin = SmoothSkin().by_geometry('pPlane1')
    index_list = smooth_skin.get_index_of_points_affected_by_multiple_influences('joint2', 'joint1')
    print(index_list)
    smooth_skin.surface = 'nurbsCylinder1'
    # print(smooth_skin.surface)
    # print(smooth_skin.closest_point_to_surface(index_list[0]))
    # print(smooth_skin.mesh.numVertices)
    smooth_skin.apply_skinning([4, 5, 6, 7, 1], [1, .75, .5, .25, 0], 'joint1')
    # print(smooth_skin.get_skinning('joint1'))
    # print(smooth_skin.get_index_of_points_affected_by_multiple_influences('joint1'))
    # selection_points_list, values = smooth_skin.get_index_of_points_affected_by_influence('joint1')
    # print(selection_points_list)
    # print(values)
    # print(selection_points_list.length())

    # selection = cmds.ls(selection=True)
    # components = ApiComponents()
    # components.set_selection_list(selection)
    # components.index_list()





