import maya.cmds as cmds
from RMPY import RMNameConvention
from RMPY import RMRigTools

def skeletonHands():
    NameConv = RMNameConvention.RMNameConvention()
    palmGroups = ["R_middle00_Rig_grp", "R_ring00_Rig_grp", "R_pinky00_Rig_grp", "R_index00_Rig_grp",
                  "L_middle00_Rig_grp", "L_ring00_Rig_grp", "L_pinky00_Rig_grp", "L_index00_Rig_grp"]
    for eachGroup in palmGroups:
        Group = cmds.ls(eachGroup)[0]
        NewJoint = cmds.joint(name=NameConv.RMGetAShortName(Group) + "Carpos")
        NewJoint = NameConv.RMRenameBasedOnBaseName(Group, NewJoint, {'name': str(NewJoint)})
        NewJoint = NameConv.RMRenameSetFromName(NewJoint, "skinjoint", "objectType")
        RMRigTools.RMAlign(Group, NewJoint, 3)
        cmds.parent(NewJoint, Group)

if __name__ == '__main__':
	skeletonHands()