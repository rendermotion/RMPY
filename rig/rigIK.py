import pymel.core as pm
from RMPY import RMRigTools
from RMPY.AutoRig import RMSpaceSwitch
from RMPY.rig import rigBase
import RMPY.core.main as rm
from RMPY.rig import rigLineBetweenPoints


class IKRigModel(rigBase.BaseModel):
    def __init__(self, *args, **kwargs):
        super(IKRigModel, self).__init__(*args, **kwargs)
        self.name = ''
        self.guides = []
        self.ik_handle = None
        self.pole_vector_line = None
        self.line_between_points_rig = None

        self.controls_dict = {'poleVector': None, 'ikHandle': None}
        self.reset_controls_dict = {'poleVector': None, 'ikHandle': None}

        self.root_kinematics = None
        self.root_joints = None
        self.root_controls = None

        self.kinematics = []


class IKRig(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(IKRig, self).__init__(*args, **kwargs)
        self._model = IKRigModel()
        self.rig_space_switch = RMSpaceSwitch.RMSpaceSwitch()
        self.guides = None
        self.joints = None
        self.line_between_points_rig = None

    @property
    def controls_dict(self):
        return self._model.controls_dict

    @property
    def reset_controls_dict(self):
        return self._model.reset_controls_dict

    @property
    def line_between_points_rig(self):
        return self._model.line_between_points_rig

    @line_between_points_rig.setter
    def line_between_points_rig(self, value):
        self._model.line_between_points_rig = value

    @property
    def model(self):
        return self._model

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
    def guides(self, guides_list):
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
    def root_controls(self):
        return self._model.root_controls

    @root_controls.setter
    def root_controls(self, rootControl):
        self._model.root_controls = rootControl

    @classmethod
    def build_from_guides(cls, guides):
        new_ik_instance = cls()
        new_ik_instance._model.guides = guides
        new_ik_instance.build_joints()
        return new_ik_instance

    @classmethod
    def build_from_joints(cls, joints):
        new_ik_instance = cls()
        new_ik_instance._model.joints = joints
        return new_ik_instance

    def build_joints(self):
        self.root_joints, self.joints = self.create.joint.point_base(self.guides)

    def BoneChainLenght(self, BoneChain):
        distancia = 0
        for index in range(1, len(BoneChain)):
            distancia += RMRigTools.RMPointDistance(BoneChain[index - 1], BoneChain[index])
        return distancia

    def create_point_base(self, *args, **kwargs):
        self.guides = args
        self.create_using_known()

    def create_using_known(self, ik_start=0, ik_end=None):
        if not self.joints:
            self.build_joints()
        self.IKCreate(ik_start=ik_start, ik_end=ik_end)
        self.create_pole_vector()
        self.structure()

    def structure(self):
        self.root_joints.setParent(self.rig_system.joints)
        self.root_controls = pm.group(empty=True, name='ikControls')
        print self.root_controls
        self.name_convention.rename_name_in_format(self.root_controls, useName=True)

        self.root_kinematics = pm.group(empty=True, name='ikKinematics')
        print self.root_kinematics
        self.name_convention.rename_name_in_format(self.root_kinematics, useName=True)

        # self.ik_handle.setParent(self.root_kinematics)

        for each_kinematics in self.kinematics:
            each_kinematics.setParent(self.root_kinematics)

        for each_control in self.reset_controls_dict:
            self.reset_controls_dict[each_control].setParent(self.root_controls)
        self.root_controls.setParent(self.rig_system.controls)
        self.root_kinematics.setParent(self.rig_system.kinematics)

    def IKCreate(self, ik_start=0, ik_end=None):
        if not ik_end:
            ik_end = len(self.joints)-1

        reset_ikHandle, control_ikHandle = self.create.controls.point_base(
            self.joints[ik_end],
            type='box',
            x_ratio=.3,
            y_ratio=.3,
            z_ratio=.3,
            parent_base_size=True,
            name="%sIK" % self.name_convention.get_a_short_name(self.joints[ik_end]))

        self.reset_controls.append(reset_ikHandle)
        self.controls.append(control_ikHandle)
        self.reset_controls_dict['ikHandle'] = reset_ikHandle
        self.controls_dict['ikHandle'] = control_ikHandle
        # self.ikControl = self.name_convention.RMRenameBasedOnBaseName(self.joints[len(self.joints)-1], self.ikControl,
        # NewName = self.name_convention.RMGetAShortName(self.joints[len(self.joints)-1]) + "IK")
        RMRigTools.RMLockAndHideAttributes(self.controls_dict['ikHandle'], "111111000h")

        self.ik_handle, effector = pm.ikHandle(sj=self.joints[ik_start],
                                               ee=self.joints[ik_end],
                                               sol="ikRPsolver", name="LimbIKHandle")
        self.name_convention.rename_based_on_base_name(self.joints[ik_end], self.ik_handle)
        self.name_convention.rename_based_on_base_name(self.joints[ik_end], effector)

        pm.orientConstraint(self.controls_dict['ikHandle'], self.joints[ik_end])

        point_constraint = pm.pointConstraint(self.controls_dict['ikHandle'], self.ik_handle, name="LimbCntrlHandleConstraint")
        self.name_convention.rename_based_on_base_name(self.joints[ik_end], point_constraint)
        self.kinematics.append(self.ik_handle)
        RMRigTools.RMChangeRotateOrder(self.controls_dict['ikHandle'], 'yzx')

    def identify_joints(self, ik_handle):
        endEffector = pm.ikHandle(ik_handle, q=True, endEffector=True)
        EndJoint = RMRigTools.RMCustomPickWalk(endEffector, 'joint', 1, Direction="up")
        EndJoint = RMRigTools.RMCustomPickWalk(EndJoint[len(EndJoint) - 1], 'joint', 1)
        EndJoint = EndJoint[1]
        StartJoint = pm.ikHandle(ik_handle, q=True, startJoint=True)
        return RMRigTools.FindInHieararchy(StartJoint, EndJoint)

    def create_pole_vector(self, ik_handle=None):
        if not ik_handle:
            ik_handle = self.ik_handle

        if not self.joints:
            self.joints = self.identify_joints(ik_handle)

        locator = self.create.space_locator.pole_vector(*self.joints)
        distance = self.rm.point_distance(locator, self.joints[1])

        reset_controls_pole_vector, controls_pole_vector = \
            self.create.controls.point_base(locator,
                                            type='box',
                                            size=distance / 5,
                                            name=self.name_convention.get_a_short_name(
                                                self.joints[
                                                    1]) + "PoleVectorIK",
                                            centered=True)
        self.reset_controls.append(reset_controls_pole_vector)
        self.controls.append(controls_pole_vector)

        self.reset_controls_dict['poleVector'] = reset_controls_pole_vector
        self.controls_dict['poleVector'] = controls_pole_vector

        self.line_between_points_rig = rigLineBetweenPoints.LineBetweenPoints(rig_system=self.rig_system)
        self.line_between_points_rig.create_point_base(self.controls_dict['poleVector'], self.joints[1])

        self.controls_dict['poleVector'].visibility >> self.line_between_points_rig.curve.visibility
        self.controls_dict['poleVector'].lodVisibility >> self.line_between_points_rig.curve.lodVisibility

        pm.parent(self.line_between_points_rig.curve, self.rig_system.display)

        pole_vector_cnstraint = pm.poleVectorConstraint(self.controls_dict['poleVector'], ik_handle, name="PoleVector")
        self.name_convention.rename_based_on_base_name(self.controls_dict['poleVector'], pole_vector_cnstraint,
                                                       name=pole_vector_cnstraint)

        pm.delete(locator)

    def make_stretchy(self, ik_handle=None):
        if not ik_handle:
            ik_handle = self.ik_handle
        if not self.joints:
            self.joints = self.identify_joints(ik_handle)

        totalDistance = self.BoneChainLenght(self.joints)
        transformStartPoint = pm.spaceLocator(name="StretchyIkHandleStartPoint")
        transformStartPoint = self.name_convention.rename_name_in_format(transformStartPoint, useName=True)
        transformEndPoint = pm.spaceLocator(name="StretchyIkHandleEndPoint")
        transformEndPoint = self.name_convention.rename_name_in_format(transformEndPoint, useName=True)

        if self.root_joints:
            pm.parent(transformStartPoint, self.root_joints)
            pm.parent(transformEndPoint, self.root_joints)

        StartPointConstraint = pm.pointConstraint(self.joints[0], transformStartPoint)
        EndPointConstraint = pm.pointConstraint(ik_handle, transformEndPoint)

        distanceNode = pm.shadingNode("distanceBetween", asUtility=True,
                                      name="IKBaseDistanceNode" + self.name_convention.get_a_short_name(self.joints[2]))
        distanceNode = self.name_convention.rename_based_on_base_name(self.joints[2], distanceNode, name=distanceNode)

        pm.connectAttr(transformStartPoint + ".worldPosition[0]", distanceNode + ".point1", f=True)
        pm.connectAttr(transformEndPoint + ".worldPosition[0]", distanceNode + ".point2", f=True)

        conditionNode = pm.shadingNode("condition", asUtility=True,
                                       name="IkCondition" + self.name_convention.get_a_short_name(self.joints[2]))
        conditionNode = self.name_convention.rename_based_on_base_name(self.joints[2], conditionNode,
                                                                 name= conditionNode)
        pm.connectAttr(distanceNode + ".distance", conditionNode + ".colorIfFalseR", f=True)
        pm.connectAttr(distanceNode + ".distance", conditionNode + ".secondTerm", f=True)
        pm.setAttr(conditionNode + ".operation", 3)
        pm.setAttr(conditionNode + ".firstTerm", totalDistance)
        pm.setAttr(conditionNode + ".colorIfTrueR", totalDistance)
        multiplyDivide = pm.shadingNode("multiplyDivide", asUtility=True,
                                        name="IKStretchMultiply" + self.name_convention.get_a_short_name(
                                            self.joints[2]))
        multiplyDivide = self.name_convention.rename_based_on_base_name(self.joints[2], multiplyDivide,
                                                                        name=multiplyDivide)

        pm.connectAttr(conditionNode + ".outColorR", multiplyDivide + ".input1X", f=True)
        pm.setAttr(multiplyDivide + ".input2X", totalDistance)
        pm.setAttr(multiplyDivide + ".operation", 2)

        # self.SPSW.AddEnumParameters(["off","on"], self.ikControl, Name = "StretchyIK")
        self.rig_space_switch.AddNumericParameter(self.controls_dict['ikHandle'], Name="StretchyIK")
        IKSwitchDivide = pm.shadingNode("multiplyDivide", asUtility=True,
                                        name="IkSwitchDivide" + self.name_convention.get_a_short_name(self.joints[2]))
        IKSwitchDivide = self.name_convention.rename_based_on_base_name(self.joints[2], IKSwitchDivide,
                                                                  name=IKSwitchDivide)
        pm.connectAttr("%s.StretchyIK" % self.controls_dict['ikHandle'], IKSwitchDivide + ".input1X")
        pm.setAttr(IKSwitchDivide + ".input2X", 10)
        pm.setAttr(IKSwitchDivide + ".operation", 2)

        IkSwitchblendTwoAttr = pm.shadingNode("blendTwoAttr", asUtility=True,
                                              name="IkSwitchBlendTwoAttr" + self.name_convention.get_a_short_name(
                                                  self.joints[2]))
        IkSwitchblendTwoAttr = self.name_convention.rename_based_on_base_name(self.joints[2], IkSwitchblendTwoAttr,
                                                                              name=IkSwitchblendTwoAttr)

        pm.connectAttr(multiplyDivide + ".outputX", IkSwitchblendTwoAttr + ".input[1]", force=True)
        pm.setAttr(IkSwitchblendTwoAttr + ".input[0]", 1)
        pm.connectAttr(IKSwitchDivide + ".outputX", IkSwitchblendTwoAttr + ".attributesBlender", force=True)

        for joints in self.joints[:-1]:
            pm.connectAttr(IkSwitchblendTwoAttr + ".output", joints + ".scaleX")


if __name__ == '__main__':

    root = pm.ls('L_shoulder01_rig_pnt')[0]
    root_arm = pm.ls('L_shoulder01_rig_pnt')[0]
    arm_points = rm.descendents_list(root_arm)
    ik_rig = IKRig()
    ik_rig.create_point_base(*arm_points[:3])
    print 'done'

