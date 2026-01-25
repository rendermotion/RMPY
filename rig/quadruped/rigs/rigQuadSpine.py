from RMPY.rig.quadruped.rigs import rigIKQuadSpine
from RMPY.rig import rigPointOnSurface
from RMPY.rig import rigBase
from RMPY.rig import rigSingleJoint

import pymel.core as pm
import importlib
importlib.reload(rigIKQuadSpine)

class QuadSpineModel(rigBase.BaseModel):
    def __init__(self):
        super(QuadSpineModel, self).__init__()
        self.ik_spine = None
        self.hip = None
        self.points_on_surface = []
        self.surface = None
        self.back = None
        self.center = None
        self.chest = None


class RigQuadSpine(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', QuadSpineModel())
        super(RigQuadSpine, self).__init__(*args, **kwargs)
        self._model.ik_spine = rigIKQuadSpine.RigIKQuadSpine(rig_system=self.rig_system)
        self._model.chest = rigSingleJoint.RigSingleJoint(rig_system=self.rig_system)
        self._model.back = rigSingleJoint.RigSingleJoint(rig_system=self.rig_system)
        self._model.center = rigSingleJoint.RigSingleJoint(rig_system=self.rig_system)
        self.tip = None
        self.root = None
    @property
    def ik_spine(self):
        return self._model.ik_spine

    @property
    def chest(self):
        return self._model.chest

    @property
    def center(self):
        return self._model.center

    @property
    def back(self):
        return self._model.back

    @property
    def surface(self):
        return self._model.surface

    @property
    def points_on_surface(self):
        return self._model.points_on_surface

    def create_point_base(self, *args, **kwargs):
        super(RigQuadSpine, self).create_point_base(*args, **kwargs)
        kwargs['stretchy_ik'] = kwargs.pop('stretchy_ik', True)
        kwargs['hierarchize'] = kwargs.pop('hierarchize', False)
        self.ik_spine.create_point_base(*args, **kwargs)
        self._model.surface = self.create.loft.point_base(*pm.ls(args), type='line')
        pm.parent(self.surface, self.rig_system.kinematics)
        for each in self.ik_spine.reset_controls:
            self.points_on_surface.append(rigPointOnSurface.RigPointOnSurface(self.surface, rig_system=self.rig_system))
            self.points_on_surface[-1].create_point_base(each)
            self.create.constraint.node_base(self.points_on_surface[-1].tip, each, mo=True)

        self.back.create_point_base(args[0], name='back', centered=True)
        self.back.custom_world_align(self.back.reset_controls[0])
        self.chest.create_point_base(args[-1], name='chest', centered=True)
        self.chest.custom_world_align(self.chest.reset_controls[0])

        self.center.create_point_base(args[int(len(args)/2)], name='center', centered=True)
        self.center.custom_world_align(self.center.reset_controls[0])

        pm.skinCluster(self.back.joints + self.center.joints + self.chest.joints, self.surface)
        self.joints.extend(self.ik_spine.joints)
        self.root = self.create.group.point_base(args[0], type='world')
        self.custom_world_align(self.root)
        pm.parent(self.root, self.rig_system.kinematics)
        self.name_convention.rename_name_in_format(self.root, name='rigTip')
        self.chest.set_parent(self.root)
        self.back.set_parent(self.root)
        self.center.set_parent(self.root)


if __name__ == '__main__':
    spine_points = [u'C_spine00_reference_pnt', u'C_spine01_reference_pnt', u'C_spine02_reference_pnt',
                    u'C_spine03_reference_pnt', u'C_spine04_reference_pnt', u'C_spine05_reference_pnt',
                    ]

    rig_quad_spine = RigQuadSpine()
    rig_quad_spine.create_point_base(*spine_points)
