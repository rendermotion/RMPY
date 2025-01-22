import pymel.core as pm
from RMPY.rig import rigIK
from RMPY.rig import rigFK
from RMPY.rig import rigBase
from RMPY.rig import rigSingleJoint
from RMPY.rig import constraintSwitch
import RMPY.core.rig_core as rm
import maya.api.OpenMaya as om

class Leg(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(Leg, self).__init__(*args, **kwargs)
        self.ik_rig = None
        self.fk_rig = None
        self.palm = None
        self.ik_fk_switch = None

    def create_point_base(self, *args, **kwargs):
        super(Leg, self).create_point_base(*args, **kwargs)

        align_args = []
        for each in args:
            align_args.append(self.create.space_locator.node_base(each)[0])
            self.name_convention.rename_name_in_format(align_args[-1], name=self.name_convention.get_a_short_name(each),
                                                       system='reference')
        arm_position_vector = om.MVector(pm.xform(align_args[0], q=True, ws=True, rp=True))
        elbow_position_vector = om.MVector(pm.xform(align_args[1], q=True, ws=True, rp=True))
        wrist_position_vector = om.MVector(pm.xform(align_args[2], q=True, ws=True, rp=True))
        args = align_args
        up_vector = (arm_position_vector - elbow_position_vector) ^ (arm_position_vector - wrist_position_vector)
        for index, each in enumerate(args[1:-2]):
            self.transform.aim_point_based(each, each, args[index + 2],
                                           use_vector_as_up_axis=(up_vector.x, up_vector.y, up_vector.z))
        pm.matchTransform(args[-2], args[-3], rotation=True, position=False, scale=False)

        self.ik_rig = rigIK.IKRig(rig_system=self.rig_system)
        self.ik_rig.create_point_base(*args[:-1], control_orientation='world',
                                      last_joint_follows_control=False)
        self.fk_rig = rigFK.RigFK(rig_system=self.rig_system)
        self.fk_rig.create_point_base(*args, orient_type='point_orient')
        self.palm = rigSingleJoint.RigSingleJoint(rig_system=self.rig_system)

        self.palm.create_point_base(args[-1], name='palm', type='box')
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
    leg_points = rm.descendents_list(root_arm)[:4]

    arm_rig = Leg()
    arm_rig.create_point_base(*leg_points)



