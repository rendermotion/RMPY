from RMPY.rig import rigBase
from RMPY.rig import rigIKFK
import RMPY.rig.rigFK
import pymel.core as pm
from RMPY.rig.biped.rig import rigRibonTwistJoint
import maya.api.OpenMaya as om


class ArmModel(rigBase.BaseModel):
    def __init__(self, *args, **kwargs):
        super(ArmModel, self).__init__(*args, **kwargs)
        self.rig_clavicle = None
        self.rig_arm = None
        self.twist_arm = None
        self.twist_forearm = None


class Arm(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', ArmModel())
        super(Arm, self).__init__(*args, **kwargs)
        self._model.rig_clavicle = RMPY.rig.rigFK.RigFK(rig_system=self.rig_system)
        self._model.rig_arm = rigIKFK.RigIkFk(rig_system=self.rig_system)
        self._model.twist_arm = rigRibonTwistJoint.RibbonTwistJoint(rig_system=self.rig_system)
        self._model.twist_forearm = rigRibonTwistJoint.RibbonTwistJoint(rig_system=self.rig_system)

    @property
    def rig_clavicle(self):
        return self._model.rig_clavicle

    @property
    def rig_arm(self):
        return self._model.rig_arm

    @property
    def twist_arm(self):
        return self._model.twist_arm

    @property
    def twist_forearm(self):
        return self._model.twist_forearm

    def create_point_base(self, *args, **kwargs):
        super(Arm, self).create_point_base(*args, **kwargs)
        align_args = []
        best_guess_point_orientation = kwargs.pop('best_guess_point_orientation', True)
        if best_guess_point_orientation:
            for each in args:
                align_args.append(self.create.space_locator.node_base(each)[0])
                self.name_convention.rename_name_in_format(align_args[-1], name=self.name_convention.get_a_short_name(each),
                                                           system='reference')
            arm_position_vector = om.MVector(pm.xform(align_args[1], q=True, ws=True, rp=True))
            elbow_position_vector = om.MVector(pm.xform(align_args[2], q=True, ws=True, rp=True))
            wrist_position_vector = om.MVector(pm.xform(align_args[3], q=True, ws=True, rp=True))
            args = align_args
            up_vector = (arm_position_vector - elbow_position_vector) ^ (arm_position_vector - wrist_position_vector)*-1
            for index, each in enumerate(args[1:-1]):
                self.transform.aim_point_based(each, each, args[index + 2],
                                               use_vector_as_up_axis=(up_vector.x, up_vector.y, up_vector.z),
                                               up_axis='z')
            pm.matchTransform(args[-1], args[-2], rotation=True, position=False, scale=False)

        self.setup_name_convention_node_base(args[1], name='arm', system='arm')
        self.update_name_convention()
        self.rig_system.create()
        self.rig_clavicle.create_point_base(*args[:2], name='clavicle')
        self.rig_arm.create_point_base(*args[1:], name='arm')
        self.rig_arm.set_parent(self.rig_clavicle)
        self.reset_controls = self.rig_clavicle.reset_controls + self.rig_arm.reset_controls
        self.controls = self.rig_clavicle.controls + self.rig_arm.controls

        self.twist_arm.create_point_base(self.rig_clavicle.joints[0], self.rig_arm.joints[0], self.rig_arm.joints[1],
                                         folicule_number=5, system='upperArm', root_transform = self.root)
        self.twist_forearm.create_point_base(self.rig_arm.joints[1], self.rig_arm.joints[1], self.rig_arm.joints[2],
                                             folicule_number=5, system='forearm', root_transform = self.root)

        self.reset_joints = [self.rig_clavicle.reset_joints[0]] + self.twist_arm.reset_joints + self.twist_forearm.reset_joints
        self.joints.extend([self.rig_clavicle.joints[0]])
        self.joints.extend(self.twist_arm.joints)
        self.joints.extend(self.twist_forearm.joints)

        self.attach_points['tip'] = self.rig_arm.tip
        pm.delete(align_args)


if __name__ == '__main__':
    arm_points = pm.ls([each.format('R') for each in ['{}_clavicle01_reference_pnt', '{}_arm01_reference_pnt', '{}_elbow01_reference_pnt',
                       '{}_wrist01_reference_pnt']])
    new_arm = Arm()
    new_arm.create_point_base(*arm_points)










