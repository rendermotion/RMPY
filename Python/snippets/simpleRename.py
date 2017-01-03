import RMNameConvention
NameConv  = RMNameConvention.RMNameConvention()
reload (RMNameConvention)
selection = cmds.ls(selection=True)
for i in selection:
	#NameConv.RMRenameNameInFormat(i, Side = "MD", System = "rig")
	#cmds.rename(i, "%s%s"%("ButterflyGirl_",i))
	#NameConv.RMRenameSetFromName( i , "RH","Side")
	#newName = NameConv.RMRenameSetFromName( i , "MD","Side")
	NameConv.RMRenameSetFromName( i , "DelantalRivet","Name")


