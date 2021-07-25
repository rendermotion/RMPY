from RMPY.rig import rigProp
import pymel.core as pm


class RigWorld(rigProp.RigProp):
    def __init__(self, *args, **kwargs):
        super(RigWorld, self).__init__(*args, **kwargs)
        self.build()

    def build(self):
        reference_group = pm.group(empty=True)
        self.name_convention.rename_name_in_format(reference_group, name='world', system='reference')
        super(RigWorld, self).create_point_base(reference_group, name='control', depth=3, centered=True)
        self.attach_points['tip'] = self.controls[-1]
        pm.delete(self.rig_system.joints, reference_group)


if __name__ == '__main__':
    RigWorld()







