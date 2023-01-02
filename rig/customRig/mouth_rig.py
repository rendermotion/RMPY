from RMPY.rig import rigLaces
import pymel.core as pm


def build():
    root_upper_lip = pm.ls('C_upperLip00_reference_grp')[0]
    upper_mouth = rigLaces.RigLaces()
    upper_mouth.create_point_base(*root_upper_lip.getChildren(), link_type='static')
    upper_mouth.rename_as_skinned_joints()
    print upper_mouth.zero_joint

    root_lower_lip = pm.ls('C_lowerLip00_reference_grp')[0]
    lower_mouth = rigLaces.RigLaces()
    lower_mouth.create_point_base(*root_lower_lip.getChildren(), link_type='static')
    lower_mouth.rename_as_skinned_joints()
    print lower_mouth.zero_joint

    upper_mouth.create.constraint.node_base('C_joint00_head_sknjnt', upper_mouth.rig_system.controls, mo=True)
    lower_mouth.create.constraint.node_base('C_joint00_jaw_sknjnt', lower_mouth.rig_system.controls, mo=True)


if __name__ == '__main__':
    build()