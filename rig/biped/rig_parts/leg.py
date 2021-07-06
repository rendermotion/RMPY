import pymel.core as pm
from RMPY.rig import rigIK
from RMPY.rig import rigFK
from RMPY.rig import rigBase
from RMPY.rig import rigSingleJoint
from RMPY.rig import constraintSwitch
import RMPY.core.main as rm


class Leg(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(Leg, self).__init__(*args, **kwargs)
        self.ik_rig = None
        self.fk_rig = None
        self.palm = None
        self.ik_fk_switch = None

    def create_point_base(self, *arm_points, **kwargs):
        super(Leg, self).create_point_base(*arm_points, **kwargs)
        self.ik_rig = rigIK.IKRig(rig_system=self.rig_system)
        self.ik_rig.create_point_base(*arm_points[:-1], control_orientation='world',
                                      last_joint_follows_control=False)
        self.fk_rig = rigFK.RigFK(rig_system=self.rig_system)
        self.fk_rig.create_point_base(*arm_points, orient_type='point_orient')
        self.palm = rigSingleJoint.RigSingleJoint(rig_system=self.rig_system)

        self.palm.create_point_base(arm_points[-1], name='palm',  type='box')
        self.ik_fk_switch = constraintSwitch.ConstraintSwitch(rig_system=self.rig_system)
        self.ik_fk_switch.build(self.ik_rig.joints, self.fk_rig.joints, control=self.palm.controls[0],
                                attribute_name='IkFkSwitch')
        for each_control in self.ik_rig.controls:
            self.ik_fk_switch.attribute_output_a >> each_control.visibility

        for each_control in self.fk_rig.controls:
            self.ik_fk_switch.attribute_output_b >> each_control.visibility
        # pm.parentConstraint(self.fk_limb.controls[0], self.ik_limb.reset_controls['poleVector'], mo=True)
        # pm.parentConstraint(self.fk_limb.controls[0], self.ik_limb.reset_controls['ikHandleSecondary'], mo=True)
        pm.parentConstraint(self.fk_rig.controls[0], self.ik_rig.root_joints, mo=True)


if __name__ == '__main__':
    root_arm = pm.ls('L_leg01_reference_pnt')[0]
    leg_points = rm.descendants_list(root_arm)[:4]

    arm_rig = Leg()
    arm_rig.create_point_base(*leg_points)



