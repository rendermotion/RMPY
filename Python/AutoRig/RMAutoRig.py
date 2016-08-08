
from AutoRig import RMLimbIKFK
from AutoRig import RMSpaceSwitch
from AutoRig.Hand import RMGenericHandRig
from AutoRig import RMSpine
from AutoRig import RMNeckHead
import maya.mel as mel
import RMNameConvention
#from MetacubeScripts import MetacubeFileNameConvention
from AutoRig import RMFeet
reload (RMFeet)
reload (RMSpine)
reload (RMNeckHead)
reload (RMLimbIKFK)
reload (RMSpaceSwitch)
reload (RMGenericHandRig)
reload (RMNameConvention)
import RMRigTools

import maya.cmds as cmds

class RMBiped(object):
    def __init__(self, NameConv = None):
        if not NameConv:
            self.NameConv = RMNameConvention.RMNameConvention()
        else:
            self.NameConv = NameConv
        self.NameConv.DefaultNames["LastName"] = "Character01"
        self.SPSW = RMSpaceSwitch.RMSpaceSwitch()

        self.Spine = RMSpine.RMSpine()
        self.LimbArmLeft = RMLimbIKFK.RMLimbIKFK(self.NameConv)
        self.LimbLegRight = RMLimbIKFK.RMLimbIKFK(self.NameConv)
        self.LimbLegLeft = RMLimbIKFK.RMLimbIKFK(self.NameConv)
        self.LimbArmRight = RMLimbIKFK.RMLimbIKFK(self.NameConv)
        self.LFfeet = RMFeet.RMFeetRig()
        self.RHfeet = RMFeet.RMFeetRig()

        self.NeckHead = RMNeckHead.RMNeckHead()
        #self.MetaNameConv = MetacubeFileNameConvention.MetacubeFileNameConvention()

    def CreateBipedRig(self):

        #if self.MetaNameConv.nameInFormat:
        #    CharacterName = self.MetaNameConv.AssetType+"_" + self.MetaNameConv.AssetName + "_rig"
        CharacterName = "MainCharacter"

        if cmds.objExists(CharacterName):
            MainGroup = CharacterName
        else:
            MainGroup = cmds.group(empty = True, name = CharacterName)
        #else:
        #    MainGroup = cmds.group(empty = True, name = "MainCharacter")


        if cmds.objExists("mesh_grp"):
            mesh = "mesh_grp"
        else:
            mesh = cmds.group( empty = True, name = "mesh_grp")    
        if cmds.objExists("rig_grp"):
            rig = "rig_grp"
        else:
            rig = cmds.group( empty = True, name = "rig_grp")

        deformation = cmds.group( empty = True, name = "deformation")
        kinematics = cmds.group( empty = True, name = "kinematics")
        joints = cmds.group( empty = True, name = "joints")
        controls = cmds.group( empty = True, name = "controls_grp")

        self.kinematics = kinematics
        self.deformation = deformation
        self.joints = joints
        self.controls = controls

        meshp = cmds.listRelatives( mesh , parent = True )
        if not meshp:
            cmds.parent(mesh ,MainGroup)
        rigp = cmds.listRelatives( rig , parent = True )
        if not rigp:
            cmds.parent(rig ,MainGroup)

        cmds.parent(controls ,MainGroup)
        cmds.parent(deformation , rig)
        cmds.parent(kinematics , rig)
        cmds.parent(joints , rig)
        
        #Creacion del spine 
        spineJoints = ["Character01_MD_Spine_pnt_rfr","Character01_MD_Spine1_pnt_rfr","Character01_MD_Spine2_pnt_rfr","Character01_MD_Spine3_pnt_rfr","Character01_MD_Spine4_pnt_rfr"]
        hip = ["Character01_MD_Spine_pnt_rfr","Character01_MD_Hip_pnt_rfr"]
        clavLF = ["Character01_LF_clavicle_pnt_rfr","Character01_LF_shoulder_pnt_rfr"]
        clavRH = ["Character01_RH_clavicle_pnt_rfr","Character01_RH_shoulder_pnt_rfr"]
        self.Spine.RMCreateSpineRig(spineJoints,hip,clavLF,clavRH)

        spineKinematics = cmds.group(empty = True, name = "spineKinematics")
        spineKinematics = self.NameConv.RMRenameNameInFormat( spineKinematics, System = "kinematics")
        spineControls = cmds.group(empty = True, name = "spineControls")
        spineControls = self.NameConv.RMRenameNameInFormat( spineControls, System = "controls")
        spineJoints = cmds.group(empty = True, name = "spineJoints")
        spineJoints = self.NameConv.RMRenameNameInFormat( spineJoints, System = "joints")

        cmds.parent (spineKinematics, kinematics)
        cmds.parent (spineControls, controls)
        cmds.parent (spineJoints, deformation)

        cmds.parent(self.Spine.ResetCOG,spineControls)
        RMRigTools.RMParentArray( spineKinematics , self.Spine.kinematics)
        cmds.parent(self.Spine.rootSpineJoints, spineJoints)

        #Creacion de la cabeza

        neck = ["Character01_MD_neck_pnt_rfr","Character01_MD_head_pnt_rfr"]
        Head = ["Character01_MD_head_pnt_rfr","Character01_MD_headTip_ball_pnt_rfr"]
        Jaw = ["Character01_MD_jaw_pnt_rfr","Character01_MD_jawTip_pnt_rfr"]

        self.NeckHead.RMCreateHeadAndNeckRig(Head, neck, Jaw)
        cmds.parent( self.NeckHead.RootNeckJoints, self.Spine.chestJoint)
        cmds.parent( self.NeckHead.resetNeckControl, self.Spine.chestControl)
        

        #Creacion del Brazo 

        self.LimbArmRight.RMLimbRig("Character01_RH_shoulder_pnt_rfr", FKAxisFree='010')
        RHArmDic = self.OrganizeLimb(self.LimbArmRight,"RH","Arm", self.Spine.RightClavicleJoints[1],self.Spine.chestJoint)

        self.LimbArmLeft.RMLimbRig("Character01_LF_shoulder_pnt_rfr",FKAxisFree='110')
        RHArmDic = self.OrganizeLimb(self.LimbArmLeft,"LF","Arm", self.Spine.LeftClavicleJoints[1],self.Spine.chestJoint)


        GHRightRig = RMGenericHandRig.RMGenericHandRig()
        GHRightRig.CreateHandRig("Character01_RH_palm_pnt_rfr")

        #cmds.group(name = "Character01_RH_palmMover_grp_rig")
        RMRigTools.RMAlign("Character01_RH_palm_pnt_rfr", self.LimbArmRight.IKControlResetPoint , 3)
        RMRigTools.RMAlign("Character01_RH_palm_pnt_rfr", self.LimbArmRight.ThirdLimbParent , 3)

        self.LimbArmRight.SPSW.RMCreateListConstraintSwitch([GHRightRig.MainKinematics],[self.LimbArmRight.ikControl]         , self.LimbArmRight.SpaceSwitchControl,SpaceSwitchName="IKFKSwitch")
        self.LimbArmRight.SPSW.RMCreateListConstraintSwitch([GHRightRig.MainKinematics],[self.LimbArmRight.FKTrirdLimbControl], self.LimbArmRight.SpaceSwitchControl,SpaceSwitchName="IKFKSwitch", reverse = True)
        
        cmds.parent ( GHRightRig.MainKinematics, RHArmDic["kinematics"])
        cmds.parent ( GHRightRig.GHS.palmJoint , self.LimbArmRight.TJElbow.TwistJoints[len(self.LimbArmRight.TJElbow.TwistJoints) - 1])
        cmds.parent ( GHRightRig.PalmResetPoint, RHArmDic["controls"] )


        GHLeftRig = RMGenericHandRig.RMGenericHandRig()
        GHLeftRig.CreateHandRig("Character01_LF_palm_pnt_rfr")

        RMRigTools.RMAlign("Character01_LF_palm_pnt_rfr", self.LimbArmLeft.IKControlResetPoint , 3)
        RMRigTools.RMAlign("Character01_LF_palm_pnt_rfr", self.LimbArmLeft.ThirdLimbParent , 3)

        self.LimbArmLeft.SPSW.RMCreateListConstraintSwitch([GHLeftRig.MainKinematics],[self.LimbArmLeft.ikControl]         , self.LimbArmLeft.SpaceSwitchControl,SpaceSwitchName="IKFKSwitch")
        self.LimbArmLeft.SPSW.RMCreateListConstraintSwitch([GHLeftRig.MainKinematics],[self.LimbArmLeft.FKTrirdLimbControl], self.LimbArmLeft.SpaceSwitchControl,SpaceSwitchName="IKFKSwitch", reverse = True)
        
        cmds.parent ( GHLeftRig.MainKinematics, RHArmDic["kinematics"])
        cmds.parent ( GHLeftRig.GHS.palmJoint , self.LimbArmLeft.TJElbow.TwistJoints[len(self.LimbArmLeft.TJElbow.TwistJoints) - 1])
        cmds.parent ( GHLeftRig.PalmResetPoint, RHArmDic["controls"] )

        #Creacion de pierna


        self.LimbLegRight.RMLimbRig("Character01_RH_leg_pnt_rfr",FKAxisFree='001')
        RHLegDic = self.OrganizeLimb(self.LimbLegRight,"RH","Leg", self.Spine.hipJoints[1],self.Spine.hipJoints[1])

        self.LimbLegLeft.RMLimbRig("Character01_LF_leg_pnt_rfr",FKAxisFree='001')
        LFLegDic = self.OrganizeLimb(self.LimbLegLeft,"LF","Leg", self.Spine.hipJoints[1],self.Spine.hipJoints[1])

        StandarFeetLFPoints = {"feet" : ["Character01_LF_ankleFeet_pnt_rfr","Character01_LF_ball_pnt_rfr","Character01_LF_toe_pnt_rfr"],
                    "limitBack":"Character01_LF_footLimitBack_pnt_rfr",
                    "limitOut":"Character01_LF_footLimitOuter_pnt_rfr",
                    "limitIn":"Character01_LF_footLimitInner_pnt_rfr"}

        #self.LFfeet = RMFeetRig()
        self.LFfeet.RigFeetIKFK(StandarFeetLFPoints, self.LimbLegLeft.ikControl, self.LimbLegLeft.FKTrirdLimbControl)

        self.LimbLegLeft.SPSW.RMCreateListConstraintSwitch(self.LFfeet.StandardFeetJoints ,self.LFfeet.StandardFeetIKJoints , self.LimbLegLeft.SpaceSwitchControl, SpaceSwitchName="IKFKSwitch")
        self.LimbLegLeft.SPSW.RMCreateListConstraintSwitch(self.LFfeet.StandardFeetJoints ,self.LFfeet.StandardFeetFKJoints , self.LimbLegLeft.SpaceSwitchControl, SpaceSwitchName="IKFKSwitch", reverse = True)

        cmds.parent(self.LFfeet.rootJoints, self.LimbLegLeft.TJElbow.TwistJoints[len(self.LimbLegLeft.TJElbow.TwistJoints) -1])

        feetJointsGroup = cmds.group(empty = True, name = "FeetJoints")
        feetJointsGroup = self.NameConv.RMRenameNameInFormat(feetJointsGroup,Side="LF")
        cmds.parent(self.LFfeet.MainFeetKinematics  , feetJointsGroup)
        cmds.parent(self.LFfeet.rootFKJoints, feetJointsGroup)
        cmds.parent(feetJointsGroup, self.joints)

       
        cmds.pointConstraint(self.LimbLegLeft.ikControl,self.LimbLegLeft.IkHandle,remove=True)
        cmds.parent(self.LimbLegLeft.IkHandle, self.LFfeet.IKAttachPoint)


        StandarFeetRHPoints = {"feet" : ["Character01_RH_ankleFeet_pnt_rfr","Character01_RH_ball_pnt_rfr","Character01_RH_toe_pnt_rfr"],
                    "limitBack":"Character01_RH_footLimitBack_pnt_rfr",
                    "limitOut":"Character01_RH_footLimitOuter_pnt_rfr",
                    "limitIn":"Character01_RH_footLimitInner_pnt_rfr"}

        self.RHfeet = RMFeetRig()
        self.RHfeet.RigFeetIKFK(StandarFeetLFPoints, self.LimbLegRight.ikControl, self.LimbLegRight.FKTrirdLimbControl)

        self.LimbLegRight.SPSW.RMCreateListConstraintSwitch(self.RHfeet.StandardFeetJoints ,self.RHfeet.StandardFeetIKJoints , self.LimbLegRight.SpaceSwitchControl, SpaceSwitchName="IKFKSwitch")
        self.LimbLegRight.SPSW.RMCreateListConstraintSwitch(self.RHfeet.StandardFeetJoints ,self.RHfeet.StandardFeetFKJoints , self.LimbLegRight.SpaceSwitchControl, SpaceSwitchName="IKFKSwitch", reverse = True)

        cmds.parent(self.RHfeet.rootJoints, self.LimbLegRight.TJElbow.TwistJoints[len(self.LimbLegRight.TJElbow.TwistJoints) - 1])

        
        feetJointsGroup = cmds.group(empty = True,name = "FeetJoints")
        feetJointsGroup = self.NameConv.RMRenameNameInFormat(feetJointsGroup,Side="RH")
        cmds.parent(self.RHfeet.MainFeetKinematics  , feetJointsGroup)
        cmds.parent(self.RHfeet.rootFKJoints, feetJointsGroup)
        cmds.parent(feetJointsGroup, self.joints)

        cmds.pointConstraint(self.LimbLegRight.ikControl,self.LimbLegRight.IkHandle,remove=True)
        cmds.parent(self.LimbLegRight.IkHandle, self.RHfeet.IKAttachPoint)

        
    def OrganizeLimb (self, limbObject, Name, Side, ObjectAttached,deformationParent):
        limbKinematics = cmds.group(empty = True, name = Name + "Kinematics")
        limbKinematics = self.NameConv.RMRenameNameInFormat( limbKinematics ,Side = Side, System = "kinematics")
        limbControls = cmds.group(empty = True, name = Name + "Controls")
        limbControls = self.NameConv.RMRenameNameInFormat( limbControls , Side = Side, System = "controls")
        limbJoints = cmds.group(empty = True, name = Name + "Joints")
        limbJoints = self.NameConv.RMRenameNameInFormat( limbJoints , Side = Side, System = "joints")

        cmds.parent ( limbKinematics, self.kinematics )
        cmds.parent ( limbControls, self.controls)
        cmds.parent ( limbJoints, self.joints)

        RMRigTools.RMParentArray(limbKinematics,limbObject.kinematics)

        cmds.parent( limbObject.limbMover , limbJoints)

        cmds.parentConstraint(ObjectAttached , limbObject.limbMover, mo = True)

        cmds.parent( limbObject.IKControls, limbControls)
        cmds.parent( limbObject.FKControls, limbControls)
        cmds.parent( limbObject.ResetSpaceSwitchControl, limbControls)

        cmds.parent ( limbObject.TJArm.TwistControlResetPoint , limbControls)
        cmds.parent ( limbObject.TJArm.TwistResetJoints , deformationParent)
        cmds.parent ( limbObject.TJElbow.TwistControlResetPoint , limbControls)
        #No es necesario emparentar las Twist delelbow dado que fueron emparentadas dentro de la classe Limb al momento de creacion
        RMRigTools.RMParentArray(limbKinematics , limbObject.TJArm.kinematics)
        RMRigTools.RMParentArray(limbKinematics , limbObject.TJElbow.kinematics)

        return {"kinematics":limbKinematics, "controls":limbControls,"joints":limbJoints}

BipedRig = RMBiped()
BipedRig.CreateBipedRig()




