from RMPY.rig import rigSurfaceInfo
import pymel.core as pm


class RigPointOnSurfaceModel(rigSurfaceInfo.SurfaceInfoModel):
    def __init__(self):
        super(RigPointOnSurfaceModel, self).__init__()
        self.surface = None


class RigPointOnSurface(rigSurfaceInfo.SurfaceInfo):
    def __init__(self, surface, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', RigPointOnSurfaceModel())
        kwargs['follow_v'] = True
        # args.append(surface)
        super(RigPointOnSurface, self).__init__(surface, *args, **kwargs)
        self._model.surface = surface
        self.tip = None

    @property
    def surface(self):
        return self._model.surface

    def create_point_base(self, scene_node, **kwargs):
        super(RigPointOnSurface, self).create_point_base(scene_node, **kwargs)
        cls_point_on_surface = pm.createNode('closestPointOnSurface')
        self.surface.worldSpace[0] >> cls_point_on_surface.inputSurface

        reference_point = self.create.space_locator.point_base(scene_node)
        reference_point.worldPosition >> cls_point_on_surface.inPosition

        pm.setAttr(self.parameter_u_attribute, cls_point_on_surface.parameterU.get())
        pm.setAttr(self.parameter_v_attribute, cls_point_on_surface.parameterV.get())
        # pm.delete(reference_point)
        reference_point.setParent(self.rig_system.kinematics)
        pm.delete(cls_point_on_surface)
        self.connect(reference_point)
        self.tip = reference_point

if __name__ == '__main__':
    rig_point = RigPointOnSurface(pm.ls('C_extrude00_spine_grp')[0])
    rig_point.create_point_base(pm.ls('C_clusterOnCurve06_spine_grp')[0])
