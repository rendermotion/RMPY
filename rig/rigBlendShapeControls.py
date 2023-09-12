from RMPY.rig import rigBase
import pymel.core as pm


class RigBlendShapeControls(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(RigBlendShapeControls, self).__init__(*args, **kwargs)
        self.root = kwargs.pop('root', None)
        self.points = kwargs.pop('points', None)

        if self.root:
            self.setup_name_convention_node_base(self.root)
            self.points = pm.ls(self.root)[0].getChildren()
            self.rig_system._create_controls()
        else:
            if self.points:
                self.rig_system._create_controls()

            else:
                print('please provide root or points to build')

        self.build()

    def build(self):
        for each_ref_point in self.points:
            reset_control, control = self.create.controls.point_base(each_ref_point,
                                                                     type='b',
                                                                     size=1.0)
            self.name_convention.rename_name_in_format(control,
                                                       side=self.name_convention.get_from_name(each_ref_point, 'side'),
                                                       name='facial',
                                                       objectType='control'
                                                )

            self.controls.append(control)
            self.reset_controls.append(reset_control)
            reset_control.setParent(self.rig_system.controls)
            self.rm.lock_and_hide_attributes(control, bit_string='0000000000')


if __name__ == '__main__':
    facial_controls = RigBlendShapeControls(root='C_facialControls_reference_pnt')
