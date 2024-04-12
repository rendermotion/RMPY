from maya.api import OpenMaya
from maya.api import OpenMayaAnim
import maya.cmds as cmds
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
        for each in string_joint_list:
            dag_path = self.getDagPath(each)
            self._joint_list.append(dag_path)
    def get_index_of_points_affected_by_influences(self, *influences):
        self.joint_list = influences
        vertex_index = []
        for each_influence in self.joint_list:
            selection_list, weights = self.skin_cluster.getPointsAffectedByInfluence(each_influence)
            # index_of_influence = self.skin_cluster.indexForInfluenceObject(each_influence)
            influence_list = []
            for each in range(selection_list.length()):
                scene_object, vertices = selection_list.getComponent(each)
                fn_vertices = OpenMaya.MFnSingleIndexedComponent(vertices)
                influence_list.extend(fn_vertices.getElements())
            vertex_index.append(set(influence_list))
        return vertex_index
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

    def apply_skinning(self, vertex_indices, weight_values):
        vertex_list = OpenMaya.MSelectionList()
        for each in vertex_indices:
            vertex_list.add(f'{self.mesh.name}.vtx[{each}]')
            vertex_dag_path, vertex_object = vertex_list.getComponent(0)
            influence_indices = OpenMaya.MIntArray()
            influence_indices.append(2)
            weights = OpenMaya.MDoubleArray(weight_values)
            self.skin_cluster.setWeights(self.getDagPath(self.mesh.name),
                                         vertex_object,
                                         influence_indices,
                                         weights,
                              normalize=False,
                              returnOldWeights=True)
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
    index_list = smooth_skin.get_index_of_points_affected_by_influences('joint2')
    print(index_list)
    smooth_skin.surface = 'nurbsCylinder1'
    print(smooth_skin.surface)
    # print(smooth_skin.closest_point_to_surface(index_list[0]))
    print(smooth_skin.mesh.numVertices)


