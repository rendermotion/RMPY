from RMPY.rig import rigBase
import pymel.core as pm


class RigSegmentScaleCompensateModel(rigBase.BaseModel):
    def __init__(self):
        super(RigSegmentScaleCompensateModel, self).__init__()
        self.column_from_matrix = []
        self.multiply = []
        self.normalize = []
        self.z_normal = None
        self.multMatrix_output = None
        self.four_by_four_normalized_matrix = None
        self.four_by_four_translation_matrix = None
        self.translate_constants = []


class RigSegmentScaleCompensate(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        """
        The segment scale compensate rig is used mainly on fk setups to avoid shearing in scaling of children nodes.
        It is a setup that allows to scale a parent and even if you have a children that is rotate it will not shear.
        """
        kwargs['model'] = kwargs.pop('model', RigSegmentScaleCompensateModel())
        super(RigSegmentScaleCompensate, self).__init__(*args, **kwargs)

    def create_node_base(self, *args, **kwargs):
        super(RigSegmentScaleCompensate, self).create_node_base(*args, **kwargs)
        root_transform = kwargs.pop('root_transform', None)
        self.root = root_transform
        output_node = args[0]
        parent_node = output_node.getParent()
        self._model.four_by_four_normalized_matrix = pm.createNode('fourByFourMatrix', name = 'normalizedMatrix')
        self._model.four_by_four_translation_matrix = pm.createNode('fourByFourMatrix', name = 'translationMatrix')
        self._model.multMatrix_output = pm.createNode('multMatrix', name='finalTransform')
        self.name_convention.rename_name_in_format(self.four_by_four_normalized_matrix,
                                                   self.four_by_four_translation_matrix,
                                                   self.multMatrix_output, useName=True)

        self.four_by_four_translation_matrix.output >> self.multMatrix_output.matrixIn[0]
        if self.root:
            self.world_scale_matrix >> self.multMatrix_output.matrixIn[1]
        self.four_by_four_normalized_matrix.output >> self.multMatrix_output.matrixIn[2]
        parent_node.worldInverseMatrix[0] >> self.multMatrix_output.matrixIn[3]

        for index, axis in zip(range(3), 'xyz'):
            self.multiply.append(pm.createNode(f'multiply',
                                               name=f'multiply{axis.upper()}'))
            self.column_from_matrix.append(pm.createNode(f'columnFromMatrix',
                                                         name=f'columnFromMatrix{axis.upper()}'))
            parent_node.worldMatrix[0] >> self.column_from_matrix[-1].matrix
            self.column_from_matrix[-1].input.set(index)

            self.translate_constants.append(pm.createNode(f'floatConstant', name=f'originalTranslation{axis.upper()}'))
            self.name_convention.rename_name_in_format(self.multiply[-1],
                                                       self.column_from_matrix[-1],
                                                       useName=True)
            self.translate_constants[-1].inFloat.set(output_node.attr(f'translate{axis.upper()}').get())
            output_node.attr(f'translate{axis.upper()}').set(0)
            self.translate_constants[-1].outFloat >> self.multiply[index].input[0]
            self.column_from_matrix[-1].outputW >> self.four_by_four_normalized_matrix.attr(f'in3{index}')
            parent_node.attr(f'scale{axis.upper()}') >> self.multiply[index].input[1]
            self.multiply[-1].output >> self.four_by_four_translation_matrix.attr(f'in3{index}')
            """if axis == 'z':
                self._model.z_normal = pm.createNode('crossProduct', name='axisZ')
                self.normalize[0].output >> self.z_normal.input1
                self.normalize[1].output >> self.z_normal.input2
                self.normalize.append(self.z_normal)

            else:
                self.normalize.append(pm.createNode(f'normalize', name=f'normalize{axis.upper()}'))
                self.name_convention.rename_name_in_format(self.normalize[-1], useName=True)
            """
            self.normalize.append(pm.createNode(f'normalize', name=f'normalize{axis.upper()}'))
            self.name_convention.rename_name_in_format(self.normalize[-1], useName=True)
            parent_node.worldMatrix[0] >> self.column_from_matrix[-1].matrix

        for axis_index, axis in enumerate('XYZ'):
            for index, secondary_axis in enumerate('XYZ'):
                self.normalize[index].attr(f'output{axis}') >> self.four_by_four_normalized_matrix.attr(
                    f'in{index}{axis_index}')
                # if axis_index <= 1:
                #     self.column_from_matrix[index].attr(f'output{axis}') >> self.normalize[axis_index].attr(
                #         f'input{secondary_axis}')
                self.column_from_matrix[index].attr(f'output{axis}') >> self.normalize[axis_index].attr(
                    f'input{secondary_axis}')

                '''if axis_index <= 1:
                    self.normalize[index].attr(f'output{axis}') >> self.four_by_four_normalized_matrix.attr(f'in{index}{axis_index}')
                    self.column_from_matrix[index].attr(f'output{axis}') >> self.normalize[axis_index].attr(
                        f'input{secondary_axis}')
                    print(self.normalize)
                    print(index, axis_index)
                    print(f"connecting {self.column_from_matrix[index].attr(f'output{axis}')}")
                    print(f"to ... {self.normalize[axis_index].attr(f'input{secondary_axis}')}")

                    
                else:
                    self.z_normal.attr(f'output{axis}') >> self.four_by_four_normalized_matrix.attr(f'in{index}{axis_index}')
                '''
        self.multMatrix_output.matrixSum >> output_node.offsetParentMatrix


if __name__ == '__main__':
    my_rig = RigSegmentScaleCompensate()
    my_rig.create_node_base(*pm.ls('L_fk02_arm_grp'))