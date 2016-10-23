import maya.cmds as cmds
selection = cmds.ls(selection=True)
for i in selection:
	cmds.rename (i , "R" + i[1:-1])