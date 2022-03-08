from RMPY import nameConvention
import pymel.core as pm

name_conv = nameConvention.NameConvention()
name_conv.default_names['system'] = 'reference'
#name_conv.TypeDictionary['joint']='JXX'
#name_conv.TypeDictionary['control']='CTRL'

selection = pm.ls(selection=True)
#NameConv.RMRenameGuessTypeInName(selection)


def rename_selection():
	selection = pm.ls(selection=True)
	for each in selection:
		name_conv.rename_name_in_format(each, side='L', system='reference', name='backPawMech')


def set_in_name():
	selection = pm.ls(selection=True)
	for each in selection:
		name_conv.rename_set_from_name(each, 'R', 'side')


set_in_name()






