from AutoRig.Hand import RMGenericHandRig
import maya.cmds as cmds
import RMNameConvention
import RMRigTools
reload (RMGenericHandRig)
HandRig = RMGenericHandRig.RMGenericHandRig()
HandRig.CreateHandRig("Character01_LF_palm_pnt_rfr")



def skeletonHands():
	NameConv = RMNameConvention.RMNameConvention()
	palmGroups = ["*_LF_middle00_grp_Rig","*_LF_ring00_grp_Rig","*_LF_pinky00_grp_Rig","*_LF_index00_grp_Rig"]
	for eachGroup in palmGroups:
		Group = cmds.ls(eachGroup)[0]
		NewJoint = cmds.joint( name= NameConv.RMGetAShortName(Group) + "skeleton")
		NewJoint = NameConv.RMRenameBasedOnBaseName(Group ,NewJoint, NewName = NewJoint)
		NewJoint = NameConv.RMRenameSetFromName(NewJoint , TextString = "skinjoint" , Token = "Type")
		RMRigTools.RMAlign ( Group, NewJoint,3)
		cmds.parent ( NewJoint, Group )

skeletonHands()