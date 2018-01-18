from RMPY import RMNameConvention
from RMPY import RMRigTools
import pymel.core as pm

def get_key(searc_value, search_dic):
    for key, value in search_dic.iteritems():
        if value == searc_value:
            return key
original_name_conv = RMNameConvention.RMNameConvention()
original_name_conv.NameConvention = {
                "CharacteName": 0,
                "name": 2,
                'side': 1,
                'objectType': 3,
                "system": 4
                }
original_name_conv.validation['side'] = ['LF', 'RH', 'MD']
original_name_conv.translator['side'] = {'left': 'LF', 'right': 'RH', 'center': 'MD'}
original_name_conv.DefaultNames['side'] = 'MD'

name_conv = RMNameConvention.RMNameConvention()

def changeNameConv(correct_object):

    correct_object = RMRigTools.validate_pymel_nodes(correct_object)
    print correct_object
    for each in correct_object:
        name = original_name_conv.RMGetFromName(each, 'name')
        side = original_name_conv.RMGetFromName(each, 'side')
        side = get_key(side, original_name_conv.translator['side'])
        system = original_name_conv.RMGetFromName(each, 'system')
        objectType = original_name_conv.RMGetFromName(each, 'objectType')
        print each
        name_conv.RMRenameNameInFormat(each, {'name': name, 'side': side, 'objectType': objectType}, useName=False)
        for each_children in each.getChildren():
            if pm.objectType(each_children) == 'transform':
                changeNameConv([each_children])


if __name__=='__main__':
    selection = pm.ls(selection = True)
    changeNameConv(selection)
