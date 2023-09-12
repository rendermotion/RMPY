from RMPY.core import config
import  json
import pymel.core as pm
import json
import os
from RMPY.core import config
from RMPY.core import file_os


class DataManager(object):
    """
    The main save and load functions once you initialize it it will look for the variable
    in config named file_path and it will attempt to save to this location the resulting
    dictionary in json format
    """
    def __init__(self):
        self._file_path = config.output.file_path

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, filepath_string):
        file_os.validate_path(filepath_string)
        self._file_path = filepath_string

    def save(self, file_name, data):
        with open('{}/{}.json'.format(self.file_path, file_name), 'w') as outfile:
            json.dump(data, outfile)

        outfile.close()

    def load(self, file_name):
        full_path_file_name = '{}/{}.json'.format(self.file_path, file_name)
        if os.path.exists(full_path_file_name):
            try:
                with open(full_path_file_name) as data_file:
                    data_loaded = json.load(data_file)
                data_file.close()
                return data_loaded
            except IOError:
                print('error trying to open file: \n {}'.format(full_path_file_name))
        return None

    def search(self, search_string):
        files = os.listdir('{}'.format(self.file_path))

        return_list = []
        for each_file in files:
            if search_string in str(each_file):
                return_list.append(each_file)
        return return_list

    def get_by_data_type(self, data_type):
        valid_files = self.search('.json')

        result_files = []
        for each_file in valid_files:
            simple_name = each_file.split('.')[0]
        loaded_data = self.load(simple_name)
        if 'data_type' in loaded_data:
            if loaded_data['data_type'] == data_type:
                result_files.append(simple_name)
        return result_files


if __name__ == '__main__':
    pass


