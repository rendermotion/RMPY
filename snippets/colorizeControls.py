import pymel.core as pm
from RMPY import RMNameConvention
controls_list = pm.ls('*_ctr')
print controls_list
#controls_list = pm.ls(selection = True)
name_conv = RMNameConvention.RMNameConvention()
for each in controls_list:
    shapes = each.getShapes()
    side = name_conv.RMGetFromName(each, 'side')
    if shapes:
        shapes[0].overrideEnabled.set(1)
        if side == 'L':
            shapes[0].overrideColor.set(17)  #yellow
        if side == 'R':
            shapes[0].overrideColor.set(13)  # red
        if side == 'C':
            shapes[0].overrideColor.set(18)  # Blue
