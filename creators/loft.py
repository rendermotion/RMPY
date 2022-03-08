from RMPY import nameConvention
from RMPY.core import config
import pymel.core as pm
from RMPY.creators import creatorsBase
from RMPY.creators import curve
from RMPY.creators import spaceLocator


class Creator(creatorsBase.CreatorsBase):
    def __init__(self, *args, **kwargs):
        super(Creator, self).__init__(*args, **kwargs)
        self.path = None
        self.skin_surface = None
        self.surface_radius = None
        self.profile = None
        self.curve_creator = curve.Curve()
        self.locator_creator = spaceLocator.SpaceLocator()

    def point_base(self, *points, **kwargs):
        super(Creator, self).point_base(*points, **kwargs)
        radius = kwargs.pop('radius', 1)
        delete_history = kwargs.pop('delete_history', True)

        self.path = self.curve_creator.point_base(*points, ep=True)
        self._create_profile(**kwargs)

        original_surf = pm.extrude(self.profile, self.path, fixedPath=True,
                                   useComponentPivot=1, useProfileNormal=True)

        swap_uv = pm.rebuildSurface(original_surf[0], keepControlPoints=True, rebuildType=0,
                                    keepRange=0)

        new_surface = pm.reverseSurface(swap_uv[0], direction=3)
        self.skin_surface = new_surface[0]
        self.name_convention.rename_name_in_format(self.skin_surface, name='extrude')

        cps = pm.createNode('closestPointOnSurface')
        measure_locator = self.locator_creator.point_base(points[0])
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
        self._create_profile(**kwargs)
        print self.profile

        original_surf = pm.extrude(self.profile, self.path, fixedPath=True,
                                   useComponentPivot=1, useProfileNormal=True)
        if swap_uv:
            swap_uv_curve = pm.rebuildSurface(original_surf[0], keepControlPoints=True, rebuildType=0, keepRange=0)
            new_surface = pm.reverseSurface(swap_uv_curve[0], direction=3)
            self.skin_surface = new_surface[0]
        else:
            self.skin_surface = original_surf

        self.name_convention.rename_name_in_format(self.skin_surface, name='extrude')

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

    def _create_profile(self, **kwargs):
        profile_type = kwargs.pop('type', 'circle')
        radius = kwargs.pop('radius', 1)
        lenght = kwargs.pop('lenght', 1)

        if profile_type == 'line':
            curve_creator = curve.Curve()
            self.profile = curve_creator.point_base([1*lenght, 0, 0], [.5*lenght, 0, 0], [-.5*lenght, 0, 0], [-1*lenght, 0, 0])
            self.name_convention.rename_name_in_format(self.profile, name='line')
        elif profile_type == 'circle':
            self.profile = pm.circle(radius=radius)[0]
            self.name_convention.rename_name_in_format(self.profile, name='circle')


if __name__ == '__main__':
    selection = pm.ls(selection=True)
    nurbs_surface = Creator()
    nurbs_surface.curve_base(selection, type='line')
    #nurbs_surface.point_base(*selection, ep=True, delete_history=False)
    #nurbs_surface.uniform_rebuild(10)'''