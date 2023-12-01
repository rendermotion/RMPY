from maya.api import OpenMaya
from maya.api import OpenMayaAnim


def getMfnMesh(name):
    sel = OpenMaya.MSelectionList()
    try:
        sel.add(str(name))
    except RuntimeError as e:
        return e

    dagPath = sel.getDagPath(0)
    return OpenMaya.MFnMesh(dagPath)


def getDagPath(name):
    sel = OpenMaya.MSelectionList()
    try:
        sel.add(str(name))
    except RuntimeError as e:
        return e
    return sel.getDagPath(0)


def getMFnSkinCluster(name):
    sel = OpenMaya.MSelectionList()
    try:
        sel.add(str(name))
    except RuntimeError as e:
        return e

    m_object = sel.getDependNode(0)
    return OpenMayaAnim.MFnSkinCluster(m_object)


def shells(geometry):
    """
        returns a list of vertex indices that correspond to each shell of the geometry
    """
    cube_mesh = getMfnMesh(geometry)
    mesh_vertices = cube_mesh.getVertices()
    return shells_match_existence(get_face_list(mesh_vertices))

class TopologyMatch(object):
    def __init__(self, face_source, face_destination, **kwargs):
        self.geometry_source=kwargs.pop('geometry_source')
        self.geometry_destination=kwargs.pop


def get_face_list(mesh_vertices):
    face_range = 0
    previous_face_range = 0
    number_of_face_vertex_list = mesh_vertices[0]
    vertex_in_face_list = mesh_vertices[1]
    faces_lists = []
    for each_face_range in number_of_face_vertex_list:
        face_range = face_range + each_face_range
        face_vertices_set = set(vertex_in_face_list[previous_face_range:face_range])
        previous_face_range = face_range
        faces_lists.append(face_vertices_set)
    return faces_lists


def shells_match_existence(list_of_shells_sets):
    final_shell_result = []
    while len(list_of_shells_sets) > 1:
        index_list = []
        interest_set = list_of_shells_sets[0]
        shells_list = list_of_shells_sets[1:]
        for index, each_vertex_set in enumerate(shells_list):
            if interest_set.intersection(each_vertex_set):
                index_list.append(index)
        index_list.reverse()
        if index_list:
            for each in index_list:
                interest_set = interest_set.union(shells_list[each])
            for each in index_list:
                shells_list.pop(each)
            shells_list.insert(0, interest_set)
        else:
            final_shell_result.append(interest_set)
        list_of_shells_sets = shells_list

    final_shell_result.append(list_of_shells_sets[0])
    return final_shell_result


def get_vertex():
    dag_path = getDagPath('pCylinderShape1.vtx[*]')
    return dag_path.node()

def vertex_positions(scene_node):
    mfnObject=getMfnMesh(scene_node)
    return mfnObject.getPoints()

def copy_vertex_position(source, destination):
    source_mesh = getMfnMesh(source)
    destination_mesh = getMfnMesh(destination)
    destination_mesh.setPoints(source_mesh.getPoints())


def closest_point_to_surface(surface, geometry, index_of_interest):
    surface_path = getDagPath(surface)
    omNurb = OpenMaya.MFnNurbsSurface(surface_path.node())
    mesh_geo = getMfnMesh(geometry)
    return_list = []
    points = mesh_geo.getPoints()
    for each_index in index_of_interest:
        return_list.append(omNurb.closestPoint(points[each_index]))
    return return_list


def get_index_of_points_affected_influences(skin_cluster, influence_list):
    vertex_index = []
    for each_influence in influence_list:
        selection_list, weights = skin_cluster.getPointsAffectedByInfluence(each_influence)
        index_of_influence = skin_cluster.indexForInfluenceObject(each_influence)
        influence_list = []
        for each in range(selection_list.length()):
            scene_object, vertices = selection_list.getComponent(each)
            fn_vertices = OpenMaya.MFnSingleIndexedComponent(vertices)
            influence_list.extend(fn_vertices.getElements())
        vertex_index.append(set(influence_list))
    return vertex_index

