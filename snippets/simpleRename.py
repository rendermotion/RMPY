from RMPY import nameConvention
import pymel.core as pm

name_conv = nameConvention.NameConvention()
name_conv.default_names['system']= 'reference'
#name_conv.TypeDictionary['joint']='JXX'
#name_conv.TypeDictionary['control']='CTRL'

selection = pm.ls(selection=True)
#NameConv.RMRenameGuessTypeInName(selection)

for each in selection:
	name_conv.rename_name_in_format(each, system='reference', name='rope')




