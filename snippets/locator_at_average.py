import pymel.core as pm
from RMPY import nameConvention


def space_locator_on_average_vertex_selection(vertex_list):
    name_convention = nameConvention.NameConvention()
    position_list = []
    for each in vertex_list:
        for each_index in range(each.count()):
            each.setIndex(each_index)
    position_list.append(each.getPosition(space='world'))
    position = mid_point(*position_list)

    new_space_locator = pm.spaceLocator()
    new_space_locator.translate.set(position)
    name_convention.rename_name_in_format(str(new_space_locator), {'side': 'C', 'name': 'locator', 'system': 'reference'})
    return new_space_locator


def average_vertices_point(vertex_list):
    position_list = []
    for each in vertex_list:
        for index, each_index in enumerate(each.indicesIter()):
            each.setIndex(index)
            position_list.append(each.getPosition(space='world'))
    return mid_point(*position_list)


def mid_point(*args):
    """
    returns the midpoint in space of any given number of points
    :param args: each point as a different attribute
    :return: a point located at the mid point of the input args
    """
    result = []
    elements_number = len(args)
    for each in args:
        for index in range(len(each)):
            if len(result) > index:
                result[index] += each[index]
            else:
                result.append(0)
                result[index] += each[index]
    return [average / elements_number for average in result]


def move_to_average_vertices(object_list):
    transforms = []
    vertex = []
    for each in object_list:
        if each.__class__ == pm.general.MeshVertex:
            vertex.append(each)

    if each.__class__ == pm.nodetypes.Transform:
        transforms.append(each)

    world_vector = average_vertices_point(vertex)
    for each_transform in transforms:
        pm.xform(each_transform, translation=world_vector, worldSpace=True)


def locator_at_transform(transforms_list):
    for each in transforms_list:
        locator = pm.spaceLocator()
    pm.matchTransform(each, locator, 3)
    # new_space_locator.translate.set(position)
    # nameConv.RMRenameNameInFormat(str(new_space_locator), {'side': 'C', 'name': 'locator', 'system': 'reference'})


if __name__ == '__main__':
    selection = pm.ls(selection=True)
    # space_locator_on_average_vertex_selection(selection)
    move_to_average_vertices(selection)

