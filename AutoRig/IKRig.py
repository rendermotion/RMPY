import pymel.core as pm
import maya.OpenMayaUI as mui
import maya.api.OpenMaya as om

import math
from RMPY import nameConvention
from RMPY import RMRigTools
from RMPY import RMRigShapeControls
from RMPY.AutoRig import rigStructure
from RMPY.AutoRig import RMSpaceSwitch

reload(rigStructure)

class IKRigModel(object):
    def __init__(self):
        self.name = ''
        self.guides = []
        self.joints = []
        self.ik_handle = None
        self.controls = {'poleVector': None, 'ikHandle': None}
        self.reset_controls = {'poleVector': None, 'ikHandle': None}
        self.root_kinematics = None
        self.root_joints = None
        self.root_controls = None
        self.kinematics = []


class GenericRig(object):
    def __init__(self, name_conv=None):
        if not name_conv:
            self.name_conv = nameConvention.NameConvention()
        else:
            self.name_conv = name_conv
        self.rig_tools = RMRigTools.RMRigTools()
        self.rig_structure = rigStructure.RigStructure()
        self.rig_controls = RMRigShapeControls.RMRigShapeControls()
        self.rig_space_switch = RMSpaceSwitch.RMSpaceSwitch()


class IKRig(GenericRig):
    def __init__(self, name_conv=None):
        super(IKRig, self).__init__(name_conv=name_conv)
        self._model = IKRigModel()

    @property
    def model(self):
        return self._model

    @property
    def joints(self):
        return self._model.joints

    @joints.setter
    def joints(self, joint_list):
        self._model.joints = joint_list

    @property
    def controls(self):
        return self._model.controls

    @controls.setter
    def controls(self, controls_list):
        self._model.controls = controls_list

    @property
    def ik_handle(self):
        return self._model.ik_handle

    @ik_handle.setter
    def ik_handle(self, ik_handle_node):
        self._model.ik_handle = ik_handle_node

    @property
    def guides(self):
        return self._model.guides

    @guides.setter
    def guides(self,guides_list):
        self._model.guides = guides_list

    @property
    def root_kinematics(self):
        return self._model.root_kinematics

    @root_kinematics.setter
    def root_kinematics(self, kinematics_node):
        self._model.root_kinematics = kinematics_node

    @property
    def kinematics(self):
        return self._model.kinematics

    @property
    def root_joints(self):
        return self._model.root_joints

    @root_joints.setter
    def root_joints(self,maya_node):
        self._model.root_joints = maya_node

    @property
    def reset_controls(self):
        return self._model.reset_controls

    @reset_controls.setter
    def reset_controls(self, scene_node):
        self._model.reset_controls = scene_node

    @property
    def root_controls(self):
        return self._model.root_controls

    @root_controls.setter
    def root_controls(self, rootControl):
        self._model.root_controls = rootControl

    @classmethod
    def build_from_guides(cls, guides):
        new_ik_instance = cls()
        new_ik_instance.model.guides = guides
        new_ik_instance.build_joints()
        return new_ik_instance

    @classmethod
    def build_from_joints(cls, joints):
        new_ik_instance = cls()
        new_ik_instance.model.joints = joints
        return new_ik_instance

    def build_joints(self):
        self.root_joints, self.joints = self.rig_tools.create_bones_at_points(self.model.guides)

    def BoneChainLenght(self, BoneChain):
        distancia = 0
        for index in range(1, len(BoneChain)):
            distancia += RMRigTools.RMPointDistance(BoneChain[index - 1], BoneChain[index])
        return distancia

    def create(self, ik_start=0, ik_end=None):
        if not self.joints:
            self.build_joints()
        self.IKCreate(ik_start=ik_start, ik_end=ik_end)
        self.create_pole_vector()
        self.structure()

    def structure(self):
        self.root_joints.setParent(self.rig_structure.joints)
        self.root_controls = pm.group(empty=True, name='ikControls')
        print self.root_controls
        self.name_conv.rename_name_in_format(self.root_controls, useName=True)

        self.root_kinematics = pm.group(empty=True, name='ikKinematics')
        print self.root_kinematics
        self.name_conv.rename_name_in_format(self.root_kinematics, useName=True)

        #self.ik_handle.setParent(self.root_kinematics)

        for each_kinematics in self.kinematics:
            each_kinematics.setParent(self.root_kinematics)

        for each_control in self.reset_controls:
            self.reset_controls[each_control].setParent(self.root_controls)
        self.root_controls.setParent(self.rig_structure.controls)
        self.root_kinematics.setParent(self.rig_structure.kinematics)

    def IKCreate(self, ik_start=0, ik_end=None):
        if not ik_end:
            ik_end = len(self.joints)-1

        self.reset_controls['ikHandle'], self.controls['ikHandle'] = self.rig_controls.RMCreateBoxCtrl(
            self.joints[ik_end],
            Xratio=.3,
            Yratio=.3,
            Zratio=.3,
            ParentBaseSize=True,
            name="%sIK" % self.name_conv.get_a_short_name(self.joints[ik_end]))
        # self.ikControl = self.name_conv.RMRenameBasedOnBaseName(self.joints[len(self.joints)-1], self.ikControl, NewName = self.name_conv.RMGetAShortName(self.joints[len(self.joints)-1]) + "IK")
        RMRigTools.RMLockAndHideAttributes(self.controls['ikHandle'], "111111000h")

        self.ik_handle, effector = pm.ikHandle(sj=self.joints[ik_start],
                                               ee=self.joints[ik_end],
                                               sol="ikRPsolver", name="LimbIKHandle")
        self.name_conv.rename_based_on_base_name(self.joints[ik_end], self.ik_handle, {})
        self.name_conv.rename_based_on_base_name(self.joints[ik_end], effector, {})

        pm.orientConstraint(self.controls['ikHandle'], self.joints[ik_end])

        point_constraint = pm.pointConstraint(self.controls['ikHandle'], self.ik_handle, name="LimbCntrlHandleConstraint")
        self.name_conv.rename_based_on_base_name(self.joints[ik_end], point_constraint, {})
        self.kinematics.append(self.ik_handle)

        RMRigTools.RMChangeRotateOrder(self.controls['ikHandle'], 'yzx')

    def identify_joints(self, ik_handle):
        endEffector = pm.ikHandle(ik_handle, q=True, endEffector=True)
        EndJoint = RMRigTools.RMCustomPickWalk(endEffector, 'joint', 1, Direction="up")
        EndJoint = RMRigTools.RMCustomPickWalk(EndJoint[len(EndJoint) - 1], 'joint', 1)
        EndJoint = EndJoint[1]
        StartJoint = pm.ikHandle(ik_handle, q=True, startJoint=True)
        return RMRigTools.FindInHieararchy(StartJoint, EndJoint)

    def get_polevector_from_reference_nodes(self, node_list):
        """
        :param node_list: list of 3 nodes where the pole vector will be calculated.  
        :return: a space locator that it is located where the pole vector should be.
        """
        VP1 = om.MVector(pm.xform(node_list[0], a=True, ws=True, q=True, rp=True))
        VP2 = om.MVector(pm.xform(node_list[1], a=True, ws=True, q=True, rp=True))
        VP3 = om.MVector(pm.xform(node_list[2], a=True, ws=True, q=True, rp=True))
        PoleVector = pm.spaceLocator(name="poleVector")
        PoleVector = self.name_conv.rename_based_on_base_name(node_list[1], PoleVector, {'name': PoleVector})
        pm.xform(PoleVector, ws=True, t=self.pole_vector(VP1, VP2, VP3))
        return PoleVector

    def create_pole_vector(self, ik_handle=None):
        if not ik_handle:
            ik_handle = self.ik_handle
        if not self.joints:
            self.joints = self.identify_joints(ik_handle)
        locator = self.get_polevector_from_reference_nodes(self.joints)

        distancia = RMRigTools.RMPointDistance(locator, self.joints[1])

        self.reset_controls['poleVector'], self.controls['poleVector'] = self.rig_controls.RMCreateBoxCtrl(locator,
                                                                                                    customSize=distancia / 5,
                                                                                                    name=self.name_conv.get_a_short_name(
                                                                                                        self.joints[
                                                                                                            1]) + "PoleVectorIK",
                                                                                                    centered=True)
        data_group, curve = self.rig_tools.RMCreateLineBetwenPoints(self.controls['poleVector'], self.joints[1])
        pm.parent(curve, self.controls['poleVector'])
        pm.parentConstraint(self.rig_structure.world, curve)

        pole_vector_cnstraint = pm.poleVectorConstraint(self.controls['poleVector'], ik_handle, name="PoleVector")
        self.name_conv.rename_based_on_base_name(self.controls['poleVector'], pole_vector_cnstraint,
                                                 {'name': pole_vector_cnstraint})
        self.kinematics.append(data_group)
        pm.delete(locator)

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

    def make_stretchy(self, ik_handle=None):
        if not ik_handle:
            ik_handle = self.ik_handle
        if not self.joints:
            self.joints = self.identify_joints(ik_handle)

        totalDistance = self.BoneChainLenght(self.joints)
        transformStartPoint = pm.spaceLocator(name="StretchyIkHandleStartPoint")
        transformStartPoint = self.name_conv.rename_name_in_format(transformStartPoint, useName=True)
        transformEndPoint = pm.spaceLocator(name="StretchyIkHandleEndPoint")
        transformEndPoint = self.name_conv.rename_name_in_format(transformEndPoint, useName=True)

        if self.root_joints:
            pm.parent(transformStartPoint, self.root_joints)
            pm.parent(transformEndPoint, self.root_joints)

        StartPointConstraint = pm.pointConstraint(self.joints[0], transformStartPoint)
        EndPointConstraint = pm.pointConstraint(ik_handle, transformEndPoint)

        distanceNode = pm.shadingNode("distanceBetween", asUtility=True,
                                      name="IKBaseDistanceNode" + self.name_conv.get_a_short_name(self.joints[2]))
        distanceNode = self.name_conv.rename_based_on_base_name(self.joints[2], distanceNode, {'name': distanceNode})

        pm.connectAttr(transformStartPoint + ".worldPosition[0]", distanceNode + ".point1", f=True)
        pm.connectAttr(transformEndPoint + ".worldPosition[0]", distanceNode + ".point2", f=True)

        conditionNode = pm.shadingNode("condition", asUtility=True,
                                       name="IkCondition" + self.name_conv.get_a_short_name(self.joints[2]))
        conditionNode = self.name_conv.rename_based_on_base_name(self.joints[2], conditionNode,
                                                                 {'name': conditionNode})
        pm.connectAttr(distanceNode + ".distance", conditionNode + ".colorIfFalseR", f=True)
        pm.connectAttr(distanceNode + ".distance", conditionNode + ".secondTerm", f=True)
        pm.setAttr(conditionNode + ".operation", 3)
        pm.setAttr(conditionNode + ".firstTerm", totalDistance)
        pm.setAttr(conditionNode + ".colorIfTrueR", totalDistance)
        multiplyDivide = pm.shadingNode("multiplyDivide", asUtility=True,
                                        name="IKStretchMultiply" + self.name_conv.get_a_short_name(
                                            self.joints[2]))
        multiplyDivide = self.name_conv.rename_based_on_base_name(self.joints[2], multiplyDivide,
                                                                  {'name': multiplyDivide})

        pm.connectAttr(conditionNode + ".outColorR", multiplyDivide + ".input1X", f=True)
        pm.setAttr(multiplyDivide + ".input2X", totalDistance)
        pm.setAttr(multiplyDivide + ".operation", 2)

        # self.SPSW.AddEnumParameters(["off","on"], self.ikControl, Name = "StretchyIK")
        self.rig_space_switch.AddNumericParameter(self.controls['ikHandle'], Name="StretchyIK")
        IKSwitchDivide = pm.shadingNode("multiplyDivide", asUtility=True,
                                        name="IkSwitchDivide" + self.name_conv.get_a_short_name(self.joints[2]))
        IKSwitchDivide = self.name_conv.rename_based_on_base_name(self.joints[2], IKSwitchDivide,
                                                                  {'name': IKSwitchDivide})
        pm.connectAttr("%s.StretchyIK" % self.controls['ikHandle'], IKSwitchDivide + ".input1X")
        pm.setAttr(IKSwitchDivide + ".input2X", 10)
        pm.setAttr(IKSwitchDivide + ".operation", 2)

        IkSwitchblendTwoAttr = pm.shadingNode("blendTwoAttr", asUtility=True,
                                              name="IkSwitchBlendTwoAttr" + self.name_conv.get_a_short_name(
                                                  self.joints[2]))
        IkSwitchblendTwoAttr = self.name_conv.rename_based_on_base_name(self.joints[2], IkSwitchblendTwoAttr,
                                                                        {'name': IkSwitchblendTwoAttr})

        pm.connectAttr(multiplyDivide + ".outputX", IkSwitchblendTwoAttr + ".input[1]", force=True)
        pm.setAttr(IkSwitchblendTwoAttr + ".input[0]", 1)
        pm.connectAttr(IKSwitchDivide + ".outputX", IkSwitchblendTwoAttr + ".attributesBlender", force=True)

        for joints in self.joints[:-1]:
            pm.connectAttr(IkSwitchblendTwoAttr + ".output", joints + ".scaleX")


if __name__ == '__main__':
    reload(RMRigTools)
    selection = pm.ls(selection=True)
    ikrig = ik_rig.build_from_guides(selection)
