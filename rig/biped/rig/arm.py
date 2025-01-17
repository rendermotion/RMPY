from RMPY.rig import rigBase
from RMPY.rig import rigIKFK
import RMPY.rig.rigFK
import pymel.core as pm
from RMPY.rig.biped.rig import rigRibonTwistJoint


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
        self.setup_name_convention_node_base(args[1], name='arm', system='arm')
        self.update_name_convention()
        self.rig_system.create()
        self.rig_clavicle.create_point_base(*args[:2], name='clavicle')
        self.rig_arm.create_point_base(*args[1:], name='arm')
        self.rig_arm.set_parent(self.rig_clavicle)

        self.twist_arm.create_point_base(self.rig_clavicle.joints[0], self.rig_arm.joints[0], self.rig_arm.joints[1],
                                         folicule_number=5, system='upperArm')
        self.twist_forearm.create_point_base(self.rig_arm.joints[1], self.rig_arm.joints[1], self.rig_arm.joints[2],
                                             folicule_number=5, system='forearm')

        self.reset_joints = [self.rig_clavicle.reset_joints[0]] + self.twist_arm.reset_joints + self.twist_forearm.reset_joints
        self.joints.extend([self.rig_clavicle.joints[0]])
        self.joints.extend(self.twist_arm.joints)
        self.joints.extend(self.twist_forearm.joints)
        self.reset_controls = self.rig_clavicle.reset_controls + self.rig_arm.reset_controls
        self.controls = self.rig_clavicle.controls + self.rig_arm.controls
        self.attach_points['tip'] = self.rig_arm.tip


if __name__ == '__main__':
    arm_points = pm.ls('L_clavicle01_reference_pnt', 'L_arm01_reference_pnt', 'L_elbow01_reference_pnt',
                       'L_wrist01_reference_pnt')
    new_arm = Arm()
    new_arm.create_point_base(*arm_points)
    print ('reset = {}'.format(new_arm.reset_joints))
    print ('Joints = {}'.format(new_arm.joints))










