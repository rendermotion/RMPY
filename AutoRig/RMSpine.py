import pymel.core as pm
import maya.api.OpenMaya as om
from RMPY import nameConvention
from RMPY import RMRigTools
from RMPY import RMRigShapeControls

import pprint
import math


class RMSpine(object):
    def __init__(self,NameConv = None):
        if not NameConv:
            self.NameConv = nameConvention.NameConvention()
        else:
            self.NameConv = NameConv
        self.kinematics = []

        self.spineIK = None
        self.spineJoints = None
        self.rootSpineJoints = None
        self.spineCurve = None
        self.chestJoint = None
        self.COG = None
        self.ResetCOG = None
        self.rootHip = None
        self.hipJoints = None
        self.SpineLength = None
        self.secondaryControls = []
        self.hipControl = None
        self.resetHipControl = None

        self.chestControl = None
        self.resetChestControl = None

        self.waistControl = None
        self.resetWaistControl = None

        self.rootLeftClavicleJoints = None
        self.LeftClavicleJoints = None
        self.rootRightClavicleJoints = None
        self.RightClavicleJoints = None

        self.ResetChestRotationControl = None
        self.ChestRotationControl = None
        
        self.resetRightClavicleControl = None
        self.rightClavicleControl = None
        self.resetLeftClavicleControl = None
        self.leftClavicleControl = None


    def RMCreateSpineRig(self,SpineRef,HipRefPnts,leftClavicle,RightClavicle):

        self.rootSpineJoints,  self.spineJoints, self.chestJoint = self.RMCreateSpineJointStructure(SpineRef)
        self.RMCreateSpineIKSystem()

        self.rootHip,  self.hipJoints = self.RMCreateHipJointStructure(HipRefPnts)
        self.resetHipControl, self.hipControl = self.RMCreateHipSystem()

        self.rootLeftClavicleJoints, self.LeftClavicleJoints = self.RMCreateClavicleJointStructure(leftClavicle)
        self.resetLeftClavicleControl, self.leftClavicleControl = self.RMCreateClavicleSystem(self.rootLeftClavicleJoints ,self.LeftClavicleJoints )

        self.rootRightClavicleJoints, self.RightClavicleJoints = self.RMCreateClavicleJointStructure(RightClavicle)
        self.resetRightClavicleControl, self.rightClavicleControl = self.RMCreateClavicleSystem(self.rootRightClavicleJoints, self.RightClavicleJoints)

        self.RMCleanUP()


    def RMCleanUP(self):


        self.NameConv.rename_set_from_name(self.LeftClavicleJoints[0], "sknjnt", "objectType")
        self.NameConv.rename_set_from_name(self.RightClavicleJoints[0], "sknjnt", "objectType")
        self.NameConv.rename_set_from_name(self.spineJoints, "sknjnt", "objectType")
        self.NameConv.rename_set_from_name(self.hipJoints[0], "sknjnt", "objectType")
        self.NameConv.rename_set_from_name(self.chestJoint, "sknjnt", "objectType")


        RMRigTools.RMLockAndHideAttributes(self.hipControl, "000111000h")
        RMRigTools.RMLockAndHideAttributes(self.ChestRotationControl, "000111000h")
        RMRigTools.RMLockAndHideAttributes(self.waistControl, "000111000h")
        RMRigTools.RMLockAndHideAttributes(self.COG, "111111000h")
        RMRigTools.RMLockAndHideAttributes(self.chestControl, "111111000h")
        RMRigTools.RMLockAndHideAttributes(self.leftClavicleControl, "111111000h")
        RMRigTools.RMLockAndHideAttributes(self.rightClavicleControl, "111111000h")



    def RMCreateSpineJointStructure(self,SpineRef):
        rootSpine, joints = RMRigTools.RMCreateBonesAtPoints(SpineRef, ZAxisOrientation="z")

        SpineLength = RMRigTools.RMPointDistance(joints[0],joints[len(joints) - 1])
        chestJoint = pm.joint(name="chest")

        self.NameConv.rename_name_in_format(chestJoint, name=chestJoint)

        RMRigTools.RMAlign(joints[len(joints)-1],chestJoint,3)
        #pm.parent(chestJoint, joints[len(joints)-1])
        pm.makeIdentity(chestJoint, apply = True , r = False, t = True, s = True, n=0)
        pm.xform(chestJoint,t=[SpineLength/4,0,0],os=True, relative=True )
        return rootSpine, joints, chestJoint


    
    def RMCreateSpineIKSystem(self):

        self.spineIK, effector, self.spineCurve = pm.ikHandle(startJoint = self.spineJoints[0],endEffector = self.spineJoints[len(self.spineJoints)-1],createCurve = True,numSpans = len(self.spineJoints) ,solver = "ikSplineSolver",name = "spineIK")

        self.NameConv.rename_based_on_base_name(self.spineJoints[len(self.spineJoints) - 1], self.spineIK)
        self.NameConv.rename_based_on_base_name(self.spineJoints[len(self.spineJoints) - 1], effector,
                                                name="spineIKEffector")
        self.NameConv.rename_based_on_base_name(self.spineJoints[len(self.spineJoints) - 1], self.spineCurve,
                                                name="spineIKCurve")

        Clusters = RMRigTools.RMCreateClustersOnCurve(self.spineCurve)
        ClustersGroup = RMRigTools.RMCreateGroupOnObj(Clusters[0])
        RMRigTools.RMParentArray(ClustersGroup, Clusters[1:])
        self.kinematics.append(ClustersGroup)
        self.kinematics.append(self.spineIK)

        #ResetCOG, COG = RMRigShapeControls.create_box_ctrl(self.spineJoints[0],Yratio=3,Zratio=3)
        ResetCOG, COG = RMRigShapeControls.RMImportMoveControl(self.spineJoints[0], scale=RMRigTools.RMLenghtOfBone(self.spineJoints[0]) * 7)

        self.NameConv.rename_set_from_name(COG, "COG", "name")
        


        ResetChest, Chest = RMRigShapeControls.RMCreateBoxCtrl(self.spineJoints[len(self.spineJoints) - 1],Yratio=3,Zratio=3)
        self.NameConv.rename_set_from_name(Chest, "Chest", "name")

        SpineLength = RMRigTools.RMPointDistance(COG,Chest)

        ResetChestRotation, ChestRotation = RMRigShapeControls.RMCircularControl (Chest, radius = SpineLength ,name = "ChestRotation" )

        pm.parent(ResetChestRotation, Chest)


        pm.parentConstraint ( ChestRotation , self.chestJoint, mo = True)

        self.ResetChestRotationControl = ResetChestRotation
        self.ChestRotationControl = ChestRotation
        
        #pm.parent(ResetChest,COG)


        pm.setAttr(self.spineIK + ".dTwistControlEnable",1)
        pm.setAttr(self.spineIK + ".dWorldUpType", 4)
        #pm.setAttr(self.spineIK + ".dForwardAxis",0)#Valid Option only in Maya 2016
        pm.setAttr(self.spineIK + ".dWorldUpAxis",0)
        pm.connectAttr(COG + ".worldMatrix[0]", self.spineIK + ".dWorldUpMatrix")
        pm.connectAttr(Chest + ".worldMatrix[0]", self.spineIK + ".dWorldUpMatrixEnd")

        locators = RMRigTools.RMCreateNLocatorsBetweenObjects (COG, Chest, 3, align="FirstObj")
        

        ChestControls=[]
        ChestGroups=[]
        AllSpine = [COG]
        spineControlGroup = pm.group(empty=True, name="SpineControls")
        self.NameConv.rename_name_in_format(spineControlGroup, name=spineControlGroup)


        self.secondaryControls
        for eachPosition in locators:
            ControlGroup , NewControl = RMRigShapeControls.RMImportMoveControl(eachPosition, scale=SpineLength)
            self.secondaryControls.append(NewControl)
            ChestGroups.append(ControlGroup)
            ChestControls.append(NewControl)
            AllSpine.append(NewControl)
            ResetTransformGroup = RMRigTools.RMCreateGroupOnObj(ControlGroup)
            print ResetTransformGroup
            print spineControlGroup
            pm.parent(ResetTransformGroup, spineControlGroup)
            pm.delete(eachPosition)
            RMRigTools.RMLockAndHideAttributes(NewControl,"111000000h")

        AllSpine.append(Chest)

        pm.parent(spineControlGroup, COG)
        
        ChestChildGroup = RMRigTools.RMCreateGroupOnObj(Chest, Type="child", NameConv=self.NameConv)
        pm.xform(ChestChildGroup, t = [-SpineLength/2, 0 ,0], os = True,relative = True)
        spineEnds = [COG, ChestChildGroup]

        self.RMRedistributeConstraint(AllSpine, Clusters, 3, ConstraintType="parent")
        self.RMRedistributeConstraint(spineEnds, ChestGroups, 3, ConstraintType="parent")


        DeformedShape, OrigShape = pm.listRelatives(self.spineCurve, children = True,shapes=True)
        curveInfoOriginal = pm.shadingNode('curveInfo', asUtility=True, name = "SpineCurveOriginalInfo")
        curveInfoDeformed = pm.shadingNode('curveInfo', asUtility=True, name = "SpineCurveDeformedInfo")
        self.NameConv.rename_name_in_format(curveInfoOriginal, name=curveInfoOriginal)
        self.NameConv.rename_name_in_format(curveInfoDeformed, name=curveInfoDeformed)

        pm.connectAttr( OrigShape + ".worldSpace[0]", curveInfoOriginal + ".inputCurve")
        pm.connectAttr( DeformedShape + ".worldSpace[0]", curveInfoDeformed + ".inputCurve")
        curveScaleRatio = pm.shadingNode('multiplyDivide', asUtility=True, name="SpineScaleRatio")
        self.NameConv.rename_name_in_format(curveScaleRatio, name=curveScaleRatio)

        pm.connectAttr(curveInfoDeformed + ".arcLength", curveScaleRatio + ".input1X" )
        pm.connectAttr(curveInfoOriginal + ".arcLength", curveScaleRatio + ".input2X" )
        pm.setAttr(curveScaleRatio + ".operation",2)

        #preparation for Scale multiplication function of each spine joint
        pm.addAttr(Chest, at="float",sn = "ssf", ln = "spineSquashFactor",   hnv = 1, hxv = 1, h = 0, k = 1, smn = -10, smx = 10)

        GaussLen = len(self.spineJoints)
        center = len(self.spineJoints)/2
        powMaxValue = 5
        powRate = powMaxValue/center
        index = 1

        for eachJoint in self.spineJoints[1:]:
            #translate stretch multiplication functions of each spine joint
            SpineStretchMult = pm.shadingNode( 'multiplyDivide', asUtility=True, name="SpineTranslateStretchMult" + self.NameConv.get_a_short_name(eachJoint))
            self.NameConv.rename_name_in_format(SpineStretchMult, name=SpineStretchMult)
            CurrentXPosition = pm.getAttr( eachJoint + ".translateX")
            pm.setAttr(SpineStretchMult + ".input2X", CurrentXPosition)
            pm.connectAttr( curveScaleRatio + ".outputX", SpineStretchMult + ".input1X")
            pm.connectAttr( SpineStretchMult + ".outputX", eachJoint + ".translateX")
            
            #Scale multiplication function of each spine joint
            
            if index >= center:
                PowValue = (GaussLen - 1 - index) 
            else:
                PowValue = index

            SpineStretchRatio = pm.shadingNode( 'multiplyDivide', asUtility = True, name = "SpineStretchRatio" + self.NameConv.get_a_short_name(eachJoint))
            self.NameConv.rename_name_in_format(SpineStretchRatio, name=SpineStretchRatio)
            pm.connectAttr(Chest+".spineSquashFactor ", SpineStretchRatio + ".input1X")
            pm.setAttr(SpineStretchRatio + ".input2X", PowValue)
            pm.setAttr(SpineStretchRatio + ".operation", 1)

            SpineScaleStretchPow = pm.shadingNode( 'multiplyDivide', asUtility = True, name = "SpineScaleStretchPow" + self.NameConv.get_a_short_name(eachJoint))
            self.NameConv.rename_name_in_format(SpineScaleStretchPow, name=SpineScaleStretchPow)
            pm.connectAttr(curveScaleRatio+".outputX ", SpineScaleStretchPow + ".input1X")
            pm.connectAttr(SpineStretchRatio + ".outputX ", SpineScaleStretchPow + ".input2X")
            pm.setAttr(SpineScaleStretchPow + ".operation", 3)

            SpineInversScaleRatio = pm.shadingNode( 'multiplyDivide', asUtility=True, name = "SpineInverseScaleRatio")
            self.NameConv.rename_name_in_format(SpineInversScaleRatio, name=SpineInversScaleRatio)
            pm.connectAttr(SpineScaleStretchPow+".outputX ",SpineInversScaleRatio + ".input1X")
            pm.setAttr(SpineInversScaleRatio + ".input2X", -1)
            pm.setAttr(SpineInversScaleRatio + ".operation", 3)

            pm.connectAttr(SpineInversScaleRatio + ".outputX", eachJoint + ".scaleY")
            pm.connectAttr(SpineInversScaleRatio + ".outputX", eachJoint + ".scaleZ")
            index += 1


        resetWaist, waist = RMRigShapeControls.RMCircularControl( AllSpine[1], radius = SpineLength*.8,name = "waist")
        


        pm.parent( ResetChest, waist)
        pm.parent( resetWaist, COG)

        self.chestControl = Chest
        self.resetChestControl = ResetChest
        self.waistControl = waist
        self.resetWaistControl = resetWaist
        self.COG = COG
        self.ResetCOG = ResetCOG
        self.SpineLength = SpineLength

    def RMCreateHipJointStructure(self,HipRefPnts):
        rootHip , hipJoints = RMRigTools.RMCreateBonesAtPoints(HipRefPnts, ZAxisOrientation = "z")
        self.NameConv.rename_set_from_name(hipJoints, "Thehip", "name")
        self.NameConv.rename_set_from_name(hipJoints, "hip", "name")
        return rootHip , hipJoints
    
    def RMCreateHipSystem(self):
        #resetHipControl, hipControl = RMRigShapeControls.circular_control(self.rootHip,radius = self.SpineLength *.7,name = "hip")
        resetHipControl, hipControl = RMRigShapeControls.RMImportMoveControl(self.rootHip, scale = self.SpineLength, name = "hip",Type = "circleDeform")
        pm.parent( resetHipControl, self.COG)
        pm.parentConstraint( hipControl, self.hipJoints[0])
        pm.parent( self.rootHip, self.spineJoints[0])
        return resetHipControl, hipControl

        #self.rootHip
        #self.hipJoints
    def RMCreateClavicleJointStructure(self,ClavRefPnts):
        rootClavicle , ClavicleJoints = RMRigTools.RMCreateBonesAtPoints(ClavRefPnts, ZAxisOrientation = "z")
        self.NameConv.rename_set_from_name(ClavicleJoints[1], "clavicle", "name")
        pm.parent( rootClavicle , self.chestJoint )

        return rootClavicle , ClavicleJoints
    
    def RMCreateClavicleSystem(self,rootClavicle,ClavicleJoints):
        resetClavicleControl, clavicleControl = RMRigShapeControls.RMCreateBoxCtrl( ClavicleJoints[0] )
        pm.parent( resetClavicleControl, self.ChestRotationControl )
        pm.parentConstraint( clavicleControl, ClavicleJoints[0])
        return resetClavicleControl , clavicleControl


    def RMRedistributeConstraint(self,ListOfDrivers, ListOfConstrained, MaxInfluences, KeepBorders = True, ConstraintType = "parent"):

        DeltaMaxInfluence =  1/(float (len(ListOfDrivers))-1)
        CentersControlDic = {}
        for i in range (0,len( ListOfDrivers)):
            CentersControlDic[ListOfDrivers[i]] = ( DeltaMaxInfluence*i)

        pprint.pprint (CentersControlDic)
        DeltaPositionConstrained = float(1/(float(len(ListOfConstrained))-1))
        PositionConstDic = {}

        for i in range(0,len( ListOfConstrained)):
            PositionConstDic[ListOfConstrained[i]] = (DeltaPositionConstrained*i)

        pprint.pprint (PositionConstDic)

        reach = MaxInfluences * DeltaMaxInfluence

        for eachConstrained in ListOfConstrained:
            for eachDriver in ListOfDrivers:
                weight = self.RMGaussCosine( PositionConstDic [ eachConstrained ], CentersControlDic [ eachDriver ], reach )
                if weight > 0:
                    if ConstraintType == "parent":
                        pm.parentConstraint(eachDriver, eachConstrained , weight = weight,mo = True)
                    elif ConstraintType == "point":
                        pm.pointConstraint(eachDriver, eachConstrained  , weight = weight,mo = True)
                    elif ConstraintType == "orient":
                        pm.orientConstraint(eachDriver, eachConstrained , weight = weight,mo = True)
                    else:
                        print ("not valid costraintType requested, valid types are point, parent, or orient")


    def RMGaussCosine(self,XValue,Center,GaussLen):
        DistanceFromCenter = abs(XValue - Center)
        if DistanceFromCenter < GaussLen / 2:
            return (math.cos(DistanceFromCenter/(GaussLen/2) * math.pi) + 1)/2
        else:
            return 0





