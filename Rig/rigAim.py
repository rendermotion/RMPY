import pymel.core as pm
from RMPY.rig import rigBase
from RMPY.core import config


class AimRigModel(rigBase.BaseModel):
    def __init__(self):
        super(AimRigModel, self).__init__()
        self.aim = None


class RigAim(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(RigAim, self).__init__(*args, **kwargs)
        self._model = AimRigModel()
        self.tip = None
        self.aim = None

    @property
    def aim(self):
        return self._model.aim

    @aim.setter
    def aim(self, value):
        self._model.aim = value

    def create_point_base(self, point, **kwargs):
        super(RigAim, self).create_point_base(point, **kwargs)
        root = self.create.group.point_base(point, type='world', name='root')
        aim = pm.duplicate(root)[0]
        self.name_convention.rename_name_in_format(aim, name='aim')

        pm.move(aim, 10, **{'move{}'.format(config.axis_order[0].upper()): True, 'objectSpace': True, 'relative': True})
        aim.setParent(self.rig_system.kinematics)
        root.setParent(self.rig_system.kinematics)
        reset = self.create.group.point_base(root, type='inserted', name='reset')

        self.tip = reset
        self.aim = root

        reset_control, control = self.create.controls.point_base(aim, name='aim')
        reset_control.setParent(self.rig_system.controls)
        parent = kwargs.pop('parent', control)
        aim_vector = [0, 0, 0]
        aim_vector[config.axis_order[0]] = 1
        up_vector = [0, 0, 0]
        up_vector[config.axis_order[1]] = 1
        self.create.constraint.point(point, reset, mo=True)
        pm.aimConstraint(aim, root, aimVector=aim_vector, worldUpType='objectrotation',
                         upVector=up_vector, worldUpObject=parent, worldUpVector=[0, 1, 0])
        self.rm.align(root, reset_control, translate=False)
        pm.parentConstraint(control, aim)
        self.reset_controls.append(reset_control)
        self.controls.append(control)


if __name__ == '__main__':
    head_aim = RigAim()
    head_aim.create_point_base('C_head_reference_pnt')
