from RMPY import RMNameConvention
import pymel.core as pm
reload (RMNameConvention)

NameConv  = RMNameConvention.RMNameConvention()
#NameConv.TypeDictionary['skinjoint']='JNT'
#NameConv.TypeDictionary['joint']='JXX'
#NameConv.TypeDictionary['control']='CTRL'

selection = pm.ls(selection=True)
#NameConv.RMRenameGuessTypeInName(selection)
for i in selection:
	#TokenArray = i.split('_')
	#NameConv.rename_name_in_format(i, side = 'L', system = 'backTire', useName=True)
	#cmds.rename(i,'_'.join(TokenArray[1:]))
	#cmds.rename(i,'Ankle_'+'_'.join(TokenArray[1:]))
	#cmds.rename(i,'_'.join(TokenArray[1:-1]))
	#NameConv.RMRenameNameInFormat (i, Side = "MD", System = "rig")
	#cmds.rename(i, "%s%s"%("ButterflyGirl_",i))
	#NameConv.rename_set_from_name( i , "control","type")
	NameConv.rename_set_from_name( i , "backLeg","name")
	#NameConv.rename_set_from_name( i , "right","side")
	#NameConv.rename_set_from_name( i , "statics","system")
	#NameConv.RMRenameSetFromName( i , "skinjoint","objectType")


