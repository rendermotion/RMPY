import pymel.core as pm
from RMPY import nameConvention


def color_code_controls(controls, force=None):
    name_convention = nameConvention.NameConvention()
    for each in controls:
        if not force:
            if name_convention.is_name_in_format(each):
                if name_convention.get_from_name(each, 'side') == 'L':
                    each.overrideEnabled.set(True)
                    each.overrideColor.set(17)
                elif name_convention.get_from_name(each, 'side') == 'R':
                    each.overrideEnabled.set(True)
                    each.overrideColor.set(13)
                else:
                    each.overrideEnabled.set(True)
                    each.overrideColor.set(18)
                shape = pm.ls(each.getShape())
            else:
                print ('{} name_not in format'.format(each))
                if 'L_'in str(each):
                    each.overrideEnabled.set(True)
                    each.overrideColor.set(17)
                elif 'R_'in str(each):
                    each.overrideEnabled.set(True)
                    each.overrideColor.set(13)
                else:
                    each.overrideEnabled.set(True)
                    each.overrideColor.set(18)
                shape = pm.ls(each.getShape())

            if shape:
                shape[0].overrideEnabled.set(False)
        else:
            each.overrideEnabled.set(True)
            each.overrideColor.set(14)


def color_now_all_ctrls(*args, **kwargs):
    if not args:
        selection = kwargs.pop('selection', True)
        if selection:
            controls = pm.ls(selection=True)
    controls = args
    if not controls:
        controls = pm.ls('*_ctr')
    color_code_controls(controls, force=False)


def transfer_curve(source, destination, world_space=True):
    '''
    Matches one curve to another, first creates all the right vertices on the destination,
    by connecting the worldspace from the source to the create input of the destination.
    And then the cvs are placed on the right position in worldspace
    '''

    match_number_of_shapes(source, destination)

    for shape_source, shape_destination in zip(object_valid_shapes(source), object_valid_shapes(destination)):

        shape_source.worldSpace[0] >> shape_destination .create
        shape_source.updateCurve()

        if world_space:
            for source_cv, destination_cv in zip(shape_source.cv, shape_destination.cv):
                destination_cv.setPosition(source_cv.getPosition(space='world'), space='world')
        else:
            for source_cv, destination_cv in zip(shape_source.cv, shape_destination.cv):
                destination_cv.setPosition(source_cv.getPosition(space='object'), space='object')

        shape_source.worldSpace[0] // shape_destination.create


def transfer_curve_by_selection():
    selection = pm.ls(selection=True)
    for each_object in selection[1:]:
        transfer_curve(selection[0], each_object, world_space=False)


def object_valid_shapes(scene_object):
    object_shapes = []
    for each_shape in scene_object.getShapes():
        if not each_shape.intermediateObject.get():
            object_shapes.append(each_shape)

    return object_shapes


def match_number_of_shapes(source, destination):
    number_of_shapes = len(object_valid_shapes(source)) - len(object_valid_shapes(destination))
    if number_of_shapes > 0:
        for each in range(number_of_shapes):
            pm.createNode('nurbsCurve', parent=destination)

    if number_of_shapes < 0:
        pm.delete(object_valid_shapes(destination)[number_of_shapes:])


def mirror_shape(*shapes, **kwargs):
    scale_vector = kwargs.pop('scale_vector', [1, 1, 1])
    world_space = kwargs.pop('world_space', False)
    scale_factor = pm.datatypes.Point(scale_vector)

    for each_shape in shapes:
        if world_space:
            for source_cv in each_shape.cv:
                current_position = source_cv.getPosition(space='world')
                new_position = pm.datatypes.Point([current_position[0] * scale_factor[0],
                                                   current_position[1] * scale_factor[1],
                                                   current_position[2] * scale_factor[2]])
                source_cv.setPosition(new_position, space='world')
        else:
            for source_cv in each_shape.cv:
                current_position = source_cv.getPosition(space='object')
                new_position = pm.datatypes.Point([current_position[0] * scale_factor[0],
                                                   current_position[1] * scale_factor[1],
                                                   current_position[2] * scale_factor[2]])
                source_cv.setPosition(new_position, space='object')
        each_shape.updateCurve()


def mirror_controls(*controls):
    for each in controls:
        source_shape = pm.ls(each)[0]
        oposite_side = get_oposite_side(each)
        if oposite_side:
            oposite_side = pm.ls(oposite_side)[0]
            destination_shape = pm.ls(oposite_side)[0]
            transfer_curve(source_shape, destination_shape, world_space=False)
            mirror_shape(destination_shape, scale_vector=[1, 1, 1])
        else:
            print 'coulnt find oposite curve for {}'.format(each)


def get_oposite_side(control):
    if 'L_' in str(control):
        return control.replace('L_', 'R_')
    elif 'R_' in str(control):
        return control.replace('R_', 'L_')
    return None


def mirror_selection():
    selection = pm.ls(selection=True)
    mirror_controls(*selection)


def add_nurbs_curve_shape(scene_object):
    pm.createNode()
    scene_object


if __name__ == '__main__':
    selection = pm.ls(selection=True)
    # mirror_selection()
    color_now_all_ctrls(*selection)
    # mirror_controls(*selection)
    # get_same_number_of_shapes(*selection)
    # print selection[0].getShapes()
    # shapes = object_valid_shapes(selection[0])
    # match_number_of_shapes(selection[0], selection[1])
    # transfer_curve_by_selection()
    # mirror_selection()
    # mirror_shape(*selection, scale_vector=[-1, 1, 1])
