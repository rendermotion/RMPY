import maya.cmds as cmds
import RMRigTools
selection = cmds.ls(selection = True)
print selection
for i in selection:
    Children = RMRigTools.RMRemoveChildren(i)
    cmds.rotate (0, 180, 0 ,i, r=True, os=True )
    if Children:
    	RMRigTools.RMParentArray( i , Children)

