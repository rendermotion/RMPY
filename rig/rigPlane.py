from RMPY.rig import rigBase
import pymel.core as pm
from RMPY.core import config


class RigPlaneModel(rigBase.BaseModel):
    def __init__(self):
        super(RigPlaneModel, self).__init__()
        self.makePlane = None
        self.plane = None
        self.nurbs_plane = None


class RigPlane(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', RigPlaneModel())
        super(RigPlane, self).__init__(*args, **kwargs)

    def create_point_base(self, *args, **kwargs):
        super().create_point_base(*args, **kwargs)
        poly_output = kwargs.pop('poly_output', False)
        u_spans = kwargs.pop('u_spans', 1)
        v_spans = kwargs.pop('v_spans', 1)
        construction_history = kwargs.pop('construction_history', True)

        self._model.nurbs_plane, self._model.makePlane = pm.nurbsPlane(axis=[0, 1, 0],
                                                                       width=self.rm.point_distance(*args),
                                                                       lengthRatio=.1)
        center_locator = self.create.space_locator.point_base(*args, name='center')
        up_vector_locator = self.create.space_locator.node_base(args[0], name='upVector')[0]

        pm.move(1.0, up_vector_locator, moveY=True, objectSpace=True, relative=True)
        self.transform.aim_point_based(self.nurbs_plane, center_locator, args[1], up_vector_locator)
        pm.delete(center_locator, up_vector_locator)
        self.name_convention.rename_name_in_format(self.nurbs_plane, name='plane')
        self.nurbs_plane.setParent(self.rig_system.kinematics)
        if poly_output:
            self._model.plane = pm.ls(pm.nurbsToPoly(self.nurbs_plane, uNumber=u_spans, vNumber=v_spans,
                                                     uType=1, vType=1,
                                                     polygonType=1,
                                                     constructionHistory=construction_history, format=2))[0]
            self.name_convention.rename_name_in_format(self.plane, name='plane')
            pm.parent(self.plane, self.rig_system.kinematics)
            if not construction_history:
                pm.delete(self.nurbs_plane)




if __name__ == '__main__':
    selection = pm.ls(selection=True)
    rig_piston = RigPlane()
    rig_piston.create_point_base(*selection)
