from RMPY.rig import rigBase
from RMPY.rig.spaceSwitches import rigEnumSpaceSwitch


class HipSpaceSwitch(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(HipSpaceSwitch, self).__init__(*args, **kwargs)

    def build(self, hip_rig, spine_rig, world_rig):
        enum_space_switch = rigEnumSpaceSwitch.RigEnumSpaceSwitch(world_rig.tip, spine_rig.joints[0],
                                                                  spine_rig.back.controls[0],
                                                                  alias_list=['world', 'spine', 'backControl'],
                                                                  attribute_name='hipSpace',
                                                                  control=hip_rig.controls[0],
                                                                  parent=False, orient=True)

        enum_space_switch.add_object(hip_rig.controls[0], mo=True)