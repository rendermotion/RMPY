import pymel.core as pm


def type_in_hierarchy(scene_object, mesh_list=None, object_type='joint'):
    """
    Returns the objects of type object_type that you can find in the hierarchy of scene_object.
    Parameters
    __________
    Arguments
    +++++++++
    scene_object : pymel_transform
        The object where the function it is going to start searching in the hierarchy.

    Keyword Arguments
    +++++++++++++++++
    mesh_list : list
        This is a recursive function, that uses this mesh list, to keep track of the returned value, on each call.
        So there is no need to provide anything on the mesh_list.
    object_type : str
         The maya object type that  it is going to be searched on the hierarchy
    return: list
        A list containing all the objects found.
    """
    if mesh_list is None:
        mesh_list = []
    if pm.objectType(scene_object) == object_type:
        mesh_list.append(scene_object)
    for each in scene_object.getChildren():
        type_in_hierarchy(each, mesh_list=mesh_list, object_type=object_type)
    return mesh_list


def shape_type_in_hierarchy(scene_object, mesh_list=None, object_type='mesh'):
    """
    Returns the transforms of objects that have a specific mesh type.
    __________
    Arguments
    +++++++++
    scene_object : pymel_transform
        The object where the function it is going to start searching in the hierarchy.

    Keyword Arguments
    +++++++++++++++++
    mesh_list : list
        This is a recursive function, that uses this mesh list, to keep track of the returned value, on each call.
        So there is no need to provide anything on the mesh_list.
    object_type : str
         The maya object type that  it is going to be searched on the hierarchy
    return: list
        A list containing all the objects found.
    """
    if mesh_list is None:
        mesh_list = []
    if scene_object.getShape():
        if pm.objectType(scene_object.getShape()) == object_type:
            mesh_list.append(scene_object)
    for each in scene_object.getChildren(type='transform'):
        shape_type_in_hierarchy(each, mesh_list=mesh_list, object_type=object_type)
    return mesh_list


def skinned_mesh_in_hierarchy(scene_object, mesh_list=None):
    if mesh_list is None:
        mesh_list = []
    if pm.objectType(scene_object) == 'mesh':
        for each_deformer in pm.listHistory(scene_object, interestLevel=0, pruneDagObjects=True):
            if each_deformer.__class__ == pm.nodetypes.SkinCluster:
                mesh_list.append(scene_object.getParent())
                break
    for each in scene_object.getChildren():
        skinned_mesh_in_hierarchy(each, mesh_list=mesh_list)
    return mesh_list


def none_skinned_mesh_in_hierarchy(scene_object, mesh_list=None):
    if mesh_list is None:
        mesh_list = []
    if pm.objectType(scene_object) == 'mesh':
        if not scene_object.intermediateObject.get():
            skin_clusters = []
            for each_deformer in pm.listHistory(scene_object, interestLevel=0, pruneDagObjects=True):
                if each_deformer.__class__ == pm.nodetypes.SkinCluster:
                    skin_clusters.append(each_deformer)
                    break

            if not skin_clusters:
                mesh_list.append(scene_object.getParent())

    for each in scene_object.getChildren():
        none_skinned_mesh_in_hierarchy(each, mesh_list=mesh_list)
    return mesh_list


def by_token_in_name(scene_object, token='_CTRL', **kwargs):
    if token in str(scene_object):
        pm.select(scene_object, add=True)
    for each in scene_object.getChildren(**kwargs):
        by_token_in_name(each, token=token, **kwargs)


def select_by_function(select_function, **kwargs):
    replace = kwargs.pop('replace', True)
    selection = pm.ls(selection=True)
    if not selection:
        selection = pm.ls('geo_GRP')
    if replace:
        pm.select(clear=True)
    for each in selection:
        pm.select(select_function(each, **kwargs), add=True)


def intermediate_shapes():
    selection = pm.ls(selection=True)
    shapes_list = []
    for each in selection:
        for each_shape in each.getShapes():
            if each_shape.intermediateObject.get() == 1:
                shapes_list.append(each_shape)
    return shapes_list


if __name__ == '__main__':
    scene_object = pm.ls(selection=True)[0]
    # scene_objects = type_in_hierarchy(volunteer, object_type='mesh')
    # print scene_objects
    # select_by_function(shape_type_in_hierarchy, object_type='nurbsCurve')
    # select_by_function(shape_type_in_hierarchy,mesh_list=None, object_type='mesh')
    # shape_type_in_hierarchy(scene_object)
    # select_by_function(none_skinned_mesh_in_hierarchy)
    # select_by_function(skinned_mesh_in_hierarchy)
    # print none_skinned_mesh_in_hierarchy(pm.ls('C_frontRopes_0001_GRP')[0])
    pm.select(type_in_hierarchy(scene_object))