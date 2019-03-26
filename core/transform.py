import pymel.core as pm
from RMPY.core import validate
from RMPY.core import config


def align(*args, **kwargs):
    translate = kwargs.pop('translate', True)
    rotate = kwargs.pop('rotate', True)
    main_object = validate.as_pymel_nodes(args[0])
    objects_to_align = validate.as_pymel_nodes(args[1:])
    for each in objects_to_align:
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
    children = pm.listRelatives(scene_joint, children=True)
    if children:
        if len(children) > 0 and pm.objectType(children[0]) != "locator":
            return pm.getAttr('{}.translate{}'.format(children[0], config.axis_order[0].upper()))
        else:
            return joint_size(scene_joint)
    else:
        return joint_size(scene_joint)


def joint_size(scene_joint):
    if pm.objectType(scene_joint) == "joint":
        radius = pm.getAttr(scene_joint + ".radius")
        return (radius * 2)
    else:
        return 1.0
    
def is_close(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def aim_vector_based(*args, **kwargs):
    destination = validate.as_pymel_nodes(args[0])

    aim_axis = kwargs.pop('aim_axis', config.orient_axis[0])
    up_axis = kwargs.pop('up_axis', config.orient_axis[1])

    position_source01 = validate.as_vector_position(destination)
    destination_position = kwargs.pop('destination_position',
                                      [position_source01[0], position_source01[1], position_source01[2], 1.0])

    if len(destination_position) == 3:
        destination_position.append(1.0)

    x_dir = validate.as_vector_position(args[1])
    x_dir.normalize()

    if len(args) == 3:
        up_vector = validate.as_vector_position(args[2])
    else:
        up_vector = [0, 1, 0]

    z_dir = x_dir.cross(up_vector)
    z_dir.normalize()
    y_dir = z_dir.cross(x_dir)
    orientation = [x_dir, y_dir, z_dir]

    z_mult = 1
    y_mult = 1
    x_mult = 1
    if aim_axis in 'xX':
        x_vector_index = 0
        if up_axis in 'yY':
            y_vector_index = 1
            z_vector_index = 2
        else:
            y_vector_index = 2
            z_vector_index = 1
            y_mult = -1
    elif aim_axis in 'yY':
        y_vector_index = 0
        if up_axis in 'xX':
            x_vector_index = 1
            z_vector_index = 2
            z_mult = -1
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
            x_mult = -1

    newMatrix = pm.datatypes.Matrix([[orientation[x_vector_index][0] * x_mult,
                                      orientation[x_vector_index][1] * x_mult,
                                      orientation[x_vector_index][2] * x_mult, 0.0],
                                     [orientation[y_vector_index][0] * y_mult,
                                      orientation[y_vector_index][1] * y_mult,
                                      orientation[y_vector_index][2] * y_mult, 0.0],
                                     [orientation[z_vector_index][0] * z_mult,
                                      orientation[z_vector_index][1] * z_mult,
                                      orientation[z_vector_index][2] * z_mult, 0.0],
                                     destination_position])
    inverse = destination.parentInverseMatrix.get()
    destination.setMatrix(newMatrix * inverse)


def aim_point_based(*args, **kwargs):
    """makes an object aim on the desired direction
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
    aim_axis = kwargs.pop('aim_axis', config.orient_axis[0])
    up_axis = kwargs.pop('up_axis', config.orient_axis[1])
    edit_translate = kwargs.pop('edit_translate', True)

    if len(args) == 3:
        position_source01 = validate.as_vector_position(args[1])
        position_source02 = validate.as_vector_position(args[2])
        up_vector = pm.datatypes.Vector(0.0, 1.0, 0.0)

    elif len(args) == 4:
        position_source01 = validate.as_vector_position(args[1])
        position_source02 = validate.as_vector_position(args[2])
        position_source03 = validate.as_vector_position(args[3])
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
    init_position = validate.as_vector_position(args[0])
    end_position = validate.as_vector_position(args[-1])
    direction_vector = end_position - init_position
    distance = direction_vector.length()
    step_vector = direction_vector.normal() * (distance / (len(args)-1))
    for index, each in enumerate(args[1:-1]):
        pm.move(each, init_position + (step_vector * (index + 1)), worldSpace=True)


class Axis(object):
    def __init__(self, *args, **kwargs):
        self.node = pm.ls(args[0])[0]
        print self.node
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


if __name__ == '__main__':
    selection = pm.ls(selection=True)
    #equidistant(*selection)
















