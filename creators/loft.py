from RMPY import nameConvention
from RMPY.core import config
import pymel.core as pm

from RMPY.creators import creatorsBase
from RMPY.creators import curve
from RMPY.creators import spaceLocator


class Creator(creatorsBase.Creator):
    def __init__(self, *args, **kwargs):
        super(Creator, self).__init__(*args, **kwargs)
        self.path = None
        self.skin_surface = None
        self.surface_radius = None
        self.circle = None

    def surface_radius(self):
        return self._model.surface_radius

    def point_base(self, *points, **kwargs):
        super(Creator, self).point_base(*points, **kwargs)
        radius = kwargs.pop('radius', 1)
        delete_history = kwargs.pop('delete_history', True)
        curve = curve.Curve()
        locator = spaceLocator.Creator()

        self.path = curve.point_base(*points, ep=True)
        self.circle = pm.circle(radius=radius)[0]

        self.name_conv.rename_name_in_format(self.circle, name='circle')

        original_surf = pm.extrude(self.circle, self.path, fixedPath=True,
                                   useComponentPivot=1, useProfileNormal=True)

        swap_uv = pm.rebuildSurface(original_surf[0], keepControlPoints=True, rebuildType=0,
                                    keepRange=0)

        new_surface = pm.reverseSurface(swap_uv[0], direction=3)
        self.skin_surface = new_surface[0]
        self.name_conv.rename_name_in_format(self.skin_surface, name='extrude')

        cps = pm.createNode('closestPointOnSurface')
        measure_locator = locator.point_base(points[0])
        measure_locator.worldPosition >> cps.inPosition
        self.skin_surface.worldSpace[0] >> cps.inputSurface
        u_closer_value = cps.parameterU.get()
        pm.delete(measure_locator, cps)

        if u_closer_value > .5:
            new_surface = pm.reverseSurface(self.skin_surface, direction=0)
            self.skin_surface = new_surface[0]

        if delete_history:
            self.delete_history()
        return self.skin_surface

    def curve_base(self, *path, **kwargs):
        swap_uv = kwargs.pop('swap_uv', True)
        radius = kwargs.pop('radius', 1)
        delete_history = kwargs.pop('delete_history', False)
        self.path = path[0]
        self.circle = pm.circle(radius=radius)[0]

        self.name_conv.rename_name_in_format(self.circle, name='circle')
        original_surf = pm.extrude(self.circle, self.path, fixedPath=True,
                                   useComponentPivot=1, useProfileNormal=True)
        if swap_uv:
            swap_uv_curve = pm.rebuildSurface(original_surf[0], keepControlPoints=True, rebuildType=0, keepRange=0)
            new_surface = pm.reverseSurface(swap_uv_curve[0], direction=3)
            self.skin_surface = new_surface[0]
        else:
            self.skin_surface = original_surf

        self.name_conv.rename_name_in_format(self.skin_surface, name='extrude')

        if delete_history:
            self.delete_history()

        return self.skin_surface

    def delete_history(self):
        pm.delete(self.skin_surface, constructionHistory=True)
        pm.delete(self.path)
        pm.delete(self.circle)

    def uniform_rebuild(self, number_of_points):
        rebuild_surf = pm.rebuildSurface(self.skin_surface, rebuildType=0,
                                         spansV=number_of_points,
                                         keepRange=True)
        self.skin_surface = rebuild_surf[0]


if __name__ == '__main__':

    selection = pm.ls(selection=True)
    nurbs_surface = Creator()
    nurbs_surface.curve_base()
    #nurbs_surface.point_base(*selection, ep=True, delete_history=False)
    #nurbs_surface.uniform_rebuild(10)