from RMPY.rig import rigBase
from RMPY.rig.spaceSwitches import rigEnumSpaceSwitch
import pymel.core as pm

class HandSpaceSwitch(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(HandSpaceSwitch, self).__init__(*args, **kwargs)

    def build(self, hand_rig, world_rig, arm_rig):
        enum_space_switch = rigEnumSpaceSwitch.RigEnumSpaceSwitch(world_rig.tip, arm_rig.rig_arm.joints[-2],
                                                                  arm_rig.rig_arm.ik_rig.controls_dict['ikHandle'],
                                                                  alias_list=['world', 'arm', 'ik_control'],
                                                                  attribute_name='space',
                                                                  control=hand_rig.controls[0],
                                                                  orient=True, rig_system=hand_rig.rig_system)
        enum_space_switch.add_object(hand_rig.controls[0])
        pm.addAttr(arm_rig.rig_arm.ik_rig.controls_dict['ikHandle'], ln='wristStartOffset', min=0, max=10, k=True)
        anim_blend = pm.createNode('animBlendNodeAdditiveRotation')
        anim_blend.inputA.set(enum_space_switch.space_rigs_dict['ik_control'].tip.rotate.get())
        anim_blend.output >> enum_space_switch.space_rigs_dict['ik_control'].tip.rotate
        self.create.connect.times_factor(arm_rig.rig_arm.ik_rig.controls_dict['ikHandle'].wristStartOffset,  anim_blend.weightA, .1)

        # enum_space_switch.space_rigs_dict['ik_control'].tip.rotate.set(0, 0, 0)




