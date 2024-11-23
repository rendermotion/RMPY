import os
import pymel.core as pm

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


def validate_path(path_file_name):
    path_file_name = path_file_name
    incremental_list_path = []
    original_tokens = path_file_name.split('/')
    for index, each_token in enumerate(path_file_name.split('/')[:-1]):
        if each_token != '' and index > 4:
            incremental_list_path.append(each_token)
            file_path_joined = '/'.join(incremental_list_path)
            if original_tokens[index + 1] not in next(os.walk(file_path_joined))[1]:
                os.mkdir('{}/{}'.format(file_path_joined, original_tokens[index + 1]))
                print ('in {} \n the path {} was created'.format(file_path_joined, each_token))
        else:
            incremental_list_path.append(each_token)


if __name__ == '__main__':
    pass