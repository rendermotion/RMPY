import maya.cmds as cmds
selection = cmds.ls(selection=True)
for i in selection:
	cmds.select(i,replace=True)
	joint = cmds.joint(name = "%sjoint"%i)
	cmds.parent(joint,world = True)
	cmds.parentConstraint(i,joint,mo = False)

