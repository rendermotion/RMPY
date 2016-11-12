import RMNameConvention
NameConv  = RMNameConvention.RMNameConvention()
reload (RMNameConvention)
selection = cmds.ls(selection=True)
for i in selection:
	NameConv.RMRenameNameInFormat(i, Side = "RH", System = "TorsoBelts")
	#NameConv.RMRenameSetFromName( i , "RH","Side")

