import maya.cmds as cmds
from RMPY.AutoRig import RMTwistJoints
from RMPY.AutoRig import RMRibbon
from RMPY import nameConvention
from RMPY import RMUncategorized


from RMPY import RMRigTools


def AddRibbon (SknJointStructure, SknParentGroup, currentTwists, ToDeleteNodes, LookAtAxis = "Y"):
    NameConv = nameConvention.NameConvention()
    ObjectTransformDiclist = RMUncategorized.ObjectTransformDic(currentTwists)
    for i in ToDeleteNodes:
        if cmds.objExists(i):
            cmds.delete(i)
    RMUncategorized.SetObjectTransformDic(ObjectTransformDiclist)

    TJArm = RMTwistJoints.RMTwistJoints()
    TJArm.RMCreateTwistJoints(SknJointStructure[0], SknJointStructure[1], NumberOfTB=2, LookAtAxis = LookAtAxis)

    constraintTJArm = cmds.parentConstraint(SknParentGroup, TJArm.TwistControlResetPoint, mo=True)[0]
    constraintTJArm = NameConv.rename_based_on_base_name(SknJointStructure[1], constraintTJArm, {})

    Ribbon=RMRibbon.RMRibbon()
    Ribbon.RibbonCreation(SknJointStructure[0], SknJointStructure[1], foliculeNumber = 4)

    for index in range(len(currentTwists)):
        cmds.parentConstraint ( Ribbon.jointStructure[index], currentTwists[index], mo=True)
    for index in range(len(Ribbon.resetControls)):
        cmds.parentConstraint (TJArm.TwistJoints[index], Ribbon.resetControls[index], mo = True)

    cmds.addAttr(Ribbon.controls[0], at="float", ln="Volume",     hnv = 1, hxv = 1, h = 0, k = 1, smn = -10, smx = 10)
    cmds.addAttr(Ribbon.controls[1], at="float", ln="VolumeUp",     hnv = 1, hxv = 1, h = 0, k = 1, smn = -10, smx = 10)
    cmds.addAttr(Ribbon.controls[1], at="float", ln="VolumeLow",     hnv = 1, hxv = 1, h = 0, k = 1, smn = -10, smx = 10)
    cmds.addAttr(Ribbon.controls[2], at="float", ln="Volume",     hnv = 1, hxv = 1, h = 0, k = 1, smn = -10, smx = 10)

    RMRigTools.RMConnectWithLimits('%s.Volume'%Ribbon.controls[0],'%s.scaleY'%currentTwists[0],[[-10,0],[0,1],[10,4]])
    RMRigTools.RMConnectWithLimits('%s.Volume'%Ribbon.controls[0],'%s.scaleZ'%currentTwists[0],[[-10,0],[0,1],[10,4]])
    RMRigTools.RMConnectWithLimits('%s.VolumeUp'%Ribbon.controls[1],'%s.scaleY'%currentTwists[1],[[-10,0],[0,1],[10,4]])
    RMRigTools.RMConnectWithLimits('%s.VolumeUp'%Ribbon.controls[1],'%s.scaleZ'%currentTwists[1],[[-10,0],[0,1],[10,4]])
    RMRigTools.RMConnectWithLimits('%s.VolumeLow'%Ribbon.controls[1],'%s.scaleY'%currentTwists[2],[[-10,0],[0,1],[10,4]])
    RMRigTools.RMConnectWithLimits('%s.VolumeLow'%Ribbon.controls[1],'%s.scaleZ'%currentTwists[2],[[-10,0],[0,1],[10,4]])

    RMRigTools.RMConnectWithLimits('%s.Volume'%Ribbon.controls[2],'%s.scaleY'%currentTwists[3],[[-10,0],[0,1],[10,4]])
    RMRigTools.RMConnectWithLimits('%s.Volume'%Ribbon.controls[2],'%s.scaleZ'%currentTwists[3],[[-10,0],[0,1],[10,4]])


