import maya.cmds as cmds
import maya.api.OpenMaya as om
import RMNameConvention
reload (RMNameConvention)
import RMRigTools
reload (RMRigTools)
import RMRigShapeControls
reload (RMRigShapeControls)

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

        self.RMCreateTwist( TwistJoint, LookAtObject,NumberOfTB = NumberOfTB, LookAtAxis = LookAtAxis)
        self.TwistOrigin =  TwistJoint
        self.TwistEnd =  LookAtObject
        self.RMStretchyTwistJoints()


    def RMCreateTwist(self, TwistJoint, LookAtObject,  NumberOfTB = 3, LookAtAxis = "Y"):
        #LookAtObject = cmds.listRelatives( TwistJoint,type = "transform",children=True)[]
    
        positionA = cmds.xform(TwistJoint ,q=True,ws=True,rp=True)
        positionB = cmds.xform(LookAtObject ,q=True,ws=True,rp=True)

        vectorA = om.MVector(positionA)
        vectorB = om.MVector(positionB)

        self.RMCreateBonesBetweenPoints(vectorA,vectorB,NumberOfTB, AlignObject = TwistJoint)

        Distance = RMRigTools.RMPointDistance( TwistJoint, LookAtObject)
        
        cmds.parentConstraint (TwistJoint,self.TwistResetJoints)

        resetPoint , control = RMRigShapeControls.RMCreateBoxCtrl(self.TwistJoints[0], Xratio = .1, Yratio = .1, Zratio = .1, customSize = Distance/5 ,name = "TwistOrigin" + self.NameConv.RMGetAShortName (TwistJoint).title())
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

        cmds.xform( resetPoint, os = True, relative=True,  t = MoveList)

        cmds.aimConstraint( LookAtObject,self.TwistJoints[0], aim = [1,0,0], worldUpVector = [0,0,1], worldUpType = "object", worldUpObject = control)

        TwistJointDivide = cmds.shadingNode( "multiplyDivide", asUtility = True, name = "TwistJoint" + self.NameConv.RMGetAShortName( TwistJoint).title())
        TwistJointDivide = self.NameConv.RMRenameBasedOnBaseName( TwistJoint , TwistJointDivide,  NewName = self.NameConv.RMGetAShortName( TwistJointDivide))


        TwistAddition = cmds.shadingNode( "plusMinusAverage", asUtility = True, name = "TwistJointAdd" + self.NameConv.RMGetAShortName( TwistJoint).title())
        TwistAddition = self.NameConv.RMRenameBasedOnBaseName( TwistJoint , TwistAddition,  NewName = self.NameConv.RMGetAShortName( TwistAddition))
        NegativeLookAtRotation = cmds.shadingNode( "multiplyDivide", asUtility = True, name = "NegativeLookAtRotation" + self.NameConv.RMGetAShortName( TwistJoint).title())
        NegativeLookAtRotation = self.NameConv.RMRenameBasedOnBaseName( TwistJoint , NegativeLookAtRotation,  NewName = self.NameConv.RMGetAShortName( NegativeLookAtRotation))
        cmds.connectAttr( LookAtObject + ".rotateX", NegativeLookAtRotation + ".input1X")
        cmds.setAttr(NegativeLookAtRotation + ".input2X", -1 )
        cmds.setAttr(NegativeLookAtRotation + ".operation", 1 )
        cmds.connectAttr(self.TwistJoints[0]+".rotateX", TwistAddition + ".input1D[0]")
        cmds.connectAttr( NegativeLookAtRotation + ".outputX", TwistAddition + ".input1D[1]")
        cmds.connectAttr(TwistAddition + ".output1D", TwistJointDivide + ".input1X")


        #cmds.connectAttr(self.TwistJoints[0]+".rotateX", TwistJointDivide + ".input1X") in this case the rotation of the lookatNode was not affecting
        cmds.setAttr(TwistJointDivide + ".input2X", -(len(self.TwistJoints) - 1))
        cmds.setAttr(TwistJointDivide + ".operation", 2 )

        for eachJoint in self.TwistJoints[1:]:
            cmds.connectAttr(TwistJointDivide+".outputX", eachJoint + ".rotateX")


        self.TwistControlResetPoint = resetPoint
        self.TwistControl = control

    def RMDistanceBetweenPointsMeasure(self, Point01, Point02, name = ""):
        if name != "":
            transformStartPoint = "start" + name
            transformEndPoint = "end" + name
        else:
            transformStartPoint = "startPoint"
            transformEndPoint = "endPoint"

        transformStartPoint = cmds.spaceLocator(name=transformStartPoint)[0]
        transformStartPoint = self.NameConv.RMRenameNameInFormat(transformStartPoint)
        transformEndPoint  = cmds.spaceLocator (name=transformEndPoint)[0]
        transformEndPoint = self.NameConv.RMRenameNameInFormat(transformEndPoint)

        StartPointConstraint = cmds.pointConstraint (Point01, transformStartPoint)
        EndPointConstraint = cmds.pointConstraint (Point02, transformEndPoint)

        distanceNode = cmds.shadingNode("distanceBetween", asUtility=True, name = "DistanceNode")
        distanceNode = self.NameConv.RMRenameBasedOnBaseName( Point01, distanceNode, NewName = distanceNode)

        cmds.connectAttr(transformStartPoint + ".worldPosition[0]", distanceNode + ".point1",f=True)
        cmds.connectAttr(transformEndPoint + ".worldPosition[0]", distanceNode + ".point2",f=True)

        return [transformStartPoint,transformEndPoint] , distanceNode

    def RMStretchyTwistJoints(self):
        locators , distanceNode = self.RMDistanceBetweenPointsMeasure(self.TwistOrigin, self.TwistEnd,"Twist" + self.NameConv.RMGetAShortName(self.TwistOrigin).title())

        stretchyRefGroup = cmds.group(empty = True, name = "StretchyRefPoints" + self.NameConv.RMGetAShortName(self.TwistOrigin).title())
        stretchyRefGroup = self.NameConv.RMRenameBasedOnBaseName(self.TwistOrigin, stretchyRefGroup, NewName = stretchyRefGroup)
        RMRigTools.RMParentArray(stretchyRefGroup, locators)

        TwistJointDivide = cmds.shadingNode( "multiplyDivide", asUtility = True, name = "StretchyTwistJoint" + self.NameConv.RMGetAShortName(self.TwistOrigin).title())
        TwistJointDivide = self.NameConv.RMRenameNameInFormat( TwistJointDivide)
        TwistJointDivide = self.NameConv.RMRenameBasedOnBaseName(self.TwistOrigin , TwistJointDivide,  NewName = self.NameConv.RMGetAShortName(TwistJointDivide))

        cmds.connectAttr(distanceNode+".distance", TwistJointDivide + ".input1X")
        cmds.setAttr(TwistJointDivide + ".input2X", (len(self.TwistJoints) - 1))
        cmds.setAttr(TwistJointDivide + ".operation", 2)

        for eachJoint in self.TwistJoints[1:]:
            cmds.connectAttr(TwistJointDivide + ".outputX", eachJoint + ".translateX")
        self.kinematics.append(stretchyRefGroup)


    def RMCreateBonesBetweenPoints(self,InitialPoint, FinalPoint, NumberOfTB,AlignObject = None):
        DirectionVector  = FinalPoint-InitialPoint
        TotalLength = DirectionVector.length()
        Step = TotalLength / NumberOfTB
        StepVector = DirectionVector.normal() * Step
        locatorsList = []

        for count in range(0,NumberOfTB + 1):
            Locator = cmds.spaceLocator()
            if AlignObject:
                if self.NameConv.RMIsNameInFormat (AlignObject):
                    Locator[0] = self.NameConv.RMRenameBasedOnBaseName(AlignObject,Locator[0], NewName= 'TwistJoint' + self.NameConv.RMGetFromName(AlignObject,"Name").capitalize())
            locatorsList.append(Locator[0])
            cmds.xform(Locator[0], translation = list(InitialPoint + (StepVector * count)), worldSpace=True)
            RMRigTools.RMAlign(AlignObject,Locator[0],2)
        self.TwistResetJoints , self.TwistJoints = RMRigTools.RMCreateBonesAtPoints(locatorsList)
        self.deleteList(locatorsList)
        return self.TwistResetJoints, self.TwistJoints

    def deleteList (self,listToDelete):
        for eachObject in listToDelete:
            cmds.delete(eachObject)

#TJ = RMTwistJoints()
#TJ.RMCreateTwistJoints("Character01_LF_shoulder_pnt_rfr","Character01_LF_elbow_pnt_rfr")








