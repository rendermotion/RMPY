import pymel.core as pm
from RMPY.rig import rigBase
from RMPY.core import config


class AimRigModel(rigBase.BaseModel):
    def __init__(self):
        super(AimRigModel, self).__init__()
        self.aim = None


class RigAim(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', AimRigModel())
        super(RigAim, self).__init__(*args, **kwargs)
        self.tip = None
        self.aim = None
        self.root = None

    @property
    def aim(self):
        return self._model.aim

    @aim.setter
    def aim(self, value):
        self._model.aim = value

    def create_point_base(self, point, **kwargs):
        super(RigAim, self).create_point_base(point, **kwargs)
        create_joint = kwargs.pop('create_joint', True)
        aim = self.create.group.point_base(point, type='world', name='root')
        target = pm.duplicate(aim)[0]
        self.name_convention.rename_name_in_format(aim, name='aim')
        self.name_convention.rename_name_in_format(target, name='target')

        pm.move(target, 10, **{'move{}'.format(config.axis_order[0].upper()): True, 'objectSpace': True, 'relative': True})
        target.setParent(self.rig_system.kinematics)
        aim.setParent(self.rig_system.kinematics)
        self.root = self.create.group.point_base(aim, type='inserted', name='reset')

        # self.tip = self.root
        self.aim = aim

        reset_control, control = self.create.controls.point_base(target, name='aim')
        reset_control.setParent(self.rig_system.controls)
        world_up_object = kwargs.pop('world_up_object', control)

        aim_vector = [0, 0, 0]
        aim_vector[config.axis_order_index[0]] = 1
        up_vector = [0, 0, 0]
        up_vector[config.axis_order_index[1]] = 1

        pm.aimConstraint(target, aim, aimVector=aim_vector, worldUpType='objectrotation',
                         upVector=up_vector, worldUpObject=world_up_object, worldUpVector=[0, 1, 0])
        self.rm.align(aim, reset_control, translate=False)
        if create_joint:
            reset_joints, new_joints_list = self.create.joint.point_base(self.aim)
            self.create.constraint.node_base(self.aim, new_joints_list[0], mo=True)
            reset_joints.setParent(self.rig_system.joints)
            self.reset_joints.extend(reset_joints)
            self.joints.extend(new_joints_list)

        self.create.constraint.node_base(control, target, mo=True)
        self.reset_controls.append(reset_control)
        self.controls.append(control)


if __name__ == '__main__':
    head_aim = RigAim()
    head_aim.create_point_base('R_eye_reference_pnt')
