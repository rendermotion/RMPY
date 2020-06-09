import pymel.core as pm
import maya.cmds as cmds


def lock_and_hide_attributes(*scene_objects, **kwargs):
    bit_string = kwargs.pop('bit_string', '0000000000')

    info_dic = {".translateX": 0,
                ".translateY": 1,
                ".translateZ": 2,
                ".rotateX": 3,
                ".rotateY": 4,
                ".rotateZ": 5,
                ".scaleX": 6,
                ".scaleY": 7,
                ".scaleZ": 8,
                ".visibility": 9}

    if len(bit_string) == 10:
        for eachObj in scene_objects:
            for parameter in info_dic:
                if bit_string[info_dic[parameter]] == "0":
                    pm.setAttr('%s%s' % (eachObj, parameter), k=False, l=True)
                elif bit_string[info_dic[parameter]] == "1":
                    pm.setAttr('%s%s' % (eachObj, parameter), k=True, l=False)
                elif bit_string[info_dic[parameter]] == "L":
                    pm.setAttr('%s%s' % (eachObj, parameter), l=False)
                elif bit_string[info_dic[parameter]] == "l":
                    pm.setAttr('%s%s' % (eachObj, parameter), l=True)
                elif bit_string[info_dic[parameter]] == "H":
                    pm.setAttr('%s%s' % (eachObj, parameter), k=True)
                elif bit_string[info_dic[parameter]] == "h":
                    pm.setAttr('%s%s' % (eachObj, parameter), k=False)
                else:
                    pass
    else:
        print "error in LockAndHideAttr Not valid Len on BitString"
        return False
    return True


class GeneralAttribute(object):
    def __init__(self, attribute, **kwargs):
        self.data = kwargs.pop('data', {})
        self.name = None
        self.multi_name = None
        self.node = None
        self.internal_error = False
        self.isMulti = False

        name_splited = str(attribute).split('.')

        # print '{} type {}'.format(attribute, attribute.get(type=True))

        if len(name_splited) <= 3:
            self.node = name_splited[0]
            if len(name_splited) == 3:
                self.isMulti = True
                self.multi_name = name_splited[2]
                self.name = name_splited[1]
            else:
                self.name = name_splited[1]

            if self.data == {}:
                self.get_data_dict()
            else:
                self.set_data_dict()
        else:
            print 'attribute not recognized {}'.format(attribute)

    def set_data_dict(self, *data_dictionary):
        """
        :param data_dictionary (dict): the data dictionary
        :return:
        """
        if data_dictionary:
            self.data = data_dictionary[0]

        if cmds.getAttr('{}.{}'.format(self.node, self.name), type=True) == 'TdataCompound':
            if self.data['value']:
                self.set_multi_index()
            else:
                print 'the attribute {} in {} didnt contained any data to set'.format(self.name, self.node)
        else:
            if not cmds.getAttr('{}.{}'.format(self.node, self.name), lock=True):
                cmds.setAttr('{}.{}'.format(self.node, self.name), self.data['value'])
            else:
                print 'the following attribute could not be loaded since it is locked . {}.{}'.format(self.node, self.name)

        return self.data

    def get_data_dict(self):
        if self.isMulti:
            dict_data = self.get_multi_index()
            self.data['value'] = dict_data
            self.data['name'] = self.name
            self.data['multi_name'] = self.multi_name
            self.data['type'] = cmds.getAttr('{}.{}[{}].{}'.format(self.node, self.name, 0, self.multi_name), type=True)
        else:
            pm_attr = pm.Attribute('{}.{}'.format(self.node, self.name))
            self.data['type'] = pm_attr.get(type=True)
            self.data['value'] = pm_attr.get()
            self.data['name'] = self.name
        return self.data

    def set_multi_index(self):
        """
        sets the corresponding dictionary for a multi index attribute
        """
        for index in self.data['value'].keys():
            if cmds.getAttr('{}.{}[{}].{}'.format(self.node, self.name, index, self.multi_name), type=True) == 'TdataCompound':
                if not cmds.getAttr('{}.{}[{}].{}'.format(self.node, self.name, index, self.multi_name), lock=True):
                    cmds.removeMultiInstance('{}.{}[{}].{}'.format(self.node, self.name, index, self.multi_name))
                if self.data['value'][index][0] is not None:
                    for multi_index, multi_value in zip(*self.data['value'][index]):
                        cmds.setAttr('{}.{}[{}].{}[{}]'.format(self.node, self.name, index, self.multi_name, multi_index),
                        multi_value)
            else:
                'the folowing attribute was not modified {}'.format('{}.{}[{}].{}'.format(self.node, self.name, index, self.multi_name))

    def get_multi_index(self):
        """
        gets the corresponding dictionary for a multi index attribute
        """
        valid_indices = cmds.getAttr('{}.{}'.format(self.node, self.name), mi=True)
        dict_data = {}
        try:
            if valid_indices:
                for index in valid_indices:
                    indices = cmds.getAttr('{}.{}[{}].{}'.format(self.node, self.name, index, self.multi_name), mi=True)
                    values = cmds.getAttr('{}.{}[{}].{}'.format(self.node, self.name, index, self.multi_name))
                    if values.__class__ is list:
                        if values[0].__class__ is tuple:
                            values = values[0]
                    dict_data[index] = [indices, values]
        except():
            print 'an error ocurred trying to save data value {}'.format(pm.Attribute('{}.{}'.format(self.node, self.name)))
        return dict_data


if __name__ == '__main__':

    attachment = cmds.ls('zAttachment1')[0]
    for each_attribute in cmds.listAttr(attachment, k=True) + cmds.listAttr(attachment, cb=True):
        # print each_attribute
        # if '.' not in each_attribute:
        # print cmds.getAttr('{}.{}'.format(attachment, each_attribute), type=True)
        attribute = GeneralAttribute('{}.{}'.format(attachment, each_attribute))
        print attribute.get_data_dict()
        attribute.set_data_dict()