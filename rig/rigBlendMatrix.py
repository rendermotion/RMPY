from RMPY.rig import rigBase
import pymel.core as pm

class RigBlendMatrixModel(rigBase.BaseModel):
    def __init__(self):
        super(RigBlendMatrixModel, self).__init__()
        self.blend_matrix = None
        self.matrix_mult = None
        self.offsets_blend_matrix = None

class RigBlendMatrix(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', RigBlendMatrixModel())
        super(RigBlendMatrix, self).__init__(*args, **kwargs)

    def create_node_base(self, *args, **kwargs):
        super(RigBlendMatrix, self).create_node_base(*args)
        drivers = args[:-1]
        driven = []
        maintain_offset = kwargs.pop('mo', False)
        #  set the drivers node list all nodes from the beginning of the list till the one before
        #  the last one are drivers the last object is going to be the driven.
        drivers = args[:-1]
        driven = args[-1]
        self._model.matrix_mult = pm.createNode('multMatrix')
        self.blend_matrix = pm.createNode('blendMatrix')
        self.name_convention.rename_name_in_format(self.matrix_mult, self.blend_matrix,
                                                   name=f'blend{self.name_convention.get_a_short_name(driven)}')

        if maintain_offset:
            self._model.offsets_blend_matrix = pm.createNode('blendMatrix')
            self.name_convention.rename_name_in_format(self.offsets_blend_matrix, name=f'offset{self.name_convention.get_a_short_name(driven)}')
            for index, driver in enumerate(drivers):
                print(driven.worldMatrix[0].get() * driver.worldInverseMatrix[0].get())
                self.offsets_blend_matrix.target[index].targetMatrix.set(driven.worldMatrix[0].get() * driver.worldInverseMatrix[0].get())
                # self.blend_matrix.target[index].weight >> self.offsets_blend_matrix.target[index].weight
            self.offsets_blend_matrix.outputMatrix >> self.matrix_mult.matrixIn[0]

        driven.translate.set(0, 0, 0)
        driven.rotate.set(0, 0, 0)
        driven.scale.set(1, 1, 1)

        for index, driver in enumerate(drivers):
            driver.worldMatrix[0] >> self.blend_matrix.target[index].targetMatrix
            if maintain_offset:
                self.blend_matrix.target[index].weight >> self.offsets_blend_matrix.target[index].weight
            # driver.worldMatrix[0] >> self.matrix_mult.matrixIn[1]
        self.blend_matrix.outputMatrix >> self.matrix_mult.matrixIn[1]
        self.matrix_mult.matrixSum >> driven.offsetParentMatrix

        if driven.getParent():
            driven.getParent().worldInverseMatrix[0] >> self.matrix_mult.matrixIn[2]

        if pm.objectType(driven) == 'joint':
            driven.jointOrient.set(0, 0, 0)


if __name__ == '__main__':
    selection = pm.ls(selection=True)
    my_rig = RigBlendMatrix()
    my_rig.create_node_base(*selection, mo=False)