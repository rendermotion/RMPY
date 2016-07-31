import maya.cmds as cmds
import RMRigTools
reload (RMRigTools)
import RMRigShapeControls
reload (RMRigShapeControls)
import RMNameConvention
reload (RMNameConvention)


class RMLimbIKFK(object):
    def __init__(self, NameConv = None):
        if not NameConv:
            self.NameConv = RMNameConvention.RMNameConvention()
        else:
            self.NameConv = NameConv

        self.IKjointStructure = None
        self.IKSkinJointStructure = None
        self.IKparentGroup = None
        self.IkHandle = None

        self.FKjointStructure = None
        self.FKparentGroup = None

        self.SknJointStructure = None
        self.SknparentGroup = None

    def RMLimbJointEstructure(self,OriginPoint,ZAxisOrientation = "z", ):
        LimbReferencePonits = RMRigTools.RMCustomPickWalk(OriginPoint,'transform',2)
        return RMRigTools.RMCreateBonesAtPoints(LimbReferencePonits,NameConv = self.NameConv, ZAxisOrientation = ZAxisOrientation)

    def RMIdentifyIKJoints(ikHandle):
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
            self.IKjointStructure = RMIdentifyIKJoints(ikHandle)
        totalDistance = self.BoneChainLenght(self.IKjointStructure)
        transformStartPoint = cmds.spaceLocator(name="StretchyIkHandleStartPoint")[0]
        transformEndPoint  = cmds.spaceLocator (name="StretchyIkHandleEndPoint")[0]
        if self.IKparentGroup:
            cmds.parent(transformStartPoint,self.IKparentGroup)
            cmds.parent(transformEndPoint,self.IKparentGroup)

        StartPointConstraint = cmds.pointConstraint(self.IKjointStructure[0],transformStartPoint)
        EndPointConstraint = cmds.pointConstraint(ikHandle,transformEndPoint)

        distanceNode = cmds.shadingNode("distanceBetween", asUtility=True)

        cmds.connectAttr(transformStartPoint + ".worldPosition[0]", distanceNode + ".point1",f=True)
        cmds.connectAttr(transformEndPoint + ".worldPosition[0]", distanceNode + ".point2",f=True)
        
        conditionNode = cmds.shadingNode("condition",asUtility=True)
        cmds.connectAttr(distanceNode + ".distance",conditionNode + ".colorIfFalseR",f=True)
        cmds.connectAttr(distanceNode + ".distance",conditionNode + ".secondTerm",f=True)
        cmds.setAttr(conditionNode + ".operation",3)
        cmds.setAttr(conditionNode +".firstTerm",totalDistance)
        cmds.setAttr(conditionNode +".colorIfTrueR",totalDistance)
        multiplyDivide = cmds.shadingNode("multiplyDivide", asUtility=True)
        cmds.connectAttr(conditionNode + ".outColorR",multiplyDivide+".input1X" ,f=True)
        cmds.setAttr(multiplyDivide + ".input2X",totalDistance)
        cmds.setAttr(multiplyDivide + ".operation",2)
        for joints in self.IKjointStructure[:-1]:
            cmds.connectAttr( multiplyDivide + ".outputX", joints + ".scaleX",force = True)

    def RMLimbRig(self,RootReferencePoint):

        self.IKparentGroup , self.IKjointStructure = self.RMLimbJointEstructure(RootReferencePoint)
        self.RMCreateIKControls()
        #self.RMMakeIkStretchy(self.IkHandle)

        #self.FKparentGroup , self.FKjointStructure = self.RMLimbJointEstructure(RootReferencePoint)        
        #self.RMCreateFKControls()
    
    def RMCreateFKControls(self,AxisFree = "Y"):
        FKFirstLimbControl = RMRigShapeControls.RMCreateBoxCtrl(self.FKjointStructure[0],Xratio=1,Yratio=.3,Zratio=.3)
        ArmParent = RMRigTools.RMCreateGroupOnObj(FKFirstLimbControl)
        RMRigTools.RMLinkHerarchyRotation (self.FKjointStructure[0], self.FKjointStructure[1],FKFirstLimbControl)

        RMRigTools.RMLockAndHideAttributes (FKFirstLimbControl,'0000111000')

        FKSecondLimbControl = RMRigShapeControls.RMCreateBoxCtrl(self.FKjointStructure[1],Xratio=1,Yratio=.3,Zratio=.3)
        SecondLimbParent = RMRigTools.RMCreateGroupOnObj(FKSecondLimbControl)
        cmds.parent(SecondLimbParent, FKFirstLimbControl)

        RMRigTools.RMLinkHerarchyRotation (self.FKjointStructure[1], self.FKjointStructure[2], FKSecondLimbControl)
        if AxisFree == "Y":
            RMRigTools.RMLockAndHideAttributes (FKSecondLimbControl,'0000100000')
        if AxisFree == "Z":
            RMRigTools.RMLockAndHideAttributes (FKSecondLimbControl,'0000010000')

    def RMCreateIKControls(self):
        
        self.ikControl = RMRigShapeControls.RMCreateBoxCtrl(self.IKjointStructure[len(self.IKjointStructure)-1], Xratio = .3, Yratio = .3, Zratio = .3, ParentBaseSize = True)
        self.ikControl = self.NameConv.RMRenameBasedOnBaseName(self.IKjointStructure[len(self.IKjointStructure)-1],self.ikControl)
        
        self.IkHandle, effector = cmds.ikHandle (sj = self.IKjointStructure[0], ee = self.IKjointStructure[len(self.IKjointStructure)-1], name = "LimbIKHandle")
        self.IkHandle = self.NameConv.RMRenameBasedOnBaseName(self.IKjointStructure[len(self.IKjointStructure)-1],self.IkHandle)
        effector = self.NameConv.RMRenameBasedOnBaseName(self.IKjointStructure[len(self.IKjointStructure)-1],effector)

        PointConstraint = cmds.pointConstraint (self.ikControl, self.IkHandle, name = "LimbCntrlHandleConstraint")
        PointConstraint = self.NameConv.RMRenameBasedOnBaseName(self.IKjointStructure[len(self.IKjointStructure)-1],PointConstraint[0])
        


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
