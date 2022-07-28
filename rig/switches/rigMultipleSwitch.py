from RMPY.rig import rigBase


class RigMultipleSwitchModel(rigBase.BaseModel):
    def __init__(self):
        super(RigMultipleSwitchModel, self).__init__()
        self.control = None
        self.switch = {}
        self.attribute_name = 'attribute'


class RigMultipleSwitch(rigBase.RigBase):
    """
    Base class for multiple switches, a switch is a logic rig that outputs 1 or 0
    depending on the input.
    In cases where you can have multiple channels to ouptut where each one can have a 1 or 0 different than the others
    channels you can use this as base. This Class it is just a data structure intended to have access to multiple switches,
    based on a key, that would be a string.
    """
    def __init__(self, *args, **kwargs):
        if 'model' not in kwargs.keys():
            kwargs['model'] = RigMultipleSwitchModel()
        super(RigMultipleSwitch, self).__init__(*args, **kwargs)
        self.control = kwargs.pop('control', None)
        self._model.attribute_name = kwargs.pop('attribute_name', self.attribute_name)

    @property
    def attribute_name(self):
        return self._model.attribute_name

    @property
    def switch(self):
        return self._model.switch

    @property
    def control(self):
        return self._model.control

    @control.setter
    def control(self, value):
        self._model.control = value

