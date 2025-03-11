import pymel.core as pm

from RMPY.rig import rigBase
from RMPY.rig import rigSegmentScaleCompensate


class RigFKModel(rigBase.BaseModel):
    def __init__(self, *args, **kwargs):
        super(RigFKModel, self).__init__(*args, **kwargs)


class RigFK(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', RigFKModel())
        super(RigFK, self).__init__(*args, **kwargs)
        self.joints = []

    def create_point_base(self, *args, **kwargs):
        kwargs['name'] = kwargs.pop('name', 'fk')
        segment_compensate = kwargs.pop('segment_compensate', True)
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
                if segment_compensate:
                    rig_segment_compensate = rigSegmentScaleCompensate.RigSegmentScaleCompensate(rig_system=self.rig_system)

                    rig_segment_compensate.create_node_base(reset_group, root_transform=self.root)

            # self.create.constraint.define_constraints(point=False, scale=True, parent=True, orient=False)
            # self.create.constraint.node_base(control, eachJoint, mo=True)
            self.create.constraint.matrix_node_base(control, eachJoint, mo=True)# , mo=True
            # eachJoint.segmentScaleCompensate.set(0)
            # pm.disconnectAttr(eachJoint.inverseScale)
        # joint_list[-1].segmentScaleCompensate.set(0)


if __name__ == '__main__':
    rig_fk = RigFK()
    # rig_fk.create_point_base(u'C_Hip01_reference_pnt', u'C_tail01_reference_pnt', u'C_tail02_reference_pnt',
    #                          u'C_tail03_reference_pnt', u'C_tail04_reference_pnt', u'C_tail05_reference_pnt',
    #                          orient_type='point_orient')
    rig_fk.create_point_base('L_arm01_reference_pnt', 'L_elbow01_reference_pnt', 'L_wrist01_reference_pnt')


