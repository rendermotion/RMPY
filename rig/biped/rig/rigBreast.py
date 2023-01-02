from RMPY.rig import rigAim
from RMPY.rig import rigBase
from RMPY.rig import rigMuscleSpline
from RMPY.core import config
import pymel.core.datatypes as dataTypes
import pymel.core as pm


class BreastModel(rigBase.BaseModel):
    def __init__(self):
        super(BreastModel, self).__init__()
        self.breast_aim = None
        self.dynamic_breast = None


class Breast(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', BreastModel())
        super(Breast, self).__init__(*args, **kwargs)

    @property
    def breast_aim(self):
        return self._model.breast_aim

    @property
    def dynamic_breast(self):
        return self._model.dynamic_breast

    def create_point_base(self, *args, **kwargs):
        super(Breast, self).create_point_base(*args, **kwargs)
        aim_distance = kwargs.pop('aim_distance', 7)
        reference_point_main_eyes = self.create.space_locator.node_base(*args)[0]
        self.rm.align(reference_point_main_eyes, args[0], rotate=True)
        self.attach_points['root'] = self.create.group.point_base(args[0], type='world', name='root')
        self.root.setParent(self.rig_system.kinematics)

        pm.move(reference_point_main_eyes, aim_distance, **{'move{}'.format(config.axis_order[0].upper()): True,
                'objectSpace': True, 'relative': True})
        pm.rotate(reference_point_main_eyes, -90, rotateX=True, objectSpace=True, relative=True)
        front_point = pm.duplicate(reference_point_main_eyes)[0]
        back_point = pm.duplicate(reference_point_main_eyes)[0]

        self.name_convention.rename_name_in_format(back_point, reference_point_main_eyes, front_point,
                                                   name='dynamicBreast',
                                                   system='reference')

        pm.move(front_point, 2, moveY=True, objectSpace=True, relative=True)
        pm.move(back_point, -2, moveY=True, objectSpace=True, relative=True)

        self._model.dynamic_breast = rigMuscleSpline.MuscleSpline()
        self.dynamic_breast.create_point_base(back_point, reference_point_main_eyes, front_point)
        self.dynamic_breast.create_joints_on_curve(1)
        self.dynamic_breast.controls[1].jiggle.set(2)
        self.dynamic_breast.controls[1].jiggleX.set(1)
        self.dynamic_breast.controls[1].jiggleY.set(1)
        self.dynamic_breast.controls[1].jiggleZ.set(1)
        self.dynamic_breast.controls[1].cycle.set(70)
        self.dynamic_breast.controls[1].rest.set(300)

        pm.delete(back_point, reference_point_main_eyes, front_point)
        self._model.breast_aim = rigAim.RigAim(rig_system=self.rig_system)
        self.breast_aim.create_point_base(args[0])
        self.breast_aim.set_parent(self.root)

        self.create.constraint.node_base(self.breast_aim.aim, *self.dynamic_breast.reset_controls, mo=True)

        reset_joint, joint_list = self.create.joint.point_base(self.root)
        reset_joint.setParent(self.rig_system.joints)
        self.create.constraint.node_base(self.root, reset_joint, self.breast_aim.reset_controls[0], mo=True)
        pm.aimConstraint(self.dynamic_breast.tip, joint_list[0], upVector=[0, 1, 0], worldUpObject=self.root,
                         worldUpType='objectrotation',
                         worldUpVector=[0, 1, 0])
        self.joints.extend(joint_list)

        # self.create.constraint.node_base(self.controls[0], *self.breast_aim.reset_controls, mo=True)


if __name__ == '__main__':
    rig_breast = Breast()
    rig_breast.create_point_base('R_breast00_reference_pnt')
    print rig_breast.joints
    rig_breast.rename_as_skinned_joints(nub=False)