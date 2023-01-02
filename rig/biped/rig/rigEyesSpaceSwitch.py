from RMPY.rig.spaceSwitches import rigFloatSpaceSwitch
from RMPY.rig import rigBase


class EyeSpaceSwitch(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(EyeSpaceSwitch, self).__init__(*args, **kwargs)

    def build(self, eye_rig,  head_rig, world_rig):

        enum_space_switch = rigFloatSpaceSwitch.RigFloatSpaceSwitch(world_rig.tip, head_rig.tip,
                                                                    attribute_name='worldHead',
                                                                    control=eye_rig.controls[0],
                                                                    parent=True, rig_system=eye_rig.rig_system)
        reset_control = self.create.group.point_base(eye_rig.controls[0], name='resetSpaceSwitch')
        enum_space_switch.add_object(reset_control, mo=True)



