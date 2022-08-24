from RMPY.rig import rigFK
from RMPY.rig import rigBase
from RMPY.rig import rigFollowPosition
import pymel.core as pm


class RigForwardBackwardFKSpineModel(rigBase.BaseModel):
    def __init__(self):
        super(RigForwardBackwardFKSpineModel, self).__init__()
        self.rig_forward_fk = None
        self.rig_backward_fk = None


class RigForwardBackwardFKSpine(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', RigForwardBackwardFKSpineModel())
        super(RigForwardBackwardFKSpine, self).__init__(*args, **kwargs)
        self._model.rig_forward_fk = rigFK.RigFK()
        self._model.rig_backward_fk = rigFK.RigFK(rig_system=self.rig_forward_fk.rig_system)

    @property
    def rig_forward_fk(self):
        return self._model.rig_forward_fk

    @property
    def rig_backward_fk(self):
        return self._model.rig_backward_fk

    def create_point_base(self, *args, **kwargs):
        super(RigForwardBackwardFKSpine, self).create_point_base(*args, **kwargs)

        self.rig_forward_fk.create_point_base(*args, name='forwardFK', orient_type='point_orient')
        self.rig_backward_fk.create_point_base(*reversed(args))

        self.rig_backward_fk.reset_controls[0].setParent(self.rig_forward_fk.controls[-1])

        for forward_driver, backward_driven in zip(reversed(self.rig_forward_fk.joints[1:-1]),
                                                   self.rig_backward_fk.reset_controls[1:]):
            self_follow_position = rigFollowPosition.FollowPosition()
            self_follow_position.build(backward_driven, forward_driver)

        self.joints.extend(reversed(self.rig_backward_fk.joints))


if __name__ == '__main__':
    spine_root = pm.ls('*Spine*', type='transform')
    print spine_root
    fk_spine = RigForwardBackwardFKSpine()
    fk_spine.create_point_base(*spine_root)
    fk_spine.rename_as_skinned_joints(nub=False)



