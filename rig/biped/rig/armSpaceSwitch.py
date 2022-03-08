from RMPY.rig import rigBase
from RMPY.rig.spaceSwitches import rigEnumSpaceSwitch


class ArmSpaceSwitch(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(ArmSpaceSwitch, self).__init__(*args, **kwargs)

    def build(self, arm_rig, world_rig):
        print arm_rig.rig_arm.ik_rig.controls
        enum_space_switch = rigEnumSpaceSwitch.RigEnumSpaceSwitch(world_rig.tip, arm_rig.rig_clavicle.tip,
                                                                  alias_list=['world', 'shoulder'],
                                                                  attribute_name='space',
                                                                  control=arm_rig.rig_arm.ik_rig.controls[0], parent=True)
        enum_space_switch.add_object(arm_rig.rig_arm.ik_rig.reset_controls[0])
