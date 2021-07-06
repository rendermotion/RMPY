import RMPY.rig.rigBase
import RMPY.rig.rigIKFK
import RMPY.rig.rigFK
import pymel.core as pm


class ArmModel(RMPY.rig.rigBase.BaseModel):
    def __init__(self, *args, **kwargs):
        super(ArmModel, self).__init__(*args, **kwargs)
        rig_system = kwargs.pop('rig_system', None)
        self.rig_clavicle = RMPY.rig.rigFK.RigFK(rig_system=rig_system)
        self.rig_arm = RMPY.rig.rigIKFK.RigIkFk(rig_system=rig_system)


class Arm(RMPY.rig.rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(Arm, self).__init__(*args, **kwargs)
        self._model = ArmModel(rig_system=self.rig_system)
        self.reset_joints = []
        self.joints = []
        self.reset_controls = []
        self.controls = []

    @property
    def rig_clavicle(self):
        return self._model.rig_clavicle

    @property
    def rig_arm(self):
        return self._model.rig_arm

    def create_point_base(self, *args, **kwargs):
        self.setup_name_convention_node_base(args[1], name='arm')
        self.update_name_convention()
        self.rig_system.create()
        self.rig_clavicle.create_point_base(*args[:2], name='clavicle')
        self.rig_arm.create_point_base(*args[1:], name='arm')
        self.rig_arm.set_parent(self.rig_clavicle)

        self.reset_joints = self.rig_clavicle.reset_joints + self.rig_arm.reset_joints
        self.joints = self.rig_clavicle.joints + self.rig_arm.joints
        self.reset_controls = self.rig_clavicle.reset_controls + self.rig_arm.reset_controls
        self.controls = self.rig_clavicle.controls + self.rig_arm.controls


if __name__ == '__main__':
    arm_points = pm.ls('L_clavicle01_reference_pnt', 'L_shoulder01_reference_pnt', 'L_elbow01_reference_pnt',
                       'L_wrist01_reference_pnt')
    new_arm = Arm()
    new_arm.create_point_base(*arm_points)
    print 'reset = {}'.format(new_arm.reset_joints)
    print 'Joints = {}'.format(new_arm.joints)