LFSknParentGroup       = 'Character01_LF_shoulder00_grp_Limbskn'
LFArmSknJointStructure = ['Character01_LF_shoulder00_jnt_Limbskn','Character01_LF_elbow00_jnt_Limbskn']
#ArmLeftControlsParent  = "Character01_Arm_LFControls00_grp_controls"
currentTwists          = [u'Character01_LF_TwistJointShoulder00_sknjnt_Limbskn', u'Character01_LF_TwistJointShoulder01_sknjnt_Limbskn', u'Character01_LF_TwistJointShoulder02_sknjnt_Limbskn', u'Character01_LF_TwistJointShoulder03_sknjnt_Limbskn']
ToDeleteNodes          = [u'Character01_LF_TwistOLimbskninShoulder00_grp_Limbskn', u'Character01_LF_TwistJointShoulder00_jnt_Limbskn_aimConstraint1', u'Character01_LF_NegativeLookAtRotationShoulder00_mult_Limbskn', u'Character01_LF_TwistJointAddShoulder00_pma_Limbskn', u'Character01_LF_TwistJointShoulder00_mult_Limbskn', u'Character01_MD_endTwistShoulder01_loc_LimbsknShape', u'Character01_MD_startTwistShoulder01_loc_LimbsknShape', u'Character01_LF_DistanceNode00_dbtw_Limbskn', u'Character01_LF_StretchyTwistJointShoulder00_mult_Limbskn']

AddRibbon (LFArmSknJointStructure, LFSknParentGroup, currentTwists, ToDeleteNodes,"Y") 

RHSknParentGroup       = 'Character01_RH_shoulder00_grp_Limbskn'
RHArmSknJointStructure = ['Character01_RH_shoulder00_jnt_Limbskn','Character01_RH_elbow00_jnt_Limbskn']
#ArmRHControlsParent  = "Character01_Arm_RHControls00_grp_controls"
RHcurrentTwists          = [u'Character01_RH_TwistJointShoulder00_sknjnt_Limbskn', u'Character01_RH_TwistJointShoulder01_sknjnt_Limbskn', u'Character01_RH_TwistJointShoulder02_sknjnt_Limbskn', u'Character01_RH_TwistJointShoulder03_sknjnt_Limbskn']
RHToDeleteNodes          = [u'Character01_RH_TwistOriginShoulder00_grp_Limbskn',u'Character01_RH_TwistJointShoulder00_jnt_Limbskn_aimConstraint1', u'Character01_RH_NegativeLookAtRotationShoulder00_mult_Limbskn', u'Character01_RH_TwistJointAddShoulder00_pma_Limbskn', u'Character01_RH_TwistJointShoulder00_mult_Limbskn', u'Character01_MD_endTwistShoulder00_loc_LimbsknShape', u'Character01_MD_startTwistShoulder00_loc_LimbsknShape', u'Character01_RH_DistanceNode00_dbtw_Limbskn', u'Character01_RH_StretchyTwistJointShoulder00_mult_Limbskn']

AddRibbon (RHArmSknJointStructure, RHSknParentGroup, RHcurrentTwists, RHToDeleteNodes, "Y")

LFSknParentGroup         = 'Character01_LF_elbow00_jnt_Limbskn'
LFArmSknJointStructure   = ['Character01_LF_elbow00_jnt_Limbskn','Character01_LF_wrist00_jnt_Limbskn']
LFcurrentTwists          = [u'Character01_LF_TwistJointElbow00_sknjnt_Limbskn', u'Character01_LF_TwistJointElbow01_sknjnt_Limbskn', u'Character01_LF_TwistJointElbow02_sknjnt_Limbskn', u'Character01_LF_TwistJointElbow03_sknjnt_Limbskn']
LFToDeleteNodes          = [u'Character01_LF_TwistOriginElbow00_grp_Limbskn',u'Character01_MD_startTwistElbow01_loc_LimbsknShape', u'Character01_MD_endTwistElbow01_loc_LimbsknShape', u'Character01_LF_StretchyTwistJointElbow00_mult_Limbskn', u'Character01_LF_DistanceNode01_dbtw_Limbskn', u'Character01_LF_TwistJointElbow00_mult_Limbskn', u'Character01_LF_TwistJointAddElbow00_pma_Limbskn', u'Character01_LF_TwistJointElbow00_jnt_Limbskn_aimConstraint1', u'Character01_LF_NegativeLookAtRotationElbow00_mult_Limbskn']

