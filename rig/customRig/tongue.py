from RMPY.rig import rigLaces
from RMPY.rig import rigSplineIK
from RMPY.rig import rigFK
from RMPY.rig import rigFollowPosition
import pymel.core as pm
reload(rigLaces)


def build():
    tongue_base_root = pm.ls('C_tongueBase00_reference_grp')[0]
    rig_tongue_base = rigLaces.RigLaces()
    rig_tongue_base.create_point_base(*tongue_base_root.getChildren(), single_orient_object=True, joint_number=1)
    tongue_root = pm.ls('C_tongue00_reference_grp')[0]
    rig_spline_tongue = rigSplineIK.RigSplineIK()
    rig_spline_tongue.create_point_base(*tongue_root.getChildren(), curve=rig_tongue_base.curve)
    rig_tongue = rigFK.RigFK()
    rig_tongue.create_point_base(*rig_spline_tongue.joints,   orient_type='point_orient')
    rig_tongue.create.constraint.node_base(rig_spline_tongue.joints[0], rig_tongue.reset_controls[0])

    for each_joint, each_reset in zip(rig_spline_tongue.joints[1:], rig_tongue.reset_controls[1:]):
        rig_follow_position = rigFollowPosition.FollowPosition()
        rig_follow_position.build(each_reset, each_joint)

    pm.addAttr('C_joint00_jaw_ctr', ln='tongue_out', proxy=rig_spline_tongue.ik.offset, k=True)
    print rig_tongue_base.reset_controls
    for parent, index_sets in zip(['C_joint02_Spine_sknjnt', 'C_joint00_neck_ctr', 'C_joint00_jaw_ctr'],
                                  [(0, 4), (4, 7), (7, 24)]):
        for index in range(*index_sets):
            rig_tongue_base.create.constraint.node_base(parent, rig_tongue_base.reset_controls[index], mo=True)
    rig_tongue.rename_as_skinned_joints()


if __name__ == '__main__':
    build()
