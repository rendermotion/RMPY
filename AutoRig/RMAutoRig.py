
from RMPY.AutoRig import RMLimbIKFK
from RMPY.AutoRig import RMSpaceSwitch
from RMPY.AutoRig.Hand import RMGenericHandRig
from RMPY.AutoRig import RMSpine
from RMPY.AutoRig import RMNeckHead
from RMPY.AutoRig import RMVisibilitySwitch
import maya.mel as mel
from RMPY import RMNameConvention
try:
    from MetacubeScripts import MetacubeFileNameConvention
except:
    pass
from RMPY.AutoRig import RMFeet
from RMPY import RMRigShapeControls

from RMPY import RMRigTools

import pymel.core as pm


reload(RMFeet)
reload(RMSpine)
reload(RMNeckHead)
reload(RMLimbIKFK)
reload(RMSpaceSwitch)
reload(RMGenericHandRig)
reload(RMNameConvention)
reload(RMVisibilitySwitch)
reload(RMRigShapeControls)
reload(RMRigTools)
reload(RMSpine)

class RMBiped(object):
    def __init__(self, NameConv = None):
        if not NameConv:
            self.NameConv = RMNameConvention.RMNameConvention()
        else:
            self.NameConv = NameConv
        self.NameConv.default_names["LastName"] = "Character01"
        self.SPSW = RMSpaceSwitch.RMSpaceSwitch()
        self.rig_tools = RMRigTools.RMRigTools()

        self.Spine = None
        self.LimbArmLeft = None
        self.LimbLegRight = None
        self.LimbLegLeft = None
        self.LimbArmRight = None
        self.LFfeet = None
        self.RHfeet = None
        self.moverMain = None
        self.GHRightRig = None
        self.GHLeftRig = None
        self.Mover01 = None
        self.Mover02 = None
        self.placer = None
        self.NeckHead = RMNeckHead.RMNeckHead()
        try:
            self.MetaNameConv = MetacubeFileNameConvention.MetacubeFileNameConvention()
        except:
            pass
        self.GHRightRig = None
        self.GHLeftRig = None

        self.geometryGroups=["body_grp", "cloth_grp", "accesories_grp","hair_grp", "trackers_grp","collision_grp", "pxycloth_grp", "pxyhair_grp", "dynspline_grp"]

    def CreateBipedRig(self):
        try:
            CharacterName = self.MetaNameConv.AssetType + "_" + self.MetaNameConv.AssetName + "_rig"
        except :
            CharacterName = "MainCharacter"

        if pm.objExists(CharacterName):
            MainGroup = CharacterName
        else:
            MainGroup = pm.group(empty=True, name = CharacterName)


        if pm.objExists("mesh_grp"):
            mesh = pm.ls("mesh_grp")[0]
        else:
            mesh = pm.group(empty=True, name = "mesh_grp")

        if pm.objExists("rig_grp"):
            rig = pm.ls("rig_grp")[0]
        else:
            rig = pm.group(empty=True, name="rig_grp")
        pm.setAttr("%s.visibility" % rig, False)
        
        for eachgroup in self.geometryGroups:
            if not pm.objExists(eachgroup):
                pm.group( empty = True, name = eachgroup)
                pm.parent(eachgroup, mesh)

        deformation = pm.group( empty = True, name = "deformation")
        kinematics = pm.group( empty = True, name = "kinematics")
        joints = pm.group( empty = True, name = "joints")
        controls = pm.group( empty = True, name = "controls_grp")
        self.world = pm.group( empty = True, name ="world"+ CharacterName)
        self.moverWorld = pm.group( empty = True, name ="moverWorld"+ CharacterName)

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

        pm.parent(self.world, self.kinematics)
        pm.parent(self.moverWorld, self.kinematics)

        

        meshp = pm.listRelatives( mesh , parent = True )
        if not meshp:
            pm.parent(mesh ,MainGroup)
        rigp = pm.listRelatives( rig , parent = True )
        if not rigp:
            pm.parent(rig ,MainGroup)

        pm.parent(controls ,MainGroup)
        pm.parent(deformation , rig)
        pm.parent(kinematics , rig)
        pm.parent(joints , rig)


        #Creacion del spine 
        spineJoints = ["C_Spine01_rig_pnt","C_Spine02_rig_pnt","C_Spine03_rig_pnt","C_Spine04_rig_pnt","C_Spine05_rig_pnt"]
        hip = ["C_Spine01_rig_pnt","C_Hip01_rig_pnt"]
        clavLF = ["L_clavicle01_rig_pnt","L_shoulder01_rig_pnt"]
        clavRH = ["R_clavicle01_rig_pnt","R_shoulder01_rig_pnt"]

        self.Spine.RMCreateSpineRig(spineJoints,hip,clavLF,clavRH)

        spineKinematics = pm.group(empty = True, name="spineKinematics")
        self.NameConv.rename_name_in_format(spineKinematics, system="kinematics")
        spineControls = pm.group(empty = True, name="spineControls")
        self.NameConv.rename_name_in_format(spineControls, system="controls")
        spineJoints = pm.group(empty = True, name = "spineJoints")
        self.NameConv.rename_name_in_format(spineJoints, system="joints")

        pm.parent(spineKinematics, kinematics)
        pm.parent(spineControls, controls)
        pm.parent(spineJoints, deformation)

        pm.parent(self.Spine.ResetCOG, spineControls)
        pm.parent(self.Spine.kinematics, spineKinematics)
        pm.parent(self.Spine.rootSpineJoints, spineJoints)


        mover01Reset, self.Mover01 = RMRigShapeControls.RMCircularControl ( self.world , axis = "Y" , radius = self.Spine.SpineLength * 1.5  , name = "mover02")
        mover02Reset, self.Mover02 = RMRigShapeControls.RMCircularControl ( self.world , axis = "Y" , radius = self.Spine.SpineLength * 2, name = "mover01")
        placerReset , self.placer  = RMRigShapeControls.RMCircularControl ( self.world , axis = "Y" , radius = self.Spine.SpineLength * 2.5  , name = "mainPlacer")

        self.mainMover = self.Mover01
        pm.parent( placerReset, controls)
        pm.parent( mover02Reset, self.placer)
        pm.parent( mover01Reset, self.Mover02)
        pm.parent(spineControls,self.Mover01)
        pm.parentConstraint( self.Mover01 , self.moverWorld )


        '''
        WorldRClavicle = pm.group(empty = True, name = "clavicleWorld" )
        WorldRClavicle = self.NameConv.RMRenameBasedOnBaseName (self.Spine.rightClavicleControl, WorldRClavicle, NewName = "world", System = "RClavicleSpaceSwitch")
        RMRigTools.RMAlign(self.Spine.rightClavicleControl, WorldRClavicle ,3)
        pm.parent( WorldRClavicle, self.moverWorld)
        RSpaceSwitchGroup = RMRigTools.RMCreateGroupOnObj(self.Spine.rightClavicleControl)
        self.SPSW.CreateSpaceSwitch(RSpaceSwitchGroup,[self.Spine.resetRightClavicleControl, WorldRClavicle],self.Spine.rightClavicleControl, constraintType = "orient")

        WorldLClavicle = pm.group(empty = True, name = "clavicleWorld" )
        WorldLClavicle = self.NameConv.RMRenameBasedOnBaseName (self.Spine.leftClavicleControl, WorldLClavicle, NewName = "world", System = "LClavicleSpaceSwitch")
        RMRigTools.RMAlign(self.Spine.leftClavicleControl, WorldLClavicle ,3)
        pm.parent( WorldLClavicle, self.moverWorld)
        LSpaceSwitchGroup = RMRigTools.RMCreateGroupOnObj(self.Spine.leftClavicleControl)
        self.SPSW.CreateSpaceSwitch(LSpaceSwitchGroup,[self.Spine.resetLeftClavicleControl, WorldLClavicle],self.Spine.leftClavicleControl, constraintType = "orient")
        '''

        #Creacion de la cabeza

        neck = ["C_neck01_rig_pnt","C_head01_rig_pnt"]
        Head = ["C_head01_rig_pnt","C_headTip01_rig_pnt"]
        Jaw = ["C_jaw01_rig_pnt","C_jawTip01_rig_pnt"]

        self.NeckHead.RMCreateHeadAndNeckRig(Head, neck, Jaw)
        pm.parent( self.NeckHead.RootNeckJoints, self.Spine.chestJoint )
        pm.parent( self.NeckHead.resetNeckControl, self.Spine.ChestRotationControl )

        WorldHead = pm.group(empty = True, name="worldHead" )
        self.NameConv.rename_based_on_base_name(self.NeckHead.headControl, WorldHead, name="world", system="HeadSpaceSwitch")
        RMRigTools.RMAlign(self.NeckHead.resetHeadControl, WorldHead ,3)
        pm.parent(WorldHead ,self.world)

        HeadResetPoint = pm.group(empty = True, name = "NeckOrientConstraint")
        self.NameConv.rename_based_on_base_name (self.NeckHead.headControl, HeadResetPoint,
                                                 name="Neck", system="HeadSpaceSwitch")
        RMRigTools.RMAlign(self.NeckHead.resetHeadControl, HeadResetPoint ,3)
        pm.parent(HeadResetPoint, self.NeckHead.NeckJoints[1] )

        self.SPSW.CreateSpaceSwitch(self.NeckHead.resetHeadControl,[ HeadResetPoint , WorldHead ], self.NeckHead.headControl , constraintType = "orient",mo = True)


        #Creacion de Brazos
        #BrazoDerecho
        self.LimbArmRight.RMLimbRig("R_shoulder01_rig_pnt", FKAxisFree='010')
        RHArmDic = self.OrganizeLimb(self.LimbArmRight,"RH","Arm", self.Spine.RightClavicleJoints[1],self.Spine.chestJoint)


        RHWorldFKArm = pm.group(empty = True, name = "ArmWorld" )
        self.NameConv.rename_based_on_base_name (self.LimbArmRight.FKparentGroup, RHWorldFKArm, name="world",
                                                                                               system="RFKArmSpaceSwitch")
        RMRigTools.RMAlign(self.LimbArmRight.FKparentGroup, RHWorldFKArm ,3)
        pm.parent(RHWorldFKArm, self.moverWorld)
        RSpaceSwitchGroup = self.rig_tools.RMCreateGroupOnObj(self.LimbArmRight.FKparentGroup)
        self.SPSW.CreateSpaceSwitchReverse(self.LimbArmRight.FKparentGroup,
                                           [RSpaceSwitchGroup, RHWorldFKArm],
                                           self.LimbArmRight.FKFirstLimbControl,
                                           sswtype="float",
                                           Name="", mo=False,
                                           constraintType="orient")

        #BrazoIzquierdo
        self.LimbArmLeft.RMLimbRig("L_shoulder01_rig_pnt",FKAxisFree='010')
        RHArmDic = self.OrganizeLimb(self.LimbArmLeft,"LF","Arm", self.Spine.LeftClavicleJoints[1],self.Spine.chestJoint)


        LFWorldFKArm = pm.group(empty = True, name = "ArmWorld" )
        self.NameConv.rename_based_on_base_name(self.LimbArmLeft.FKparentGroup, LFWorldFKArm,
                                                 name="world", system="LFKArmSpaceSwitch")
        RMRigTools.RMAlign(self.LimbArmLeft.FKparentGroup, LFWorldFKArm ,3)
        pm.parent( LFWorldFKArm, self.moverWorld)
        LSpaceSwitchGroup = self.rig_tools.RMCreateGroupOnObj(self.LimbArmLeft.FKparentGroup)
        self.SPSW.CreateSpaceSwitchReverse(self.LimbArmLeft.FKparentGroup,[LSpaceSwitchGroup, LFWorldFKArm],self.LimbArmLeft.FKFirstLimbControl,sswtype = "float", Name="", mo = False, constraintType = "orient")


        #ManoDerecha
        self.GHRightRig = RMGenericHandRig.RMGenericHandRig()
        self.GHRightRig.CreateHandRig("R_palm01_rig_pnt",self.LimbArmRight.SpaceSwitchControl)

        #pm.group(name = "R_palmMover_grp_rig")
        RMRigTools.RMAlign("R_palm01_rig_pnt", self.LimbArmRight.IKControlResetPoint , 3)
        RMRigTools.RMAlign("R_palm01_rig_pnt", self.LimbArmRight.ThirdLimbParent , 3)


        self.LimbArmRight.SPSW.RMCreateListConstraintSwitch([self.GHRightRig.MainKinematics],[self.LimbArmRight.IKjointStructure[2]]         , self.LimbArmRight.SpaceSwitchControl,SpaceSwitchName="IKFKSwitch")
        self.LimbArmRight.SPSW.RMCreateListConstraintSwitch([self.GHRightRig.MainKinematics],[self.LimbArmRight.FKTrirdLimbControl], self.LimbArmRight.SpaceSwitchControl,SpaceSwitchName="IKFKSwitch", reverse = True)
        self.LimbArmLeft.SPSW.CreateSpaceSwitch(self.LimbArmRight.IKControlResetPoint,[self.Spine.rightClavicleControl ,self.world, self.Spine.COG, self.Spine.hipJoints[0], self.NeckHead.HeadJoints[0],self.moverWorld], self.LimbArmRight.ikControl)

        pm.parent ( self.GHRightRig.MainKinematics, RHArmDic["kinematics"])
        pm.parent ( self.GHRightRig.GHS.palmJoint , self.LimbArmRight.TJElbow.TwistJoints[len(self.LimbArmRight.TJElbow.TwistJoints) - 1])
        pm.parent ( self.GHRightRig.PalmResetPoint, RHArmDic["controls"] )

        #ManoIzquierda
        self.GHLeftRig = RMGenericHandRig.RMGenericHandRig()
        self.GHLeftRig.CreateHandRig("L_palm01_rig_pnt", PalmControl = self.LimbArmLeft.SpaceSwitchControl )

        RMRigTools.RMAlign("L_palm01_rig_pnt", self.LimbArmLeft.IKControlResetPoint , 3)
        RMRigTools.RMAlign("L_palm01_rig_pnt", self.LimbArmLeft.ThirdLimbParent , 3)

        self.LimbArmLeft.SPSW.RMCreateListConstraintSwitch ([self.GHLeftRig.MainKinematics],[self.LimbArmLeft.IKjointStructure[2]], self.LimbArmLeft.SpaceSwitchControl,SpaceSwitchName="IKFKSwitch")
        self.LimbArmLeft.SPSW.RMCreateListConstraintSwitch ([self.GHLeftRig.MainKinematics],[self.LimbArmLeft.FKTrirdLimbControl] , self.LimbArmLeft.SpaceSwitchControl,SpaceSwitchName="IKFKSwitch", reverse = True)
        self.LimbArmLeft.SPSW.CreateSpaceSwitch(self.LimbArmLeft.IKControlResetPoint,[self.Spine.leftClavicleControl ,self.world, self.Spine.COG, self.Spine.hipJoints[0], self.NeckHead.HeadJoints[0],self.moverWorld], self.LimbArmLeft.ikControl)
        
        pm.parent ( self.GHLeftRig.MainKinematics, RHArmDic["kinematics"])
        pm.parent ( self.GHLeftRig.GHS.palmJoint , self.LimbArmLeft.TJElbow.TwistJoints[len(self.LimbArmLeft.TJElbow.TwistJoints) - 1])
        pm.parent ( self.GHLeftRig.PalmResetPoint, RHArmDic["controls"])

        #Creacion de pierna

        self.LimbLegRight.RMLimbRig("R_leg01_rig_pnt",FKAxisFree='001')
        RHLegDic = self.OrganizeLimb(self.LimbLegRight,"RH","Leg", self.Spine.hipJoints[1],self.Spine.hipJoints[1])

        self.LimbLegLeft.RMLimbRig("L_leg01_rig_pnt",FKAxisFree='001')
        LFLegDic = self.OrganizeLimb(self.LimbLegLeft,"LF","Leg", self.Spine.hipJoints[1],self.Spine.hipJoints[1])

        
        Locator = pm.spaceLocator(name = "referenceLocator")
        
        RMRigTools.RMAlign("L_ball01_rig_pnt", Locator, 1)
        pm.setAttr(Locator +".rotateX", 90)
        pm.setAttr(Locator +".rotateZ", -90)

        RMRigTools.RMAlign(Locator, self.LimbLegLeft.IKControlResetPoint , 2)
        RMRigTools.RMAlign(Locator, self.LimbLegLeft.ThirdLimbParent , 2)
        RMRigTools.RMAlign(Locator, self.LimbLegRight.IKControlResetPoint , 2)
        RMRigTools.RMAlign(Locator, self.LimbLegRight.ThirdLimbParent , 2)


        pm.delete(Locator)


        StandarFeetLFPoints = {"feet" : ["L_ankleFeet01_rig_pnt","L_ball01_rig_pnt","L_toe01_rig_pnt"],
                    "limitBack":"L_footLimitBack01_rig_pnt",
                    "limitOut":"L_footLimitOuter01_rig_pnt",
                    "limitIn":"L_footLimitInner01_rig_pnt"}

        self.LFfeet.RigFeetIKFK(StandarFeetLFPoints, self.LimbLegLeft.ikControl, self.LimbLegLeft.FKTrirdLimbControl)

        self.LimbLegLeft.SPSW.RMCreateListConstraintSwitch(self.LFfeet.StandardFeetJoints, self.LFfeet.StandardFeetIKJoints , self.LimbLegLeft.SpaceSwitchControl, SpaceSwitchName="IKFKSwitch")
        self.LimbLegLeft.SPSW.RMCreateListConstraintSwitch(self.LFfeet.StandardFeetJoints, self.LFfeet.StandardFeetFKJoints , self.LimbLegLeft.SpaceSwitchControl, SpaceSwitchName="IKFKSwitch", reverse = True)

        pm.parent(self.LFfeet.rootJoints, self.LimbLegLeft.TJElbow.TwistJoints[len(self.LimbLegLeft.TJElbow.TwistJoints) -1])

        feetJointsGroup = pm.group(empty = True, name="FeetJoints")
        self.NameConv.rename_name_in_format(feetJointsGroup, side="LF")
        pm.parent(self.LFfeet.MainFeetKinematics  , feetJointsGroup)
        pm.parent(self.LFfeet.rootFKJoints, feetJointsGroup)
        pm.parent(feetJointsGroup, self.joints)

        pm.pointConstraint(self.LimbLegLeft.ikControl, self.LimbLegLeft.IkHandle,remove=True)
        pm.parent(self.LimbLegLeft.IkHandle, self.LFfeet.IKAttachPoint)

        pm.parent( self.LFfeet.rootIKJoints, self.LimbLegLeft.IKjointStructure[2] )


        StandarFeetRHPoints = {"feet" : ["R_ankleFeet01_rig_pnt","R_ball01_rig_pnt","R_toe01_rig_pnt"],
                    "limitBack":"R_footLimitBack01_rig_pnt",
                    "limitOut":"R_footLimitOuter01_rig_pnt",
                    "limitIn":"R_footLimitInner01_rig_pnt"}


        self.RHfeet.RigFeetIKFK(StandarFeetRHPoints, self.LimbLegRight.ikControl, self.LimbLegRight.FKTrirdLimbControl)

        self.LimbLegRight.SPSW.RMCreateListConstraintSwitch(self.RHfeet.StandardFeetJoints ,self.RHfeet.StandardFeetIKJoints , self.LimbLegRight.SpaceSwitchControl, SpaceSwitchName="IKFKSwitch")
        self.LimbLegRight.SPSW.RMCreateListConstraintSwitch(self.RHfeet.StandardFeetJoints ,self.RHfeet.StandardFeetFKJoints , self.LimbLegRight.SpaceSwitchControl, SpaceSwitchName="IKFKSwitch", reverse = True)

        pm.parent(self.RHfeet.rootJoints, self.LimbLegRight.TJElbow.TwistJoints[len(self.LimbLegRight.TJElbow.TwistJoints) - 1])

        
        feetJointsGroup = pm.group(empty = True,name = "FeetJoints")
        self.NameConv.rename_name_in_format(feetJointsGroup, side="right")
        pm.parent(self.RHfeet.MainFeetKinematics  , feetJointsGroup)
        pm.parent(self.RHfeet.rootFKJoints, feetJointsGroup)
        pm.parent(feetJointsGroup, self.joints)

        pm.pointConstraint(self.LimbLegRight.ikControl,self.LimbLegRight.IkHandle,remove=True)
        pm.parent(self.LimbLegRight.IkHandle, self.RHfeet.IKAttachPoint)

        pm.parent( self.RHfeet.rootIKJoints, self.LimbLegRight.IKjointStructure[2])

        #pm.parentConstraint(placer,self.kinematics)
        self.ColorCode()
        self.Visibility()

        
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
        self.NeckHead
        self.GHRightRig = None
        self.GHLeftRig = None
        '''
        VisSwitch = RMVisibilitySwitch.RMVisibilitySwitch()

        Vgroup , VControl = RMRigShapeControls.RMImportMoveControl( self.NeckHead.HeadJoints[0] ,scale = RMRigTools.RMLenghtOfBone(self.NeckHead.HeadJoints[0]),Type="v")
        pm.setAttr("%s.rotateX" % Vgroup, 0)
        pm.setAttr("%s.rotateY" % Vgroup, 0)
        pm.setAttr("%s.rotateZ" % Vgroup, 0)
        
        RMRigTools.RMAlign(self.NeckHead.HeadJoints[1] , Vgroup , 1)
        

        pm.parentConstraint( self.Mover01 , Vgroup, mo = True)
        pm.parent(Vgroup,"controls_grp")

        VisSwitch.ConstraintVisibility( [self.LimbArmLeft.PoleVectorControl,   self.LimbArmLeft.ikControl,  self.LimbArmLeft.FKFirstLimbControl,  self.LimbArmLeft.FKSecondLimbControl,  self.LimbArmLeft.FKTrirdLimbControl , self.LimbArmLeft.SpaceSwitchControl,
                                         self.LimbArmRight.PoleVectorControl, self.LimbArmRight.ikControl, self.LimbArmRight.FKFirstLimbControl, self.LimbArmRight.FKSecondLimbControl, self.LimbArmRight.FKTrirdLimbControl, self.LimbArmRight.SpaceSwitchControl,
                                         self.LimbLegLeft.PoleVectorControl,   self.LimbLegLeft.ikControl,  self.LimbLegLeft.FKFirstLimbControl,  self.LimbLegLeft.FKSecondLimbControl,  self.LimbLegLeft.FKTrirdLimbControl,  self.LimbLegLeft.SpaceSwitchControl,
                                         self.LimbLegRight.PoleVectorControl, self.LimbLegRight.ikControl, self.LimbLegRight.FKFirstLimbControl, self.LimbLegRight.FKSecondLimbControl, self.LimbLegRight.FKTrirdLimbControl, self.LimbLegRight.SpaceSwitchControl,
                                         self.Spine.rightClavicleControl,self.Spine.leftClavicleControl,self.Spine.waistControl,self.Spine.chestControl,self.Spine.hipControl,self.Spine.COG,
                                         self.LFfeet.SecondLimbFeetControl,self.RHfeet.SecondLimbFeetControl, 
                                         self.GHRightRig.MainControl , self.GHLeftRig.MainControl] , VControl, VisibilitySwitch = "Controls", visibilityType = "lodVisibility")
        #print self.LFfeet.feetMainMoveIK
        #print self.RHfeet.feetMainMoveIK
        VisSwitch.ConstraintVisibility([ self.LimbArmLeft.TJArm.TwistControl,  self.LimbArmLeft.TJElbow.TwistControl,
                                        self.LimbArmRight.TJArm.TwistControl, self.LimbArmRight.TJElbow.TwistControl,
                                         self.LimbLegLeft.TJArm.TwistControl,  self.LimbLegLeft.TJElbow.TwistControl,
                                        self.LimbLegRight.TJArm.TwistControl, self.LimbLegRight.TJElbow.TwistControl ] ,VControl, VisibilitySwitch = "Secondary", visibilityType = "lodVisibility")

        VisSwitch.ConstraintVisibility( ["body_grp"] ,VControl, VisibilitySwitch = "Geometry")
        VisSwitch.AddAffectedObject( VControl, self.Spine.secondaryControls, VisibilitySwitch = "Secondary" ,visibilityType = "lodVisibility")
        VisSwitch.AddAffectedObject( VControl, self.GHRightRig.fingerControlsReset, VisibilitySwitch = "Controls" ,visibilityType = "lodVisibility")
        VisSwitch.AddAffectedObject( VControl, self.GHLeftRig.fingerControlsReset, VisibilitySwitch = "Controls" ,visibilityType = "lodVisibility")

        RMRigTools.RMLockAndHideAttributes(VControl,"0000000000")
        #VisSwitch.AddEnumParameters( VControl, VisibilitySwitch = "Facial"   )

        pass

    def ColorCode(self):
        RightControls = pm.ls("R_*_ctr")
        LeftControls = pm.ls("L_*_ctr")
        MiddleControls = pm.ls("C_*_ctr")

        for eachControl in RightControls:
            pm.setAttr(eachControl + ".overrideEnabled",True)
            pm.setAttr(eachControl + ".overrideColor",14)
        for eachControl in LeftControls:
            pm.setAttr(eachControl + ".overrideEnabled",True)
            pm.setAttr(eachControl + ".overrideColor",13)
        for eachControl in MiddleControls:
            pm.setAttr(eachControl + ".overrideEnabled",True)
            pm.setAttr(eachControl + ".overrideColor",17)
            
        COGCtrl = pm.ls("*COG*_ctr")[0]
        print COGCtrl
        #pm.setAttr(COGCtrl + ".overrideEnabled",True)
        pm.setAttr(COGCtrl + ".overrideColor",6)



        
    def OrganizeLimb (self, limbObject, Name, Side, ObjectAttached,deformationParent):
        limbKinematics = pm.group(empty=True, name=Name + "Kinematics")
        self.NameConv.rename_name_in_format(limbKinematics, side=Side, system="kinematics")
        limbControls = pm.group(empty=True, name=Name + "Controls")
        self.NameConv.rename_name_in_format(limbControls, side=Side, system="controls")
        limbJoints = pm.group(empty=True, name=Name + "Joints")
        self.NameConv.rename_name_in_format(limbJoints, side=Side, System="joints")

        pm.parent(limbKinematics, self.kinematics )
        pm.parent(limbControls, self.mainMover)
        pm.parent(limbJoints, self.joints)

        pm.parent(limbObject.kinematics, limbKinematics)

        pm.parent( limbObject.limbMover , limbJoints)

        pm.parentConstraint(ObjectAttached , limbObject.limbMover, mo = True)

        pm.parent( limbObject.IKControls, limbControls)
        pm.parent( limbObject.FKControls, limbControls)
        pm.parent( limbObject.ResetSpaceSwitchControl, limbControls)

        pm.parent ( limbObject.TJArm.TwistControlResetPoint , limbControls)
        pm.parent ( limbObject.TJArm.TwistResetJoints , deformationParent)
        pm.parent ( limbObject.TJElbow.TwistControlResetPoint , limbControls)
        #No es necesario emparentar las Twist delelbow dado que fueron emparentadas dentro de la classe Limb al momento de creacion
        pm.parent(limbObject.TJArm.kinematics, limbKinematics)
        pm.parent(limbObject.TJElbow.kinematics, limbKinematics)

        return {"kinematics":limbKinematics, "controls":limbControls,"joints":limbJoints}








