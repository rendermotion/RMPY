import pymel.core as pm
import maya.api.OpenMaya as om
from RMPY import RMNameConvention
reload(RMNameConvention)
from RMPY import RMRigTools
reload(RMRigTools)
from RMPY import RMRigShapeControls
reload(RMRigShapeControls)

class RMTwistJoints(object):
    def __init__(self, NameConv = None):
        if not NameConv:
            self.NameConv = RMNameConvention.RMNameConvention()
        else:
            self.NameConv = NameConv
        self.kinematics = []
        self.TwistJoints = None
        self.TwistResetJoints = None
        self.TwistControlResetPoint = None
        self.TwistControl = None
        self.TwistOrigin = None
        self.TwistEnd = None

    def RMCreateTwistJoints(self, TwistJoint, LookAtObject, NumberOfTB = 3, LookAtAxis = "Y"):

        self.RMCreateTwist( TwistJoint, LookAtObject, NumberOfTB = NumberOfTB, LookAtAxis = LookAtAxis)
        self.TwistOrigin =  TwistJoint
        self.TwistEnd =  LookAtObject
        self.RMStretchyTwistJoints()


    def RMCreateTwist(self, TwistJoint, LookAtObject,  NumberOfTB = 3, LookAtAxis = "Y"):
        #LookAtObject = pm.listRelatives( TwistJoint,type = "transform",children=True)[]
    
        positionA = pm.xform(TwistJoint ,q=True,ws=True,rp=True)
        positionB = pm.xform(LookAtObject ,q=True,ws=True,rp=True)

        vectorA = om.MVector(positionA)
        vectorB = om.MVector(positionB)

        self.RMCreateBonesBetweenPoints(vectorA,vectorB,NumberOfTB, AlignObject=TwistJoint)

        Distance = RMRigTools.RMPointDistance( TwistJoint, LookAtObject)
        
        pm.parentConstraint (TwistJoint, self.TwistResetJoints)

        resetPoint , control = RMRigShapeControls.RMCreateBoxCtrl(self.TwistJoints[0],
                                                                  Xratio=.1,
                                                                  Yratio=.1,
                                                                  Zratio=.1,
                                                                  customSize=Distance/5 ,
                                                                  name="TwistOrigin%s" % self.NameConv.RMGetAShortName(TwistJoint).title())
        #control = self.NameConv.RMRenameBasedOnBaseName(TwistJoint , control,  NewName = self.NameConv.RMGetAShortName(control))
        #resetPoint = self.NameConv.RMRenameBasedOnBaseName(TwistJoint , resetPoint,  NewName = self.NameConv.RMGetAShortName(resetPoint))
        
        sign = 1
        MoveDistance = Distance/5
        if "-" in LookAtAxis:
            sign = -1
        if "Z" in LookAtAxis or "z" in LookAtAxis:
            MoveList = [0,0, MoveDistance * sign]
            WUV = [0,0,sign]
        elif "Y" in LookAtAxis or "y" in LookAtAxis:
            MoveList = [0,MoveDistance * sign,0 ]
            WUV = [0,sign,0]

        pm.xform( resetPoint, os = True, relative=True,  t = MoveList)

        pm.aimConstraint( LookAtObject,self.TwistJoints[0], aim = [1,0,0], worldUpVector = [0,0,1], worldUpType = "object", worldUpObject = control)

        TwistJointDivide = pm.shadingNode("multiplyDivide", asUtility=True,
                                          name="TwistJoint%s" % self.NameConv.RMGetAShortName( TwistJoint).title())
        self.NameConv.RMRenameBasedOnBaseName(TwistJoint, TwistJointDivide,
                                              {'name': self.NameConv.RMGetAShortName(TwistJointDivide)})


        TwistAddition = pm.shadingNode( "plusMinusAverage", asUtility = True, name = "TwistJointAdd" + self.NameConv.RMGetAShortName( TwistJoint).title())
        self.NameConv.RMRenameBasedOnBaseName(TwistJoint, TwistAddition,
                                              {'name': self.NameConv.RMGetAShortName(TwistAddition)})
        NegativeLookAtRotation = pm.shadingNode("multiplyDivide", asUtility=True,
                                                name="NegativeLookAtRotation%s" %
                                                     self.NameConv.RMGetAShortName(TwistJoint).title())
        self.NameConv.RMRenameBasedOnBaseName(TwistJoint , NegativeLookAtRotation,
                                              {'name': self.NameConv.RMGetAShortName(NegativeLookAtRotation)})
        pm.connectAttr( LookAtObject + ".rotateX", NegativeLookAtRotation + ".input1X")
        pm.setAttr("%s.input2X" % NegativeLookAtRotation, -1)
        pm.setAttr("%s.operation" % NegativeLookAtRotation, 1)
        pm.connectAttr("%s.rotateX" % self.TwistJoints[0], "%s.input1D[0]" % TwistAddition)
        pm.connectAttr("%s.outputX" % NegativeLookAtRotation, "%s.input1D[1]" % TwistAddition)
        pm.connectAttr("%s.output1D" % TwistAddition, "%s.input1X" % TwistJointDivide)


        #pm.connectAttr(self.TwistJoints[0]+".rotateX", TwistJointDivide + ".input1X") in this case the rotation of the lookatNode was not affecting
        pm.setAttr("%s.input2X" % TwistJointDivide, -(len(self.TwistJoints) - 1))
        pm.setAttr("%s.operation" % TwistJointDivide, 2)

        for eachJoint in self.TwistJoints[1:]:
            pm.connectAttr("%s.outputX" % TwistJointDivide, "%s.rotateX" % eachJoint)


        self.TwistControlResetPoint = resetPoint
        self.TwistControl = control

    def RMDistanceBetweenPointsMeasure(self, Point01, Point02, name = ""):
        if name != "":
            transformStartPoint = "start" + name
            transformEndPoint = "end" + name
        else:
            transformStartPoint = "startPoint"
            transformEndPoint = "endPoint"

        transformStartPoint = pm.spaceLocator(name=transformStartPoint)
        self.NameConv.RMRenameNameInFormat(transformStartPoint, {})
        transformEndPoint = pm.spaceLocator(name=transformEndPoint)
        self.NameConv.RMRenameNameInFormat(transformEndPoint, {})

        StartPointConstraint = pm.pointConstraint(Point01, transformStartPoint)
        EndPointConstraint = pm.pointConstraint(Point02, transformEndPoint)

        distanceNode = pm.shadingNode("distanceBetween", asUtility=True, name="DistanceNode")
        self.NameConv.RMRenameBasedOnBaseName(Point01, distanceNode, {'name': distanceNode})

        pm.connectAttr("%s.worldPosition[0]" % transformStartPoint, "%s.point1" % distanceNode, f=True)
        pm.connectAttr("%s.worldPosition[0]" % transformEndPoint, "%s.point2" % distanceNode, f=True)

        return [transformStartPoint, transformEndPoint], distanceNode

    def RMStretchyTwistJoints(self):
        locators , distanceNode = self.RMDistanceBetweenPointsMeasure(self.TwistOrigin, self.TwistEnd,"Twist" + self.NameConv.RMGetAShortName(self.TwistOrigin).title())

        stretchyRefGroup = pm.group(empty=True, name="StretchyRefPoints%s" %
                                    self.NameConv.RMGetAShortName(self.TwistOrigin).title())
        self.NameConv.RMRenameBasedOnBaseName(self.TwistOrigin, stretchyRefGroup, {'name': stretchyRefGroup})
        RMRigTools.RMParentArray(stretchyRefGroup, locators)

        TwistJointDivide = pm.shadingNode("multiplyDivide", asUtility=True,
                                          name="StretchyTwistJoint%s" % self.NameConv.RMGetAShortName(self.TwistOrigin).title())
        #self.NameConv.RMRenameNameInFormat(TwistJointDivide,{})
        self.NameConv.RMRenameBasedOnBaseName(self.TwistOrigin, TwistJointDivide, {'name': TwistJointDivide})

        pm.connectAttr("%s.distance" % distanceNode, "%s.input1X" % TwistJointDivide)
        pm.setAttr("%s.input2X" % TwistJointDivide, (len(self.TwistJoints) - 1))
        pm.setAttr("%s.operation" % TwistJointDivide, 2)

        for eachJoint in self.TwistJoints[1:]:
            pm.connectAttr("%s.outputX" % TwistJointDivide, "%s.translateX" % eachJoint)
        self.kinematics.append(stretchyRefGroup)

    def RMCreateBonesBetweenPoints(self, InitialPoint, FinalPoint, NumberOfTB, AlignObject=None):
        DirectionVector  = FinalPoint-InitialPoint
        TotalLength = DirectionVector.length()
        Step = TotalLength / NumberOfTB
        StepVector = DirectionVector.normal() * Step
        locatorsList = []

        for count in range(0, NumberOfTB + 1):
            Locator = pm.spaceLocator()
            if AlignObject:
                if self.NameConv.RMIsNameInFormat (AlignObject):
                    self.NameConv.RMRenameBasedOnBaseName(AlignObject, Locator,
                                                          {'name': 'TwistJoint%s' %
                                                                   (self.NameConv.RMGetFromName(AlignObject,
                                                                                                "name").capitalize())})#.capitalize()
            locatorsList.append(Locator)
            pm.xform(Locator, translation=list(InitialPoint+(StepVector*count)), worldSpace=True)
            RMRigTools.RMAlign(AlignObject, Locator, 2)
        self.TwistResetJoints, self.TwistJoints = RMRigTools.RMCreateBonesAtPoints(locatorsList)
        self.deleteList(locatorsList)
        return self.TwistResetJoints, self.TwistJoints

    def deleteList(self, listToDelete):
        for eachObject in listToDelete:
            pm.delete(eachObject)

#TJ = RMTwistJoints()
#TJ.RMCreateTwistJoints("Character01_LF_shoulder_pnt_rfr","Character01_LF_elbow_pnt_rfr")








