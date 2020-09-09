from RMPY.rig.switches import rigMultipleSwitch
from RMPY.rig.switches import rigFloatRangeSwitch
import pymel.core as pm
reload(rigFloatRangeSwitch)


class RigEnumSwitchModel(rigMultipleSwitch.RigMultipleSwitch):
    """
    Base class for switches, a switch is a logic rig that outputs 1 or 0
    depending on the input.
    The initialize function initializes the attribute_output_false creating
    a reverse having as input the attribute_output.
    """
    def __init__(self, *args, **kwargs):
        super(RigEnumSwitchModel, self).__init__(*args, **kwargs)
        self.attribute_name = 'enum_attribute'


class RigEnumSwitch(rigMultipleSwitch.RigMultipleSwitch):
    def __init__(self, *args, **kwargs):
        if 'model' not in kwargs.keys():
            kwargs['model'] = RigEnumSwitchModel()
        super(RigEnumSwitch, self).__init__(*args, **kwargs)

    def add_enum_names(self, *enum_names, **kwargs):
        self._model.attribute_name = kwargs.pop('attribute_name', self.attribute_name)

        if self.attribute_name not in pm.listAttr(self.control):
            pm.addAttr(self.control, ln=self.attribute_name, at='enum', k=True, enumName=enum_names)

        for index, each_enum in enumerate(enum_names):
            self.switch[each_enum] = rigFloatRangeSwitch.FloatRangeSwitch(control=self.control)
            self.switch[each_enum].set_control(attribute_name=self.attribute_name,
                                               raise_min=float(index)-.6,
                                               raise_max=float(index)-.4,
                                               decay_min=float(index) + .4,
                                               decay_max=float(index) + .6)

    @property
    def switch(self):
        return self._model.switch

    @property
    def attribute_name(self):
        return self._model.attribute_name


if __name__ == '__main__':
    rig_enum_names = RigEnumSwitch(control='nurbsCircle1')
    rig_enum_names.add_enum_names('cube', 'sphere', attribute_name='sphereCube')
    cube, sphere = pm.ls('pCube1', 'pSphere1')
    rig_enum_names.switch['cube'].attribute_output >> cube.visibility
    rig_enum_names.switch['sphere'].attribute_output >> sphere.visibility