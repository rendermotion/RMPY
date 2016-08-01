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
        self.chestJoint = None
        self.COG = None
        self.rootHip = None
        self.hipJoints = None
        self.SpineLength = None
        self.secondaryControls = []



    def RMCreateSpineRig(self,SpineRef,HipRefPnts):
        self.rootSpine,  self.spineJoints, self.chestJoint = self.RMCreateSpineJointStructure(SpineRef)
        self.RMCreateSpineIKSystem()
        self.rootHip,  self.hipJoints = self.RMCreateHipJointStructure(HipRefPnts)
        self.RMCreateHipSystem()

    def RMCreateSpineJointStructure(self,SpineRef):
        rootSpine , joints = RMRigTools.RMCreateBonesAtPoints(SpineRef,ZAxisOrientation = "z")

        SpineLength = RMRigTools.RMPointDistance(joints[0],joints[len(joints) - 1])
        chestJoint = cmds.joint(name = "chest")
        print chestJoint
        chestJoint = self.NameConv.RMRenameNameInFormat(chestJoint)

        RMRigTools.RMAlign(joints[len(joints)-1],chestJoint,3)
        #cmds.parent(chestJoint, joints[len(joints)-1])
        cmds.makeIdentity(chestJoint, apply = True , r = False, t = True, s = True, n = 0)
        cmds.xform(chestJoint,t=[SpineLength/4,0,0],os=True, relative=True )
        return rootSpine, joints, chestJoint


    
    def RMCreateSpineIKSystem(self):

        self.spineIK, effector, self.spineCurve = cmds.ikHandle(startJoint = self.spineJoints[0],endEffector = self.spineJoints[len(self.spineJoints)-1],createCurve = True,numSpans = len(self.spineJoints) ,solver = "ikSplineSolver",name = "spineIK")
        self.spineIK = self.NameConv.RMRenameBasedOnBaseName(self.spineJoints[len(self.spineJoints)-1],self.spineIK)
        effector = self.NameConv.RMRenameBasedOnBaseName(self.spineJoints[len(self.spineJoints)-1],effector,NewName = "spineIKEffector")
        self.spineCurve = self.NameConv.RMRenameBasedOnBaseName(self.spineJoints[len(self.spineJoints)-1],self.spineCurve,NewName = "spineIKCurve")

        Clusters = RMRigTools.RMCreateClustersOnCurve(self.spineCurve)
        ClustersGroup = RMRigTools.RMCreateGroupOnObj(Clusters[0])
        RMRigTools.RMParentArray(ClustersGroup,Clusters[1:])


        ResetCOG, COG = RMRigShapeControls.RMCreateBoxCtrl(self.spineJoints[0],Yratio=3,Zratio=3)
        COG = self.NameConv.RMRenameSetFromName(COG,"COG","Name")
        


        ResetChest, Chest = RMRigShapeControls.RMCreateBoxCtrl(self.spineJoints[len(self.spineJoints) - 1],Yratio=3,Zratio=3)
        Chest = self.NameConv.RMRenameSetFromName(Chest,"Chest","Name")

        cmds.parentConstraint(Chest , self.chestJoint, mo = True)
        
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


        self.secondaryControls
        for eachPosition in locators:
            ControlGroup , NewControl = RMRigShapeControls.RMImportMoveControl(eachPosition, scale = SpineLength)
            self.secondaryControls.append(NewControl)
            ChestGroups.append(ControlGroup)
            ChestControls.append(NewControl)
            AllSpine.append(NewControl)
            ResetTransformGroup = RMRigTools.RMCreateGroupOnObj(ControlGroup)
            cmds.parent(ResetTransformGroup,spineControlGroup)
            cmds.delete(eachPosition)
            RMRigTools.RMLockAndHideAttr(NewControl,"1110000000")

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

        #preparation for Scale multiplication function of each spine joint
        cmds.addAttr(Chest, at="float",sn = "ssf", ln = "spineSquashFactor",   hnv = 1, hxv = 1, h = 0, k = 1, smn = -10, smx = 10)

        GaussLen = len(spineJoints)
        center = len(spineJoints)/2
        powMaxValue = 5
        powRate = powMaxValue/center
        index = 1

        for eachJoint in self.spineJoints[1:]:
            #translate stretch multiplication functions of each spine joint
            SpineStretchMult = cmds.shadingNode( 'multiplyDivide', asUtility=True, name = "SpineTranslateStretchMult" + self.NameConv.RMGetAShortName(eachJoint))
            SpineStretchMult = self.NameConv.RMRenameNameInFormat( SpineStretchMult)
            CurrentXPosition = cmds.getAttr( eachJoint + ".translateX")
            cmds.setAttr(SpineStretchMult + ".input2X", CurrentXPosition)
            cmds.connectAttr( curveScaleRatio + ".outputX", SpineStretchMult + ".input1X")
            cmds.connectAttr( SpineStretchMult + ".outputX", eachJoint + ".translateX")
            
            #Scale multiplication function of each spine joint
            
            if index >= center:
                PowValue = (GaussLen - 1 - index) 
            else:
                PowValue = index

            SpineStretchRatio = cmds.shadingNode( 'multiplyDivide', asUtility = True, name = "SpineStretchRatio" + self.NameConv.RMGetAShortName(eachJoint))
            cmds.connectAttr(Chest+".spineSquashFactor ", SpineStretchRatio + ".input1X")
            cmds.setAttr(SpineStretchRatio + ".input2X", PowValue)
            cmds.setAttr(SpineStretchRatio + ".operation", 1)

            SpineScaleStretchPow = cmds.shadingNode( 'multiplyDivide', asUtility = True, name = "SpineScaleStretchPow" + self.NameConv.RMGetAShortName(eachJoint))
            cmds.connectAttr(curveScaleRatio+".outputX ", SpineScaleStretchPow + ".input1X")
            cmds.connectAttr(SpineStretchRatio + ".outputX ", SpineScaleStretchPow + ".input2X")
            cmds.setAttr(SpineScaleStretchPow + ".operation", 3)

            SpineInversScaleRatio = cmds.shadingNode( 'multiplyDivide', asUtility=True, name = "SpineInverseScaleRatio")
            SpineInversScaleRatio = self.NameConv.RMRenameNameInFormat( SpineInversScaleRatio)
            cmds.connectAttr(SpineScaleStretchPow+".outputX ",SpineInversScaleRatio + ".input1X")
            cmds.setAttr(SpineInversScaleRatio + ".input2X", -1)
            cmds.setAttr(SpineInversScaleRatio + ".operation", 3)

            cmds.connectAttr( SpineInversScaleRatio + ".outputX", eachJoint + ".scaleY")
            cmds.connectAttr( SpineInversScaleRatio + ".outputX", eachJoint + ".scaleZ")
            index += 1


        resetWaist, waist = RMRigShapeControls.RMCircularControl( AllSpine[1], radius = SpineLength*.8,name = "waist")
        cmds.parent( ResetChest, waist)
        cmds.parent( resetWaist, COG)


        self.COG = COG
        self.SpineLength = SpineLength

    def RMCreateHipJointStructure(self,HipRefPnts):
        rootHip , hipJoints = RMRigTools.RMCreateBonesAtPoints(HipRefPnts,ZAxisOrientation = "z")
        return rootHip , hipJoints
    
    def RMCreateHipSystem(self):

        resetHipControl, hipControl = RMRigShapeControls.RMCircularControl(self.rootHip,radius = self.SpineLength *.7,name = "hip")
        cmds.parent(resetHipControl,self.COG)
        cmds.parentConstraint(hipControl,self.hipJoints[0])
        #self.rootHip
        #self.hipJoints
      

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
hip = ["Character01_MD_Spine_pnt_rfr","Character01_MD_Hip_pnt_rfr"]
RSP.RMCreateSpineRig(spineJoints,hip)

#reverse = self.NameConv.RMRenameNameInFormat(reverse)
#parentConstraint[0] = self.NameConv.RMRenameNameInFormat (parentConstraint[0])





