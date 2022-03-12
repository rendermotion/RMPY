from RMPY.rig import rigBase
from RMPY.rig.spaceSwitches import rigEnumSpaceSwitch


class NeckHeadSpaceSwitch(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(NeckHeadSpaceSwitch, self).__init__(*args, **kwargs)

    def build(self, rig_neck_head, spine_rig, world_rig):
        print world_rig.tip, rig_neck_head.controls[-2]
        head_enum_space_switch = rigEnumSpaceSwitch.RigEnumSpaceSwitch(world_rig.tip, rig_neck_head.controls[-2],
                                                                       alias_list=['world', 'neck'],
                                                                       attribute_name='headSpace',
                                                                       control=rig_neck_head.head.controls[0],
                                                                       parent=False,
                                                                       orient=True)

        head_enum_space_switch.add_object(rig_neck_head.head.controls[0],  mo=True)

        neck_enum_space_switch = rigEnumSpaceSwitch.RigEnumSpaceSwitch(world_rig.tip, spine_rig.tip,
                                                                       spine_rig.chest.controls[0],
                                                                       alias_list=['world', 'spine', 'chestControl'],
                                                                       attribute_name='neckSpace',
                                                                       control=rig_neck_head.controls[0],
                                                                       parent=False,
                                                                       orient=True)

        neck_enum_space_switch.add_object(rig_neck_head.controls[0],  mo=True)



