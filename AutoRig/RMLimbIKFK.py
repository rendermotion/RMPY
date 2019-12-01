import pymel.core as pm
import maya.api.OpenMaya as om
from RMPY import RMRigTools


from RMPY import RMRigShapeControls
from RMPY import nameConvention
from RMPY.AutoRig import RMSpaceSwitch
import math
from RMPY.AutoRig import RMTwistJoints


class RMLimbIKFK(object):
    def __init__(self, worldNode = None , NameConv = None):
        if not NameConv:
            self.NameConv = nameConvention.NameConvention()
        else:
            self.NameConv = NameConv
        self.shapeControls = RMRigShapeControls.RMRigShapeControls( NameConv = NameConv)
        self.rig_tools = RMRigTools.RMRigTools(NameConv = NameConv)

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
        self.IKControlResetPoint = None
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
        self.NameConv.rename_set_from_name(self.IKjointStructure, "Limbik", "system")
        self.NameConv.rename_set_from_name(self.IKparentGroup, "Limbik", "system")

        self.RMCreateIKControls()
        self.RMMakeIkStretchy(self.IkHandle)
        self.RMCreatePoleVector(self.IkHandle)

        

        pm.setAttr("%s.rotateZ"%self.PoleVectorControlResetPnt,90)
        pm.setAttr("%s.rotateX"%self.PoleVectorControlResetPnt,90)


        self.FKparentGroup, self.FKjointStructure = self.RMLimbJointEstructure(RootReferencePoint)
        self.NameConv.rename_set_from_name(self.FKjointStructure, "Limbfk", "system")
        self.NameConv.rename_set_from_name(self.FKparentGroup, "Limbfk", "system")
        self.RMCreateFKControls(AxisFree=FKAxisFree)

        self.SknParentGroup, self.SknJointStructure = self.RMLimbJointEstructure(RootReferencePoint)
        self.NameConv.rename_set_from_name(self.SknJointStructure, "Limbskn", "system")
        self.NameConv.rename_set_from_name(self.SknParentGroup, "Limbskn", "system")

        self.RMSkinSpaceSwitch()
        self.IKControls = pm.group(empty=True, name="%sIkControls" % self.NameConv.get_a_short_name(RootReferencePoint))
        self.NameConv.rename_name_in_format(self.IKControls, side=self.NameConv.get_from_name(RootReferencePoint, "side"))
        pm.parent(self.IKControlResetPoint, self.IKControls)
        pm.parent(self.PoleVectorControlResetPnt, self.IKControls)

        if FKAxisFree == "010":
            LookAtAxis="Y"
        else:
            LookAtAxis="Z"

        self.TJArm.RMCreateTwistJoints(self.SknJointStructure[0], self.SknJointStructure[1],LookAtAxis = LookAtAxis)

        constraintTJArm=pm.parentConstraint(self.SknParentGroup, self.TJArm.TwistControlResetPoint, mo=True)
        self.NameConv.rename_based_on_base_name(self.SknJointStructure[1], constraintTJArm)
        
        self.TJElbow.RMCreateTwistJoints(self.SknJointStructure[1], self.SknJointStructure[2],LookAtAxis = LookAtAxis)


        constraintTJElbow = pm.parentConstraint(self.SknJointStructure[0], self.TJElbow.TwistControlResetPoint, mo=True)
        self.NameConv.rename_based_on_base_name(self.SknJointStructure[1], constraintTJElbow)

        pm.parent(self.TJElbow.TwistResetJoints, self.TJArm.TwistJoints[len(self.TJArm.TwistJoints) - 1])
        self.NameConv.rename_set_from_name(self.TJElbow.TwistJoints, "sknjnt", "objectType")
        self.NameConv.rename_set_from_name(self.TJArm.TwistJoints, "sknjnt", "objectType")


        self.limbMover = pm.group(empty = True, name = "armMover")
        self.NameConv.rename_name_in_format(self.limbMover, system="joints")
        pm.parent( self.FKparentGroup , self.limbMover)
        pm.parent( self.IKparentGroup , self.limbMover)
        pm.parent( self.SknParentGroup, self.limbMover)

        self.SPSW.ConstraintVisibility ([self.PoleVectorControl,self.ikControl]                                   ,self.SpaceSwitchControl,SpaceSwitchName = "IKFKSwitch", reverse = False)
        self.SPSW.ConstraintVisibility ([self.FKFirstLimbControl,self.FKSecondLimbControl,self.FKTrirdLimbControl],self.SpaceSwitchControl,SpaceSwitchName = "IKFKSwitch" ,reverse = True)

        self.libmAttachPoint = self.SknJointStructure[2]
        self.IKAttachPoint = self.IKjointStructure   [2]
        self.FKAttachPoint = self.FKjointStructure   [2]


    def RMLimbJointEstructure(self,OriginPoint,ZAxisOrientation = "z"):
        LimbReferencePonits = RMRigTools.RMCustomPickWalk(OriginPoint,'transform',2)
        return self.rig_tools.RMCreateBonesAtPoints(LimbReferencePonits, ZAxisOrientation = ZAxisOrientation)

    def RMIdentifyIKJoints(self, ikHandle):
        endEffector = pm.ikHandle(ikHandle, q=True, endEffector=True)
        EndJoint = RMRigTools.RMCustomPickWalk(endEffector, 'joint', 1, Direction = "up")
        EndJoint = RMRigTools.RMCustomPickWalk(EndJoint[len(EndJoint)-1], 'joint', 1)
        EndJoint = EndJoint[1]
        StartJoint = pm.ikHandle(ikHandle, q=True, startJoint=True)
        return RMRigTools.FindInHieararchy (StartJoint, EndJoint)

    def BoneChainLenght(self, BoneChain):
        distancia = 0
        for index in range(1, len(BoneChain)):
           distancia += RMRigTools.RMPointDistance(BoneChain[index-1],BoneChain[index])
        return distancia

    def RMMakeIkStretchy(self, ikHandle):
        
        if not self.IKjointStructure:
            self.IKjointStructure = self.RMIdentifyIKJoints(ikHandle)
        totalDistance = self.BoneChainLenght(self.IKjointStructure)
        transformStartPoint = pm.spaceLocator(name="StretchyIkHandleStartPoint")
        self.NameConv.rename_name_in_format(transformStartPoint)
        transformEndPoint = pm.spaceLocator(name="StretchyIkHandleEndPoint")
        self.NameConv.rename_name_in_format(transformEndPoint)
        if self.IKparentGroup:
            print (self.IKparentGroup,self.IKparentGroup.__class__)
            pm.parent(transformStartPoint, self.IKparentGroup)
            pm.parent(transformEndPoint, self.IKparentGroup)

        StartPointConstraint = pm.pointConstraint(self.IKjointStructure[0], transformStartPoint)
        EndPointConstraint = pm.pointConstraint(ikHandle, transformEndPoint)

        distanceNode = pm.shadingNode("distanceBetween",
                                      asUtility=True,
                                      name="IKBaseDistanceNode%s" %
                                           self.NameConv.get_a_short_name(self.IKjointStructure[2]))

        self.NameConv.rename_based_on_base_name(self.IKjointStructure[2], distanceNode, name=distanceNode)

        pm.connectAttr("%s.worldPosition[0]" % transformStartPoint, "%s.point1" % distanceNode,f=True)
        pm.connectAttr("%s.worldPosition[0]" % transformEndPoint, "%s.point2" % distanceNode,f=True)
        
        conditionNode = pm.shadingNode("condition", asUtility=True, name="IkCondition" + self.NameConv.get_a_short_name(self.IKjointStructure[2]))
        self.NameConv.rename_based_on_base_name(self.IKjointStructure[2], conditionNode, name=conditionNode)
        pm.connectAttr("%s.distance" % distanceNode, "%s.colorIfFalseR" % conditionNode,f=True)
        pm.connectAttr("%s.distance" % distanceNode, "%s.secondTerm" % conditionNode,f=True)
        pm.setAttr("%s.operation" % conditionNode, 3)
        pm.setAttr("%s.firstTerm" % conditionNode, totalDistance)
        pm.setAttr("%s.colorIfTrueR" % conditionNode, totalDistance)
        multiplyDivide = pm.shadingNode("multiplyDivide", asUtility=True,
                                        name="IKStretchMultiply%s" %
                                             self.NameConv.get_a_short_name(self.IKjointStructure[2]))
        self.NameConv.rename_based_on_base_name(self.IKjointStructure[2],
                                                multiplyDivide, name=multiplyDivide)

        pm.connectAttr("%s.outColorR" % conditionNode, "%s.input1X" % multiplyDivide, f=True)
        pm.setAttr("%s.input2X" % multiplyDivide, totalDistance)
        pm.setAttr("%s.operation" % multiplyDivide,2)


        #self.SPSW.AddEnumParameters(["off","on"], self.ikControl, Name = "StretchyIK")
        self.SPSW.AddNumericParameter(self.ikControl, Name="StretchyIK")
        IKSwitchDivide = pm.shadingNode("multiplyDivide",
                                        asUtility=True,
                                        name="IkSwitchDivide%s" % self.NameConv.get_a_short_name(self.IKjointStructure[2]))
        self.NameConv.rename_based_on_base_name(self.IKjointStructure[2],
                                                IKSwitchDivide, name=IKSwitchDivide)
        pm.connectAttr("%s.StretchyIK" % self.ikControl, "%s.input1X" % IKSwitchDivide)
        pm.setAttr("%s.input2X" % IKSwitchDivide, 10)
        pm.setAttr("%s.operation" % IKSwitchDivide, 2)

        IkSwitchblendTwoAttr = pm.shadingNode("blendTwoAttr", asUtility=True,
                                              name="IkSwitchBlendTwoAttr%s" %
                                                   self.NameConv.get_a_short_name(self.IKjointStructure[2]))
        self.NameConv.rename_based_on_base_name(self.IKjointStructure[2], IkSwitchblendTwoAttr,
                                                name=IkSwitchblendTwoAttr)

        pm.connectAttr("%s.outputX" % multiplyDivide, "%s.input[1]" % IkSwitchblendTwoAttr, force=True)
        pm.setAttr("%s.input[0]" % IkSwitchblendTwoAttr, 1)
        pm.connectAttr("%s.outputX" % IKSwitchDivide, "%s.attributesBlender" % IkSwitchblendTwoAttr, force=True)

        for joints in self.IKjointStructure[:-1]:
            pm.connectAttr("%s.output" % IkSwitchblendTwoAttr, "%s.scaleX" % joints)
            #IkSwitchCondition = pm.shadingNode("condition",asUtility=True,name="IkSwitchCondition" + self.NameConv.RMGetAShortName(joints))
            #IkSwitchCondition = self.NameConv.RMRenameNameInFormat(IkSwitchCondition)
            #pm.connectAttr( IKSwitchDivide + ".outputX", IkSwitchCondition + ".firstTerm" ,force = True)
            #pm.setAttr(IkSwitchCondition + ".secondTerm",0)
            #pm.setAttr(IkSwitchCondition + ".operation",0)
            #pm.connectAttr( multiplyDivide + ".outputX", IkSwitchCondition + ".colorIfFalseR" ,force = True)
            #pm.setAttr(IkSwitchCondition + ".colorIfTrueR", 1 )
            #pm.connectAttr(IkSwitchCondition + ".outColorR", joints + ".scaleX")

    def RMSkinSpaceSwitch (self):
        
        BoxResetPoint, BoxControl = self.shapeControls.RMCreateBoxCtrl(self.SknJointStructure[len(self.SknJointStructure)-1],
                                                                       name="IKFKSwitch")
        LongitudBrazo = RMRigTools.RMLenghtOfBone(self.SknJointStructure[1])
        pm.xform(BoxControl, objectSpace=True, relative=True, t=[LongitudBrazo/2,0,0])
        self.SPSW.RMCreateListConstraintSwitch( self.SknJointStructure, self.IKjointStructure, BoxControl,
                                                SpaceSwitchName="IKFKSwitch")
        self.SPSW.RMCreateListConstraintSwitch( self.SknJointStructure, self.FKjointStructure, BoxControl,
                                                SpaceSwitchName="IKFKSwitch", reverse = True)
        
        RMRigTools.RMLockAndHideAttributes(BoxControl, "000000000h")
        pm.parentConstraint(self.SknJointStructure[len(self.SknJointStructure)-1], BoxResetPoint)

        self.SpaceSwitchControl = BoxControl
        self.ResetSpaceSwitchControl = BoxResetPoint

    
    def RMCreateFKControls(self, AxisFree = "111"):
        #ArmParent ,FKFirstLimbControl = self.shapeControls.create_box_ctrl(self.FKjointStructure[0],Xratio=1,Yratio=.3,Zratio=.3, name = self.NameConv.RMGetAShortName(self.FKjointStructure[0]) + "FK")
        ArmParent ,FKFirstLimbControl = self.shapeControls.RMCircularControl(self.FKjointStructure[0], radius = RMRigTools.RMLenghtOfBone(self.FKjointStructure[0])/2, name =self.NameConv.get_a_short_name(self.FKjointStructure[0]) + "FK")
        
        RMRigTools.RMLinkHerarchyRotation(self.FKjointStructure[0], self.FKjointStructure[0],FKFirstLimbControl)

        RMRigTools.RMLockAndHideAttributes(FKFirstLimbControl,'000111000h')

        #SecondLimbParent ,FKSecondLimbControl = self.shapeControls.create_box_ctrl(self.FKjointStructure[1],Xratio=1,Yratio=.3,Zratio=.3, name = self.NameConv.RMGetAShortName(self.FKjointStructure[1])+ "FK")
        SecondLimbParent ,FKSecondLimbControl = self.shapeControls.RMCircularControl(self.FKjointStructure[1], radius = RMRigTools.RMLenghtOfBone(self.FKjointStructure[1])/2, name =self.NameConv.get_a_short_name(self.FKjointStructure[1]) + "FK")

        pm.parent(SecondLimbParent, FKFirstLimbControl)

        RMRigTools.RMLinkHerarchyRotation (self.FKjointStructure[1], self.FKjointStructure[1], FKSecondLimbControl)
        RMRigTools.RMLockAndHideAttributes (FKSecondLimbControl,'000%s000h'%AxisFree)

        #ThirdLimbParent ,FKTrirdLimbControl = self.shapeControls.create_box_ctrl(self.FKjointStructure[2], Xratio=.3, Yratio=.3, Zratio=.3 , ParentBaseSize = True, name = self.NameConv.RMGetAShortName(self.FKjointStructure[2]) + "FK")
        ThirdLimbParent ,FKTrirdLimbControl = self.shapeControls.RMCircularControl(self.FKjointStructure[2], radius = RMRigTools.RMLenghtOfBone(self.FKjointStructure[1])/3, name =self.NameConv.get_a_short_name(self.FKjointStructure[2]) + "FK")

        
        pm.parent(ThirdLimbParent, FKSecondLimbControl)

        #RMRigTools.RMLinkHerarchyRotation (self.FKjointStructure[2], self.FKjointStructure[2], FKTrirdLimbControl)
        pm.parentConstraint( FKTrirdLimbControl ,  self.FKjointStructure[2])

        RMRigTools.RMLockAndHideAttributes(FKTrirdLimbControl,'000111000h')
        
        self.FKFirstLimbControl = FKFirstLimbControl
        self.FKSecondLimbControl = FKSecondLimbControl
        self.ThirdLimbParent = ThirdLimbParent
        self.FKTrirdLimbControl = FKTrirdLimbControl
        pm.parentConstraint(self.FKparentGroup, ArmParent)
        self.ThirdLimbParent = ThirdLimbParent
        self.FKControls = ArmParent

        RMRigTools.RMChangeRotateOrder (self.FKTrirdLimbControl, 'yzx')

    def RMCreateIKControls(self):
        
        self.IKControlResetPoint, self.ikControl = self.shapeControls.RMCreateBoxCtrl(self.IKjointStructure[len(self.IKjointStructure)-1],
                                                                                      Xratio=.3,
                                                                                      Yratio=.3,
                                                                                      Zratio=.3,
                                                                                      ParentBaseSize=True,
                                                                                      name=self.NameConv.get_a_short_name("%sIK" % self.IKjointStructure[len(self.IKjointStructure) - 1]))
        #self.ikControl = self.NameConv.RMRenameBasedOnBaseName(self.IKjointStructure[len(self.IKjointStructure)-1], self.ikControl, NewName = self.NameConv.RMGetAShortName(self.IKjointStructure[len(self.IKjointStructure)-1]) + "IK")
        RMRigTools.RMLockAndHideAttributes(self.ikControl, "111111000h")
        
        self.IkHandle, effector = pm.ikHandle(sj=self.IKjointStructure[0],
                                              ee=self.IKjointStructure[len(self.IKjointStructure)-1],
                                              sol="ikRPsolver", name="LimbIKHandle")
        self.NameConv.rename_based_on_base_name(self.IKjointStructure[len(self.IKjointStructure) - 1], self.IkHandle)
        self.NameConv.rename_based_on_base_name(self.IKjointStructure[len(self.IKjointStructure) - 1], effector)

        pm.orientConstraint(self.ikControl, self.IKjointStructure[len(self.IKjointStructure)-1])

        PointConstraint = pm.pointConstraint(self.ikControl, self.IkHandle, name="LimbCntrlHandleConstraint")
        self.NameConv.rename_based_on_base_name(self.IKjointStructure[len(self.IKjointStructure) - 1], PointConstraint)
        self.kinematics.append(self.IkHandle)

        RMRigTools.RMChangeRotateOrder (self.ikControl, 'yzx')


    def RMGetPoleVectorReferencePoint(self,JointList):
        VP1 = om.MVector(pm.xform(JointList[0],a=True,ws=True,q=True,rp=True))
        VP2 = om.MVector(pm.xform(JointList[1],a=True,ws=True,q=True,rp=True))
        VP3 = om.MVector(pm.xform(JointList[2],a=True,ws=True,q=True,rp=True))
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
        PoleVector = pm.spaceLocator(name="poleVector")
        self.NameConv.rename_based_on_base_name(JointList[1], PoleVector, name=PoleVector)

        pm.xform(PoleVector, ws=True, t=result)
        return PoleVector

    def RMCreatePoleVector(self,IKHandle):

        if not self.IKjointStructure:
            self.IKjointStructure = self.RMIdentifyIKJoints(IKHandle)
        locator = self.RMGetPoleVectorReferencePoint(self.IKjointStructure)
        
        distancia = RMRigTools.RMPointDistance(locator, self.IKjointStructure[1])

        self.PoleVectorControlResetPnt, self.PoleVectorControl = self.shapeControls.RMCreateBoxCtrl(locator, customSize=distancia / 5, name=self.NameConv.get_a_short_name(self.IKjointStructure[1]) + "PoleVectorIK", centered = True)

        dataGroup, Curve = self.rig_tools.RMCreateLineBetwenPoints(self.PoleVectorControl, self.IKjointStructure[1])
        pm.parent(Curve, self.PoleVectorControl)
        pm.parentConstraint(self.world, Curve)

        PoleVectorCnstraint = pm.poleVectorConstraint(self.PoleVectorControl, IKHandle, name="PoleVector")
        self.NameConv.rename_based_on_base_name(self.PoleVectorControl, PoleVectorCnstraint, name=PoleVectorCnstraint)

        self.kinematics.append(dataGroup)
        pm.delete(locator)

