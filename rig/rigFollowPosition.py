from RMPY.rig import rigBase
import pymel.core as pm

for required_plugings in ['matrixNodes']:
    if not required_plugings in pm.pluginInfo(q=True, listPlugins=True):
        pm.loadPlugin(required_plugings)
        print 'plugin {} loaded'.format(required_plugings)

    else:
        print 'plugin maya muscle already loaded'


class FollowPosition(rigBase.RigBase):
    def __init__(self, *args, **klwargs):
        super(FollowPosition, self).__init__(*args, **klwargs)

    def build(self, main_point,  offset_reference):

        decompose_matrix = pm.createNode('decomposeMatrix')
        self.name_convention.rename_name_in_format(decompose_matrix)
        decompose_matrix.inputRotateOrder.set(5)
        decompose_matrix.outputTranslate >> main_point.translate
        decompose_matrix.outputRotate >> main_point.rotate
        mult_matrix = pm.createNode('multMatrix')
        self.name_convention.rename_name_in_format(mult_matrix)
        offset_reference.matrix >> mult_matrix.matrixIn[0]
        # offset_reference.worldMatrix[0] >> mult_matrix.matrixIn[0]
        # offset_reference.worldInverseMatrix[0] >> mult_matrix.matrixIn[1]
        mult_matrix.matrixSum >> decompose_matrix.inputMatrix

if __name__ == '__main__':
    follow_position = FollowPosition()
    follow_position.build(*pm.ls('C_joint03_tongue_grp', 'C_joint00_tongue_ctr', 'C_joint02_tongue_jnt'))