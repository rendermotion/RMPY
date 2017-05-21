from RMPY import RMNameConvention
reload (RMNameConvention)

NameConv  = RMNameConvention.RMNameConvention()
NameConv.TypeDictionary['skinjoint']='JNT'
NameConv.TypeDictionary['joint']='JXX'
NameConv.TypeDictionary['control']='CTRL'

selection = cmds.ls(selection=True)
#NameConv.RMRenameGuessTypeInName(selection)
for i in selection:
	TokenArray = i.split('_')
	#cmds.rename(i,'_'.join(TokenArray[1:]))
	#cmds.rename(i,'Ankle_'+'_'.join(TokenArray[1:]))
	cmds.rename(i,'_'.join(TokenArray[1:-1]))
	#NameConv.RMRenameNameInFormat (i, Side = "MD", System = "rig")
	#cmds.rename(i, "%s%s"%("ButterflyGirl_",i))
	#NameConv.RMRenameSetFromName( i , "control","Type")
	#newName = NameConv.RMRenameSetFromName( i , "SideDress","Name")
	#NameConv.RMRenameSetFromName( i , "DressBack","Name")
	#NameConv.RMRenameSetFromName( i , "DressRig","System")


