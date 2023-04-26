from maya.api import OpenMaya
from maya.api import OpenMayaAnim
import pymel.core as pm


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
    geo_shells = []
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

    return shells_match_existence(faces_lists)


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
    dag_path = getDagPath('pCube3Shape.vtx[*]')
    return dag_path.node()


def copy_vertex_position(source, destination):
    source_mesh = getMfnMesh(source)
    destination_mesh = getMfnMesh(destination)
    destination_mesh.setPoints(source_mesh.getPoints())


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
    iterator = OpenMaya.MItSelectionList(selection_list)
    # print selection_list.getDependNode(0)
    # print iterator.getStrings()
    # print iterator.getDagPath().fullPathName()
    # print skin_cluster.influenceObjects()[0].node()
    print (get_vertex().apiTypeStr)
    print (getDagPath('pCube3Shape.vtx[*]'))
    empty_object = OpenMaya.MObject()
    influence_indices = OpenMaya.MIntArray()
    for i in range(0, count):
        influence_indices.append(i)
    print (skin_cluster.getWeights(getDagPath('pCube3Shape.vtx[*]'), empty_object, influence_indices))

    # while not iterator.isDone():
    #     dag_path = iterator.getDagPath()
    #     print dag_path
    #     iterator.next()


if __name__ == '__main__':
    selection = pm.ls(selection=True)
    copy_vertex_position(*selection)
    # print shells('pCube3')
    # shells_result = shells('C_featherBones00_hip_msh')
    # print len(shells_result)
    # print shells_result
