from AutoRig.Hand import RMGenericHandRig
import maya.cmds as cmds
import nameConvention
import RMRigTools

HandRig = RMGenericHandRig.RMGenericHandRig()
HandRig.CreateHandRig("Character01_LF_palm_pnt_rfr")

def skeletonHands():
	NameConv = nameConvention.NameConvention()
	palmGroups = ["*_LF_middle00_grp_Rig","*_LF_ring00_grp_Rig","*_LF_pinky00_grp_Rig","*_LF_index00_grp_Rig"]
	for eachGroup in palmGroups:
		Group = cmds.ls(eachGroup)[0]
		NewJoint = cmds.joint(name=NameConv.get_a_short_name(Group) + "skeleton")
		NewJoint = NameConv.rename_based_on_base_name(Group, NewJoint, NewName = NewJoint)
		NewJoint = NameConv.rename_set_from_name(NewJoint, TextString ="skinjoint", Token ="Type")
		RMRigTools.RMAlign ( Group, NewJoint,3)
		cmds.parent ( NewJoint, Group )

skeletonHands()