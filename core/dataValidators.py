import pymel.core as pm
import inspect


def as_pymel_nodes(*nodes):
    return_list = []
    for each in nodes:
        if pm.general.PyNode in inspect.getmro(type(each)):
            return_list.append(each)
        else:
            try:
                return_list.extend(pm.ls(each))
            except:
                print("Error, can't convert %s to PyNode" % each)
                raise AttributeError
    return return_list

def as_vector_position(input_data):
    if input_data.__class__ == pm.general.MeshVertex:
        return pm.datatypes.Vector(input_data.getPosition(space='world'))

    elif input_data.__class__ == str or pm.general.PyNode in inspect.getmro(type(input_data)):
        # input_data_pm = as_pymel_nodes(input_data)
        pivot_position = pm.xform(input_data, q=True, ws=True, rp=True)
        return pm.datatypes.Vector(pivot_position)

    elif input_data.__class__ == list:
        return pm.datatypes.Vector(input_data)

    elif input_data.__class__ == pm.datatypes.Vector:
        return input_data


def as_vector_rotation(input_data):
    if input_data.__class__ == pm.general.MeshVertex:
        return pm.datatypes.Vector(input_data.getNormal(space='world'))

    elif input_data.__class__ == str or pm.general.PyNode in inspect.getmro(type(input_data)):
        # input_data_pm = as_pymel_nodes(input_data)
        pivot_position = pm.xform(input_data, q=True, ws=True, rp=True)
        return pm.datatypes.Vector(pivot_position)

    elif input_data.__class__ == list:
        return pm.datatypes.Vector(input_data)


def as_point(input_data):
    if input_data.__class__ == pm.general.MeshVertex:
        position = as_vector_position(input_data)
        x_vector = as_vector_rotation(input_data)
        up_vector = pm.datatypes.Vector([0, 1, 0])
        dot_result = x_vector.dot(up_vector)
        if dot_result == 1 or dot_result == -1:
            up_vector = pm.datatypes.Vector([1, 0, 0])
        y_vector = up_vector.cross(x_vector)
        z_vector = x_vector.cross(y_vector)
        new_space_locator = pm.spaceLocator()
        new_space_locator.offsetParentMatrix.set(list([x_vector[0], x_vector[1], x_vector[2], 0,
                                                       y_vector[0],y_vector[1], y_vector[2], 0,
                                                       z_vector[0],z_vector[1], z_vector[2], 0,
                                                       position[0],position[1], position[2], 1]))
    else:
        print('not valid Data {}'.format(input_data.__class__))


if __name__ == '__main__':
    import maya.cmds as cmds

    selection = pm.ls(selection=True)[0]
    as_point(selection)

import maya.cmds as cmds

def remove_prefix(prefix):
    """Removes the specified prefix from all objects in the Maya scene.

    Args:
        prefix (str): The prefix to be removed.
    """

    for obj in cmds.ls('{}*'.format(prefix)):
        new_name = obj[len(prefix):]
        cmds.rename(obj, new_name)

prefix_to_remove = "__pasted"  # Replace with the desired prefix
remove_prefix(prefix_to_remove)