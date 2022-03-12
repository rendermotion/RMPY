from RMPY.rig import rigBase
from RMPY.rig.spaceSwitches import rigEnumSpaceSwitch


class BackLegSpaceSwitch(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(BackLegSpaceSwitch, self).__init__(*args, **kwargs)

    def build(self, back_leg, world_rig):
        enum_space_switch = rigEnumSpaceSwitch.RigEnumSpaceSwitch(world_rig.tip, back_leg.root,
                                                                  alias_list=['world', 'hip'],
                                                                  attribute_name='space',
                                                                  control=back_leg.leg.controls_dict['ikHandle'],
                                                                  parent=True)
        enum_space_switch.add_object(back_leg.leg.controls_dict['ikHandle'], mo=True)