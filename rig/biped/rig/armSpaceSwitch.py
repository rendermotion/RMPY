from RMPY.rig import rigBase
from RMPY.rig.spaceSwitches import rigEnumSpaceSwitch


class ArmSpaceSwitch(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(ArmSpaceSwitch, self).__init__(*args, **kwargs)

    def build(self, arm_rig, world_rig, cog_rig):
        # Creates the ik control spaceswitch
        enum_space_switch = rigEnumSpaceSwitch.RigEnumSpaceSwitch(world_rig.tip, arm_rig.rig_clavicle.tip,
                                                                  alias_list=['world', 'shoulder'],
                                                                  attribute_name='space',
                                                                  control=arm_rig.rig_arm.ik_rig.controls[0],
                                                                  parent=True, rig_system=arm_rig.rig_system)
        enum_space_switch.add_object(arm_rig.rig_arm.ik_rig.controls[0])
        # Creates the ik pole vector control spaceswitch
        enum_space_switch = rigEnumSpaceSwitch.RigEnumSpaceSwitch(world_rig.tip, arm_rig.rig_clavicle.tip, arm_rig.rig_arm.ik_rig.controls[0],
                                                                  alias_list=['world', 'shoulder', 'ikHandle'],
                                                                  attribute_name='space',
                                                                  control=arm_rig.rig_arm.ik_rig.controls[1],
                                                                  parent=True,
                                                                  rig_system=arm_rig.rig_system)
        enum_space_switch.add_object(arm_rig.rig_arm.ik_rig.controls[1])
        # creates the fk control spaceswitch
        enum_space_switch = rigEnumSpaceSwitch.RigEnumSpaceSwitch(arm_rig.rig_clavicle.tip, world_rig.tip,
                                                                  cog_rig.tip,
                                                                  alias_list=['shoulder', 'world', 'hip'],
                                                                  attribute_name='space',
                                                                  control=arm_rig.rig_arm.fk_rig.controls[0],
                                                                  orient=True,
                                                                  rig_system=arm_rig.rig_system)
        enum_space_switch.add_object(arm_rig.rig_arm.fk_rig.controls[0])


if __name__ == '__main__':
    enum_space_switch = rigEnumSpaceSwitch.RigEnumSpaceSwitch('pTorus1', 'pCube1', 'pCylinder1',
                                                              alias_list=['torus', 'cube', 'cylinder'],
                                                              attribute_name='primitives',
                                                              control='pSphere1',
                                                              parent=True)

    enum_space_switch.add_object('pSphere1')
