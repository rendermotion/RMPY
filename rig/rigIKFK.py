import pymel.core as pm
from RMPY.rig import rigIK
from RMPY.rig import rigFK
from RMPY.rig import rigBase
from RMPY.rig import rigSingleJoint
from RMPY.rig import constraintSwitch


class RigIkFkModel(rigBase.BaseModel):
    def __init__(self):
        super(RigIkFkModel, self).__init__()
        self.ik_rig = None
        self.fk_rig = None
        self.switch_control_rig = None
        self.ik_fk_switch = None


class RigIkFk(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(RigIkFk, self).__init__(*args, **kwargs)
        self._model = RigIkFkModel()
        self.joints = []
        self.reset_joints = []

    @property
    def ik_rig(self):
        if self._model.ik_rig is None:
            self._model.ik_rig = rigIK.IKRig(rig_system=self.rig_system)
        return self._model.ik_rig

    @property
    def fk_rig(self):
        if self._model.fk_rig is None:
            self._model.fk_rig = rigFK.RigFK(rig_system=self.rig_system)
        return self._model.fk_rig

    @property
    def switch_control_rig(self):
        if self._model.switch_control_rig is None:
            self._model.switch_control_rig = rigSingleJoint.RigSingleJoint(rig_system=self.rig_system)
        return self._model.switch_control_rig

    @property
    def ik_fk_switch(self):
        if self._model.ik_fk_switch is None:
            self._model.ik_fk_switch = constraintSwitch.ConstraintSwitch(rig_system=self.rig_system)
        return self._model.ik_fk_switch

    def create_point_base(self, *creation_points, **kwargs):
        super(RigIkFk, self).create_point_base(*creation_points, **kwargs)
        # self.root = self.create.group.point_base(creation_points[0], type='world')
        # self.root.setParent(self.rig_system.kinematics)

        # self.name_convention.rename_name_in_format(self.root, name='mainMover')

        self.ik_rig.create_point_base(*creation_points, control_orientation='world', last_joint_follows_control=False)
        self.ik_rig.make_stretchy()

        self.fk_rig.create_point_base(*creation_points, orient_type='point_orient') # orient_type='point_orient')

        self.switch_control_rig.create_point_base(creation_points[0], name='root', type='box')
        self.root = self.switch_control_rig.root

        self.switch_control_rig.custom_world_align(self.switch_control_rig.reset_controls[0])

        self.ik_fk_switch.build(self.ik_rig.joints[:-1], self.fk_rig.joints[:-1])

        self.ik_fk_switch.build(self.ik_rig.joints[-1:], self.fk_rig.joints[-1:], point=True, parent=False, control=self.switch_control_rig.controls[0],
                                attribute_name='IkFkSwitch')
        # pm.listConnections(self.ik_fk_switch.outputs[-1])
        # self.create.constraint.matrix_node_base(self.fk_rig.root, self.switch_control_rig.tip)
        self.fk_rig.set_parent(self.switch_control_rig)
        # self.create.constraint.matrix_node_base(self.ik_rig.root, self.switch_control_rig.tip)
        self.ik_rig.set_parent(self.switch_control_rig)

        self.attach_points['tip'] = self.ik_fk_switch.outputs[-1]

        for each_token in self.ik_rig.controls_dict:
            self.ik_fk_switch.attribute_output_a >> self.ik_rig.controls_dict[each_token].visibility

        for each_control in self.fk_rig.controls:
            self.ik_fk_switch.attribute_output_b >> each_control.visibility
        # pm.parentConstraint(self.fk_limb.controls[0], self.ik_limb.reset_controls['poleVector'], mo=True)
        # pm.parentConstraint(self.fk_limb.controls[0], self.ik_limb.reset_controls['ikHandleSecondary'], mo=True)
        # pm.parentConstraint(self.fk_rig.controls[0], self.ik_rig.root_joints, mo=True)

        self.joints = self.ik_fk_switch.joints
        self.reset_joints = self.ik_fk_switch.reset_joints


if __name__ == '__main__':
    # root_arm = pm.ls('L_shoulder01_reference_pnt')[0]
    # arm_root_points = rm.descendents_list(root_arm)[:3]
    # arm_rig = RigIkFk()
    # arm_rig.create_point_base(*arm_root_points)
    leg_root_points = ['R_arm01_reference_pnt', 'R_elbow01_reference_pnt',
                       'R_wrist01_reference_pnt']
    leg_rig = RigIkFk()
    leg_rig.create_point_base(*leg_root_points)

    leg_root_points = ['L_arm01_reference_pnt', 'L_elbow01_reference_pnt',
                       'L_wrist01_reference_pnt']
    leg_rig = RigIkFk()
    leg_rig.create_point_base(*leg_root_points)



