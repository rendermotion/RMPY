import RMRigTools
import maya.cmds
selection = cmds.ls(selection=True)
for i in selection:
	cmds.select( i, replace=True)
	cmds.joint()
