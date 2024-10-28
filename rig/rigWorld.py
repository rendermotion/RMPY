from RMPY.rig import rigProp
import pymel.core as pm


class RigWorld(rigProp.RigProp):
    def __init__(self, *args, **kwargs):
        super(RigWorld, self).__init__(*args, **kwargs)
        self.build()

    @property
    def settings_height(self):
        return self.reset_controls[-1].translateY.get()

    @settings_height.setter
    def settings_height(self, value):
        self.reset_controls[-1].translateY.set(value)

    def build(self):
        reference_group = pm.group(empty=True)
        print(reference_group)
        self.name_convention.rename_name_in_format(reference_group, name='world', system='reference')
        super(RigWorld, self).create_point_base(reference_group, name='control', depth=4, centered=True)
        self.rm.lock_and_hide_attributes(self.controls[-1], bit_string='0000000000')
        self.name_convention.rename_set_from_name(self.controls[-1], 'settings', 'name')
        self.attach_points['tip'] = self.controls[-2]
        pm.delete(self.rig_system.joints, reference_group)


if __name__ == '__main__':
    rig_world = RigWorld()
    # rig_world.settings_height = 5







