from RMPY.rig import rigSimpleIk


class IKLeg(rigSimpleIk.SimpleIK):
    def __init__(self, *args, **kwargs):
        super(IKLeg, self).__init__(*args, **kwargs)

    def create_point_base(self, *args, **kwargs):
        root_joints, joints = self.create.joint.point_base(*args, orient_type='point_orient')
        self.reset_joints.append(root_joints)
        [self.joints.append(each) for each in joints]
        self.create_node_base(self.joints[0], self.joints[-1])


if __name__ == '__main__':
    ik_leg_rig = IKLeg()
    ik_leg_rig.create_point_base(u'L_leg01_reference_pnt', u'L_Knee01_reference_pnt', u'L_ankle01_reference_pnt')
    print ik_leg_rig.joints




