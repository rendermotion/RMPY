import maya.cmds as cmds
from RMPY.AutoRig import RMSpaceSwitch
from RMPY import RMNameConvention
from RMPY import RMRigTools
reload(RMNameConvention)
reload(RMSpaceSwitch)

def clavicleSpaceSwitch():
	kinematics = cmds.ls("kinematics")[0]
	Mover01 = cmds.ls("*_MD_mover00_ctr_Rig")[0]
	rightClavicleControl = cmds.ls("*RH_clavicle00_ctr_Rig")[0]
	leftClavicleControl = cmds.ls("*LF_clavicle00_ctr_Rig")[0]
	resetLeftClavicleControl = cmds.ls("*LF_clavicle01_grp_Rig")[0]
	resetRightClavicleControl = cmds.ls("*RH_clavicle01_grp_Rig")[0]
	LimbArmRightikControl= cmds.ls("*_RH_wristIK00_ctr_Rig")[0]
	LimbArmLeftikControl= cmds.ls("*_LF_wristIK00_ctr_Rig")[0]

	NameConv = RMNameConvention.RMNameConvention()

	moverWorld = cmds.group( empty = True, name ="moverWorld")
	cmds.parent(moverWorld, kinematics)
	cmds.parentConstraint( Mover01 , moverWorld )

	SPSW = RMSpaceSwitch.RMSpaceSwitch()

	LFShoulderFK = cmds.ls("*_LF_shoulder00_grp_Limbfk")[0]
	LFFKShoulder = cmds.ls("*_LF_clavicle01_jnt_Rig")[0]
	LFControlShoulder = cmds.ls("*_LF_shoulderFK00_ctr_Rig")[0]

	RHShoulderFK = cmds.ls("*_RH_shoulder00_grp_Limbfk")[0]
	RHFKShoulder = cmds.ls("*_RH_clavicle01_jnt_Rig")[0]
	RHControlShoulder = cmds.ls("*_RH_shoulderFK00_ctr_Rig")[0]

	LFWorldFKArm = cmds.group(empty = True, name = "ArmWorld" )
	LFWorldFKArm = NameConv.rename_based_on_base_name (LFShoulderFK, LFWorldFKArm, {'name': "world", 'system': "LFKArmSpaceSwitch"})
	RMRigTools.RMAlign(LFShoulderFK, LFWorldFKArm ,3)
	cmds.parent( LFWorldFKArm, moverWorld)
	LSpaceSwitchGroup = RMRigTools.RMCreateGroupOnObj(LFShoulderFK)
	SPSW.CreateSpaceSwitchReverse(LFShoulderFK,[LSpaceSwitchGroup, LFWorldFKArm],LFControlShoulder,sswtype = "float", Name="", mo = False, constraintType = "orient")

	RHWorldFKArm = cmds.group(empty = True, name = "ArmWorld" )
	RHWorldFKArm = NameConv.rename_based_on_base_name (RHShoulderFK, RHWorldFKArm, {'name': "world", 'system': "RFKArmSpaceSwitch"})
	RMRigTools.RMAlign(RHShoulderFK, RHWorldFKArm ,3)
	cmds.parent( RHWorldFKArm, moverWorld)
	RSpaceSwitchGroup = RMRigTools.RMCreateGroupOnObj(RHShoulderFK)
	SPSW.CreateSpaceSwitchReverse(RHShoulderFK,[RSpaceSwitchGroup, RHWorldFKArm],RHControlShoulder,sswtype = "float", Name="", mo = False , constraintType = "orient")

	SPSW.AddSpaceObject(LimbArmRightikControl,moverWorld)
	SPSW.AddSpaceObject(LimbArmLeftikControl,moverWorld)





