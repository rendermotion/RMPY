import maya.cmds
import maya.api.OpenMaya as om
import RMNameConvention
reload(RMNameConvention)
import RMRigTools
reload(RMRigTools)
import RMRigShapeControls
reload(RMRigShapeControls)
import pprint
import math


class RMSpine(object):
    def __init__(self,NameConv = None):
        if not NameConv:
            self.NameConv = RMNameConvention.RMNameConvention()
        else:
            self.NameConv = NameConv
        self.spineIK = None
        self.spineJoints = None
        self.rootSpine = None
        self.spineCurve = None
        self.COG = None

    def RMCreateSpineRig(self,SpineRef):

        self. rootSpine, self.spineJoints = self.RMCreateJointStructure(SpineRef)

        self.RMCreateSpineIKSystem()

    def RMCreateJointStructure(self,SpineRef):
        rootSpine , joints = RMRigTools.RMCreateBonesAtPoints(SpineRef,ZAxisOrientation = "z")
        return rootSpine , joints

    
    def RMCreateSpineIKSystem(self):

        self.spineIK, effector, self.spineCurve = cmds.ikHandle(startJoint = self.spineJoints[0],endEffector = self.spineJoints[len(self.spineJoints)-1],createCurve = True,numSpans = len(self.spineJoints) ,solver = "ikSplineSolver",name = "spineIK")
        self.spineIK = self.NameConv.RMRenameBasedOnBaseName(self.spineJoints[len(self.spineJoints)-1],self.spineIK)
        effector = self.NameConv.RMRenameBasedOnBaseName(self.spineJoints[len(self.spineJoints)-1],effector,NewName = "spineIKEffector")
        self.spineCurve = self.NameConv.RMRenameBasedOnBaseName(self.spineJoints[len(self.spineJoints)-1],self.spineCurve,NewName = "spineIKCurve")

        Clusters = RMRigTools.RMCreateClustersOnCurve(self.spineCurve)
        ClustersGroup = RMRigTools.RMCreateGroupOnObj(Clusters[0])
        RMRigTools.RMParentArray(ClustersGroup,Clusters[1:])


        COG = RMRigShapeControls.RMCreateBoxCtrl(self.spineJoints[0],Yratio=3,Zratio=3)
        COG = self.NameConv.RMRenameSetFromName(COG,"COG","Name")
        ResetCOG = RMRigTools.RMCreateGroupOnObj(COG)


        Chest = RMRigShapeControls.RMCreateBoxCtrl(self.spineJoints[len(self.spineJoints) - 1],Yratio=3,Zratio=3)
        Chest = self.NameConv.RMRenameSetFromName(Chest,"Chest","Name")
        ResetChest = RMRigTools.RMCreateGroupOnObj(Chest)
        
        #cmds.parent(ResetChest,COG)


        cmds.setAttr(self.spineIK + ".dTwistControlEnable",1)
        cmds.setAttr(self.spineIK + ".dWorldUpType",4)
        #cmds.setAttr(self.spineIK + ".dForwardAxis",0)#Valid Option only in Maya 2016
        cmds.setAttr(self.spineIK + ".dWorldUpAxis",0)
        cmds.connectAttr(COG + ".worldMatrix[0]", self.spineIK + ".dWorldUpMatrix")
        cmds.connectAttr(Chest + ".worldMatrix[0]", self.spineIK + ".dWorldUpMatrixEnd")

        locators = RMRigTools.RMCreateNLocatorsBetweenObjects (COG , Chest, 3, align = "FirstObj")
        
        SpineLength=RMRigTools.RMPointDistance(COG,Chest)

        ChestControls=[]
        ChestGroups=[]
        AllSpine = [COG]
        spineControlGroup = cmds.group(empty=True,name = "SpineControls")
        spineControlGroup = self.NameConv.RMRenameNameInFormat(spineControlGroup)


        for eachPosition in locators:
            ControlGroup , NewControl = RMRigShapeControls.RMImportMoveControl(eachPosition, scale = SpineLength)
            ChestGroups.append(ControlGroup)
            ChestControls.append(NewControl)
            AllSpine.append(NewControl)
            ResetTransformGroup = RMRigTools.RMCreateGroupOnObj(ControlGroup)
            cmds.parent(ResetTransformGroup,spineControlGroup)

        AllSpine.append(Chest)
        
        ChestChildGroup = RMRigTools.RMCreateGroupOnObj(Chest, Type = "child", NameConv = self.NameConv)
        cmds.xform(ChestChildGroup, t = [-SpineLength/2, 0 ,0], os = True,relative = True)
        spineEnds = [COG, ChestChildGroup]

        self.RMRedistributeConstraint( AllSpine, Clusters, 3, ConstraintType = "parent")
        self.RMRedistributeConstraint( spineEnds, ChestGroups, 3, ConstraintType = "parent")


        DeformedShape, OrigShape = cmds.listRelatives(self.spineCurve, children = True,shapes=True)
        curveInfoOriginal = cmds.shadingNode('curveInfo', asUtility=True, name = "SpineCurveOriginalInfo")
        curveInfoDeformed = cmds.shadingNode('curveInfo', asUtility=True, name = "SpineCurveDeformedInfo")
        curveInfoOriginal = self.NameConv.RMRenameNameInFormat( curveInfoOriginal)
        curveInfoDeformed = self.NameConv.RMRenameNameInFormat( curveInfoDeformed)

        cmds.connectAttr( OrigShape + ".worldSpace[0]", curveInfoOriginal + ".inputCurve")
        cmds.connectAttr( DeformedShape + ".worldSpace[0]", curveInfoDeformed + ".inputCurve")
        curveScaleRatio = cmds.shadingNode('multiplyDivide', asUtility=True, name = "SpineScaleRatio")
        curveScaleRatio = self.NameConv.RMRenameNameInFormat( curveScaleRatio)        

        cmds.connectAttr(curveInfoDeformed + ".arcLength", curveScaleRatio + ".input1X" )
        cmds.connectAttr(curveInfoOriginal + ".arcLength", curveScaleRatio + ".input2X" )
        cmds.setAttr (curveScaleRatio + ".operation",2)

        for eachJoint in self.spineJoints[1:]:
            SpineStretchMult = cmds.shadingNode( 'multiplyDivide', asUtility=True, name = "SpineStretchMult" + self.NameConv.RMGetAShortName(eachJoint))
            SpineStretchMult = self.NameConv.RMRenameNameInFormat( SpineStretchMult)
            CurrentXPosition = cmds.getAttr( eachJoint + ".translateX")
            cmds.setAttr(SpineStretchMult + ".input2X", CurrentXPosition)
            cmds.connectAttr( curveScaleRatio + ".outputX ", SpineStretchMult + ".input1X")
            cmds.connectAttr( SpineStretchMult + ".outputX", eachJoint + ".translateX")

        resetWaist, waist = RMRigShapeControls.RMCircularControl( AllSpine[1], radius = SpineLength*.8,name = "waist")
        cmds.parent( ResetChest, waist)
        cmds.parent( resetWaist, COG)
        resetHip , hip = RMRigShapeControls.RMCircularControl(COG,radius = SpineLength *.7,name = "waist")
        

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
                        cmds.parentConstraint(eachDriver, eachConstrained , weight = weight,mo = True)
                    elif ConstraintType == "point":
                        cmds.pointConstraint(eachDriver, eachConstrained  , weight = weight,mo = True)
                    elif ConstraintType == "orient":
                        cmds.orientConstraint(eachDriver, eachConstrained , weight = weight,mo = True)
                    else:
                        print "not valid costraintType requested, valid types are point, parent, or orient"


    def RMGaussCosine(self,XValue,Center,GaussLen):
        DistanceFromCenter = abs(XValue - Center)
        if DistanceFromCenter < GaussLen / 2:
            return (math.cos(DistanceFromCenter/(GaussLen/2) * math.pi) + 1)/2
        else:
            return 0


RSP = RMSpine()
spineJoints = ["Character01_MD_Spine_pnt_rfr","Character01_MD_Spine1_pnt_rfr","Character01_MD_Spine2_pnt_rfr","Character01_MD_Spine3_pnt_rfr","Character01_MD_Spine4_pnt_rfr"]
RSP.RMCreateSpineRig(spineJoints)

#reverse = self.NameConv.RMRenameNameInFormat(reverse)
#parentConstraint[0] = self.NameConv.RMRenameNameInFormat (parentConstraint[0])





