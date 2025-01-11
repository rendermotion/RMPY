from RMPY.rig import rigFK
import pymel.core as pm


class RigJawModel(rigFK.RigFK):
    def __init__(self):
        super(RigJawModel, self).__init__()


class RigJaw(rigFK.RigFK):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', RigJawModel())
        super(RigJaw, self).__init__(*args, **kwargs)

    def create_point_base(self, *args, **kwargs):
        super(RigJaw, self).create_point_base(*args, **kwargs)
        intermediate_reset, new_joint = self.create.joint.point_base(self.joints[0], name='intermediate')
        pm.addAttr(self.controls[0], ln='cornersFollow', k=True, min=0, max=1)
        self.reset_joints.append(intermediate_reset)
        self.joints.insert(1, new_joint[0])

        new_multiply_divide = pm.createNode('multiplyDivide')

        self.create.constraint.node_base(self.reset_controls[0], self.reset_joints[1])
        self.controls[0].rotate >> new_multiply_divide.input1
        self.controls[0].cornersFollow >> new_multiply_divide.input2X
        self.controls[0].cornersFollow >> new_multiply_divide.input2Y
        self.controls[0].cornersFollow >> new_multiply_divide.input2Z
        new_multiply_divide.output >> self.joints[1].rotate
        intermediate_reset.setParent(self.rig_system.joints)

        new_reset_static, new_joint_static = self.create.joint.point_base(self.joints[0], name='static')
        new_reset_static_intermediate, new_joint_static_intermediate = self.create.joint.point_base(self.joints[0],
                                                                                                    name='staticIntermediate')

        self.controls[0].rotate >> new_joint_static[0].rotate
        self.joints[1].rotate >> new_joint_static_intermediate[0].rotate
        new_reset_static.setParent(self.rig_system.joints)
        new_reset_static_intermediate.setParent(self.rig_system.joints)
        pm.select(clear=True)
        new_joint = pm.joint()
        self.name_convention.rename_name_in_format(new_joint, name='zeroTransform')
        new_joint.setParent(self.rig_system.joints)




if __name__ == '__main__':
    jaw_rig = RigJaw()
    jaw_rig.create_point_base('C_jaw01_reference_pnt', 'C_jawTip01_reference_pnt')
    jaw_rig.rename_as_skinned_joints()

