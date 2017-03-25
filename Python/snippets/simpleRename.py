import RMNameConvention
NameConv  = RMNameConvention.RMNameConvention()
reload (RMNameConvention)
selection = cmds.ls(selection=True)
index = 0
for i in selection:
	#NameConv.RMRenameNameInFormat(i, Side = "MD", System = "Dynamic")
	#cmds.rename(i, "%s%s"%("Belt",index))
	#index +=1
	NameConv.RMRenameSetFromName( i , "RH","Side")
	#newName = NameConv.RMRenameSetFromName( i , "MD","Side")
	#NameConv.RMRenameSetFromName( i , "HatResult","Name")


