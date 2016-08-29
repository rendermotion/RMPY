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
    def __init__(self, worldNode = None , NameConv = None):
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
        self.world = worldNode

        self.IKjointStructure = None
        self.IKparentGroup = None
        self.IkHandle = None
        self.IKControlResetPoint=None
        self.ikControl = None
        self.IKControls = None
        self.PoleVectorControlResetPnt = None
        self.PoleVectorControl = None

        self.limbMover = None

        self.SpaceSwitchControl = None
        self.ResetSpaceSwitchControl = None

        self.FKjointStructure = None
        self.FKparentGroup = None
        self.FKControls = None

        self.libmAttachPoint = None

        self.SknJointStructure = None
        self.SknParentGroup = None
        self.FKFirstLimbControl = None
        self.FKSecondLimbControl = None
        self.FKTrirdLimbControl = None

        self.ThirdLimbParent = None

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
        self.IKControls = self.NameConv.RMRenameNameInFormat(self.IKControls,Side = self.NameConv.RMGetFromName( RootReferencePoint, "Side"))
        cmds.parent(self.IKControlResetPoint,self.IKControls)
        cmds.parent(self.PoleVectorControlResetPnt,self.IKControls)

        if FKAxisFree == "010":
            LookAtAxis="Y"
        else :
            LookAtAxis="Z"

        self.TJArm.RMCreateTwistJoints (self.SknJointStructure[0], self.SknJointStructure[1],LookAtAxis = LookAtAxis)


        constraintTJArm = cmds.parentConstraint(self.SknParentGroup, self.TJArm.TwistControlResetPoint, mo=True)[0]
        constraintTJArm = self.NameConv.RMRenameBasedOnBaseName(self.SknJointStructure[1], constraintTJArm)
        
        self.TJElbow.RMCreateTwistJoints (self.SknJointStructure[1], self.SknJointStructure[2],LookAtAxis = LookAtAxis)


        constraintTJElbow = cmds.parentConstraint(self.SknJointStructure[0] , self.TJElbow.TwistControlResetPoint,mo=True)[0]
        constraintTJElbow = self.NameConv.RMRenameBasedOnBaseName(self.SknJointStructure[1], constraintTJElbow )

        cmds.parent ( self.TJElbow.TwistResetJoints, self.TJArm.TwistJoints[len(self.TJArm.TwistJoints) - 1])
        self.TJElbow.TwistJoints = self.NameConv.RMRenameSetFromName( self.TJElbow.TwistJoints, "sknjnt", "Type")
        self.TJArm.TwistJoints = self.NameConv.RMRenameSetFromName( self.TJArm.TwistJoints, "sknjnt", "Type")


        self.limbMover = cmds.group(empty = True, name = "armMover")
        self.limbMover = self.NameConv.RMRenameNameInFormat( self.limbMover ,System = "joints")
        cmds.parent( self.FKparentGroup , self.limbMover)
        cmds.parent( self.IKparentGroup , self.limbMover)
        cmds.parent( self.SknParentGroup, self.limbMover)

        self.SPSW.ConstraintVisibility ([self.PoleVectorControl,self.ikControl]                                   ,self.SpaceSwitchControl,SpaceSwitchName = "IKFKSwitch", reverse = False)
        self.SPSW.ConstraintVisibility ([self.FKFirstLimbControl,self.FKSecondLimbControl,self.FKTrirdLimbControl],self.SpaceSwitchControl,SpaceSwitchName = "IKFKSwitch" ,reverse = True)

        self.libmAttachPoint = self.SknJointStructure[2]
        self.IKAttachPoint = self.IKjointStructure   [2]
        self.FKAttachPoint = self.FKjointStructure   [2]


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

        distanceNode = cmds.shadingNode("distanceBetween", asUtility=True, name = "IKBaseDistanceNode" + self.NameConv.RMGetAShortName(self.IKjointStructure[2]))
        distanceNode = self.NameConv.RMRenameBasedOnBaseName(self.IKjointStructure[2] , distanceNode , NewName = distanceNode)

        cmds.connectAttr(transformStartPoint + ".worldPosition[0]", distanceNode + ".point1",f=True)
        cmds.connectAttr(transformEndPoint + ".worldPosition[0]", distanceNode + ".point2",f=True)
        
        conditionNode = cmds.shadingNode("condition",asUtility=True,name="IkCondition" + self.NameConv.RMGetAShortName(self.IKjointStructure[2]))
        conditionNode = self.NameConv.RMRenameBasedOnBaseName(self.IKjointStructure[2] , conditionNode , NewName = conditionNode)
        cmds.connectAttr(distanceNode + ".distance",conditionNode + ".colorIfFalseR",f=True)
        cmds.connectAttr(distanceNode + ".distance",conditionNode + ".secondTerm",f=True)
        cmds.setAttr(conditionNode + ".operation",3)
        cmds.setAttr(conditionNode +".firstTerm",totalDistance)
        cmds.setAttr(conditionNode +".colorIfTrueR",totalDistance)
        multiplyDivide = cmds.shadingNode("multiplyDivide", asUtility=True,name="IKStretchMultiply" + self.NameConv.RMGetAShortName(self.IKjointStructure[2]))
        multiplyDivide = self.NameConv.RMRenameBasedOnBaseName(self.IKjointStructure[2] , multiplyDivide , NewName = multiplyDivide)

        cmds.connectAttr(conditionNode + ".outColorR",multiplyDivide+".input1X" ,f=True)
        cmds.setAttr(multiplyDivide + ".input2X",totalDistance)
        cmds.setAttr(multiplyDivide + ".operation",2)


        #self.SPSW.AddEnumParameters(["off","on"], self.ikControl, Name = "StretchyIK")
        self.SPSW.AddNumericParameter(self.ikControl, Name = "StretchyIK")
        IKSwitchDivide = cmds.shadingNode("multiplyDivide", asUtility=True, name="IkSwitchDivide" + self.NameConv.RMGetAShortName(self.IKjointStructure[2]))
        IKSwitchDivide = self.NameConv.RMRenameBasedOnBaseName(self.IKjointStructure[2] , IKSwitchDivide , NewName = IKSwitchDivide)
        cmds.connectAttr( self.ikControl + ".StretchyIK", IKSwitchDivide + ".input1X"  )
        cmds.setAttr(IKSwitchDivide + ".input2X",10)
        cmds.setAttr(IKSwitchDivide + ".operation",2)

        IkSwitchblendTwoAttr = cmds.shadingNode("blendTwoAttr",asUtility=True,name="IkSwitchBlendTwoAttr" + self.NameConv.RMGetAShortName (self.IKjointStructure[2]) )
        IkSwitchblendTwoAttr = self.NameConv.RMRenameBasedOnBaseName(self.IKjointStructure[2] , IkSwitchblendTwoAttr , NewName = IkSwitchblendTwoAttr)

        cmds.connectAttr( multiplyDivide + ".outputX", IkSwitchblendTwoAttr + ".input[1]" ,force = True)
        cmds.setAttr(IkSwitchblendTwoAttr + ".input[0]", 1 )
        cmds.connectAttr( IKSwitchDivide + ".outputX", IkSwitchblendTwoAttr + ".attributesBlender" ,force = True)

        for joints in self.IKjointStructure[:-1]:
            cmds.connectAttr(IkSwitchblendTwoAttr + ".output", joints + ".scaleX")
            #IkSwitchCondition = cmds.shadingNode("condition",asUtility=True,name="IkSwitchCondition" + self.NameConv.RMGetAShortName(joints))
            #IkSwitchCondition = self.NameConv.RMRenameNameInFormat(IkSwitchCondition)
            #cmds.connectAttr( IKSwitchDivide + ".outputX", IkSwitchCondition + ".firstTerm" ,force = True)
            #cmds.setAttr(IkSwitchCondition + ".secondTerm",0)
            #cmds.setAttr(IkSwitchCondition + ".operation",0)
            #cmds.connectAttr( multiplyDivide + ".outputX", IkSwitchCondition + ".colorIfFalseR" ,force = True)
            #cmds.setAttr(IkSwitchCondition + ".colorIfTrueR", 1 )
            #cmds.connectAttr(IkSwitchCondition + ".outColorR", joints + ".scaleX")

    def RMSkinSpaceSwitch (self):
        
        BoxResetPoint, BoxControl = RMRigShapeControls.RMCreateBoxCtrl( self.SknJointStructure[len(self.SknJointStructure)-1], name = "IKFKSwitch")
        LongitudBrazo = RMRigTools.RMLenghtOfBone(self.SknJointStructure[1])
        cmds.xform(BoxControl, objectSpace = True,relative = True ,t=[LongitudBrazo/2,0,0])
        self.SPSW.RMCreateListConstraintSwitch( self.SknJointStructure, self.IKjointStructure, BoxControl, SpaceSwitchName="IKFKSwitch")
        self.SPSW.RMCreateListConstraintSwitch( self.SknJointStructure, self.FKjointStructure, BoxControl, SpaceSwitchName="IKFKSwitch", reverse = True)
        
        RMRigTools.RMLockAndHideAttributes(BoxControl,"000000000h")
        cmds.parentConstraint(self.SknJointStructure[len(self.SknJointStructure)-1], BoxResetPoint)

        self.SpaceSwitchControl = BoxControl
        self.ResetSpaceSwitchControl = BoxResetPoint

    
    def RMCreateFKControls(self, AxisFree = "111"):
        #ArmParent ,FKFirstLimbControl = RMRigShapeControls.RMCreateBoxCtrl(self.FKjointStructure[0],Xratio=1,Yratio=.3,Zratio=.3, name = self.NameConv.RMGetAShortName(self.FKjointStructure[0]) + "FK")
        ArmParent ,FKFirstLimbControl = RMRigShapeControls.RMCircularControl(self.FKjointStructure[0], radius = RMRigTools.RMLenghtOfBone(self.FKjointStructure[0])/2, name = self.NameConv.RMGetAShortName(self.FKjointStructure[0]) + "FK")
        
        RMRigTools.RMLinkHerarchyRotation (self.FKjointStructure[0], self.FKjointStructure[0],FKFirstLimbControl)

        RMRigTools.RMLockAndHideAttributes (FKFirstLimbControl,'000111000h')

        #SecondLimbParent ,FKSecondLimbControl = RMRigShapeControls.RMCreateBoxCtrl(self.FKjointStructure[1],Xratio=1,Yratio=.3,Zratio=.3, name = self.NameConv.RMGetAShortName(self.FKjointStructure[1])+ "FK")
        SecondLimbParent ,FKSecondLimbControl = RMRigShapeControls.RMCircularControl(self.FKjointStructure[1], radius = RMRigTools.RMLenghtOfBone(self.FKjointStructure[1])/2, name = self.NameConv.RMGetAShortName(self.FKjointStructure[1]) + "FK")

        cmds.parent(SecondLimbParent, FKFirstLimbControl)

        RMRigTools.RMLinkHerarchyRotation (self.FKjointStructure[1], self.FKjointStructure[1], FKSecondLimbControl)
        RMRigTools.RMLockAndHideAttributes (FKSecondLimbControl,'000'+ AxisFree +'000h')

        #ThirdLimbParent ,FKTrirdLimbControl = RMRigShapeControls.RMCreateBoxCtrl(self.FKjointStructure[2], Xratio=.3, Yratio=.3, Zratio=.3 , ParentBaseSize = True, name = self.NameConv.RMGetAShortName(self.FKjointStructure[2]) + "FK")
        ThirdLimbParent ,FKTrirdLimbControl = RMRigShapeControls.RMCircularControl(self.FKjointStructure[2], radius = RMRigTools.RMLenghtOfBone(self.FKjointStructure[1])/3, name = self.NameConv.RMGetAShortName(self.FKjointStructure[2]) + "FK")

        
        cmds.parent(ThirdLimbParent, FKSecondLimbControl)

        #RMRigTools.RMLinkHerarchyRotation (self.FKjointStructure[2], self.FKjointStructure[2], FKTrirdLimbControl)
        cmds.parentConstraint( FKTrirdLimbControl ,  self.FKjointStructure[2] )

        RMRigTools.RMLockAndHideAttributes (FKTrirdLimbControl,'000111000h')
        
        self.FKFirstLimbControl = FKFirstLimbControl
        self.FKSecondLimbControl = FKSecondLimbControl
        self.ThirdLimbParent = ThirdLimbParent
        self.FKTrirdLimbControl = FKTrirdLimbControl
        cmds.parentConstraint ( self.FKparentGroup , ArmParent)
        self.ThirdLimbParent = ThirdLimbParent
        self.FKControls = ArmParent

        RMRigTools.RMChangeRotateOrder (self.FKTrirdLimbControl , 'yzx')


        

    def RMCreateIKControls(self):
        
        self.IKControlResetPoint, self.ikControl = RMRigShapeControls.RMCreateBoxCtrl(self.IKjointStructure[len(self.IKjointStructure)-1], Xratio = .3, Yratio = .3, Zratio = .3, ParentBaseSize = True,name = self.NameConv.RMGetAShortName(self.IKjointStructure[len(self.IKjointStructure)-1]) + "IK")
        #self.ikControl = self.NameConv.RMRenameBasedOnBaseName(self.IKjointStructure[len(self.IKjointStructure)-1], self.ikControl, NewName = self.NameConv.RMGetAShortName(self.IKjointStructure[len(self.IKjointStructure)-1]) + "IK")
        RMRigTools.RMLockAndHideAttributes(self.ikControl,"111111000h")
        
        self.IkHandle, effector = cmds.ikHandle (sj = self.IKjointStructure[0], ee = self.IKjointStructure[len(self.IKjointStructure)-1],sol = "ikRPsolver",name = "LimbIKHandle")
        self.IkHandle = self.NameConv.RMRenameBasedOnBaseName(self.IKjointStructure[len(self.IKjointStructure)-1],self.IkHandle)
        effector = self.NameConv.RMRenameBasedOnBaseName(self.IKjointStructure[len(self.IKjointStructure)-1],effector)

        cmds.orientConstraint(self.ikControl, self.IKjointStructure[len(self.IKjointStructure)-1])

        PointConstraint = cmds.pointConstraint (self.ikControl, self.IkHandle, name = "LimbCntrlHandleConstraint")
        PointConstraint = self.NameConv.RMRenameBasedOnBaseName(self.IKjointStructure[len(self.IKjointStructure)-1],PointConstraint[0])
        self.kinematics.append( self.IkHandle)

        RMRigTools.RMChangeRotateOrder (self.ikControl , 'yzx')


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
        PoleVector = self.NameConv.RMRenameBasedOnBaseName(JointList[1],PoleVector,NewName = PoleVector)

        cmds.xform(PoleVector, ws = True, t = result)
        return PoleVector

    def RMCreatePoleVector(self,IKHandle):

        if not self.IKjointStructure:
            self.IKjointStructure = self.RMIdentifyIKJoints(IKHandle)
        locator = self.RMGetPoleVectorReferencePoint(self.IKjointStructure)
        
        distancia = RMRigTools.RMPointDistance(locator , self.IKjointStructure[1])

        self.PoleVectorControlResetPnt, self.PoleVectorControl = RMRigShapeControls.RMCreateBoxCtrl( locator, customSize = distancia / 5, name = self.NameConv.RMGetAShortName(self.IKjointStructure[1]) + "PoleVectorIK", centered = True)

        
        dataGroup, Curve = RMRigTools.RMCreateLineBetwenPoints(self.PoleVectorControl, self.IKjointStructure[1])
        cmds.parent(Curve, self.PoleVectorControl)
        cmds.parentConstraint(self.world, Curve)

        PoleVectorCnstraint = cmds.poleVectorConstraint( self.PoleVectorControl, IKHandle, name = "PoleVector")[0]
        PoleVectorCnstraint = self.NameConv.RMRenameBasedOnBaseName(self.PoleVectorControl,PoleVectorCnstraint,NewName=PoleVectorCnstraint)

        self.kinematics.append(dataGroup)
        cmds.delete(locator)

