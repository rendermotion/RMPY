import RMNameConvention
NameConv  = RMNameConvention.RMNameConvention()
reload (RMNameConvention)
selection = cmds.ls(selection=True)
for i in selection:
	#NameConv.RMRenameNameInFormat(i, Side = "LF", System = "EyelidRig")
	NameConv.RMRenameSetFromName( i , "PointOnSurface","Name")

