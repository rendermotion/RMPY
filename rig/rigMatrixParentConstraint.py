from RMPY.rig import rigBase
import pymel.core as pm

class RigParentConstraintModel(rigBase.BaseModel):
    def __init__(self):
        super(RigParentConstraintModel, self).__init__()
        self.column_from_matrix = []
        self.multiply = []
        self.normalize = []
        self.multMatrix_output = None
        self.four_by_four_normalized_matrix = None
        self.four_by_four_translation_matrix = None
        self.translate_constants = []
        self.rotation_offset = None

class RigParentConstraint(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', RigParentConstraintModel())
        super(RigParentConstraint, self).__init__(*args, **kwargs)

    def create_point_base(self,parent_node, child_node, **kwargs):
        super(RigParentConstraint, self).create_node_base(child_node, **kwargs)
        self._model.four_by_four_normalized_matrix = pm.createNode('fourByFourMatrix')
        self._model.four_by_four_translation_matrix = pm.createNode('fourByFourMatrix')
        self._model.multMatrix_output = pm.createNode('multMatrix')
        self._model.rotation_offset = pm.createNode('holdMatrix')

        self.four_by_four_translation_matrix.output >> self.multMatrix_output.matrixIn[1]
        self.rotation_offset.outMatrix >> self.multMatrix_output.matrixIn[0]
        self.four_by_four_normalized_matrix.output >> self.multMatrix_output.matrixIn[2]
        biological_parent = child_node.getParent()
        if biological_parent:
            biological_parent.worldInverseMatrix[0] >> self.multMatrix_output.matrixIn[3]

        offset_matrix = child_node.worldMatrix[0].get() * parent_node.worldInverseMatrix[0].get()
        translation_offset_vector = [offset_matrix.a30, offset_matrix.a31, offset_matrix.a32]
        offset_matrix.a30 = 0
        offset_matrix.a31 = 0
        offset_matrix.a32 = 0
        self.rotation_offset.inMatrix.set(offset_matrix)

        for index, axis in zip(range(3), 'xyz'):
            self.multiply.append(pm.createNode('multiply'))
            self.column_from_matrix.append(pm.createNode('columnFromMatrix'))
            parent_node.worldMatrix[0] >> self.column_from_matrix[-1].matrix
            self.column_from_matrix[-1].input.set(index)
            self.normalize.append(pm.createNode('normalize'))
            self.translate_constants.append(pm.createNode('floatConstant'))
            self.translate_constants[-1].inFloat.set(translation_offset_vector[index])
            child_node.attr(f'translate{axis.upper()}').set(0)
            child_node.attr(f'rotate{axis.upper()}').set(0)
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
                self.normalize[index].attr(f'output{axis}') >> self.four_by_four_normalized_matrix.attr(
                    f'in{index}{axis_index}')
                self.column_from_matrix[index].attr(f'output{axis}') >> self.normalize[axis_index].attr(
                    f'input{secondary_axis}')

        self.multMatrix_output.matrixSum >> child_node.offsetParentMatrix


if __name__ == '__main__':
    selection = pm.ls(selection=True)
    rig_parent_constraint = RigParentConstraint()
    rig_parent_constraint.create_point_base(*selection)

