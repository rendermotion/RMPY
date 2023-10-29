from RMPY.rig import rigLaces
from RMPY.rig import rigPiston
from RMPY.rig import rigPlane
from RMPY.rig import rigUVPin
import pymel.core as pm
import importlib
importlib.reload(rigPlane)


class RigPistonLaceModel(rigPiston.RigPistonModel):
    def __init__(self):
        super(RigPistonLaceModel, self).__init__()
        self.lace_rig = None
        self.uv_pin_rig_list = []
        self.plane_rig = None


class RigPistonLace(rigPiston.RigPiston):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', RigPistonLaceModel())
        super(RigPistonLace, self).__init__(*args, **kwargs)

    def create_point_base(self, *args, **kwargs):

        super(RigPistonLace, self).create_point_base(*args, **kwargs)
        kwargs['rig_system'] = self.rig_system
        self._model.lace_rig = rigLaces.RigLaces(rig_system=self.rig_system)
        self.lace_rig.create_point_base(*args, **kwargs)
        kwargs['poly_output'] = True
        kwargs['construction_history'] = False
        create_piston_controls = kwargs.pop('create_piston_controls', False)
        if create_piston_controls:
            controls = self.create.controls.point_base(*args, name='piston', type='circular')
            pm.parentConstraint(controls[0][1], self.tip)
            pm.parentConstraint(controls[1][1], self.root)
            self.reset_controls.append(controls[0][0])
            self.reset_controls.append(controls[1][0])
            self.controls.append(controls[0][1])
            self.controls.append(controls[1][1])
            pm.parent(self.reset_controls, self.rig_system.controls)
        self._model.plane_rig = rigPlane.RigPlane(rig_system=self.rig_system)
        self.plane_rig.create_point_base(*args, **kwargs)
        for each in self.lace_rig.reset_controls:
            new_uv_pin = rigUVPin.RigUVPin(rig_system=self.rig_system)
            new_uv_pin.create_point_base(each, geometry=self.plane_rig.plane)
            pm.parentConstraint(new_uv_pin.tip, each, mo=True)
            new_uv_pin.clean_up()
        self.create.constraint.node_base(self.joints[-2], self.plane_rig.plane, mo=True)





if __name__ == '__main__':
    selection = pm.ls(selection=True)
    piston_rig = RigPistonLace()
    piston_rig.create_point_base(*selection)
