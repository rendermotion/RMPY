from RMPY.rig.switches import rigBaseSwitch
import pymel.core as pm


class FloatRangeSwitchModel(rigBaseSwitch.RigBaseSwitchModel):
    def __init__(self):
        super(FloatRangeSwitchModel, self).__init__()
        self.animation_curve = None


class FloatRangeSwitch(rigBaseSwitch.RigBaseSwitch):
    def __init__(self, *args, **kwargs):
        if 'model' not in kwargs.keys():
            kwargs['model'] = FloatRangeSwitchModel()
        super(FloatRangeSwitch, self).__init__(*args, **kwargs)
        self.min_value = 0
        self.max_value = 20

        self._raise_min = 0.0
        self._raise_max = 9.0
        self._decay_min = 11.0
        self._decay_max = 20

        self.animation_curve = None
        self.attribute_output = None

        self.initialize(*args, **kwargs)
        if self.control:
            self.set_control(**kwargs)

    @property
    def animation_curve(self):
        return self._model.animation_curve

    @animation_curve.setter
    def animation_curve(self, value):
        self._model.animation_curve = value

    def set_control(self, **kwargs):
        self.attribute_name = kwargs.pop('attribute_name', 'float_switch')
        self._raise_min = kwargs.pop('raise_min', self._raise_min)
        self._raise_max = kwargs.pop('raise_max', self._raise_max)
        self._decay_min = kwargs.pop('decay_min', self._decay_min)
        self._decay_max = kwargs.pop('decay_max', self._decay_max)
        self.min_value = kwargs.pop('min_value', self.min_value)
        self.max_value = kwargs.pop('max_value', self.max_value)

        if self.attribute_name not in pm.listAttr(self.control):
            pm.addAttr(self.control, ln=self.attribute_name, at='float', min=self.min_value, max=self.max_value, k=True)
        self.set_outputs()

    def set_outputs(self):
        self.animation_curve = self.create.connect.with_limits(self.control.attr(self.attribute_name),
                                                               self.reverse.inputX, [[self._raise_min, 0],
                                                                                     [self._raise_max, 1],
                                                                                     [self._decay_min, 1],
                                                                                     [self._decay_max, 0],
                                                                                     ],
                                                               pre_infinity_type='constant',
                                                               post_infinity_type='constant',
                                                               in_tangent_type='linear',
                                                               out_tangent_type='linear', )[1]
        self.attribute_output = self.animation_curve.output

        self.initialize()  # initializes the negate output


if __name__ == '__main__':
    switch = FloatRangeSwitch(control='nurbsCircle1')
    switch.attribute_output >> pm.Attribute('pSphere1.translateX')
