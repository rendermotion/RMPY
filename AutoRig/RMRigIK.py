import pymel.core as pm
import maya.OpenMayaUI as mui
import maya.api.OpenMaya as om

import math
from RMPY import RMNameConvention
from RMPY import RMRigTools

class ik_rig_model(object):
    def __init__(self):
        self.name = ''
        self.guides = []
        self.joints = []
        self.controls = {'poleVector' :None, 'ikHandle':None}
        self.root_kinematics = None
        self.root_joints = None
        self.root_controls = None

class generic_tool(object):
    def __init__(self, nameConv = None):
        if not nameConv:
            self.nameConv = RMNameConvention.RMNameConvention()
        else:
            self.nameConv = nameConv
        self.rig_tools = RMRigTools.RMRigTools()

class ik_rig(generic_tool):
    def __init__(self, nameConv = None):
        super(ik_rig, self).__init__(nameConv = nameConv)
        self._model = ik_rig_model()

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        self._model = model

    @classmethod
    def build_from_guides(cls, guides):
        new_ik_instance = cls()
        new_ik_instance.model.guides = guides
        new_ik_instance.build_joints()
        return new_ik_instance

    def build_joints(self):
        self.rig_tools.create_bones_at_points(self.model.guides)


    @classmethod
    def build_from_joints(cls, joints):
        new_ik_instance = cls()
        new_ik_instance.model.joints = joints
        return new_ik_instance

    def BoneChainLenght(self,BoneChain):
        distancia = 0
        for index in range(1,len(BoneChain)):
           distancia += RMRigTools.RMPointDistance(BoneChain[index-1],BoneChain[index])
        return distancia

    def identify_joints(self, ikHandle):
        
        endEffector = pm.ikHandle(ikHandle, q = True, endEffector = True)
        EndJoint = RMRigTools.RMCustomPickWalk(endEffector, 'joint', 1, Direction = "up")
        EndJoint = RMRigTools.RMCustomPickWalk(EndJoint[len(EndJoint) - 1], 'joint', 1)
        EndJoint = EndJoint[1]
        StartJoint = pm.ikHandle(ikHandle, q=True, startJoint=True)
        return RMRigTools.FindInHieararchy(StartJoint, EndJoint)

    def get_polevector_from_reference_nodes(self, node_list):
        """
        :param node_list: list of 3 nodes where the pole vector will be calculated.  
        :return: a space locator that it is located where the pole vector should be.
        """
        VP1 = om.MVector(pm.xform(node_list[0], a=True, ws=True, q=True, rp=True))
        VP2 = om.MVector(pm.xform(node_list[1], a=True, ws=True, q=True, rp=True))
        VP3 = om.MVector(pm.xform(node_list[2], a=True, ws=True, q=True, rp=True))
        PoleVector = pm.spaceLocator(name="poleVector")[0]
        PoleVector = self.nameConv.RMRenameBasedOnBaseName(node_list[1], PoleVector, {'name': PoleVector})
        pm.xform(PoleVector, ws=True, t = self.pole_vector(VP1, VP2, VP3))
        return PoleVector

    def pole_vector(self, VP1, VP2, VP3):
        V1 = VP2 - VP1
        V2 = VP3 - VP2
        Angle = math.radians((math.degrees(V1.angle(V2)) + 180) / 2 - 90)
        zAxis = (V1 ^ V2).normal()
        yAxis = (V2 ^ zAxis).normal()
        xAxis = V2.normal()

        Y1 = math.cos(Angle)
        X1 = -math.sin(Angle)
        Vy = yAxis * Y1
        Vx = xAxis * X1

        Length = (V1.length() + V2.length()) / 2
        result = ((Vy + Vx) * Length) + VP2
        return result

    def make_stretchy(self, ikHandle):
        if not self._model.joints:
            self._model.joints = self.RMIdentifyIKJoints(ikHandle)

        totalDistance = self.BoneChainLenght(self._model.joints)
        transformStartPoint = pm.spaceLocator(name="StretchyIkHandleStartPoint")[0]
        transformStartPoint = self.nameConv.RMRenameNameInFormat(transformStartPoint, {})
        transformEndPoint = pm.spaceLocator(name="StretchyIkHandleEndPoint")[0]
        transformEndPoint = self.nameConv.RMRenameNameInFormat(transformEndPoint, {})

        if self.IKparentGroup:
            pm.parent(transformStartPoint, self.IKparentGroup)
            pm.parent(transformEndPoint, self.IKparentGroup)

        StartPointConstraint = pm.pointConstraint(self._model.joints[0], transformStartPoint)
        EndPointConstraint = pm.pointConstraint(ikHandle, transformEndPoint)

        distanceNode = pm.shadingNode("distanceBetween", asUtility=True,
                                        name="IKBaseDistanceNode" + self.nameConv.RMGetAShortName(self._model.joints[2]))
        distanceNode = self.nameConv.RMRenameBasedOnBaseName(self._model.joints[2], distanceNode, {'name': distanceNode})

        pm.connectAttr(transformStartPoint + ".worldPosition[0]", distanceNode + ".point1", f=True)
        pm.connectAttr(transformEndPoint + ".worldPosition[0]", distanceNode + ".point2", f=True)

        conditionNode = pm.shadingNode("condition", asUtility=True,
                                         name="IkCondition" + self.nameConv.RMGetAShortName(self._model.joints[2]))
        conditionNode = self.nameConv.RMRenameBasedOnBaseName(self._model.joints[2], conditionNode,
                                                              {'name': conditionNode})
        pm.connectAttr(distanceNode + ".distance", conditionNode + ".colorIfFalseR", f=True)
        pm.connectAttr(distanceNode + ".distance", conditionNode + ".secondTerm", f=True)
        pm.setAttr(conditionNode + ".operation", 3)
        pm.setAttr(conditionNode + ".firstTerm", totalDistance)
        pm.setAttr(conditionNode + ".colorIfTrueR", totalDistance)
        multiplyDivide = pm.shadingNode("multiplyDivide", asUtility=True,
                                          name="IKStretchMultiply" + self.nameConv.RMGetAShortName(
                                              self._model.joints[2]))
        multiplyDivide = self.nameConv.RMRenameBasedOnBaseName(self._model.joints[2], multiplyDivide,
                                                               {'name': multiplyDivide})

        pm.connectAttr(conditionNode + ".outColorR", multiplyDivide + ".input1X", f=True)
        pm.setAttr(multiplyDivide + ".input2X", totalDistance)
        pm.setAttr(multiplyDivide + ".operation", 2)

        # self.SPSW.AddEnumParameters(["off","on"], self.ikControl, Name = "StretchyIK")
        self.SPSW.AddNumericParameter(self.ikControl, Name="StretchyIK")
        IKSwitchDivide = pm.shadingNode("multiplyDivide", asUtility=True,
                                          name="IkSwitchDivide" + self.nameConv.RMGetAShortName(self._model.joints[2]))
        IKSwitchDivide = self.nameConv.RMRenameBasedOnBaseName(self._model.joints[2], IKSwitchDivide,
                                                               {'name': IKSwitchDivide})
        pm.connectAttr(self.ikControl + ".StretchyIK", IKSwitchDivide + ".input1X")
        pm.setAttr(IKSwitchDivide + ".input2X", 10)
        pm.setAttr(IKSwitchDivide + ".operation", 2)

        IkSwitchblendTwoAttr = pm.shadingNode("blendTwoAttr", asUtility=True,
                                                name="IkSwitchBlendTwoAttr" + self.nameConv.RMGetAShortName(
                                                    self._model.joints[2]))
        IkSwitchblendTwoAttr = self.nameConv.RMRenameBasedOnBaseName(self._model.joints[2], IkSwitchblendTwoAttr,
                                                                     {'name': IkSwitchblendTwoAttr})

        pm.connectAttr(multiplyDivide + ".outputX", IkSwitchblendTwoAttr + ".input[1]", force=True)
        pm.setAttr(IkSwitchblendTwoAttr + ".input[0]", 1)
        pm.connectAttr(IKSwitchDivide + ".outputX", IkSwitchblendTwoAttr + ".attributesBlender", force=True)

        for joints in self._model.joints[:-1]:
            pm.connectAttr(IkSwitchblendTwoAttr + ".output", joints + ".scaleX")

if __name__=='__main__':
    reload(RMRigTools)
    selection = pm.ls(selection = True)
    print selection
    ikrig = ik_rig.build_from_guides(selection)


