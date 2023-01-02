from RMPY.rig.switches import rigBaseSwitch
import pymel.core as pm


class FloatSwitchModel(rigBaseSwitch.RigBaseSwitchModel):
    def __init__(self):
        super(FloatSwitchModel, self).__init__()
        self.multiply = None


class FloatSwitch(rigBaseSwitch.RigBaseSwitch):
    """
    The float Range Switch outputs 0 to one, depending on an input varying from 0 to a max_value,
    for example, you want a switch to control the visibility of an object, that goes from 0 to 1,
    but want to control with an float input value, for example 0 to 10, you can doit with this switch.
    The switch it is accomplished with a multiply node.
    """
    def __init__(self, *args, **kwargs):
        super(FloatSwitch, self).__init__(*args, **kwargs)
        self._model = FloatSwitchModel()
        self.initialize(**kwargs)
        self.multiply = pm.createNode('unitConversion')
        self.name_convention.rename_name_in_format(self.multiply, name="multiplier")
        self.multiply.output >> self.reverse.inputX
        self.attribute_output = self.multiply.output
        self.max_value = kwargs.pop('max', 10.0)
        if self.control:
            self.set_control()

    @property
    def max_value(self):
        """
        the max value that will give an output of 1
        :return:
        """
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
        self._model.attribute_name = kwargs.pop('attribute_name', self.attribute_name)
        if self.attribute_name not in pm.listAttr(self.control):
            pm.addAttr(self.control, ln=self.attribute_name, at='float', min=0, max=1.0/self.max_value, k=True)
        self.set_outputs()

    def set_outputs(self):
        self.control.attr(self.attribute_name) >> self.multiply.input


if __name__ == '__main__':
    float_switch = FloatSwitch(control='nurbsCircle1')
    float_switch.attribute_output >> pm.Attribute('pSphere1.visibility')






