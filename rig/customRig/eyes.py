from RMPY.rig import rigLaces
import pymel.core as pm


def build():
    root_upper_eye = pm.ls('L_upperEye00_reference_grp')[0]
    l_upper_eye = rigLaces.RigLaces()
    l_upper_eye.create_point_base(*root_upper_eye.getChildren(), link_type='static')
    l_upper_eye.rename_as_skinned_joints()

    root_lower_eye = pm.ls('L_lowerEye00_reference_grp')[0]
    l_lower_eye = rigLaces.RigLaces()
    l_lower_eye.create_point_base(*root_lower_eye.getChildren(), link_type='static')
    l_lower_eye.rename_as_skinned_joints()
    l_lower_eye.zero_joint

    root_upper_eye = pm.ls('R_upperEye00_reference_grp')[0]
    r_upper_eye = rigLaces.RigLaces()
    r_upper_eye.create_point_base(*root_upper_eye.getChildren(), link_type='static')
    r_upper_eye.rename_as_skinned_joints()

    root_lower_eye = pm.ls('R_lowerEye00_reference_grp')[0]
    r_lower_eye = rigLaces.RigLaces()
    r_lower_eye.create_point_base(*root_lower_eye.getChildren(), link_type='static')
    r_lower_eye.rename_as_skinned_joints()
    r_lower_eye.zero_joint

    l_upper_eye.create.constraint.node_base('C_joint00_head_ctr', l_upper_eye.rig_system.controls)
    l_lower_eye.create.constraint.node_base('C_joint00_head_ctr', l_lower_eye.rig_system.controls)
    r_upper_eye.create.constraint.node_base('C_joint00_head_ctr', r_upper_eye.rig_system.controls)
    r_lower_eye.create.constraint.node_base('C_joint00_head_ctr', r_lower_eye.rig_system.controls)



if __name__ == '__main__':
    build()