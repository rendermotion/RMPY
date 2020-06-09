from RMPY.core import dataManager
import pymel.core as pm
import maya.cmds as cmds


class GeneralData(object):
    def __init__(self, *args, **kwargs):
        super(GeneralData, self).__init__()
        self.node = kwargs.pop('node', None)
        data_manager = dataManager.DataManager()
        self.save_folder = '{}'.format(data_manager.scene_path)
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
        data_manager.save(file_name, self.get_data_dictionary(), **kwargs)

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
            attribute_data = generalAttribute.GeneralAttribute('{}.{}'.format(self.node, each_attr))
            attribute_dict['data'][each_attr] = attribute_data.data
        self.data = attribute_dict
        return self.data

    def set_data_dictionary(self, *data_dict):
        if data_dict:
            self.data = data_dict[0]
        for each_attr in self.attributes:
            if each_attr in self.data['data']:
                generalAttribute.GeneralAttribute('{}.{}'.format(self.node, each_attr),
                                                  data=self.data['data'][each_attr])

    @property
    def attributes(self):
        channel_box_attriubutes = cmds.listAttr(str(self.node), cb=True)
        keyable_attributes = cmds.listAttr(str(self.node), k=True)
        if not channel_box_attriubutes:
            channel_box_attriubutes = []
        if not keyable_attributes:
            keyable_attributes = []
        return channel_box_attriubutes + keyable_attributes


if __name__ == '__main__':
    attach_ment = GeneralData.by_name('zAttachment1')
    attach_ment.save()