AddRibbon (LFArmSknJointStructure, LFSknParentGroup, LFcurrentTwists, LFToDeleteNodes, "Y")

RHSknParentGroup         = 'Character01_RH_elbow00_jnt_Limbskn'
RHArmSknJointStructure   = ['Character01_RH_elbow00_jnt_Limbskn','Character01_RH_wrist00_jnt_Limbskn']
RHcurrentTwists          = [u'Character01_RH_TwistJointElbow00_sknjnt_Limbskn', u'Character01_RH_TwistJointElbow01_sknjnt_Limbskn', u'Character01_RH_TwistJointElbow02_sknjnt_Limbskn', u'Character01_RH_TwistJointElbow03_sknjnt_Limbskn']
RHToDeleteNodes          = [u'Character01_RH_TwistOriginElbow00_grp_Limbskn',u'Character01_MD_startTwistElbow00_loc_LimbsknShape', u'Character01_MD_endTwistElbow00_loc_LimbsknShape', u'Character01_RH_StretchyTwistJointElbow00_mult_Limbskn', u'Character01_RH_DistanceNode01_dbtw_Limbskn', u'Character01_RH_TwistJointElbow00_mult_Limbskn', u'Character01_RH_TwistJointAddElbow00_pma_Limbskn', u'Character01_RH_TwistJointElbow00_jnt_Limbskn_aimConstraint1', u'Character01_RH_NegativeLookAtRotationElbow00_mult_Limbskn']

AddRibbon (RHArmSknJointStructure, RHSknParentGroup, RHcurrentTwists, RHToDeleteNodes, "Y")


#************************************LEG****************************************

RHSknParentGroup         = 'Character01_LF_leg00_grp_Limbskn'
RHArmSknJointStructure   = [u'Character01_LF_leg00_jnt_Limbskn', u'Character01_LF_Knee00_jnt_Limbskn']
RHcurrentTwists          = [u'Character01_LF_TwistJointLeg00_sknjnt_Limbskn', u'Character01_LF_TwistJointLeg01_sknjnt_Limbskn', u'Character01_LF_TwistJointLeg02_sknjnt_Limbskn' ,u'Character01_LF_TwistJointLeg03_sknjnt_Limbskn']
RHToDeleteNodes          = [u'Character01_LF_TwistOriginLeg00_grp_Limbskn',u'Character01_MD_startTwistLeg01_loc_LimbsknShape', u'Character01_MD_endTwistLeg01_loc_LimbsknShape', u'Character01_LF_DistanceNode02_dbtw_Limbskn', u'Character01_LF_StretchyTwistJointLeg00_mult_Limbskn', u'Character01_LF_TwistJointLeg00_mult_Limbskn', u'Character01_LF_TwistJointAddLeg00_pma_Limbskn', u'Character01_LF_NegativeLookAtRotationLeg00_mult_Limbskn', u'Character01_LF_TwistJointLeg00_jnt_Limbskn_aimConstraint1']

AddRibbon (RHArmSknJointStructure, RHSknParentGroup, RHcurrentTwists, RHToDeleteNodes, "Z")

RHSknParentGroup         =   'Character01_RH_leg00_grp_Limbskn'
RHArmSknJointStructure   = [u'Character01_RH_leg00_jnt_Limbskn', u'Character01_RH_Knee00_jnt_Limbskn']
RHcurrentTwists          = [u'Character01_RH_TwistJointLeg00_sknjnt_Limbskn', u'Character01_RH_TwistJointLeg01_sknjnt_Limbskn', u'Character01_RH_TwistJointLeg02_sknjnt_Limbskn' ,u'Character01_RH_TwistJointLeg03_sknjnt_Limbskn']
RHToDeleteNodes          = [u'Character01_RH_TwistOriginLeg00_grp_Limbskn',u'Character01_MD_startTwistLeg00_loc_LimbsknShape', u'Character01_MD_endTwistLeg00_loc_LimbsknShape', u'Character01_RH_DistanceNode02_dbtw_Limbskn', u'Character01_RH_StretchyTwistJointLeg00_mult_Limbskn', u'Character01_RH_TwistJointLeg00_mult_Limbskn', u'Character01_RH_TwistJointAddLeg00_pma_Limbskn', u'Character01_RH_NegativeLookAtRotationLeg00_mult_Limbskn', u'Character01_RH_TwistJointLeg00_jnt_Limbskn_aimConstraint1']


