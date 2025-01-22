from RMPY.rig import rigBase
import pymel.core as pm

class RigSegmentScaleCompensateModel(rigBase.BaseModel):
    def __init__(self):
        super(RigSegmentScaleCompensateModel, self).__init__()
        self.column_from_matrix = []
        self.multiply = []
        self.normalize = []
        self.multMatrix_output = None
        self.four_by_four_normalized_matrix = None
        self.four_by_four_translation_matrix = None
        self.translate_constants = []


class RigSegmentScaleCompensate(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', RigSegmentScaleCompensateModel())
        super(RigSegmentScaleCompensate, self).__init__(*args, **kwargs)

    def create_node_base(self, *args, **kwargs):
        super(RigSegmentScaleCompensate, self).create_node_base(*args, **kwargs)
        output_node = args[0]
        parent_node = output_node.getParent()
        self._model.four_by_four_normalized_matrix = pm.createNode('fourByFourMatrix')
        self._model.four_by_four_translation_matrix = pm.createNode('fourByFourMatrix')
        self._model.multMatrix_output = pm.createNode('multMatrix')
        self.four_by_four_translation_matrix.output >> self.multMatrix_output.matrixIn[0]
        self.four_by_four_normalized_matrix.output >> self.multMatrix_output.matrixIn[1]
        parent_node.worldInverseMatrix[0] >> self.multMatrix_output.matrixIn[2]

        for index, axis in zip(range(3), 'xyz'):
            self.multiply.append(pm.createNode('multiply'))
            self.column_from_matrix.append(pm.createNode('columnFromMatrix'))
            parent_node.worldMatrix[0] >> self.column_from_matrix[-1].matrix
            self.column_from_matrix[-1].input.set(index)
            self.normalize.append(pm.createNode('normalize'))
            self.translate_constants.append(pm.createNode('floatConstant'))
            self.translate_constants[-1].inFloat.set(output_node.attr(f'translate{axis.upper()}').get())
            output_node.attr(f'translate{axis.upper()}').set(0)
            self.translate_constants[-1].outFloat >> self.multiply[index].input[0]
            self.column_from_matrix[-1].outputW >> self.four_by_four_normalized_matrix.attr(f'in3{index}')
            parent_node.attr(f'scale{axis.upper()}') >> self.multiply[index].input[1]
            self.multiply[-1].output >> self.four_by_four_translation_matrix.attr(f'in3{index}')
            self.name_convention.rename_name_in_format(self.multiply[-1],
                                                       self.column_from_matrix[-1],
                                                       self.normalize[-1], name=axis)
            parent_node.worldMatrix[0] >> self.column_from_matrix[-1].matrix

        for axis_index, axis in enumerate('XYZ'):
            for index, secondary_axis in enumerate('XYZ'):
                self.normalize[index].attr(f'output{axis}') >> self.four_by_four_normalized_matrix.attr(f'in{index}{axis_index}')
                self.column_from_matrix[index].attr(f'output{axis}') >> self.normalize[axis_index].attr(f'input{secondary_axis}')

        self.multMatrix_output.matrixSum >> output_node.offsetParentMatrix


if __name__ == '__main__':
    my_rig = RigSegmentScaleCompensate()
    my_rig.create_node_base(*pm.ls('L_fk02_arm_grp'))