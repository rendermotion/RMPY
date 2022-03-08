from RMPY.rig import rigBase
from RMPY.rig import rigFK


class RigFeetPivotModel(rigBase.BaseModel):
    def __init__(self):
        super(RigFeetPivotModel, self).__init__()
        self.rig_fk_feet_pivot = None
        self.rig_ik_feet_pivot = None


class RigFeetPivot(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(RigFeetPivot, self).__init__(*args, **kwargs)
        self._model = RigFeetPivotModel()

    @property
    def rig_fk_feet_pivot(self):
        if not self._model.rig_fk_feet_pivot:
            self._model.rig_fk_feet_pivot = rigFK.RigFK()

        return self._model.rig_fk_feet_pivot

    @property
    def rig_ik_feet_pivot(self):
        if not self._model.rig_fk_feet_pivot:
            self._model.rig_fk_feet_pivot = rigFK.RigFK()
        return self._model.rig_ik_feet_pivot

    def create_point_base(self, *args, **kwargs):
        super(RigFeetPivot, self).create_point_base(*args, **kwargs)

        self.rig_fk_feet_pivot.create_point_base(*args)
        self.rig_ik_feet_pivot.create_point_base(*args)
