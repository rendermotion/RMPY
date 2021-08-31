from RMPY.rig import rigBase
from RMPY.rig.spaceSwitches import rigEnumSpaceSwitch


class LegSpaceSwitch(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(LegSpaceSwitch, self).__init__(*args, **kwargs)

    def build(self, leg_rig, world_rig):
        print leg_rig.leg.ik_rig.controls
        enum_space_switch = rigEnumSpaceSwitch.RigEnumSpaceSwitch(world_rig.tip, leg_rig.root,
                                                                  alias_list=['world', 'shoulder'],
                                                                  attribute_name='space',
                                                                  control=leg_rig.leg.ik_rig.controls[0], parent=True)
        enum_space_switch.add_object(leg_rig.leg.ik_rig.reset_controls[0])
