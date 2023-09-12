import pymel.core as pm
import maya.cmds as cmds
import re


class GenericAttribute(object):
    def __init__(self, attribute, **kwargs):
        """
        The GenericAttribute class it is intended to save or set the data of any attribute in an scene object.
        It works un two ways if data is provided as a kwarg on creation, the generic attribute will automatically fill
        get the data of the attribute it is provided the attribute should be provided as a string, and it will be saved
        recursively in case where the data is a compound, a multi attribute. In case the data is provided it will load
         the data on the node, on creation.
        :param attribute(string): the attribute starting with the node, provided as a string.

        :param kwargs:
            data(dict): A dictionary containing the data of the node.
            An example of the dictionary can be retrieved by loading the data with this same class.
            The data dictionary regularly has a 3 keys, name, type and value.
                name.- the name of the attribute it is representing.
                type.- the type of the attribute.
                value.-the value of the attribute or another dictionary representing
                       all the attributes on a multi attribute or a compound attribute.
        """
        self.attribute = attribute
        self.data = kwargs.pop('data', None)
        self.internal_error = False
        self.isMulti = False
        self.multi_index = []
        self.attribute_type = cmds.getAttr(attribute, type=True, silent=True)
        if cmds.getAttr(attribute, mi=True) is not None or \
                (cmds.getAttr(attribute, mi=True) is None and cmds.getAttr(attribute, size=True) == 0):
            self.isMulti = True
            if cmds.getAttr(attribute, mi=True) is None:
                self.multi_index = []
            else:
                self.multi_index = cmds.getAttr(attribute, mi=True)
        if self.data is None:
            self.data = {}
            self.get_data_dict()
        else:
            self.set_data_dict()

    def set_data_dict(self):
        """
        Sets the data on a data dictionary.
        :return: None, no value is returned
        """
        if self.data['type'] == 'TdataCompound':
            if self.data['value']:
                for each_key in self.data['value'].keys():
                    if re.match('\D', each_key) is None:
                        GenericAttribute('{}[{}]'.format(self.attribute, each_key),
                                         data=self.data['value'][each_key])

                    else:
                        GenericAttribute('{}.{}'.format(self.attribute, each_key),
                                         data=self.data['value'][each_key])
            else:
                print ('not value found on {} in attribute {}'.format(self.data['value'], self.attribute))

        elif self.data['type'] in ['pointArray']:
            if self.data['value'] is not None and not cmds.getAttr(self.attribute, lock=True) \
                    and not pm.listConnections(self.attribute):
                cmds.setAttr(self.attribute, len(self.data['value']), *self.data['value'], type='pointArray')

        elif self.data["type"] in [int, 'unicode', 'long', 'float', 'doubleArray',
                                   'double', 'enum', 'bool', bool, float]:
            if self.data['value'] is not None \
                    and not cmds.getAttr(self.attribute, lock=True) \
                    and not pm.listConnections(self.attribute):
                cmds.setAttr(self.attribute, self.data['value'])
        elif self.data["type"] in ['string']:
            print ('setting attribute {} with value {}'.format(self.attribute, self.data['value']))
            if self.data['value'] is not None and not cmds.getAttr(self.attribute, lock=True) \
                    and not pm.listConnections(self.attribute):
                cmds.setAttr(self.attribute, self.data['value'], type=str(self.data["type"]))
        else:
            print ('attribute not identified {}'.format(self.attribute))

    def get_data_dict(self):
        """
        Gets the data of an attribute and saves it in a  dictionary
        :return:
        """
        if self.attribute_type == 'TdataCompound':
            self.data["type"] = 'TdataCompound'
            self.data["value"] = {}
            self.data["name"] = self.attribute

            if self.isMulti:
                for each_index in self.multi_index:
                    self.data["value"][int(each_index)] = GenericAttribute("{}[{}]".format(self.attribute,
                                                                                           each_index)).get_data_dict()
            else:
                for each_attribute_name in self.child_attributes:
                    if self.attribute.split('.')[-1] != each_attribute_name:
                        self.data["value"][each_attribute_name] = GenericAttribute("{}.{}".format(self.attribute,
                                                                                                  each_attribute_name)).get_data_dict()
        else:
            pm_attr = pm.Attribute(self.attribute)
            self.data["type"] = pm_attr.get(type=True)
            data_value = pm_attr.get(silent=True)
            if self.data["type"]:
                if data_value.__class__ in [list, tuple]:
                    self.data["value"] = self.get_list()

                elif self.data["type"] in [int, 'unicode', 'long', 'string', 'float', 'doubleArray',
                                           'double', 'enum', 'bool', bool, float]:
                    self.data["value"] = data_value
                else:
                    # pass
                    print ('data type not supported {} {}'.format(data_value.__class__, self.data['type']))
        return self.data

    def get_list(self):
        """
        This function gets te values of a list. Getting a list can be harder than it sounds since we dont know the
        type of data it contains. For example a list could contain Matrix Data that would need to be set in an specific
        way, to be able to be saved by a json file. and not all list are supported, for example  list of geometries.
        """
        data_list = cmds.getAttr(self.attribute)
        list_of_values = []
        for each in data_list:
            if each.__class__ in [int, float, tuple, unicode, long]:
                list_of_values.append(each)
            elif each.__class__ == pm.datatypes.Matrix:
                list_of_values.append(each.get())
            else:
                print ('class_inside a list not_supported {}'.format(each.__class__))
        return list_of_values

    @property
    def child_attributes(self):
        tokens = self.attribute.split('.')
        child_attributes_list = cmds.listAttr(self.attribute)
        for each_attr in child_attributes_list:
            token_attributes = each_attr.split('.')
            if len(token_attributes) == len(tokens):
                if '.'.join(tokens[1:]) == '.'.join(token_attributes[0:len(tokens) - 1]):
                    yield token_attributes[-1]


if __name__ == '__main__':
    scene_node = cmds.ls('blendShape1')[0]
    attributes = cmds.listAttr(scene_node)
    '''for each_attribute in attributes:
        if len(each_attribute.split('.')) <=1:
            print '{}.{}'.format(scene_node, each_attribute)
            general_attribute = GenericAttribute('{}.{}'.format(scene_node, each_attribute))
            print general_attribute.get_data_dict()'''

    general_attribute = GenericAttribute('blendShape1.inputTarget[0].sculptTargetTweaks')
