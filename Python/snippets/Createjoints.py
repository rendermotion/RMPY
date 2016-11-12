import RMRigTools
import maya.cmds
selection = cmds.ls(selection=True)
RMRigTools.RMCreateBonesAtPoints(selection)