import pymel.core as pm
from RMPY.core import dataValidators
from RMPY.core import config
import maya.api.OpenMaya as om
from RMPY import nameConvention


def align(*args, **kwargs):
    """
    General align function\n 
    args[0]: the first element to which everithing will be aligned.\n
    args[1:] the elements that will be aligned.\n
    kwargs:\n
        translate: align in translation, default value True\n
        rotate: align rotation, default value True\n
    """
    translate = kwargs.pop('translate', True)
    rotate = kwargs.pop('rotate', True)
    align_objects = dataValidators.as_pymel_nodes(*args)
    main_object = align_objects[0]

    for each in align_objects[1:]:
        if translate:
            obj_position = pm.xform(main_object, q=True, ws=True, rp=True)
            pm.xform(each, ws=True, t=obj_position)
        if rotate:
            rotate_order_obj1 = pm.xform(main_object, q=True, rotateOrder=True)
            rotate_order_obj2 = pm.xform(each, q=True, rotateOrder=True)
            if rotate_order_obj1 != rotate_order_obj2:
                null_object = pm.group(em=True)
                pm.xform(null_object, rotateOrder=rotate_order_obj1)
                obj_rotation = pm.xform(main_object, q=True, ws=True, ro=True)
                pm.xform(null_object, ws=True, ro=obj_rotation)
                pm.xform(null_object, p=True, rotateOrder=rotate_order_obj2)
                obj_rotation = pm.xform(null_object, q=1, ws=1, ro=True)
                pm.xform(each, ws=True, ro=obj_rotation)
                pm.delete(null_object)
            else:
                obj_rotation = pm.xform(main_object, q=True, ws=True, ro=True)
                pm.xform(each, ws=True, ro=obj_rotation)


def joint_length(scene_joint):
    """
    Calculates the length of the joint based on the distance of the joint childrens, 
    if there are no joint childrens it will return the joint size. 
    """
    children = pm.listRelatives(scene_joint, children=True)
    if children:
        if len(children) > 0 and pm.objectType(children[0]) != "locator":
            return pm.getAttr('{}.translate{}'.format(children[0], config.axis_order[0].upper()))
        else:
            return joint_size(scene_joint)
    else:
        return joint_size(scene_joint)


def joint_size(scene_joint):
    """
    The size of the joint, which is the radius, 
    in case the object provided its not a joint, it will return 1
    scene_joint: the joint that will be measured
    """
    if pm.objectType(scene_joint) == "joint":
        radius = pm.getAttr(scene_joint + ".radius")
        return (radius * 2)
    else:
        return 1.0


def is_close(a, b, rel_tol=1e-09, abs_tol=0.0):
    """
    Compares two values by a relative threshold or an absolute 
    threshold depending which one is greater,
    if the difference between a and b is greater than the tolerance,
    it will return True, otherwise it will return false.\n
    rel_tol : by default this value will be 1e-9, and it will multiply to the higher value of a and b 
    and this will be the tolerance of the comparision unles the absolute tolerance is greater.\n
    abs_tol:by default this value is 0, and it serves as a comparision only if it is greather than the 
    maximum value a and b mulyiplyed by the relative tolerance.\n
    :a: first value to compare\n
    :b: second value to compare\n
    :return: True or false depending if the values are close one to each other
    """
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def point_distance(point01, point02):
    #point01 = dataValidators.as_pymel_nodes(point01)
    #point02 = dataValidators.as_pymel_nodes(point02)

    position01 = pm.xform(point01, q=True, ws=True, rp=True)
    position02 = pm.xform(point02, q=True, ws=True, rp=True)
    vector01, vector02 = om.MVector(position01), om.MVector(position02)
    result_vector = vector01 - vector02
    return om.MVector(result_vector).length()


def average(*args):
    result = pm.datatypes.Vector(0, 0, 0)
    for each in args:
        result += dataValidators.as_vector_position(each)
    result = result / len(args)
    return result


def aim_vector_based(*args, **kwargs):
    destination = dataValidators.as_pymel_nodes(args[0])[0]
    aim_axis = kwargs.pop('aim_axis', config.axis_order[0])
    up_axis = kwargs.pop('up_axis', config.axis_order[1])

    scale_x = kwargs.pop('scale_x', 1)
    scale_y = kwargs.pop('scale_y', 1)
    scale_z = kwargs.pop('scale_z', 1)

    position_source01 = dataValidators.as_vector_position(destination)
    destination_position = kwargs.pop('destination_position',
                                      [position_source01[0], position_source01[1], position_source01[2], 1.0])

    if len(destination_position) == 3:
        destination_position.append(1.0)
    x_dir = dataValidators.as_vector_position(args[1])
    x_dir.normalize()

    if len(args) == 3:
        up_vector = dataValidators.as_vector_position(args[2])
    else:
        up_vector = [0, 1, 0]

    z_dir = x_dir.cross(up_vector)
    z_dir.normalize()
    y_dir = z_dir.cross(x_dir)
    orientation = [x_dir, y_dir, z_dir]



    if aim_axis in 'xX':
        x_vector_index = 0
        if up_axis in 'yY':
            y_vector_index = 1
            z_vector_index = 2
        else:
            y_vector_index = 2
            z_vector_index = 1
            scale_y = scale_y * -1
    elif aim_axis in 'yY':
        y_vector_index = 0
        if up_axis in 'xX':
            x_vector_index = 1
            z_vector_index = 2
            scale_z = scale_z * -1
        else:
            x_vector_index = 2
            z_vector_index = 1
    else:
        z_vector_index = 0
        if up_axis in 'xX':
            x_vector_index = 1
            y_vector_index = 2
        else:
            x_vector_index = 2
            y_vector_index = 1
            scale_x = scale_x * -1

    newMatrix = pm.datatypes.Matrix([[orientation[x_vector_index][0] * scale_x,
                                      orientation[x_vector_index][1] * scale_x,
                                      orientation[x_vector_index][2] * scale_x, 0.0],
                                     [orientation[y_vector_index][0] * scale_y,
                                      orientation[y_vector_index][1] * scale_y,
                                      orientation[y_vector_index][2] * scale_y, 0.0],
                                     [orientation[z_vector_index][0] * scale_z,
                                      orientation[z_vector_index][1] * scale_z,
                                      orientation[z_vector_index][2] * scale_z, 0.0],
                                     destination_position])
    inverse = destination.parentInverseMatrix.get()
    destination.setMatrix(newMatrix * inverse)