AddRibbon (RHArmSknJointStructure, RHSknParentGroup, RHcurrentTwists, RHToDeleteNodes, "Z")

RHSknParentGroup         =   'Character01_RH_leg00_grp_Limbskn'
RHArmSknJointStructure   = [u'Character01_RH_Knee00_jnt_Limbskn', u'Character01_RH_ankle00_jnt_Limbskn']
RHcurrentTwists          = [u'Character01_RH_TwistJointKnee00_sknjnt_Limbskn', u'Character01_RH_TwistJointKnee01_sknjnt_Limbskn', u'Character01_RH_TwistJointKnee02_sknjnt_Limbskn', u'Character01_RH_TwistJointKnee03_sknjnt_Limbskn']
RHToDeleteNodes          = [u'Character01_RH_TwistOriginKnee00_grp_Limbskn', u'Character01_MD_endTwistKnee00_loc_LimbsknShape', u'Character01_MD_startTwistKnee00_loc_LimbsknShape', u'Character01_RH_DistanceNode03_dbtw_Limbskn', u'Character01_RH_StretchyTwistJointKnee00_mult_Limbskn', u'Character01_RH_TwistJointKnee00_mult_Limbskn', u'Character01_RH_TwistJointAddKnee00_pma_Limbskn', u'Character01_RH_TwistJointKnee00_jnt_Limbskn_aimConstraint1', u'Character01_RH_NegativeLookAtRotationKnee00_mult_Limbskn']


AddRibbon (RHArmSknJointStructure, RHSknParentGroup, RHcurrentTwists, RHToDeleteNodes, "Z")



HSknParentGroup         =   'Character01_LF_leg00_grp_Limbskn'
RHArmSknJointStructure   = [u'Character01_LF_Knee00_jnt_Limbskn', u'Character01_LF_ankle00_jnt_Limbskn']
RHcurrentTwists          = [u'Character01_LF_TwistJointKnee00_sknjnt_Limbskn', u'Character01_LF_TwistJointKnee01_sknjnt_Limbskn', u'Character01_LF_TwistJointKnee02_sknjnt_Limbskn', u'Character01_LF_TwistJointKnee03_sknjnt_Limbskn']
RHToDeleteNodes          = [u'Character01_LF_TwistOriginKnee00_grp_Limbskn', u'Character01_MD_endTwistKnee01_loc_LimbsknShape', u'Character01_MD_startTwistKnee01_loc_LimbsknShape', u'Character01_LF_DistanceNode03_dbtw_Limbskn', u'Character01_LF_StretchyTwistJointKnee00_mult_Limbskn', u'Character01_LF_TwistJointKnee00_mult_Limbskn', u'Character01_LF_TwistJointAddKnee00_pma_Limbskn', u'Character01_LF_TwistJointKnee00_jnt_Limbskn_aimConstraint1', u'Character01_LF_NegativeLookAtRotationKnee00_mult_Limbskn']

AddRibbon (RHArmSknJointStructure, RHSknParentGroup, RHcurrentTwists, RHToDeleteNodes, "Z")


#RHSknParentGroup =  'Character01_RH_shoulder00_grp_Limbskn'
#RHArmSknJointStructure = ['Character01_RH_shoulder00_jnt_Limbskn','Character01_RH_elbow00_jnt_Limbskn','Character01_RH_wrist00_jnt_Limbskn']
#ArmRightControls = "Character01_Arm_RHControls00_grp_controls"








