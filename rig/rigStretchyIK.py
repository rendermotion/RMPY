from RMPY.rig import rigSimpleIk
from RMPY.rig import rigStretchyJointChain
import pymel.core as pm


class StretchyIKModel(rigSimpleIk.SimpleIKModel):
    def __init__(self):
        super(StretchyIKModel, self).__init__()
        self.rigStretchy = None


class StretchyIK(rigSimpleIk.SimpleIK):
    def __init__(self, *args, **kwargs):
        if 'model' not in kwargs.keys():
            kwargs['model'] = StretchyIKModel()
        super(StretchyIK, self).__init__(*args, **kwargs)

    def create_point_base(self, *args, **kwargs):
        super(StretchyIK, self).create_point_base(*args, **kwargs)
        make_stretchy = kwargs.pop('make_stretchy', True)
        create_pole_vector = kwargs.pop('create_pole_vector', True)
        create_controls = kwargs.pop('create_controls', True)
        if make_stretchy:
            self.make_stretchy()
        if create_pole_vector:
            self.create_pole_vector()
        if create_controls:
            self.create_controls()

    def make_stretchy(self):
        self._model.rigStretchy = rigStretchyJointChain.StretchyJointChain(self.ik_handle, rig_system=self.rig_system)
        self._model.rigStretchy.ik_handle_based()

    def expose_attributes_on_control(self, control):
        pm.addAttr(control, longName='stretchyIK', proxy=self.ik_handle.stretchyIK)


if __name__ == '__main__':
    simple_ik = StretchyIK()
    simple_ik.create_point_base(u'L_shoulder01_reference_pnt', u'L_elbow01_reference_pnt', u'L_wrist01_reference_pnt')
    # simple_ik.make_stretchy()
    # simple_ik.create_pole_vector()
    # simple_ik.create_controls()
