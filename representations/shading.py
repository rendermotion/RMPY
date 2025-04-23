import pymel.core as pm
from RMPY.core import dataManager

"""
This representation is intended to save materials on the scene.
The materials are saved as a maya scene and the contents of the shading sets as a dictionary. 
"""


class Shading(object):
    def __init__(self):
        self.node = None
        self.repr_dict = {}
        self.extra_path = '/shading'

    def save(self, *args, **kwargs):
        if len(args) >= 1:
            file_name = args[0]
        else:
            file_name = '%s' % self.node
        data_manager = dataManager.DataManager()
        data_manager.file_path = '{}{}'.format(data_manager.file_path, self.extra_path)
        data_manager.save(file_name, self.get_repr_dict(**kwargs), **kwargs)
        pm.select(self.repr_dict)
        pm.exportSelected(f'{data_manager.file_path}/shaders.mb')

    def load(self, *args, **kwargs):
        try:
            file_name = 'shader_definition'
            data_manager = dataManager.DataManager()
            data_manager.file_path = f'{data_manager.file_path}{self.extra_path}'
            pm.importFile(f'{data_manager.file_path}/shaders.mb')
            self.repr_dict = data_manager.load(file_name, **kwargs)

        except:
            pass
        return self.repr_dict

    def get_repr_dict(self, **kwargs):
        source_transform = kwargs.pop('source_transform', '__GEO__')
        source_node = pm.ls(source_transform)[0]
        geometries = source_node.listRelatives(allDescendents=True, type='mesh')
        shading_engines = set(pm.listConnections(geometries, type='shadingEngine'))
        self.repr_dict = {}
        for each in shading_engines:
            self.repr_dict[str(each)] = [str(each) for each in pm.sets(each, q=True)]

    def set_repr_dict(self):
        for each_set in self.repr_dict:
            set_node = pm.ls(each_set)
            for each_element in self.repr_dict[each_set]:
                if pm.objectExists(each_element):
                    pm.sets(set_node, addElement=each_element)
