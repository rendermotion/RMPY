import maya.cmds as cmds
from RMPY import nameConvention
from RMPY import RMRigTools

def skeletonHands():
    NameConv = nameConvention.NameConvention()
    palmGroups = ["R_middle00_Rig_grp", "R_ring00_Rig_grp", "R_pinky00_Rig_grp", "R_index00_Rig_grp",
                  "L_middle00_Rig_grp", "L_ring00_Rig_grp", "L_pinky00_Rig_grp", "L_index00_Rig_grp"]
    for eachGroup in palmGroups:
        Group = cmds.ls(eachGroup)[0]
        NewJoint = cmds.joint(name=NameConv.get_a_short_name(Group) + "Carpos")
        NewJoint = NameConv.rename_based_on_base_name(Group, NewJoint, {'name': str(NewJoint)})
        NewJoint = NameConv.rename_set_from_name(NewJoint, "skinjoint", "objectType")
        RMRigTools.RMAlign(Group, NewJoint, 3)
        cmds.parent(NewJoint, Group)

if __name__ == '__main__':
	skeletonHands()