def aim_point_based(*args, **kwargs):
    """Makes an object aim on the desired direction.\n
    :param args: the arguments goes on the following order
         args[0]:The main scene Node that will be transformed, this is the destination node

         args[1]:first_point, this will define the position of the destination,
            or the initial reference point to calculate orientation
         args[2]: second_point, this will define aim direction, the aim direction
            is calculated between the first and second point
         args[3]: third_point, this is optional, but defines the up vector of the orientation,
            it is a point, not a vector,
            the vector will be calculated, between the first and the third point,
            if no third point exist Y axis will be used instead.
    :param kwargs:
          aim_axis: The axis that will aim on the desired orientation, can be 'x', 'y', or 'z'
          up_axis: The second axis that will be aligned to the up vector
          edit_translate: does the destination node should change, position, or only orientation.
    """
    destination = args[0]
    aim_axis = kwargs.pop('aim_axis', config.axis_order[0])
    up_axis = kwargs.pop('up_axis', config.axis_order[1])
    edit_translate = kwargs.pop('edit_translate', True)
    use_destination_up_axis = kwargs.pop('use_destination_up_axis', False)
    use_vector_as_up_axis = kwargs.pop('use_vector_as_up_axis', (0.0, 1.0, 0.0))

    if len(args) == 3:
        position_source01 = dataValidators.as_vector_position(args[1])
        position_source02 = dataValidators.as_vector_position(args[2])
        if use_destination_up_axis:
            up_vector = pm.datatypes.Vector(getattr(Transform(args[1]).axis, up_axis))
        else:
            up_vector = pm.datatypes.Vector(use_vector_as_up_axis)

    elif len(args) == 4:
        position_source01 = dataValidators.as_vector_position(args[1])
        position_source02 = dataValidators.as_vector_position(args[2])
        position_source03 = dataValidators.as_vector_position(args[3])
        up_vector = position_source03 - position_source01
    else:
        raise AttributeError

    if not edit_translate:
        destination_position = destination.getMatrix()[3]
    else:
        destination_position = [position_source01[0], position_source01[1], position_source01[2], 1.0]

    x_dir = position_source02 - position_source01
    x_dir.normalize()
    aim_vector_based(destination, x_dir, up_vector, aim_axis=aim_axis, up_axis=up_axis,
                     destination_position=destination_position)


def equidistant(*args):
    """
    Distributes any transform nodes between the position of the first and the last node provided.
     :arg: only works with transform nodes, each one of the objects that will be distribute they should not be provided
     as a list,  just one after the other.
     """
    init_position = dataValidators.as_vector_position(args[0])
    end_position = dataValidators.as_vector_position(args[-1])
    direction_vector = end_position - init_position
    distance = direction_vector.length()
    step_vector = direction_vector.normal() * (distance / (len(args)-1))
    for index, each in enumerate(args[1:-1]):
        pm.move(each, init_position + (step_vector * (index + 1)), worldSpace=True)


class Axis(object):
    def __init__(self, *args, **kwargs):
        self.node = pm.ls(args[0])[0]
    @property
    def x(self):
        matrix = self.node.getMatrix(worldSpace=True)
        return matrix[0][0:3]

    @property
    def y(self):
        matrix = self.node.getMatrix(worldSpace=True)
        return matrix[1][0:3]

    @property
    def z(self):
        matrix = self.node.getMatrix(worldSpace=True)
        return matrix[2][0:3]


class Transform(object):
    def __init__(self, *args):
        self.node = pm.ls(args[0])[0]
        self._axis = Axis(*args)

    @property
    def axis(self):
        return self._axis


def reorient_to_world(root_node):
    child_list = root_node.getChildren()
    pm.parent(child_list, None)
    custom_world_align(root_node)
    pm.parent(child_list, root_node)
    for each_node in root_node.getChildren(type='transform'):
        if not each_node.getShapes():
            print ('doing {}'.format(each_node))
            reorient_to_world(each_node)


def custom_world_align(*scene_objects):
    for each in scene_objects:
        aim_vector_based(each, pm.datatypes.Vector(0.0, 0.0, 1.0), pm.datatypes.Vector(0.0, 1.0, 0.0))


if __name__ == '__main__':
    selection = pm.ls(selection=True)
    selection.insert(0, selection[0])
    aim_point_based(*selection, use_destination_up_axis=True)
    # align(selection)