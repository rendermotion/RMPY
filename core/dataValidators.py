import pymel.core as pm
import inspect


def as_pymel_nodes(nodes):
    converted_to_list = False
    if type(nodes) not in [list, tuple]:
        nodes = [nodes]
        converted_to_list = True
    return_list = []
    for each in nodes:
        if pm.general.PyNode in inspect.getmro(type(each)):
            return_list.append(each)
        else:
            try:
                return_list += pm.ls(each)
            except:
                print "Error, can't convert %s to PyNode" % each
                raise AttributeError

    if converted_to_list:
        try:
            return return_list[0]
        except:
            raise (AttributeError, 'object/s do not exist::%s' % nodes)
    else:
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


if __name__ == '__main__':
    pm.ls(selection=True)