def test():
    skin_cluster = getMFnSkinCluster('skinCluster1')
    count = 0

    for index, each in enumerate(skin_cluster.influenceObjects()):
        # print each.__class__
        # print each.partialPathName()
        dag_path = OpenMaya.MDagPath()
        dag_path_influence_object = dag_path.getAPathTo(each.node())
        count = index + 1
        # print dag_path_influence_object.partialPathName()

    selection_list, weights = skin_cluster.getPointsAffectedByInfluence(skin_cluster.influenceObjects()[0])
    print(selection_list)
    print(weights)
    # iterator = OpenMaya.MItSelectionList(selection_list)
    # print selection_list.getDependNode(0)
    # print iterator.getStrings()
    # print iterator.getDagPath().fullPathName()
    # print skin_cluster.influenceObjects()[0].node()
    print(get_vertex().apiTypeStr)
    print(getDagPath('pCylinderShape1.vtx[*]'))
    empty_object = OpenMaya.MObject()
    influence_indices = OpenMaya.MIntArray()
    # for i in range(0, count):q
    #    influence_indices.append(i)
    influence_indices.append(0)
    skinweights = skin_cluster.getWeights(getDagPath('pCylinderShape1.vtx[*]'), empty_object, influence_indices)

    for each in skin_cluster.influenceObjects():
        print(each.partialPathName())
        print(each.node())
    print(len(skinweights))
    print(skinweights)

    # while not iterator.isDone():
    #     dag_path = iterator.getDagPath()
    #     print dag_path
    #     iterator.next()
def get_skin_value(u_value, nurbs_surface, joint_list):
    surface_path = getDagPath(nurbs_surface)
    omNurb = OpenMaya.MFnNurbsSurface(surface_path.node())
    print(omNurb)
    # omNurb.closestPoint()
    start_u, end_u = omNurb.knotDomainInU
    span_length = (end_u - start_u)/omNurb.numSpansInU
    print(span_length)
    u_value()
    joint_list
    # print(omNurb.numSpansInV)
    # print(omNurb.knotDomainInV)


def nurbs_interpolation(t_value):
    t_value_vector = OpenMaya.MFloatPoint(1, t_value, pow(t_value, 2), pow(t_value, 3))
    nurbs_matrix = OpenMaya.MFloatMatrix((1, 4, 1, 0, -3, 0, 3, 0, 3, -6, 3, 0, -1, 3, -3, 1))
    values = t_value_vector*nurbs_matrix
    return values


def test_print_nurbs_function():
    import pymel.core as pm
    number_of_points = 60
    step = 1.0 / number_of_points
    curve_a = pm.group(name='curveA', empty=True)
    curve_b = pm.group(name='curveB', empty=True)
    curve_c = pm.group(name='curveC', empty=True)
    curve_d = pm.group(name='curveD', empty=True)
    for each in range(number_of_points):
        weights = nurbs_interpolation(each*step)
        for each_value, parent in zip(weights, [curve_a, curve_b, curve_c, curve_d]):
            # value = getattr(weights, each_value)
            new_locator = pm.spaceLocator()
            new_locator.setParent(parent)
            new_locator.localScale.set([0.01, 0.01, 0.01])
            new_locator.translateX.set(float(each*step))
            new_locator.translateY.set(float(each_value))


if __name__ == '__main__':
    '''skin_cluster = getMFnSkinCluster('skinCluster2')
    joint_list = []
    for each in ['joint1', 'joint2']:
        dag_path = getDagPath(each)
        joint_list.append(dag_path)
    string_lists = get_index_of_points_affected_influences(skin_cluster, joint_list)
    for each_list in string_lists:
        print(each_list)
    '''
    get_skin_value(.2, 'nurbsCylinderShape1', 3)

    # print(closest_point_to_surface('nurbsCylinderShape1', 'pCylinderShape1', [1]))





