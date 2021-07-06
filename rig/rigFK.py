import pymel.core as pm

from RMPY.rig import rigBase


class RigFKModel(rigBase.BaseModel):
    def __init__(self, *args, **kwargs):
        super(RigFKModel, self).__init__(*args, **kwargs)


class RigFK(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(RigFK, self).__init__(*args, **kwargs)
        self._model = RigFKModel()
        self.joints = []

    def create_point_base(self, *args, **kwargs):
        super(RigFK, self).create_point_base(*args, **kwargs)

        reset_joints, joint_list = self.create.joint.point_base(*args, **kwargs)
        self.reset_joints.append(reset_joints)
        self.reset_joints[0].setParent(self.rig_system.joints)
        self.joints = joint_list

        for index, eachJoint in enumerate(joint_list[:-1]):
            reset_group, control = self.create.controls.point_base(eachJoint, **kwargs)
            self.reset_controls.append(reset_group)
            self.controls.append(control)
            if index == 0:
                reset_group.setParent(self.rig_system.controls)
            else:
                pm.parent(reset_group, self.controls[index-1])
            self.create.constraint.define_constraints(point=False, scale=True, parent=True, orient=False)
            self.create.constraint.node_base(control, eachJoint, mo=True)


if __name__ == '__main__':
    rig_fk = RigFK()
    rig_fk.create_point_base('L_clavicle01_reference_pnt', 'L_shoulder01_reference_pnt', 'L_elbow01_reference_pnt', 'L_wrist01_reference_pnt',  orient_type='point_orient')
    # rig_fk.create_point_base(u'R_leg01_reference_pnt', u'R_Knee01_reference_pnt', u'R_ankle01_reference_pnt')

