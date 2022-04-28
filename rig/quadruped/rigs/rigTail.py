from RMPY.rig import rigLaces
from RMPY.rig.quadruped.rigs import rigIKQuadSpine

from RMPY.rig import rigPointOnSurface
from RMPY.rig import rigFK
from RMPY.rig import rigBase
from RMPY.rig import rigSingleJoint

import pymel.core as pm


class TailModel(rigBase.BaseModel):
    def __init__(self):
        super(TailModel, self).__init__()
        self.ik_spine = None
        self.hip = None
        self.points_on_surface = []
        self.surface = None
        self.back = None
        self.chest = None


class RigTail(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', TailModel())
        super(RigTail, self).__init__(*args, **kwargs)
        self._model.ik_tail = rigIKQuadSpine.RigIKQuadSpine(rig_system=self.rig_system)
        self._model.fk_tail = rigFK.RigFK(rig_system=self.rig_system)
        self.root = None
        self.tip = None

    @property
    def ik_tail(self):
        return self._model.ik_tail

    @property
    def fk_tail(self):
        return self._model.fk_tail

    @property
    def surface(self):
        return self._model.surface

    @property
    def points_on_surface(self):
        return self._model.points_on_surface

    def create_point_base(self, *args, **kwargs):
        super(RigTail, self).create_point_base(*args, **kwargs)
        self.ik_tail.create_point_base(*args, hierarchize=False, stretchy_ik=False)
        self._model.surface = self.create.loft.point_base(*pm.ls(args), type='line')
        pm.parent(self.surface, self.rig_system.kinematics)
        for each in self.ik_tail.reset_controls:
            self.points_on_surface.append(rigPointOnSurface.RigPointOnSurface(self.surface, rig_system=self.rig_system))
            self.points_on_surface[-1].create_point_base(each)
            print '******** constraint_'
            print self.create.constraint.constraint_type
            self.create.constraint.node_base(self.points_on_surface[-1].tip, each, mo=True)

        self.fk_tail.create_point_base(*args, orient_type='point_orient')
        pm.skinCluster(self.fk_tail.joints, self.surface)
        self.joints.extend(self.ik_tail.joints)
        self.root = self.fk_tail.reset_controls[0]


if __name__=='__main__':
    root_points = [u'C_tail00_reference_pnt', u'C_tail01_reference_pnt', u'C_tail02_reference_pnt',
                          u'C_tail03_reference_pnt', u'C_tail04_reference_pnt', u'C_tail05_reference_pnt']

    rig_tail = RigTail()
    rig_tail.create_point_base(*root_points)