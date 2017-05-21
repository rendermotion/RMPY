import maya.cmds as cmds

selection=cmds.ls(sl=True)
for i in selection:
	cmds.parent(i+"_shape",i,s=True)
