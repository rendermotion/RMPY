from RMPY.core import config
import  json


class DataManager(object):
    """
    The main save and load functions once you initialize it it will look for the variable 
    in config named file_path and it will attempt to save to this location the resulting 
    dictionary in json format
    """
    def __init__(self):
        self.file_path = config.filePath()

    def save(self, *args, **kwargs):
        pass

    def load(self, *args, **kwargs):
        pass


if __name__ == '__main__':
    pass


