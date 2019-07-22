import pymel.core as pm
from RMPY.AutoRig import RMRigFK
from RMPY.rig import rigIK
from RMPY.rig import rigBase
from RMPY.rig import rigSingleJoint
from RMPY.rig import constraintSwitch
import RMPY.core.main as rm
reload(constraintSwitch)
reload(rigIK)
reload(RMRigFK)
reload(rigSingleJoint)


class ShoulderArmRig(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(ShoulderArmRig, self).__init__(*args, **kwargs)
        self.ik_arm = None
        self.fk_arm = None
        self.palm = None
        self.ik_fk_switch = None

    def create_point_base(self, arm_root, **kwargs):
        super(ShoulderArmRig, self).create_point_base(arm_root, **kwargs)
        self.ik_arm = rigIK.IKRig(rig_system=self.rig_system)
        self.ik_arm.create_point_base(*arm_root.getChildren()[1:], control_orientation='world',
                                      last_joint_follows_control=False)
        self.fk_arm = RMRigFK.RMRigFK(rig_system=self.rig_system)
        self.fk_arm.create_point_base(*arm_root.getChildren(), orient_type='point_orient')
        self.palm = rigSingleJoint.SingleJointRig(rig_system=self.rig_system)

        self.palm.create_point_base(arm_root.getChildren()[-1], name='palm',  type='box')
        self.ik_fk_switch = constraintSwitch.ConstraintSwitch(rig_system=self.rig_system)
        self.ik_fk_switch.build(self.ik_arm.joints, self.fk_arm.joints[1:], control=self.palm.controls[0],
                                attribute_name='IkFkSwitch')
        for each_token in self.ik_arm.controls:
            self.ik_fk_switch.attribute_output_a >> self.ik_arm.controls[each_token].visibility
        for each_control in self.fk_arm.controls[1:]:
            self.ik_fk_switch.attribute_output_b >> each_control.visibility
        # pm.parentConstraint(self.fk_limb.controls[0], self.ik_limb.reset_controls['poleVector'], mo=True)
        # pm.parentConstraint(self.fk_limb.controls[0], self.ik_limb.reset_controls['ikHandleSecondary'], mo=True)
        pm.parentConstraint(self.fk_arm.controls[0], self.ik_arm.root_joints, mo=True)


if __name__ == '__main__':
    root_arm = pm.ls('L_shoulder01_rig_pnt')[0]
    arm_points = rm.descendents_list(root_arm)
    arm_rig = ShoulderArmRig()
    arm_rig.create_point_base(pm.ls('L_lowerArm00_reference_GRP')[0])
