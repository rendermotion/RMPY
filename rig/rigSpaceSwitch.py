from RMPY.rig.switches import rigFloatSwitch
from RMPY.rig import rigBase
import pymel.core as pm

class RigSpaceSwitchModel(rigBase.BaseModel):
    def __init__(self):
        super(RigSpaceSwitchModel, self).__init__()


class RigSpaceSwitch(rigBase.RigBase):
    def __init__(self, *args, **kwargs):

        self._model = RigSpaceSwitchModel()

        self.constraints = dict(parent = kwargs.pop('parent', True),
                                point = kwargs.pop('point', False),
                                orient = kwargs.pop('orient', False),
                                scale = kwargs.pop('scale', False))
        self.spaces

    def set_control(self, *args, **kwargs):

    def set_spaces(self, *args, **kwargs):

    def _set_space(self):



    def add_object(self,):







