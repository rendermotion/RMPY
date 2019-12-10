from RMPY.rig.switches import rigBaseSwitch
import pymel.core as pm


class FloatSwitchModel(rigBaseSwitch.RigBaseSwitchModel):
    def __init__(self):
        super(FloatSwitchModel, self).__init__()
        self.multiply = None


class FloatSwitch(rigBaseSwitch.RigBaseSwitch):
    def __init__(self, *args, **kwargs):
        super(FloatSwitch, self).__init__(*args, **kwargs)
        self._model = FloatSwitchModel()
        self.initialize(*args, **kwargs)
        self.multiply = pm.createNode('unitConversion')
        self.name_convention.rename_name_in_format(self.multiply, name="multiplier")
        self.multiply.output >> self.reverse.inputX
        self.attribute_output = self.multiply.output
        self.max_value = kwargs.pop('max', 10.0)
        if self.control:
            self.set_control()

    @property
    def max_value(self):
        return self.multiply.conversionFactor.get()

    @max_value.setter
    def max_value(self, value):
        self.multiply.conversionFactor.set(1.0/value)

    @property
    def multiply(self):
        return self._model.multiply

    @multiply.setter
    def multiply(self, value):
        self._model.multiply = value

    def set_control(self, **kwargs):
        self.attribute_name = kwargs.pop('attribute_name', self.attribute_name)
        if self.attribute_name not in pm.listAttr(self.control):
            pm.addAttr(self.control, ln=self.attribute_name, at='float', min=0, max=1.0/self.max_value, k=True)
        self.set_outputs()

    def set_outputs(self):
        self.control.attr(self.attribute_name) >> self.multiply.input


if __name__ == '__main__':
    float_switch = FloatSwitch(control='nurbsCircle1')
    float_switch.attribute_output >> pm.Attribute('pSphere1.visibility')






