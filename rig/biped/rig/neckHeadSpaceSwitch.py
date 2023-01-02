from RMPY.rig import rigBase
from RMPY.rig.spaceSwitches import rigEnumSpaceSwitch


class NeckHeadSpaceSwitch(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(NeckHeadSpaceSwitch, self).__init__(*args, **kwargs)

    def build(self, neck_head_rig, world_rig, cog_rig):
        enum_space_switch = rigEnumSpaceSwitch.RigEnumSpaceSwitch(neck_head_rig.controls[0], world_rig.tip,
                                                                  cog_rig.joints[-1],
                                                                  alias_list=['neck', 'world', 'hip'],
                                                                  attribute_name='space',
                                                                  control=neck_head_rig.controls[1],
                                                                  orient=True, rig_system=neck_head_rig.rig_system)
        enum_space_switch.add_object(neck_head_rig.controls[1], mo=True)

