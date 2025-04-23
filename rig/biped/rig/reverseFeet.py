import pymel.core as pm
from RMPY.rig import rigBase
from RMPY.rig import rigAttributeSplit
from RMPY.rig import rigSimpleIk


class ReverseFeetModel(rigBase.BaseModel):
    def __init__(self):
        super(ReverseFeetModel, self).__init__()
        self.control = None
        self.kinematics_control = None


class RigReverseFeet(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(RigReverseFeet, self).__init__(*args, **kwargs)
        self._model = ReverseFeetModel()
        self.ball_rotation = None
        self.tip_rotation = None
        self.tap_rotation = None
        self.pole_vector = None
        self.dwn_fk_locators = None
        self.up_fk_locators = None
        self.dwn_ik = None
        self.up_ik = None

        self.tap_pnt = None
        self.in_pnt = None
        self.out_pnt = None

        self.reference_points = None
        self.reference_tap = None
        self.reference_in = None
        self.reference_out = None

        self.root = None
        self.reset_joints = None
        self.joints = []
        self.attach_points['attachment_ik_leg'] = None

    @property
    def control(self):
        if not self._model.control:
            reset, self._model.control = self.create.controls.point_base(self.reference_tap)
            self.reset_controls.append(reset)
            self.controls.append(self._model.control)
            reset.setParent(self.rig_system.controls)
        return self._model.control

    @control.setter
    def control(self, value):
        self._model.control = value

    @property
    def attachment_ik_leg(self):
        return self.attach_points['attachment_ik_leg']

    @property
    def kinematics_control(self):
        if not self._model.kinematics_control:
            self._model.kinematics_control = pm.group(empty=True)
            self.name_convention.rename_name_in_format(self._model.kinematics_control, name='kinematicsControl')
            self.controls.append(self._model.kinematics_control)
            self._model.kinematics_control.setParent(self.rig_system.kinematics)
        return self._model.kinematics_control

    def create_point_base(self, *points, **kwargs):
        super(RigReverseFeet, self).create_point_base(*points)
        self.create_hierarchy(*points)
        self.set_up_tip_tap_control()
        self.set_up_roll_in_out_control()
        self.setup_outputs()

    def create_hierarchy(self, *points):
        self.reference_points = points[:3]
        self.reference_tap = points[3]
        self.reference_in = points[4]
        self.reference_out = points[5]

        reset_downstream, down_stream_joints = self.create.joint.point_base(*self.reference_points[1:],
                                                                            orient_type='point_orient')
        reset_upstream, up_stream_joints = self.create.joint.point_base(*reversed(self.reference_points[:-1]),
                                                                        orient_type='point_orient')
        self.pole_vector = self.create.space_locator.pole_vector(*self.reference_points)

        self.dwn_ik = rigSimpleIk.SimpleIK(rig_system=self.rig_system)
        self.dwn_ik.create_node_base(*down_stream_joints)
        self.dwn_ik.set_as_pole_vector(self.pole_vector)
        self.dwn_ik.joints = down_stream_joints
        self.dwn_ik.reset_joints = reset_downstream

        self.up_ik = rigSimpleIk.SimpleIK(rig_system=self.rig_system)
        self.up_ik.create_node_base(*up_stream_joints)
        self.up_ik.set_as_pole_vector(self.pole_vector)
        self.up_ik.joints = up_stream_joints
        self.up_ik.reset_joints = reset_upstream

        self.dwn_fk_locators = self.create.space_locator.node_base(*self.reference_points, name='dwnFK')
        self.up_fk_locators = self.create.space_locator.node_base(*reversed(self.reference_points), name='upFK')

        self.tap_pnt = self.create.space_locator.node_base(self.reference_tap, name='tap')[0]
        self.in_pnt = self.create.space_locator.node_base(self.reference_in, name='inBank')[0]
        self.out_pnt = self.create.space_locator.node_base(self.reference_out, name='outBank')[0]

        self.rm.reorder_hierarchy(self.tap_pnt, self.in_pnt, self.out_pnt)

        self.rm.reorder_hierarchy(*self.dwn_fk_locators)
        self.rm.reorder_hierarchy(*self.up_fk_locators)

        self.up_fk_locators[0].setParent(self.dwn_fk_locators[0])
        # parent the main hierarchy to thje out_pnt rotation hieararchy
        self.dwn_fk_locators[0].setParent(self.out_pnt)

        reset_upstream.setParent(self.up_fk_locators[1])
        reset_downstream.setParent(self.up_fk_locators[1])

        self.up_ik.ik_handle.setParent(self.up_fk_locators[2])
        self.dwn_ik.ik_handle.setParent(self.dwn_fk_locators[2])

        # so far the rig is created, but now we need a reset node for the main nodes that will control.
        self.root = self.create.group.point_base(self.tap_pnt, name='root')
        self.create.group.point_base(*self.dwn_fk_locators[0:2])

        self.root.setParent(self.rig_system.kinematics)
        self.create.group.point_base(*self.up_fk_locators[0:2])
        # and a pole vector for the Ik
        self.ball_rotation = self.up_fk_locators[1]
        self.tip_rotation = self.up_fk_locators[0]
        self.tap_rotation = self.create.group.point_base(self.tap_pnt, name='tap')
        pm.parent(self.pole_vector, self.dwn_fk_locators[0])

    def set_up_tip_tap_control(self):
        pm.addAttr(self.rig_system.settings, ln='toe_break', at='double', k=True)
        self.rig_system.settings.toe_break.set(25)
        pm.addAttr(self.rig_system.settings, ln='tap_break', at='double', k=True)
        self.rig_system.settings.tap_break.set(0)
        pm.addAttr(self.rig_system.settings, ln='ball', at='double', k=True)
        pm.addAttr(self.rig_system.settings, ln='tap', at='double', k=True)
        pm.addAttr(self.rig_system.settings, ln='tip', at='double', k=True)
        pm.addAttr(self.rig_system.settings, ln='tipRotation', at='double', k=True)
        pm.addAttr(self.rig_system.settings, ln='tipUpDown', at='double', k=True)
        pm.addAttr(self.rig_system.settings, ln='tipSides', at='double', k=True)

        self.rig_system.settings.tipUpDown >> self.dwn_fk_locators[1].rotateZ
        self.rig_system.settings.tipSides >> self.dwn_fk_locators[1].rotateY

        split_ball = rigAttributeSplit.AttributeSplit(rig_system=self.rig_system)
        split_ball.create_attributes_based(self.rig_system.settings.ball, self.rig_system.settings.toe_break)
        # split_ball.output_attribute_a >> self.ball_rotation.rotateZ
        self.tip_rotation.rotateOrder.set(3)  # xzy
        split_ball.output_attribute_b >> self.tip_rotation.rotateZ

        self.rig_system.settings.tipRotation >> self.tip_rotation.rotateY

        unit_conversion_tip = pm.listConnections(self.tip_rotation.rotateZ)[0]
        self.create.connect.attributes(self.rig_system.settings.tip, unit_conversion_tip.input)
        unit_conversion_tip.conversionFactor.set(unit_conversion_tip.conversionFactor.get()*-1)

        split_tap = rigAttributeSplit.AttributeSplit(rig_system=self.rig_system)
        split_tap.create_attributes_based(split_ball.output_attribute_a, self.rig_system.settings.tap_break)
        split_tap.output_attribute_a >> self.tap_rotation.rotateZ
        tap_conversion = pm.listConnections(self.tap_rotation.rotateZ)[0]
        tap_conversion.conversionFactor.set(tap_conversion.conversionFactor.get() * -1)
        addition_node = pm.ls(self.create.connect.attributes(self.rig_system.settings.tap, tap_conversion.input))[0]
        addition_node.operation.set(2)
        split_tap.output_attribute_b >> self.ball_rotation.rotateZ
        ball_conversion = pm.listConnections(self.ball_rotation.rotateZ)[0]
        ball_conversion.conversionFactor.set(ball_conversion.conversionFactor.get()*-1)

    def set_up_roll_in_out_control(self):
        pm.addAttr(self.rig_system.settings, ln='in_out_break', at='double', k=True)
        self.rig_system.settings.in_out_break.set(0)
        pm.addAttr(self.rig_system.settings, ln='in_out', at='double', k=True)

        split_in_out = rigAttributeSplit.AttributeSplit(rig_system=self.rig_system)
        split_in_out.create_attributes_based(self.rig_system.settings.in_out, self.rig_system.settings.in_out_break)

        if self.name_convention.get_from_name(self.rig_system.settings, 'side') == 'R':
            self.create.connect.times_factor(split_in_out.output_attribute_a, self.in_pnt.rotateX, -0.01745329)
            self.create.connect.times_factor(split_in_out.output_attribute_b, self.out_pnt.rotateX, -0.01745329)
        else:
            split_in_out.output_attribute_a >> self.in_pnt.rotateX
            split_in_out.output_attribute_b >> self.out_pnt.rotateX

    def setup_outputs(self):
        reset_joints, joints = self.create.joint.point_base(self.reference_points, name='ikInPlace',
                                                            orient_type='point_orient')
        output_reset_joints, output_joints = self.create.joint.point_base(self.reference_points, name='IKOutput',
                                                                          orient_type='point_orient')
        self.reset_joints = output_reset_joints
        self.joints = output_joints
        self.attach_points['attachment_ik_leg'] = self.reset_joints
        reset_joints.setParent(self.rig_system.joints)
        self.reset_joints.setParent(self.rig_system.joints)
        for each_joint, each_driver, output_joint in zip(joints, [self.up_ik.joints[1]] + self.dwn_ik.joints, self.joints):
            pm.parentConstraint(each_driver, each_joint, mo=True)
            pm.orientConstraint(each_joint, output_joint, mo=True)

        self.control.addAttr('toe_break', proxy=str(self.rig_system.settings.toe_break))
        self.control.addAttr('tip', proxy=str(self.rig_system.settings.tip))
        self.control.addAttr('tipRotation', proxy=str(self.rig_system.settings.tipRotation))
        self.control.addAttr('tap', proxy=str(self.rig_system.settings.tap))
        self.control.addAttr('tipUpDown', proxy=str(self.rig_system.settings.tipUpDown))
        self.control.addAttr('tipSides', proxy=str(self.rig_system.settings.tipSides))

        self.rm.lock_and_hide_attributes(self.control, bit_string='000111000h')

        self.control.rotateX >> self.rig_system.settings.in_out
        self.create.connect.times_factor(self.control.rotateZ, self.rig_system.settings.ball, -57.296)
        self.control.rotateY >> self.rig_system.settings.tipRotation


if __name__ == '__main__':
    reference_root = pm.ls(u'L_ankleFeet01_reference_pnt', u'L_ball01_reference_pnt', u'L_toe01_reference_pnt',
                           u'L_footLimitBack01_reference_pnt', u'L_footLimitOuter01_reference_pnt',
                           u'L_footLimitInner01_reference_pnt')
    quad_points = [u'{}_frontPaw00_reference_pnt', u'{}_frontPawRoll00_reference_pnt',
                   u'{}_frontPawToe00_reference_pnt', u'{}_frontFootLimitBack00_reference_pnt',
                   u'{}_frontFootLimitOuter00_reference_pnt',
                   u'{}_frontFootLimitInner00_reference_pnt']

    reference_points_quadruped = pm.ls([each.format('L') for each in quad_points])

    reverse_feet = RigReverseFeet()
    reverse_feet.create_point_base(*reference_root)
    '''
    split = AttributeSplit()
    test_node = pm.ls('L_tap00_reference_CTRL')[0]
    
    split.create_attributes_based(test_node.ball, test_node.tip, test_node.toe_break)
    '''