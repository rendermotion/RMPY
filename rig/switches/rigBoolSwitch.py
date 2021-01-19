from RMPY.rig.switches import rigBaseSwitch
import pymel.core as pm


class RigBoolSwitchModel(rigBaseSwitch.RigBaseSwitchModel):
    def __init__(self):
        super(RigBoolSwitchModel, self).__init__()


class RigBoolSwitch(rigBaseSwitch.RigBaseSwitch):
    def __init__(self, *args, **kwargs):
        if 'model' not in kwargs.keys():
            kwargs['model'] = RigBoolSwitchModel()
        super(RigBoolSwitch, self).__init__(*args, **kwargs)
        self.initialize(*args, **kwargs)
        if self.control:
            self.set_control()

    def set_control(self, **kwargs):
        self.attribute_name = kwargs.pop('attribute_name', self.attribute_name)
        if self.attribute_name not in pm.listAttr(self.control):
            pm.addAttr(self.control, ln=self.attribute_name, at='bool', k=True)
        self.set_outputs()

    def set_outputs(self):
        self.control.attr(self.attribute_name) >> self.reverse.inputX
        self.attribute_output = self.control.attr(self.attribute_name)


if __name__ == '__main__':
    space_switch = RigBoolSwitch(control='nurbsCircle1')
    space_switch.attribute_output_false >> pm.Attribute('pSphere1.visibility')

