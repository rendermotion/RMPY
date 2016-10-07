import RMNameConvention
NameConv  = RMNameConvention.RMNameConvention()
selection = cmds.ls(selection=True)
for i in selection:
	 NameConv.RMRenameNameInFormat(i, Side = "RH",System = "intRig")
