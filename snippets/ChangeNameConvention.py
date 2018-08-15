from RMPY import nameConvention
from RMPY import RMRigTools
import pymel.core as pm
reload(nameConvention)

def get_key(searc_value, search_dic):
    for key, value in search_dic.iteritems():
        if value == searc_value:
            return key
original_name_conv = nameConvention.NameConvention()
original_name_conv.name_convention = {
                "CharacteName": 0,
                "name": 2,
                'side': 1,
                'objectType': 3,
                "system": 4
                }
original_name_conv.validation['side'] = ['LF', 'RH', 'MD']
original_name_conv.translator['side'] = {'left': 'LF', 'right': 'RH', 'center': 'MD'}
original_name_conv.default_names['side'] = 'MD'

name_conv = nameConvention.NameConvention()

def changeNameConv(correct_object):

    correct_object = RMRigTools.validate_pymel_nodes(correct_object)
    print correct_object
    for each in correct_object:
        name = original_name_conv.get_from_name(each, 'name')
        side = original_name_conv.get_from_name(each, 'side')
        side = get_key(side, original_name_conv.translator['side'])
        system = original_name_conv.get_from_name(each, 'system')
        objectType = original_name_conv.get_from_name(each, 'objectType')
        print each
        print 'name=%s'%name
        name_conv.rename_name_in_format(each, name=name, side=side, objectType=objectType, useName=False)
        for each_children in each.getChildren():
            if pm.objectType(each_children) == 'transform':
                changeNameConv([each_children])


if __name__ == '__main__':

    selection = pm.ls('Character01_MD_Spine_pnt_rfr')
    changeNameConv(selection)
