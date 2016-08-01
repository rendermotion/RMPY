import maya.cmds as cmds
import maya.api.OpenMaya as om
import RMRigTools
reload (RMRigTools)
import RMRigShapeControls
reload (RMRigShapeControls)
import RMNameConvention
reload (RMNameConvention)
from AutoRig import RMSpaceSwitch
import math


class RMLimbIKFK(object):
    def __init__(self, NameConv = None):
        if not NameConv:
            self.NameConv = RMNameConvention.RMNameConvention()
        else:
            self.NameConv = NameConv
        self.SPSW = RMSpaceSwitch.RMSpaceSwitch()

        self.IKjointStructure = None
        self.IKSkinJointStructure = None
        self.IKparentGroup = None
        self.IkHandle = None

        self.FKjointStructure = None
        self.FKparentGroup = None
        
        self.IKResetPoint=None 
        self.SknJointStructure = None
        self.SknparentGroup = None

        self.PoleVectorResetPnt = None
        self.PoleVector = None



    def RMLimbJointEstructure(self,OriginPoint,ZAxisOrientation = "z", ):
        LimbReferencePonits = RMRigTools.RMCustomPickWalk(OriginPoint,'transform',2)
        return RMRigTools.RMCreateBonesAtPoints(LimbReferencePonits,NameConv = self.NameConv, ZAxisOrientation = ZAxisOrientation)

    def RMIdentifyIKJoints(self,ikHandle):
        endEffector = cmds.ikHandle(ikHandle, q = True, endEffector = True)
        EndJoint = RMRigTools.RMCustomPickWalk (endEffector, 'joint', 1, Direction = "up")
        EndJoint = RMRigTools.RMCustomPickWalk (EndJoint[len(EndJoint)-1], 'joint', 1)
        EndJoint = EndJoint[1]
        StartJoint = cmds.ikHandle(ikHandle, q = True, startJoint = True)
        return RMRigTools.FindInHieararchy (StartJoint, EndJoint)

    def BoneChainLenght(self,BoneChain):
        distancia = 0
        for index in range(1,len(BoneChain)):
           distancia += RMRigTools.RMPointDistance(BoneChain[index-1],BoneChain[index])
        return distancia

    def RMMakeIkStretchy(self,ikHandle):
        
        if not self.IKjointStructure:
            self.IKjointStructure = self.RMIdentifyIKJoints(ikHandle)
        totalDistance = self.BoneChainLenght(self.IKjointStructure)
        transformStartPoint = cmds.spaceLocator(name="StretchyIkHandleStartPoint")[0]
        transformStartPoint = self.NameConv.RMRenameNameInFormat(transformStartPoint)
        transformEndPoint  = cmds.spaceLocator (name="StretchyIkHandleEndPoint")[0]
        transformEndPoint = self.NameConv.RMRenameNameInFormat(transformEndPoint)
        if self.IKparentGroup:
            cmds.parent(transformStartPoint,self.IKparentGroup)
            cmds.parent(transformEndPoint,self.IKparentGroup)

        StartPointConstraint = cmds.pointConstraint(self.IKjointStructure[0],transformStartPoint)
        EndPointConstraint = cmds.pointConstraint(ikHandle,transformEndPoint)

        distanceNode = cmds.shadingNode("distanceBetween", asUtility=True, name = "IKBaseDistanceNode")
        distanceNode = self.NameConv.RMRenameNameInFormat(distanceNode)


        cmds.connectAttr(transformStartPoint + ".worldPosition[0]", distanceNode + ".point1",f=True)
        cmds.connectAttr(transformEndPoint + ".worldPosition[0]", distanceNode + ".point2",f=True)
        
        conditionNode = cmds.shadingNode("condition",asUtility=True,name="IkCondition")
        conditionNode = self.NameConv.RMRenameNameInFormat(conditionNode)
        cmds.connectAttr(distanceNode + ".distance",conditionNode + ".colorIfFalseR",f=True)
        cmds.connectAttr(distanceNode + ".distance",conditionNode + ".secondTerm",f=True)
        cmds.setAttr(conditionNode + ".operation",3)
        cmds.setAttr(conditionNode +".firstTerm",totalDistance)
        cmds.setAttr(conditionNode +".colorIfTrueR",totalDistance)
        multiplyDivide = cmds.shadingNode("multiplyDivide", asUtility=True,name="IKStretchMultiply")
        multiplyDivide = self.NameConv.RMRenameNameInFormat(multiplyDivide)

        cmds.connectAttr(conditionNode + ".outColorR",multiplyDivide+".input1X" ,f=True)
        cmds.setAttr(multiplyDivide + ".input2X",totalDistance)
        cmds.setAttr(multiplyDivide + ".operation",2)

        self.SPSW.AddEnumParameters(["off","on"], self.ikControl, Name = "StretchyIK")

        for joints in self.IKjointStructure[:-1]:
            IkSwitchCondition = cmds.shadingNode("condition",asUtility=True,name="IkSwitchCondition" + self.NameConv.RMGetAShortName(joints))
            IkSwitchCondition = self.NameConv.RMRenameNameInFormat(IkSwitchCondition)
            cmds.connectAttr( self.ikControl + ".StretchyIK",IkSwitchCondition + ".firstTerm" ,force = True)
            cmds.setAttr(IkSwitchCondition + ".secondTerm",0)
            cmds.setAttr(IkSwitchCondition + ".operation",0)
            cmds.connectAttr( multiplyDivide + ".outputX", IkSwitchCondition + ".colorIfFalseR" ,force = True)
            cmds.setAttr(IkSwitchCondition + ".colorIfTrueR", 1 )
            cmds.connectAttr(IkSwitchCondition + ".outColorR", joints + ".scaleX")

    def RMLimbRig(self,RootReferencePoint):

        self.IKparentGroup , self.IKjointStructure = self.RMLimbJointEstructure(RootReferencePoint)
        self.RMCreateIKControls()
        self.RMMakeIkStretchy(self.IkHandle)
        self.RMCreatePoleVector(self.IkHandle)

        #self.FKparentGroup , self.FKjointStructure = self.RMLimbJointEstructure(RootReferencePoint)        
        #self.RMCreateFKControls()
    
    def RMCreateFKControls(self,AxisFree = "Y"):
        ArmParent ,FKFirstLimbControl = RMRigShapeControls.RMCreateBoxCtrl(self.FKjointStructure[0],Xratio=1,Yratio=.3,Zratio=.3)
        
        RMRigTools.RMLinkHerarchyRotation (self.FKjointStructure[0], self.FKjointStructure[1],FKFirstLimbControl)

        RMRigTools.RMLockAndHideAttributes (FKFirstLimbControl,'0000111000')

        SecondLimbParent ,FKSecondLimbControl = RMRigShapeControls.RMCreateBoxCtrl(self.FKjointStructure[1],Xratio=1,Yratio=.3,Zratio=.3)
        cmds.parent(SecondLimbParent, FKFirstLimbControl)

        RMRigTools.RMLinkHerarchyRotation (self.FKjointStructure[1], self.FKjointStructure[2], FKSecondLimbControl)
        if AxisFree == "Y":
            RMRigTools.RMLockAndHideAttributes (FKSecondLimbControl,'0000100000')
        if AxisFree == "Z":
            RMRigTools.RMLockAndHideAttributes (FKSecondLimbControl,'0000010000')

    def RMCreateIKControls(self):
        
        self.IKResetPoint, self.ikControl = RMRigShapeControls.RMCreateBoxCtrl(self.IKjointStructure[len(self.IKjointStructure)-1], Xratio = .3, Yratio = .3, Zratio = .3, ParentBaseSize = True)
        self.ikControl = self.NameConv.RMRenameBasedOnBaseName(self.IKjointStructure[len(self.IKjointStructure)-1],self.ikControl)
        
        self.IkHandle, effector = cmds.ikHandle (sj = self.IKjointStructure[0], ee = self.IKjointStructure[len(self.IKjointStructure)-1],sol = "ikRPsolver",name = "LimbIKHandle")
        self.IkHandle = self.NameConv.RMRenameBasedOnBaseName(self.IKjointStructure[len(self.IKjointStructure)-1],self.IkHandle)
        effector = self.NameConv.RMRenameBasedOnBaseName(self.IKjointStructure[len(self.IKjointStructure)-1],effector)

        PointConstraint = cmds.pointConstraint (self.ikControl, self.IkHandle, name = "LimbCntrlHandleConstraint")
        PointConstraint = self.NameConv.RMRenameBasedOnBaseName(self.IKjointStructure[len(self.IKjointStructure)-1],PointConstraint[0])

    def RMGetPoleVectorReferencePoint(self,JointList):
        VP1 = om.MVector(cmds.xform(JointList[0],a=True,ws=True,q=True,rp=True))
        VP2 = om.MVector(cmds.xform(JointList[1],a=True,ws=True,q=True,rp=True))
        VP3 = om.MVector(cmds.xform(JointList[2],a=True,ws=True,q=True,rp=True))
        V1 = VP2 - VP1
        V2 = VP3 - VP2
        Angle = math.radians((math.degrees(V1.angle(V2)) + 180)/2 - 90)

        zAxis = (V1 ^ V2).normal()
        yAxis = (V2 ^ zAxis).normal()
        xAxis = V2.normal()

        Y1 = math.cos(Angle)
        X1 = -math.sin(Angle)
        Vy = yAxis * Y1
        Vx = xAxis * X1
        Length = (V1.length() + V2.length())/2
        result = ((Vy + Vx) * Length) + VP2
        PoleVector = cmds.spaceLocator(name = "poleVector")[0]
        PoleVector = self.NameConv.RMRenameNameInFormat(PoleVector)

        cmds.xform(PoleVector, ws = True, t = result)
        return PoleVector
    def RMCreatePoleVector(self,IKHandle):

        if not self.IKjointStructure:
            self.IKjointStructure = self.RMIdentifyIKJoints(IKHandle)
        locator = self.RMGetPoleVectorReferencePoint(self.IKjointStructure)

        distancia = RMRigTools.RMPointDistance(locator,self.IKjointStructure[1])
        self.PoleVectorResetPnt, self.PoleVector = RMRigShapeControls.RMCreateBoxCtrl( locator, customSize = distancia/5, name = "PoleVector")
        RMRigTools.RMCreateLineBetwenPoints(self.PoleVector, self.IKjointStructure[1])

        #solver = cmds.ikSolver( st='ikRPSolver', name = 'PoleVectorSolver' )
        #cmds.ikHandle(IKHandle, e=True, sol = solver)
        cmds.poleVectorConstraint( self.PoleVector, IKHandle, name = "PoleVector")



LimbArmRight = RMLimbIKFK()
LimbArmRight.RMLimbRig("Character01_RH_shoulder_pnt_rfr")


#LimbArmLeft = RMLimbIKFK()
#LimbArmLeft.RMLimbRig("Character01_LF_shoulder_pnt_rfr")

#LimbLegRight = RMLimbIKFK()
#LimbLegRight.RMLimbRig("Character01_LF_leg_pnt_rfr")
#LimbLegLeft = RMLimbIKFK()
#LimbLegLeft.RMLimbRig("Character01_RH_leg_pnt_rfr")
#Limb.RMLimbJointEstructure("Character01_RH_shoulder_pnt_rfr")
#Limb.RMLimbJointEstructure("Character01_LF_leg_pnt_rfr")
#Limb.RMLimbJointEstructure("Character01_RH_leg_pnt_rfr")

#RMCreateIKControls("Character01_MD_Leg_jnt_FK",2)
#RMMakeIkStretchy('ikHandle1')
