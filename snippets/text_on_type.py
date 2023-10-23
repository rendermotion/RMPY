import pymel.core as pm
import maya.cmds as cmds

null = pm.ls('type1')[0]
translate = pm.getAttr('locator1.translateX')
txt = '{:.2f}'.format(translate)
sting_in_list_of_numbers = ''
for each in txt:
    char_number = ord(each)
    sting_in_list_of_numbers += '{} '.format(str(hex(char_number))[2:])
print(sting_in_list_of_numbers)
cmds.setAttr('type1.textInput', sting_in_list_of_numbers, type='string')