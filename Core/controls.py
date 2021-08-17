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
    source.worldSpace[0] >> destination.create
    source.worldSpace[0] // destination.create

    if world_space:
        for source_cv, destination_cv in zip(source.cv, destination.cv):
            destination_cv.setPosition(source_cv.getPosition(space='world'), space='world')
    else:
        for source_cv, destination_cv in zip(source.cv, destination.cv):
            destination_cv.setPosition(source_cv.getPosition(space='object'), space='object')


def transfer_curve_by_selection():
    selection = pm.ls(selection=True)
    for each in selection[1:]:
        transfer_curve(selection[0], each, world_space=False)


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
        source_shape = pm.ls(each)[0].getShape()
        oposite_side = get_oposite_side(each)
        if oposite_side:
            oposite_side = pm.ls(oposite_side)[0]
            destination_shape = pm.ls(oposite_side)[0].getShape()
            transfer_curve(source_shape, destination_shape, world_space=False)
            mirror_shape(destination_shape, scale_vector=[1, 1, -1])
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


if __name__ == '__main__':
    selection = pm.ls(selection=True)
    color_now_all_ctrls()
    # transfer_curve(*selection, world_space=False)
    # transfer_curve_by_selection()
    # mirror_selection()
    # mirror_shape(*selection, scale_vector=[1, -1, 1])
