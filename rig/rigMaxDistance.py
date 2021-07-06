"""
A rig to keep a point at the maximum allowed Distance with a multiply value.
This Rig is used on the stretchy IK to keep the points at the maximum
"""
from RMPY.rig import rigBase
import pymel.core as pm


class MaxDistanceModel(rigBase.BaseModel):
    def __init__(self):
        super(MaxDistanceModel, self).__init__()
        self.control_point = None
        self.aim_point = None


class MaxDistance(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', MaxDistanceModel())
        super(MaxDistance, self).__init__(*args, **kwargs)
        self.root = None
        self.tip = None

    @property
    def control_point(self):
        return self._model.control_point

    @property
    def aim_point(self):
        return self._model.aim_point

    def create_point_base(self, *args, **kwargs):
        """
            args: two points the base and the final point. the distance between this two points will be the starting
             maximum distance.
        """
        self._model.aim_point = self.create.space_locator.point_base(args[0], name='referenceRoot')
        self.root = self.create.group.point_base(self.aim_point, name='root')
        self.tip = self.create.space_locator.point_base(args[1])
        self._model.control_point = self.create.space_locator.point_base(args[1])





