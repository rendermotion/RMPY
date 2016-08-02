import maya.cmds as cmds
import maya.api.OpenMaya as om
import RMRigTools
reload (RMRigTools)
import RMRigShapeControls
reload (RMRigShapeControls)
import RMNameConvention
reload (RMNameConvention)
from AutoRig import RMSpaceSwitch
reload (RMSpaceSwitch)
import math
from AutoRig import RMTwistJoints
reload (RMTwistJoints)

class RMLimbIKFK(object):
    def __init__(self, NameConv = None):
        if not NameConv:
            self.NameConv = RMNameConvention.RMNameConvention()
        else:
            self.NameConv = NameConv

        self.SPSW = RMSpaceSwitch.RMSpaceSwitch(self.NameConv)
        self.TJArm = RMTwistJoints.RMTwistJoints(self.NameConv)
        self.TJElbow = RMTwistJoints.RMTwistJoints(self.NameConv)

        self.kinematics = []
        self.controls = []
        self.rig = []

        self.IKjointStructure = None
        self.IKparentGroup = None
        self.IkHandle = None
        self.IKControlResetPoint=None
        self.ikControl = None
        self.IKControls = None
        self.PoleVectorControlResetPnt = None
        self.PoleVectorControl = None


        self.FKjointStructure = None
        self.FKparentGroup = None
        self.FKControls = None

        self.SknJointStructure = None
        self.SknParentGroup = None





    def RMLimbRig (self, RootReferencePoint, FKAxisFree="111"):

        self.IKparentGroup , self.IKjointStructure = self.RMLimbJointEstructure(RootReferencePoint)
        self.IKjointStructure = self.NameConv.RMRenameSetFromName(self.IKjointStructure,"Limbik" ,"System")
        self.IKparentGroup = self.NameConv.RMRenameSetFromName(self.IKparentGroup,"Limbik" ,"System")

        self.RMCreateIKControls()
        self.RMMakeIkStretchy(self.IkHandle)
        self.RMCreatePoleVector(self.IkHandle)

        self.FKparentGroup , self.FKjointStructure = self.RMLimbJointEstructure(RootReferencePoint)        
        self.FKjointStructure = self.NameConv.RMRenameSetFromName(self.FKjointStructure,"Limbfk" ,"System")
        self.FKparentGroup = self.NameConv.RMRenameSetFromName(self.FKparentGroup,"Limbfk" ,"System")
        self.RMCreateFKControls(AxisFree = FKAxisFree)

        self.SknParentGroup , self.SknJointStructure = self.RMLimbJointEstructure(RootReferencePoint)     
        self.SknJointStructure = self.NameConv.RMRenameSetFromName(self.SknJointStructure,"Limbskn" ,"System")
        self.SknParentGroup = self.NameConv.RMRenameSetFromName(self.SknParentGroup,"Limbskn" ,"System")

        self.RMSkinSpaceSwitch()
        self.IKControls = cmds.group( empty = True, name = self.NameConv.RMGetAShortName(RootReferencePoint) + "IkControls")
        self.IKControls = self.NameConv.RMRenameNameInFormat( self.IKControls)
        cmds.parent(self.IKControlResetPoint,self.IKControls)
        cmds.parent(self.PoleVectorControlResetPnt,self.IKControls)

        self.TJArm.RMCreateTwistJoints (self.SknJointStructure[0], self.SknJointStructure[1])

        constraintTJArm = cmds.parentConstraint(self.SknParentGroup, self.TJArm.TwistControlResetPoint, mo=True)[0]
        constraintTJArm = self.NameConv.RMRenameBasedOnBaseName(self.SknJointStructure[1], constraintTJArm)

        self.TJElbow.RMCreateTwistJoints (self.SknJointStructure[1], self.SknJointStructure[2])
        constraintTJElbow = cmds.parentConstraint(self.SknJointStructure[0] , self.TJElbow.TwistControlResetPoint,mo=True)[0]
        constraintTJElbow = self.NameConv.RMRenameBasedOnBaseName(self.SknJointStructure[1], constraintTJElbow )

        cmds.parent ( self.TJElbow.TwistResetJoints, self.TJArm.TwistJoints[len(self.TJArm.TwistJoints) - 1])
        self.NameConv.RMRenameSetFromName( self.TJElbow.TwistJoints, "sknjnt", "Type")

    def RMLimbJointEstructure(self,OriginPoint,ZAxisOrientation = "z"):
        LimbReferencePonits = RMRigTools.RMCustomPickWalk(OriginPoint,'transform',2)
        return RMRigTools.RMCreateBonesAtPoints(LimbReferencePonits, NameConv = self.NameConv, ZAxisOrientation = ZAxisOrientation)

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

    def RMSkinSpaceSwitch (self):
        
        BoxResetPoint, BoxControl = RMRigShapeControls.RMCreateBoxCtrl( self.SknJointStructure[len(self.SknJointStructure)-1], name = "IKFKSwitch")
        LongitudBrazo = RMRigTools.RMLenghtOfBone(self.SknJointStructure[1])
        cmds.xform(BoxControl, objectSpace = True,relative = True ,t=[LongitudBrazo/2,0,0])
        self.SPSW.RMCreateListConstraintSwitch( self.SknJointStructure, self.IKjointStructure, BoxControl, SpaceSwitchName="IKFKSwitch")
        self.SPSW.RMCreateListConstraintSwitch( self.SknJointStructure, self.FKjointStructure, BoxControl, SpaceSwitchName="IKFKSwitch",reverse = True)
        RMRigTools.RMLockAndHideAttributes(BoxControl,"0000000000")
        cmds.parentConstraint(self.SknJointStructure[len(self.SknJointStructure)-1], BoxResetPoint)

    
    def RMCreateFKControls(self, AxisFree = "111"):
        ArmParent ,FKFirstLimbControl = RMRigShapeControls.RMCreateBoxCtrl(self.FKjointStructure[0],Xratio=1,Yratio=.3,Zratio=.3)
        
        RMRigTools.RMLinkHerarchyRotation (self.FKjointStructure[0], self.FKjointStructure[1],FKFirstLimbControl)

        RMRigTools.RMLockAndHideAttributes (FKFirstLimbControl,'0001110000')

        SecondLimbParent ,FKSecondLimbControl = RMRigShapeControls.RMCreateBoxCtrl(self.FKjointStructure[1],Xratio=1,Yratio=.3,Zratio=.3)
        cmds.parent(SecondLimbParent, FKFirstLimbControl)

        RMRigTools.RMLinkHerarchyRotation (self.FKjointStructure[1], self.FKjointStructure[2], FKSecondLimbControl)
        RMRigTools.RMLockAndHideAttributes (FKSecondLimbControl,'000'+ AxisFree +'0000')

        self.FKControls = ArmParent
        

    def RMCreateIKControls(self):
        
        self.IKControlResetPoint, self.ikControl = RMRigShapeControls.RMCreateBoxCtrl(self.IKjointStructure[len(self.IKjointStructure)-1], Xratio = .3, Yratio = .3, Zratio = .3, ParentBaseSize = True)
        self.ikControl = self.NameConv.RMRenameBasedOnBaseName(self.IKjointStructure[len(self.IKjointStructure)-1],self.ikControl)
        
        self.IkHandle, effector = cmds.ikHandle (sj = self.IKjointStructure[0], ee = self.IKjointStructure[len(self.IKjointStructure)-1],sol = "ikRPsolver",name = "LimbIKHandle")
        self.IkHandle = self.NameConv.RMRenameBasedOnBaseName(self.IKjointStructure[len(self.IKjointStructure)-1],self.IkHandle)
        effector = self.NameConv.RMRenameBasedOnBaseName(self.IKjointStructure[len(self.IKjointStructure)-1],effector)

        PointConstraint = cmds.pointConstraint (self.ikControl, self.IkHandle, name = "LimbCntrlHandleConstraint")
        PointConstraint = self.NameConv.RMRenameBasedOnBaseName(self.IKjointStructure[len(self.IKjointStructure)-1],PointConstraint[0])
        self.kinematics.append( self.IkHandle)

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
        PoleVector = self.NameConv.RMRenameBasedOnBaseName(JointList[1],PoleVector)

        cmds.xform(PoleVector, ws = True, t = result)
        return PoleVector

    def RMCreatePoleVector(self,IKHandle):

        if not self.IKjointStructure:
            self.IKjointStructure = self.RMIdentifyIKJoints(IKHandle)
        locator = self.RMGetPoleVectorReferencePoint(self.IKjointStructure)
        
        distancia = RMRigTools.RMPointDistance(locator , self.IKjointStructure[1])

        self.PoleVectorControlResetPnt, self.PoleVectorControl = RMRigShapeControls.RMCreateBoxCtrl( locator, customSize = distancia/5, name = "PoleVector")
        
        dataGroup = RMRigTools.RMCreateLineBetwenPoints(self.PoleVectorControl, self.IKjointStructure[1])

        #solver = cmds.ikSolver( st='ikRPSolver', name = 'PoleVectorSolver' )
        #cmds.ikHandle(IKHandle, e=True, sol = solver)
        PoleVectorCnstraint = cmds.poleVectorConstraint( self.PoleVectorControl, IKHandle, name = "PoleVector")[0]

        PoleVectorCnstraint = self.NameConv.RMRenameBasedOnBaseName(self.PoleVectorControl,PoleVectorCnstraint)
        self.kinematics.append(dataGroup)
        cmds.delete(locator)

#RMCreateIKControls("Character01_MD_Leg_jnt_FK",2)
#RMMakeIkStretchy('ikHandle1')
