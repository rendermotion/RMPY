from RMPY.core import dataManager
import pymel.core as pm
import maya.cmds as cmds
from RMPY.representations.data_representation import genericAttribute
reload(genericAttribute)


class GeneralData(object):
    def __init__(self, *args, **kwargs):
        super(GeneralData, self).__init__()
        self.node = kwargs.pop('node')
        data_manager = dataManager.DataManager()
        self.save_folder = '{}'.format(data_manager.file_path)
        self.data = {}

    @classmethod
    def by_name(cls, scene_node):
        if pm.objectType(scene_node):
            new_instance = cls(node=pm.ls(scene_node)[0])
            return new_instance
        else:
            print 'object provided doesnt exists'
            return None

    def save(self, *args, **kwargs):
        if len(args) >= 1:
            file_name = args[0]
        else:
            file_name = '%s' % self.node
        data_manager = dataManager.DataManager()
        data_manager.scene_path = self.save_folder
        data_dict = self.get_data_dictionary()
        data_manager.save(file_name, data_dict, **kwargs)

    def load(self, *args, **kwargs):
        if len(args) >= 1:
            file_name = args[0]
        else:
            file_name = '%s' % self.node
        data_manager = dataManager.DataManager()
        data_manager.scene_path = self.save_folder
        self.data = data_manager.load(file_name, **kwargs)
        self.set_data_dictionary()
        return self.data

    def get_data_dictionary(self):
        attribute_dict = {"data": {},
                          "type": pm.objectType(self.node)}
        for each_attr in self.attributes:
            # if each_attr not in ['input', 'weightList', 'influenceColor']:
            attribute_data = genericAttribute.GenericAttribute('{}.{}'.format(self.node, each_attr))
            if attribute_data.data:
                if attribute_data.data['type'] is not None:
                    attribute_dict['data'][each_attr] = attribute_data.data
        self.data = attribute_dict
        # from pprint import pprint as pp
        # pp(self.data)
        return self.data

    def set_data_dictionary(self, *data_dict):
        # from pprint import pprint as pp
        # pp(self.data)
        if data_dict:
            self.data = data_dict[0]
        for each_attr in self.attributes:
            if each_attr in self.data['data']:
                # print 'setting {}.{} with data{}'.format(self.node, each_attr, self.data['data'][each_attr])
                genericAttribute.GenericAttribute('{}.{}'.format(self.node, each_attr),
                                                  data=self.data['data'][each_attr])

    @property
    def attributes(self):
        attribute_list = cmds.listAttr(str(self.node), hasData=True)
        for each_attribute in attribute_list:
            if len(each_attribute.split('.')) <= 1:
                yield '{}'.format(each_attribute)


if __name__ == '__main__':
    attach_ment = GeneralData.by_name('blendShape1')
    attach_ment.load()
