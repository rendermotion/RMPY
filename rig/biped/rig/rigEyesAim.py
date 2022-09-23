from RMPY.rig import rigAim
from RMPY.rig import rigBase
from RMPY.core import config
import pymel.core.datatypes as dataTypes
import pymel.core as pm
reload(rigAim)

class EyesAimModel(rigBase.BaseModel):
    def __init__(self):
        super(EyesAimModel, self).__init__()
        self.l_eye = None
        self.r_eye = None


class RigEyesAim(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', RigEyesAim)
        super(RigEyesAim, self).__init__()
        self.root = None

    @property
    def l_eye(self):
        return self._model.l_eye

    @property
    def r_eye(self):
        return self._model.r_eye

    def create_point_base(self, *args, **kwargs):
        super(RigEyesAim, self).create_point_base(*args, **kwargs)
        aim_distance = kwargs.pop('aim_distance', 10)
        reference_point_main_eyes = self.create.space_locator.point_base(*args)
        self.name_convention.rename_name_in_format(reference_point_main_eyes,
                                                   side='C',
                                                   name='eyes',
                                                   system='reference')
        axis_aim_a = self.transform.Axis(args[0])
        axis_aim_b = self.transform.Axis(args[1])

        axis_aim_a = getattr(axis_aim_a, (config.axis_order[0]))
        axis_aim_b = getattr(axis_aim_b, (config.axis_order[0]))

        aim_vector = axis_aim_a + axis_aim_b

        self.transform.aim_vector_based(reference_point_main_eyes, dataTypes.Vector(*aim_vector))

        self.root = self.create.group.point_base(reference_point_main_eyes, name='root')
        self.root.setParent(self.rig_system.kinematics)

        pm.move(reference_point_main_eyes, aim_distance, **{'move{}'.format(config.axis_order[0].upper()): True,
                                 'objectSpace': True,
                                 'relative': True})

        reset_controls, controls = self.create.controls.point_base(reference_point_main_eyes)
        pm.parent(reset_controls, self.rig_system.controls)

        self.create.constraint.node_base(self.root, reset_controls, mo=True)
        self.reset_controls.append(reset_controls)
        self.controls.append(controls)

        self._model.l_eye = rigAim.RigAim(rig_system=self.rig_system)
        self.l_eye.create_point_base(args[0])
        self.l_eye.set_parent(self.root)

        self._model.r_eye = rigAim.RigAim(rig_system=self.rig_system)
        self.r_eye.create_point_base(args[1])
        self.r_eye.set_parent(self.root)

        print self.l_eye.reset_controls + self.r_eye.reset_controls
        self.create.constraint.node_base(self.controls[0], *(self.l_eye.reset_controls + self.r_eye.reset_controls), mo=True)
        self.joints.extend(self.l_eye.joints)
        self.joints.extend(self.r_eye.joints)


if __name__ == '__main__':
    rig_eyes = RigEyesAim()
    rig_eyes.create_point_base(u'R_eye_reference_pnt', u'L_eye_reference_pnt', type='circle')
    print rig_eyes.joints



