import pymel.core as pm
import os
import sys

axis_order = 'xyz'
#axis_order = 'zyx'
default_reference_system_name = 'reference'


def get_file_path():
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

if __name__ == '__main__':
    print get_file_path()
