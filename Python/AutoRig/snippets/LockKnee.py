import maya.cmds
from AutoRig import RMSpaceSwitch
import pprint as pp
import RMNameConvention
import RMRigTools

def lockKneeOnSpecific (Constraint,  IKJointLimb, SkinJointLimb,  PoleVectorControl, TwistJointsControl):
	NameConv = RMNameConvention.RMNameConvention()
	ShortName = NameConv.RMGetAShortName(IKJointLimb)
	Side  =NameConv.RMGetFromName(IKJointLimb,'Side')
	group = cmds.group(empty=True, name = "Character01_%s_%sLockDriver00_grp_Rig"%(Side,ShortName))
	RigTools = RMRigTools.RMRigTools()
	ChildPoleVector = RigTools.RMCreateGroupOnObj(PoleVectorControl , "child")

	cmds.orientConstraint (IKJointLimb,ChildPoleVector, mo = False)
	#RMRigTools.RMAlign( IKJointLimb, IKJointLimb, 1)
	cmds.parentConstraint (SkinJointLimb, TwistJointsControl, mo = True )
	LegSknJoint     = cmds.listRelatives (SkinJointLimb, parent = True)
	
	cmds.parent(group , LegSknJoint )

	#RMRigTools.RMAlign( PoleVectorControl, IKJointLimb, 1)

	SpcSw = RMSpaceSwitch.RMSpaceSwitch()
	SpcSw.CreateSpaceSwitchReverse(group,[IKJointLimb, ChildPoleVector], PoleVectorControl , Name = "KneeLock", mo = False, sswtype = "float")
	SpaceSwitchDic = (SpcSw.getParentConstraintDic(Constraint))

	Plug       = [keys for keys in SpaceSwitchDic['alias'] if SpaceSwitchDic['alias'][keys] == IKJointLimb]
	Connection = cmds.listConnections("%s.%s"%(Constraint, Plug[0]), plugs = True, destination = False)
	
	print "Plug:%s"%Plug
	print "Connection:%s"%Connection

	cmds.parentConstraint(IKJointLimb  , SkinJointLimb , e=True, remove=True)
	cmds.parentConstraint(group, SkinJointLimb, mo = False)

	SpaceSwitchDic = (SpcSw.getParentConstraintDic(Constraint))
	NewPlug        = [keys for keys in SpaceSwitchDic['alias'] if SpaceSwitchDic['alias'][keys] == group]
	print "NewPlug:%s" % NewPlug

	cmds.connectAttr (Connection[0] , "%s.%s" % (Constraint, NewPlug[0]))

lockKneeOnSpecific("Character01_LF_SpaceSwitchKnee00_prc_Rig", "Character01_LF_Knee00_jnt_Limbik", "Character01_LF_Knee00_jnt_Limbskn", "Character01_LF_KneePoleVectorIK00_ctr_Rig", "Character01_LF_TwistOriginKnee00_grp_Rig")
lockKneeOnSpecific("Character01_RH_SpaceSwitchKnee00_prc_Rig", "Character01_RH_Knee00_jnt_Limbik", "Character01_RH_Knee00_jnt_Limbskn", "Character01_RH_KneePoleVectorIK00_ctr_Rig","Character01_RH_TwistOriginKnee00_grp_Rig")

lockKneeOnSpecific("Character01_LF_SpaceSwitchelbow00_prc_Rig", "Character01_LF_elbow00_jnt_Limbik", "Character01_LF_elbow00_jnt_Limbskn", "Character01_LF_elbowPoleVectorIK00_ctr_Rig","Character01_LF_TwistOriginElbow00_grp_Rig")
lockKneeOnSpecific("Character01_RH_SpaceSwitchelbow00_prc_Rig", "Character01_RH_elbow00_jnt_Limbik", "Character01_RH_elbow00_jnt_Limbskn", "Character01_RH_elbowPoleVectorIK00_ctr_Rig","Character01_RH_TwistOriginElbow00_grp_Rig")











