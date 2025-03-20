from RMPY.rig import rigBase
import pymel.core as pm

for required_plugings in ['matrixNodes']:
    if not required_plugings in pm.pluginInfo(q=True, listPlugins=True):
        pm.loadPlugin(required_plugings)
        print('plugin {} loaded'.format(required_plugings))
    else:
        print('plugin maya muscle already loaded')

"""

A rig to follow the position of an object.
 
"""


class FollowPosition(rigBase.RigBase):
    def __init__(self, *args, **klwargs):
        super(FollowPosition, self).__init__(*args, **klwargs)

    def build(self, main_point,  offset_parent_reference, offset_reference, local_offset):

        # decompose_matrix = pm.createNode('decomposeMatrix')
        # self.name_convention.rename_name_in_format(decompose_matrix)
        # decompose_matrix.inputRotateOrder.set(5)
        # decompose_matrix.outputTranslate >> main_point.translate
        # decompose_matrix.outputRotate >> main_point.rotate
        child_offset = pm.createNode('holdMatrix', name='childOffset')
        initial_position = pm.createNode('holdMatrix', name='initialPosition')
        child_offset.inMatrix.set(offset_parent_reference.worldMatrix[0].get() * offset_reference.worldInverseMatrix[0].get())
        initial_position.inMatrix.set(main_point.matrix.get())
        main_point.rotate.set([0, 0, 0])
        main_point.translate.set([0, 0, 0])

        mult_matrix = pm.createNode('multMatrix', name='reposition')
        self.name_convention.rename_name_in_format(mult_matrix, child_offset, initial_position, useName=True)

        # offset_reference.matrix >> mult_matrix.matrixIn[0]
        child_offset.outMatrix >> mult_matrix.matrixIn[0]
        # local_offset.inverseMatrix >> mult_matrix.matrixIn[0]
        offset_reference.worldMatrix[0] >> mult_matrix.matrixIn[1]
        offset_parent_reference.worldInverseMatrix[0] >> mult_matrix.matrixIn[2]
        initial_position.outMatrix >> mult_matrix.matrixIn[3]
        mult_matrix.matrixSum >> main_point.offsetParentMatrix



if __name__ == '__main__':
    follow_position = FollowPosition()
    follow_position.build(*pm.ls('C_joint03_tongue_grp', 'C_joint00_tongue_ctr', 'C_joint02_tongue_jnt'))