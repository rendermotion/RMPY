
from AutoRig import RMLimbIKFK
from AutoRig import RMSpaceSwitch
from AutoRig.Hand import RMGenericHandRig
from AutoRig import RMSpine
from AutoRig import RMNeckHead
import maya.mel as mel
import RMNameConvention
from MetacubeScripts import MetacubeFileNameConvention
from AutoRig import RMFeet
import RMRigShapeControls
import RMRigTools
import maya.cmds as cmds

reload (RMFeet)
reload (RMSpine)
reload (RMNeckHead)
reload (RMLimbIKFK)
reload (RMSpaceSwitch)
reload (RMGenericHandRig)
reload (RMNameConvention)

class RMBiped(object):
    def __init__(self, NameConv = None):
        if not NameConv:
            self.NameConv = RMNameConvention.RMNameConvention()
        else:
            self.NameConv = NameConv
        self.NameConv.DefaultNames["LastName"] = "Character01"
        self.SPSW = RMSpaceSwitch.RMSpaceSwitch()

        self.Spine = None
        self.LimbArmLeft = None
        self.LimbLegRight = None
        self.LimbLegLeft = None
        self.LimbArmRight = None
        self.LFfeet = None
        self.RHfeet = None
        self.moverMain = None
        self.Mover01 = None
        self.Mover02 = None
        self.placer = None
        self.NeckHead = RMNeckHead.RMNeckHead()
        self.MetaNameConv = MetacubeFileNameConvention.MetacubeFileNameConvention()

        self.geometryGroups=["body_grp", "cloth_grp", "accesories_grp","hair_grp", "trackers_grp","collision_grp", "pxycloth_grp", "pxyhair_grp", "dynspline_grp"]

    def CreateBipedRig(self):
        if self.MetaNameConv.nameInFormat:
            CharacterName = self.MetaNameConv.AssetType + "_" + self.MetaNameConv.AssetName + "_rig"
        else :
            CharacterName = "MainCharacter"

        if cmds.objExists(CharacterName):
            MainGroup = CharacterName
        else:
            MainGroup = cmds.group(empty = True, name = CharacterName)


        if cmds.objExists("mesh_grp"):
            mesh = "mesh_grp"
        else:
            mesh = cmds.group( empty = True, name = "mesh_grp")

        if cmds.objExists("rig_grp"):
            rig = "rig_grp"
        else:
            rig = cmds.group( empty = True, name = "rig_grp")

        
        for eachgroup in self.geometryGroups:
            if not cmds.objExists(eachgroup):
                cmds.group( empty = True, name = eachgroup)
                cmds.parent(eachgroup, mesh)

        deformation = cmds.group( empty = True, name = "deformation")
        kinematics = cmds.group( empty = True, name = "kinematics")
        joints = cmds.group( empty = True, name = "joints")
        controls = cmds.group( empty = True, name = "controls_grp")
        self.world = cmds.group( empty = True, name ="world"+ CharacterName)

        self.Spine = RMSpine.RMSpine()
        self.LimbArmLeft = RMLimbIKFK.RMLimbIKFK(worldNode = self.world, NameConv = self.NameConv)
        self.LimbLegRight = RMLimbIKFK.RMLimbIKFK(worldNode = self.world, NameConv = self.NameConv)
        self.LimbLegLeft = RMLimbIKFK.RMLimbIKFK(worldNode = self.world, NameConv = self.NameConv)
        self.LimbArmRight = RMLimbIKFK.RMLimbIKFK(worldNode = self.world, NameConv = self.NameConv)
        self.LFfeet = RMFeet.RMFeetRig()
        self.RHfeet = RMFeet.RMFeetRig()

        self.kinematics = kinematics
        self.deformation = deformation
        self.joints = joints
        self.controls = controls

        cmds.parent(self.world, self.kinematics)
        print self.world

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

        cmds.parent( self.Spine.ResetCOG,spineControls)
        RMRigTools.RMParentArray( spineKinematics , self.Spine.kinematics)
        cmds.parent( self.Spine.rootSpineJoints, spineJoints)


        mover01Reset, self.Mover01 = RMRigShapeControls.RMCircularControl ( self.world , axis = "Y" , radius = self.Spine.SpineLength * 1.5  , name = "mover02")
        mover02Reset, self.Mover02 = RMRigShapeControls.RMCircularControl ( self.world , axis = "Y" , radius = self.Spine.SpineLength * 2, name = "mover01")
        placerReset , self.placer  = RMRigShapeControls.RMCircularControl ( self.world , axis = "Y" , radius = self.Spine.SpineLength * 2.5  , name = "mainPlacer")

        self.mainMover = self.Mover01
        cmds.parent( placerReset, controls)
        cmds.parent( mover02Reset, self.placer)
        cmds.parent( mover01Reset, self.Mover02)
        
        cmds.parent(spineControls,self.Mover01)

        #Creacion de la cabeza

        neck = ["Character01_MD_neck_pnt_rfr","Character01_MD_head_pnt_rfr"]
        Head = ["Character01_MD_head_pnt_rfr","Character01_MD_headTip_ball_pnt_rfr"]
        Jaw = ["Character01_MD_jaw_pnt_rfr","Character01_MD_jawTip_pnt_rfr"]

        self.NeckHead.RMCreateHeadAndNeckRig( Head, neck, Jaw )
        cmds.parent( self.NeckHead.RootNeckJoints, self.Spine.chestJoint )
        cmds.parent( self.NeckHead.resetNeckControl, self.Spine.ChestRotationControl )

        WorldHead = cmds.group(empty = True, name = "worldHead" )
        WorldHead = self.NameConv.RMRenameBasedOnBaseName (self.NeckHead.headControl, WorldHead, NewName = "world",System = "HeadSpaceSwitch")
        RMRigTools.RMAlign(self.NeckHead.resetHeadControl, WorldHead ,3)
        cmds.parent(WorldHead ,self.world)

        HeadResetPoint = cmds.group(empty = True, name = "NeckOrientConstraint" )
        HeadResetPoint = self.NameConv.RMRenameBasedOnBaseName (self.NeckHead.headControl, HeadResetPoint, NewName = "Neck" , System = "HeadSpaceSwitch")
        RMRigTools.RMAlign(self.NeckHead.resetHeadControl, HeadResetPoint ,3)
        cmds.parent ( HeadResetPoint , self.NeckHead.NeckJoints[1] )  

        self.SPSW.CreateSpaceSwitch(self.NeckHead.resetHeadControl,[ HeadResetPoint , WorldHead ], self.NeckHead.headControl , constraintType = "orient",mo = True)


        #Creacion de Brazos

        self.LimbArmRight.RMLimbRig("Character01_RH_shoulder_pnt_rfr", FKAxisFree='010')
        RHArmDic = self.OrganizeLimb(self.LimbArmRight,"RH","Arm", self.Spine.RightClavicleJoints[1],self.Spine.chestJoint)

        self.LimbArmLeft.RMLimbRig("Character01_LF_shoulder_pnt_rfr",FKAxisFree='010')
        RHArmDic = self.OrganizeLimb(self.LimbArmLeft,"LF","Arm", self.Spine.LeftClavicleJoints[1],self.Spine.chestJoint)


        GHRightRig = RMGenericHandRig.RMGenericHandRig()
        GHRightRig.CreateHandRig("Character01_RH_palm_pnt_rfr",self.LimbArmRight.SpaceSwitchControl)

        #cmds.group(name = "Character01_RH_palmMover_grp_rig")
        RMRigTools.RMAlign("Character01_RH_palm_pnt_rfr", self.LimbArmRight.IKControlResetPoint , 3)
        RMRigTools.RMAlign("Character01_RH_palm_pnt_rfr", self.LimbArmRight.ThirdLimbParent , 3)


        self.LimbArmRight.SPSW.RMCreateListConstraintSwitch([GHRightRig.MainKinematics],[self.LimbArmRight.IKjointStructure[2]]         , self.LimbArmRight.SpaceSwitchControl,SpaceSwitchName="IKFKSwitch")
        self.LimbArmRight.SPSW.RMCreateListConstraintSwitch([GHRightRig.MainKinematics],[self.LimbArmRight.FKTrirdLimbControl], self.LimbArmRight.SpaceSwitchControl,SpaceSwitchName="IKFKSwitch", reverse = True)
        self.LimbArmLeft.SPSW.CreateSpaceSwitch(self.LimbArmRight.IKControlResetPoint,[self.Spine.rightClavicleControl ,self.world, self.Spine.COG, self.Spine.hipJoints[0], self.NeckHead.HeadJoints[0]], self.LimbArmRight.ikControl)

        cmds.parent ( GHRightRig.MainKinematics, RHArmDic["kinematics"])
        cmds.parent ( GHRightRig.GHS.palmJoint , self.LimbArmRight.TJElbow.TwistJoints[len(self.LimbArmRight.TJElbow.TwistJoints) - 1])
        cmds.parent ( GHRightRig.PalmResetPoint, RHArmDic["controls"] )


        GHLeftRig = RMGenericHandRig.RMGenericHandRig()
        GHLeftRig.CreateHandRig("Character01_LF_palm_pnt_rfr", PalmControl = self.LimbArmLeft.SpaceSwitchControl )

        RMRigTools.RMAlign("Character01_LF_palm_pnt_rfr", self.LimbArmLeft.IKControlResetPoint , 3)
        RMRigTools.RMAlign("Character01_LF_palm_pnt_rfr", self.LimbArmLeft.ThirdLimbParent , 3)

        self.LimbArmLeft.SPSW.RMCreateListConstraintSwitch ([GHLeftRig.MainKinematics],[self.LimbArmLeft.IKjointStructure[2]], self.LimbArmLeft.SpaceSwitchControl,SpaceSwitchName="IKFKSwitch")
        self.LimbArmLeft.SPSW.RMCreateListConstraintSwitch ([GHLeftRig.MainKinematics],[self.LimbArmLeft.FKTrirdLimbControl] , self.LimbArmLeft.SpaceSwitchControl,SpaceSwitchName="IKFKSwitch", reverse = True)
        self.LimbArmLeft.SPSW.CreateSpaceSwitch(self.LimbArmLeft.IKControlResetPoint,[self.Spine.leftClavicleControl ,self.world, self.Spine.COG, self.Spine.hipJoints[0], self.NeckHead.HeadJoints[0]], self.LimbArmLeft.ikControl)
        
        cmds.parent ( GHLeftRig.MainKinematics, RHArmDic["kinematics"])
        cmds.parent ( GHLeftRig.GHS.palmJoint , self.LimbArmLeft.TJElbow.TwistJoints[len(self.LimbArmLeft.TJElbow.TwistJoints) - 1])
        cmds.parent ( GHLeftRig.PalmResetPoint, RHArmDic["controls"])

        #Creacion de pierna

        self.LimbLegRight.RMLimbRig("Character01_RH_leg_pnt_rfr",FKAxisFree='001')
        RHLegDic = self.OrganizeLimb(self.LimbLegRight,"RH","Leg", self.Spine.hipJoints[1],self.Spine.hipJoints[1])

        self.LimbLegLeft.RMLimbRig("Character01_LF_leg_pnt_rfr",FKAxisFree='001')
        LFLegDic = self.OrganizeLimb(self.LimbLegLeft,"LF","Leg", self.Spine.hipJoints[1],self.Spine.hipJoints[1])

        
        Locator = cmds.spaceLocator(name = "referenceLocator")[0]
        
        RMRigTools.RMAlign( "Character01_LF_ball_pnt_rfr" , Locator , 1)
        cmds.setAttr ( Locator +".rotateX", 90)
        cmds.setAttr ( Locator +".rotateZ", -90)

        RMRigTools.RMAlign(Locator, self.LimbLegLeft.IKControlResetPoint , 2)
        RMRigTools.RMAlign(Locator, self.LimbLegLeft.ThirdLimbParent , 2)
        RMRigTools.RMAlign(Locator, self.LimbLegRight.IKControlResetPoint , 2)
        RMRigTools.RMAlign(Locator, self.LimbLegRight.ThirdLimbParent , 2)


        cmds.delete( Locator )


        StandarFeetLFPoints = {"feet" : ["Character01_LF_ankleFeet_pnt_rfr","Character01_LF_ball_pnt_rfr","Character01_LF_toe_pnt_rfr"],
                    "limitBack":"Character01_LF_footLimitBack_pnt_rfr",
                    "limitOut":"Character01_LF_footLimitOuter_pnt_rfr",
                    "limitIn":"Character01_LF_footLimitInner_pnt_rfr"}

        self.LFfeet.RigFeetIKFK(StandarFeetLFPoints, self.LimbLegLeft.ikControl, self.LimbLegLeft.FKTrirdLimbControl)

        self.LimbLegLeft.SPSW.RMCreateListConstraintSwitch(self.LFfeet.StandardFeetJoints ,self.LFfeet.StandardFeetIKJoints , self.LimbLegLeft.SpaceSwitchControl, SpaceSwitchName="IKFKSwitch")
        self.LimbLegLeft.SPSW.RMCreateListConstraintSwitch(self.LFfeet.StandardFeetJoints ,self.LFfeet.StandardFeetFKJoints , self.LimbLegLeft.SpaceSwitchControl, SpaceSwitchName="IKFKSwitch", reverse = True)

        cmds.parent(self.LFfeet.rootJoints, self.LimbLegLeft.TJElbow.TwistJoints[len(self.LimbLegLeft.TJElbow.TwistJoints) -1])

        feetJointsGroup = cmds.group(empty = True, name = "FeetJoints")
        feetJointsGroup = self.NameConv.RMRenameNameInFormat(feetJointsGroup,Side="LF")
        cmds.parent(self.LFfeet.MainFeetKinematics  , feetJointsGroup)
        cmds.parent(self.LFfeet.rootFKJoints, feetJointsGroup)
        cmds.parent(feetJointsGroup, self.joints)

        cmds.pointConstraint(self.LimbLegLeft.ikControl, self.LimbLegLeft.IkHandle,remove=True)
        cmds.parent(self.LimbLegLeft.IkHandle, self.LFfeet.IKAttachPoint)

        cmds.parent( self.LFfeet.rootIKJoints, self.LimbLegLeft.IKjointStructure[2] )


        StandarFeetRHPoints = {"feet" : ["Character01_RH_ankleFeet_pnt_rfr","Character01_RH_ball_pnt_rfr","Character01_RH_toe_pnt_rfr"],
                    "limitBack":"Character01_RH_footLimitBack_pnt_rfr",
                    "limitOut":"Character01_RH_footLimitOuter_pnt_rfr",
                    "limitIn":"Character01_RH_footLimitInner_pnt_rfr"}


        self.RHfeet.RigFeetIKFK(StandarFeetRHPoints, self.LimbLegRight.ikControl, self.LimbLegRight.FKTrirdLimbControl)

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

        cmds.parent( self.RHfeet.rootIKJoints, self.LimbLegRight.IKjointStructure[2])

        #cmds.parentConstraint(placer,self.kinematics)
        self.ColorCode()
        
        #mover01Reset, Mover01 = RMRigShapeControls.RMCircularControl ( "world" , axis = "Y" ,radius = self.Spine.SpineLength * 3  , name = "mover02")

        #self.SPSW.


    def Visibility(self):
        '''self.Spine = None
        self.LimbArmLeft = None
        self.LimbLegRight = None
        self.LimbLegLeft = None
        self.LimbArmRight = None
        self.LFfeet = None
        self.RHfeet = None
        self.moverMain = None
        self.Mover01 = None
        self.Mover02 = None
        self.placer = None
        self.NeckHead'''

        #RMRigShapeControls.RMImportMoveControl(self.NeckHead.HeadJoints[0] ,scale = RMRigTools.RMLenghtOfBone(self.NeckHead.HeadJoints[0]),Type="v")


        pass

    def ColorCode(self):
        RightControls  = cmds.ls("*_RH_*_ctr_*")
        LeftControls   = cmds.ls("*_LF_*_ctr_*")
        MiddleControls = cmds.ls("*_MD_*_ctr_*")

        for eachControl in RightControls:
            cmds.setAttr(eachControl + ".overrideEnabled",True)
            cmds.setAttr(eachControl + ".overrideColor",14)
        for eachControl in LeftControls:
            cmds.setAttr(eachControl + ".overrideEnabled",True)
            cmds.setAttr(eachControl + ".overrideColor",13)
        for eachControl in MiddleControls:
            cmds.setAttr(eachControl + ".overrideEnabled",True)
            cmds.setAttr(eachControl + ".overrideColor",17)
            
        COGCtrl = cmds.ls("*COG*_ctr_*")[0]
        print COGCtrl
        #cmds.setAttr(COGCtrl + ".overrideEnabled",True)
        cmds.setAttr(COGCtrl + ".overrideColor",6)



        
    def OrganizeLimb (self, limbObject, Name, Side, ObjectAttached,deformationParent):
        limbKinematics = cmds.group(empty = True, name = Name + "Kinematics")
        limbKinematics = self.NameConv.RMRenameNameInFormat( limbKinematics ,Side = Side, System = "kinematics")
        limbControls = cmds.group(empty = True, name = Name + "Controls")
        limbControls = self.NameConv.RMRenameNameInFormat( limbControls , Side = Side, System = "controls")
        limbJoints = cmds.group(empty = True, name = Name + "Joints")
        limbJoints = self.NameConv.RMRenameNameInFormat( limbJoints , Side = Side, System = "joints")

        cmds.parent ( limbKinematics, self.kinematics )
        cmds.parent ( limbControls, self.mainMover)
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





