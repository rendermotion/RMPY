import math
from RMPY.rig import rigBase
from RMPY.core import config
import pymel.core as pm


class RigSinFunctionModel(rigBase.BaseModel):
    def __init__(self):
        super().__init__()


class RigSinFunction(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', RigSinFunctionModel())
        super().__init__(*args, **kwargs)

    def create_point_base(self, *args, **kwargs):
        super().create_point_base(*args, **kwargs)
        self._add_control_attributes()
        script = ''
        offset = math.pi / (len(args) - 1)
        axis = config.axis_order[1].capitalize()

        count = 0
        for each_object in args:
            script += 'if ({} > {}.decay_limit/10 * {})\n'.format(offset * count, self.rig_system.settings, math.pi )
            script += '    {}.translate{} =  {}.amplitud * '.format(each_object,axis, self.rig_system.settings ) + \
              'sin({}.phase + {} * {} * {}.wave_length);\n'.format(self.rig_system.settings,offset, count, self.rig_system.settings)
            # script =  script + '    %s.translateX = %s.amplitud;\n'%(eachObject, control)
            script += 'else \n'
            script += '     {}.translate{} =   (1 - {}.decay / 10 * ((cos( {} * {}  '.format(each_object,axis, self.rig_system.settings, offset, count )+\
                      '/ ({}.decay_limit / 10) ) + 1)/2) ) * {}.amplitud * '.format(self.rig_system.settings, self.rig_system.settings ) + \
                      'sin({}.phase + {} * {} * {}.wave_length);\n'.print(self.rig_system.settings,offset, count, self.rig_system.settings)
            count += 1
        expression = pm.expression(name='sinFunction', string=script)
        self.name_convention.rename_name_in_format(expression, useName=True)

    def _add_control_attributes(self):
        pm.addAttr(self.rig_system.settings, ln='amplitud', k=True)
        pm.addAttr(self.rig_system.settings, ln='phase', k=True)
        pm.addAttr(self.rig_system.settings, ln='wave_length', k=True, min=0)
        pm.addAttr(self.rig_system.settings, ln='decay', k=True, min=0, max=10)
        pm.addAttr(self.rig_system.settings, ln='decay_limit', k=True, min=.01, max=10)
        self.rig_system.settings.decay_limit.set(10)


if __name__ == '__main__':
    selection = pm.ls(selection=True)
    sin_function = RigSinFunction()
    sin_function.create_point_base(*selection)