import pymel.core as pm
import os

axis_order = 'xyz'

default_reference_system_name = 'reference'


def get_file_path():
    """
    This function is used to calculate the initial path where all the saving functions will save,
    the path can be changed anytime directly by modifiying the config variable file_path.
    """
    scene_filename = pm.sceneName()
    if scene_filename != '':
        tokens = scene_filename.split('/')
        file_path_joined = '/'.join(tokens[:-1])
        if 'data' not in next(os.walk(file_path_joined))[1]:
            os.mkdir('{}/data'.format(file_path_joined))
        return '{}/data'.format(file_path_joined)
    else:
        return


file_path = get_file_path()

mirror_controls_axis = 'z'
mirror_controls = True


if __name__ == '__main__':
    print get_file_path()
