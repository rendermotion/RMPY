from RMPY.rig import rigBase
from RMPY.rig.spaceSwitches import rigEnumSpaceSwitch


class FrontLegSpaceSwitch(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(FrontLegSpaceSwitch, self).__init__(*args, **kwargs)

    def build(self, front_leg, world_rig):
        enum_space_switch = rigEnumSpaceSwitch.RigEnumSpaceSwitch(world_rig.tip, front_leg.shoulder.tip,
                                                                  alias_list=['world', 'shoulder'],
                                                                  attribute_name='space',
                                                                  control=front_leg.leg.leg.controls_dict['ikHandle'],
                                                                  parent=True)
        enum_space_switch.add_object(front_leg.leg.leg.controls_dict['ikHandle'], mo=True)