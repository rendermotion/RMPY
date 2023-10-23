from RMPY.rig import rigBase
import pymel.core as pm
from RMPY.core import config


class RigPlaneModel(rigBase.BaseModel):
    def __init__(self):
        super(RigPlaneModel, self).__init__()
        self.makePlane = None
        self.plane = None


class RigPlane(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', RigPlaneModel())
        super(RigPlane, self).__init__(*args, **kwargs)

    def create_point_base(self, *args, **kwargs):
        self._model.plane, self._model.makePlane = pm.nurbsPlane(axis=[0, 1, 0],
                                                                 width=self.rm.point_distance(*args), lengthRatio=.1)
        center_locator = self.create.space_locator.point_base(*args, name='center')
        up_vector_locator = self.create.space_locator.node_base(args[0], name='upVector')[0]

        pm.move(1.0, up_vector_locator, moveY=True, objectSpace=True, relative=True)
        self.transform.aim_point_based(self.plane, center_locator, args[1], up_vector_locator)


if __name__ == '__main__':
    selection = pm.ls(selection=True)
    rig_piston = RigPlane()
    rig_piston.create_point_base(*selection)
