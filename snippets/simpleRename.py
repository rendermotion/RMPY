from RMPY import nameConvention
import pymel.core as pm
reload (nameConvention)

NameConv = nameConvention.NameConvention()
NameConv.default_names['system']='reference'
#NameConv.TypeDictionary['joint']='JXX'
#NameConv.TypeDictionary['control']='CTRL'

selection = pm.ls(selection=True)
#NameConv.RMRenameGuessTypeInName(selection)
for i in selection:
	NameConv.rename_set_from_name( i , "reference", "system")
	#NameConv.rename_set_from_name( i , "statics","system")
	#NameConv.RMRenameSetFromName( i , "skinjoint","objectType")


