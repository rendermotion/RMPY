import pymel.core as pm
from RMPY import RMRigTools
from RMPY.AutoRig import RMSpaceSwitch
import RMPY.rig.rigBase
import RMPY.core.rig_core as rm
from RMPY.rig import rigLineBetweenPoints


class IKRigModel(RMPY.rig.rigBase.BaseModel):
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


class IKRig(RMPY.rig.rigBase.RigBase):
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
        self.root_joints, self.joints = self.create.joint.point_base(self.guides, name='ik', orient_type='point_orient')
        # orient_type='point_orient'

    @staticmethod
    def bone_chain_lenght(bone_chain):
        distancia = 0
        for index in range(1, len(bone_chain)):
            distancia += RMRigTools.RMPointDistance(bone_chain[index - 1], bone_chain[index])
        return distancia

    def create_point_base(self, *args, **kwargs):
        super(IKRig, self).create_point_base(*args, **kwargs)
        self.guides = args
        self.create_using_known()

    def create_using_known(self, ik_start=0, ik_end=None):
        if not self.joints:
            self.build_joints()
        self.ik_create(ik_start=ik_start, ik_end=ik_end)
        self.create_pole_vector()
        self.structure()

    def structure(self):
        self.root_joints.setParent(self.rig_system.joints)
        self.root_controls = pm.group(empty=True, name='ikControls')
        self.name_convention.rename_name_in_format(self.root_controls, useName=True)
        self.rm.align(self.joints[0], self.root_controls)
        # self.create.constraint.define_constraints(scale=True, parent=True)
        self.create.constraint.node_base(self.root_controls, self.root_joints, mo=True)
        self.root_kinematics = pm.group(empty=True, name='ikKinematics')
        self.name_convention.rename_name_in_format(self.root_kinematics, useName=True)

        # self.ik_handle.setParent(self.root_kinematics)

        for each_kinematics in self.kinematics:
            each_kinematics.setParent(self.root_kinematics)

        for each_control in self.reset_controls_dict:
            self.reset_controls_dict[each_control].setParent(self.root_controls)
        self.root_controls.setParent(self.rig_system.controls)
        self.attach_points['root'] = self.root_controls
        self.root_kinematics.setParent(self.rig_system.kinematics)

    def ik_create(self, ik_start=0, ik_end=None):
        if not ik_end:
            ik_end = len(self.joints)-1

        reset_ik_handle, control_ik_handle = self.create.controls.point_base(
            self.joints[ik_end],
            type='box',
            x_ratio=.3,
            y_ratio=.3,
            z_ratio=.3,
            parent_base_size=True,
            centered=True,
            name="%sIK" % self.name_convention.get_a_short_name(self.joints[ik_end]))

        self.custom_world_align(reset_ik_handle)
        self.reset_controls.append(reset_ik_handle)
        self.controls.append(control_ik_handle)
        self.reset_controls_dict['ikHandle'] = reset_ik_handle
        self.controls_dict['ikHandle'] = control_ik_handle

        # self.ikControl = self.name_convention.RMRenameBasedOnBaseName(self.joints[len(self.joints)-1], self.ikControl,
        # NewName = self.name_convention.RMGetAShortName(self.joints[len(self.joints)-1]) + "IK")
        RMRigTools.RMLockAndHideAttributes(self.controls_dict['ikHandle'], "111111000h")

        self.ik_handle, effector = pm.ikHandle(sj=self.joints[ik_start],
                                               ee=self.joints[ik_end],
                                               sol="ikRPsolver", name="LimbIKHandle")
        self.name_convention.rename_based_on_base_name(self.joints[ik_end], self.ik_handle)
        self.name_convention.rename_based_on_base_name(self.joints[ik_end], effector)

        # pm.orientConstraint(self.controls_dict['ikHandle'], self.joints[ik_end])

        point_constraint = pm.pointConstraint(self.controls_dict['ikHandle'], self.ik_handle, name="LimbCntrlHandleConstraint")

        self.name_convention.rename_based_on_base_name(self.joints[ik_end], point_constraint)
        self.kinematics.append(self.ik_handle)
        RMRigTools.RMChangeRotateOrder(self.controls_dict['ikHandle'], 'yzx')
        self.custom_world_align(self.reset_controls_dict['ikHandle'])

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

        locator = self.create.space_locator.pole_vector(self.joints[0], self.joints[int(len(self.joints)/2)] ,self.joints[-1])
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
        self.custom_world_align(self.reset_controls_dict['poleVector'])

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

        total_distance = self.bone_chain_lenght(self.joints)
        transform_start_point = pm.spaceLocator(name="StretchyIkHandleStartPoint")
        self.name_convention.rename_name_in_format(transform_start_point, useName=True)
        transform_end_point = pm.spaceLocator(name="StretchyIkHandleEndPoint")
        self.name_convention.rename_name_in_format(transform_end_point, useName=True)

        if self.root_joints:
            pm.parent(transform_start_point, self.root_joints)
            pm.parent(transform_end_point, self.root_joints)

        pm.pointConstraint(self.joints[0], transform_start_point)
        pm.pointConstraint(self.controls[0], transform_end_point)

        distance_node = pm.shadingNode("distanceBetween", asUtility=True, name="IKBaseDistanceNode")

        pm.connectAttr(transform_start_point.worldPosition[0], distance_node.point1, f=True)
        pm.connectAttr(transform_end_point.worldPosition[0], distance_node.point2, f=True)

        condition_node = pm.shadingNode("condition", asUtility=True, name="IkCondition")

        pm.connectAttr(distance_node + ".distance", condition_node + ".colorIfFalseR", f=True)
        pm.connectAttr(distance_node + ".distance", condition_node + ".secondTerm", f=True)
        pm.setAttr(condition_node + ".operation", 3)

        multiply_divide = pm.shadingNode("multiplyDivide", asUtility=True, name="IKStretchMultiply")
        scale_factor = pm.shadingNode("multiplyDivide", asUtility=True, name="scaleFactor")

        pm.addAttr(self.rig_system.settings, ln="scaleA", min=0, k=True,defaultValue = 1)
        pm.addAttr(self.rig_system.settings, ln="scaleB", min=0, k=True, defaultValue = 1)

        multiply_a = pm.createNode('multiply', name='scaleSegmentA')
        multiply_b = pm.createNode('multiply', name='scaleSegmentB')
        constant_a = pm.createNode('floatConstant', name='scaleSegmentA')
        constant_b = pm.createNode('floatConstant', name='scaleSegmentB')

        full_lenght = pm.createNode('sum', name='segmentLength')

        constant_a.inFloat.set(self.joints[1].translateX.get())
        constant_b.inFloat.set(self.joints[2].translateX.get())
        constant_a.outFloat >> multiply_a.input[0]
        self.rig_system.settings.scaleA >> multiply_a.input[1]

        constant_b.outFloat >> multiply_b.input[0]
        self.rig_system.settings.scaleB >> multiply_b.input[1]

        multiply_a.output >> full_lenght.input[0]
        multiply_b.output >> full_lenght.input[1]

        full_lenght.output >> scale_factor.input1X

        # scale_factor.input1X.set(total_distance)
        self.root.scaleX >> scale_factor.input2X
        pm.connectAttr(scale_factor.outputX, condition_node.firstTerm)
        pm.connectAttr(scale_factor.outputX, condition_node.colorIfTrueR)
        self.name_convention.rename_name_in_format(multiply_divide, name='stretchy')

        pm.connectAttr(condition_node + ".outColorR", multiply_divide + ".input1X", f=True)
        pm.connectAttr(scale_factor.outputX, multiply_divide.input2X)
        pm.setAttr(multiply_divide + ".operation", 2)

        # self.SPSW.AddEnumParameters(["off","on"], self.ikControl, Name = "StretchyIK")
        # self.rig_space_switch.AddNumericParameter(self.controls_dict['ikHandle'], Name="StretchyIK")
        pm.addAttr(self.rig_system.settings,  ln="StretchyIK", min=0, max=10, k=True)

        ik_switch_divide = pm.shadingNode("multiplyDivide", asUtility=True,
                                          name="IkSwitchDivide")
        pm.connectAttr(self.rig_system.settings.StretchyIK, ik_switch_divide.input1X)
        pm.setAttr(ik_switch_divide + ".input2X", 10)
        pm.setAttr(ik_switch_divide + ".operation", 2)

        ik_switchblend_two_attr = pm.shadingNode("blendTwoAttr", asUtility=True,
                                                 name="ikSwitchBlendTwoAttr")

        self.name_convention.rename_name_in_format(ik_switch_divide,ik_switchblend_two_attr, scale_factor,
                                                   multiply_divide, condition_node, distance_node, useName=True)
        pm.connectAttr(multiply_divide.outputX, ik_switchblend_two_attr.input[1], force=True)
        ik_switchblend_two_attr.input[0].set(1)
        pm.connectAttr(ik_switch_divide + ".outputX", ik_switchblend_two_attr + ".attributesBlender", force=True)

        multiply_out_a = pm.createNode('multiply', name='scaleOutSegmentA')
        multiply_out_b = pm.createNode('multiply', name='scaleOutSegmentB')

        ik_switchblend_two_attr.output >> multiply_out_a.input[0]
        self.rig_system.settings.scaleA >> multiply_out_a.input[1]
        ik_switchblend_two_attr.output >> multiply_out_b.input[0]
        self.rig_system.settings.scaleB >> multiply_out_b.input[1]

        multiply_out_a.output >> self.joints[0].scaleX
        multiply_out_b.output >> self.joints[1].scaleX
        # for joints in self.joints[:-1]:
        #     pm.connectAttr(ik_switchblend_two_attr.output, joints.scaleX)

        pm.addAttr(self.controls_dict['ikHandle'], ln="StretchyIK", proxy=self.rig_system.settings.StretchyIK)
        pm.addAttr(self.controls_dict['ikHandle'], ln="scaleA", proxy=self.rig_system.settings.scaleA)
        pm.addAttr(self.controls_dict['ikHandle'], ln="scaleB", proxy=self.rig_system.settings.scaleB)


if __name__ == '__main__':
    root_arm = pm.ls('R_arm01_reference_pnt')[0]
    arm_points = rm.descendents_list(root_arm)
    ik_rig = IKRig()
    ik_rig.create_point_base(*arm_points[:3])
    ik_rig.make_stretchy()

