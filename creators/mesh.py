from RMPY import RMRigTools
from RMPY.core import transform
import maya.api.OpenMaya as om
from RMPY.creators import creatorsBase


class Mesh(creatorsBase.CreatorsBase):
    def __init__(self):
        self.right_index = []
        self.left_index = []
        self.center_index = []
        self.source_mesh = None
        self.geo = None
        self.geo_source_vertex = None
        self.mirror_vertex_index = None
        self.cache_mirror_vertex_index = None

        self.cache_geo_source_vertex = None
        self.cache_geo = None

    def build_mirror_index(self, source_mesh, **kwargs):
        axis = kwargs.pop('axis', 'X')
        axis = axis.capitalize()
        self.source_mesh = source_mesh
        self.load_geo_points(source_mesh)
        self.vertex_sides(axis=axis)
        self.vertex_pair_sides()

    def load_geo_points(self, source_mesh, **kwargs):
        cache = kwargs.pop('cache', False)
        source = RMRigTools.validate_pymel_nodes(source_mesh)
        selection_list = om.MSelectionList()
        selection_list.add(source.fullPath())
        selObj = selection_list.getDagPath(0)
        mfnSourceObject = om.MFnMesh(selObj)
        vertex_in_source = mfnSourceObject.getPoints(space=om.MSpace.kWorld)
        if not cache:
            self.geo = mfnSourceObject
            self.geo_source_vertex = vertex_in_source
        else:
            self.cache_geo = mfnSourceObject
            self.cache_geo_source_vertex = vertex_in_source

    def vertex_sides(self, **kwargs):
        axis = kwargs.pop('axis', 'X')
        axis = axis.capitalize()
        axis_value = 'XYZ'.index(axis)
        cache = kwargs.pop('cache', False)
        self.left_index = []
        self.right_index = []
        self.center_index = []
        if not cache:
            interest_vertex_data = self.geo_source_vertex
        else:
            interest_vertex_data = self.cache_geo_source_vertex

        for vertex_index, each_vertex in enumerate(interest_vertex_data):
            if transform.is_close(interest_vertex_data[vertex_index][axis_value], 0, abs_tol=.001):
                self.center_index.append(vertex_index)
            elif interest_vertex_data[vertex_index][axis_value] > 0:
                self.left_index.append(vertex_index)
            else:
                self.right_index.append(vertex_index)

    def match_vertex_index_by_position(self, source_mesh, comparision_mesh, **kwargs):
        self.load_geo_points(source_mesh)
        tolerance = kwargs.pop('tolerance', 0.0001)
        mesh_destination = Mesh()
        # split the model in L and right to get better performance while searching.
        mesh_destination.load_geo_points(comparision_mesh)
        mesh_destination.vertex_sides()
        self.vertex_sides()
        matching_vertex_index_dictionary = {}
        source_vertices = self.geo_source_vertex
        destination_vertices = mesh_destination.geo_source_vertex

        for source_list, destination_list in zip([self.right_index, self.left_index,self.center_index],
        [mesh_destination.right_index, mesh_destination.left_index,mesh_destination.center_index ]):
            for index_source in source_list:
                matching_destination = None
                for index_destination in destination_list:
                    if transform.is_close(destination_vertices[index_destination].x, source_vertices[index_source].x, abs_tol=tolerance):
                        if transform.is_close(destination_vertices[index_destination].y, source_vertices[index_source].y, abs_tol=tolerance):
                            if transform.is_close(destination_vertices[index_destination].z, source_vertices[index_source].z, abs_tol=tolerance):
                                matching_vertex_index_dictionary[index_source] = index_destination
                                matching_destination = index_destination
                                break
            if matching_destination is not None:
                destination_list.remove(matching_destination)
            else:
                # raise RuntimeError('No mirror found for vertex {}'.format(index_source))
                pass
                # print('No mirror found for vertex {}'.format(index_source))

        return matching_vertex_index_dictionary

    def move_by_matching_dictionary(self, source_mesh, destination_mesh, matching_dictionary, **kwargs):
        revers_dictionary = kwargs.pop('revers_dictionary', False)
        self.load_geo_points(source_mesh)
        mesh_destination = Mesh()
        mesh_destination.load_geo_points(destination_mesh)

        vertex_list_source = self.geo_source_vertex
        vertex_list_destination = mesh_destination.geo_source_vertex
        for each_keys in matching_dictionary.keys():
            if not revers_dictionary:
                vertex_list_destination[each_keys] = vertex_list_source[matching_dictionary[each_keys]]
            else:
                vertex_list_destination[matching_dictionary[each_keys]] = vertex_list_source[each_keys]
        mesh_destination.geo.setPoints(vertex_list_destination)


    def vertex_pair_sides(self, **kwargs):
        cache = kwargs.pop('cache', False)
        if not cache:
            self.mirror_vertex_index = {}
            interest_vertex_index_dictionary = self.mirror_vertex_index
            source_vertex = self.geo_source_vertex
        else:
            self.cache_mirror_vertex_index = {}
            interest_vertex_index_dictionary = self.cache_mirror_vertex_index
            source_vertex = self.cache_geo_source_vertex
        for each_right in self.right_index:
            matching_left = None
            for each_left in self.left_index:
                if transform.is_close(-1 * source_vertex[each_left].x, source_vertex[each_right].x, abs_tol=.001):
                    if transform.is_close(source_vertex[each_left].y, source_vertex[each_right].y, abs_tol=.001):
                        if transform.is_close(source_vertex[each_left].z, source_vertex[each_right].z, abs_tol=.001):
                            matching_left = each_left
                            break

        if matching_left:
            self.left_index.remove(matching_left)
            interest_vertex_index_dictionary[matching_left] = each_right
        else:
            raise RuntimeError('No mirror found for vertex {}'.format(each_right))
            pass

        for each_key in interest_vertex_index_dictionary:
            self.right_index.remove(interest_vertex_index_dictionary[each_key])
            #print 'couldnt find mirror match for vertex {}'.format(each_right)

    def mirror_geo(self, geo_to_mirror):
        self.load_geo_points(geo_to_mirror, cache=True)
        self.vertex_sides(axis='X')
        self.vertex_pair_sides(cache=True)

        for each_vertex in self.left_index:
            #if each_vertex in self.mirror_vertex_index.keys():
            buffer = self.cache_geo_source_vertex[each_vertex].x
            self.cache_geo_source_vertex[each_vertex].x = -1 * self.cache_geo_source_vertex[self.mirror_vertex_index[each_vertex]].x
            self.cache_geo_source_vertex[self.mirror_vertex_index[each_vertex]].x = -1 * buffer

            buffer = self.cache_geo_source_vertex[each_vertex].y
            self.cache_geo_source_vertex[each_vertex].y = self.cache_geo_source_vertex[self.mirror_vertex_index[each_vertex]].y
            self.cache_geo_source_vertex[self.mirror_vertex_index[each_vertex]].y = buffer

            buffer = self.cache_geo_source_vertex[each_vertex].z
            self.cache_geo_source_vertex[each_vertex].z = self.cache_geo_source_vertex[self.mirror_vertex_index[each_vertex]].z
            self.cache_geo_source_vertex[self.mirror_vertex_index[each_vertex]].z = buffer

            self.cache_geo.setPoint(each_vertex, self.cache_geo_source_vertex[each_vertex], space=om.MSpace.kWorld)
            self.cache_geo.setPoint(self.mirror_vertex_index[each_vertex],
            self.cache_geo_source_vertex[self.mirror_vertex_index[each_vertex]], space=om.MSpace.kWorld)

        self.cache_geo.syncObject()

    def create_deformed_geo_based(self, deformed_geo, axis='XYZ'):
        self.load_geo_points(self.source_mesh)
        # new_deformed = pm.duplicate(deformed_geo)[0]
        self.load_geo_points(deformed_geo, cache=True)

        for each_vertex, geo_each_vertex in enumerate(self.geo_source_vertex):
            value_changed = False
            if 'X' not in axis.upper():
                if self.cache_geo_source_vertex[each_vertex].x != geo_each_vertex.x:
                    value_changed = True
                    self.cache_geo_source_vertex[each_vertex].x = geo_each_vertex.x
            if 'Y' not in axis.upper():
                if self.cache_geo_source_vertex[each_vertex].y != geo_each_vertex.y:
                    value_changed = True
                    self.cache_geo_source_vertex[each_vertex].y = geo_each_vertex.y
            if 'Z' not in axis.upper():
                if self.cache_geo_source_vertex[each_vertex].z != geo_each_vertex.z:
                    value_changed = True
                    self.cache_geo_source_vertex[each_vertex].z = geo_each_vertex.z
            if value_changed:
                self.cache_geo.setPoint(each_vertex, self.cache_geo_source_vertex[each_vertex], space=om.MSpace.kWorld)
        self.cache_geo.updateSurface()


if __name__ == '__main__':
    mesh_creator = Mesh()
    mesh_creator.load_geo_points('character')

    #mesh_creator.mirror_geo('R_knee00_corrected_MSH')
    # mesh_creator.source_mesh = 'fabricDefault_C_dressDeformed_0001_mid_GES'
    # mesh_creator.create_deformed_geo_based('fabricDefault_C_dress_0001_mid_GES', axis='')



