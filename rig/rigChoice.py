from RMPY.AutoRig import RigBase
import pymel.core as pm


class RigChoiceModel(RigBase.RigBase):
    def __init__(self):
        super(RigChoiceModel, self).__init__()
        self.choice = None

class RigChoice(RigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(RigChoice, self).__init__(*args, **kwargs)
        self.data_type = kwargs.pop('type', None)

    @property
    def output(self):
        return self.choice.output

    @property
    def selector(self):
        return self.choice.selector

    def create_list_base(self, data_name_list, data_value_list):
        self.define_type(data_value_list[0])
        self._model.choice = pm.createNode('choice')
        data_node = pm.group(empty=True)
        self.name_convention.rename_name_in_format(self.choice, name='choice')
        self.name_convention.rename_name_in_format(data_node, name='data')
        if self.data_type:
            for index, (data_name, data_value) in enumerate(zip(data_name_list, data_value_list)):
                pm.addAttr(data_node, ln=data_name, type=self.data_type, k=True)
                data_node.attr(data_name).set(data_value, type=self.data_type)
                data_node.attr(data_name) >> self.choice.input[index]
        data_node.setParent(self.rig_system.kinematics)

    def define_type(self, data_sample):
        if data_sample.__class__ is list and len(data_sample) == 3:
            self.data_type = 'double3'
        elif data_sample.__class__ is str:
            self.data_type = 'string'
        else:
            print('data not identified {}'.format(data_sample.__class__))


if __name__ == '__main__':
    names = ['antlersE5', 'antlersF6']
    values = [[254.0/255.0, 171.0/255.0, 17.0/255.0], [158.0/255.0, 188.0/255.0, 64.0/255.0]]
    values_text = ['/pathA', '/pathB']

    choice_rig = RigChoice()
    choice_rig.create_list_base(names, values_text)