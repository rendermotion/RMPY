from RMPY.rig import rigBase
import pymel.core as pm


class SimpleIKModel(rigBase.BaseModel):
    def __init__(self):
        super(SimpleIKModel, self).__init__()
        self.ik_handle = None
        self.effector = None
        self.start_joint = None
        self.end_joint = None
        self.pole_vector_constraint = None
        self.pole_vector = None


class SimpleIK(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        if 'model' not in kwargs.keys():
            kwargs['model'] = SimpleIKModel()
        super(SimpleIK, self).__init__(*args, **kwargs)

    @property
    def ik_handle(self):
        return self._model.ik_handle

    @property
    def effector(self):
        return self._model.effector

    @property
    def start_joint(self):
        return self._model.start_joint

    @property
    def end_joint(self):
        return self._model.end_joint

    @property
    def pole_vector_constraint(self):
        return self._model.pole_vector_constraint

    @property
    def pole_vector(self):
        return self._model.pole_vector

    def create_node_base(self, *joints, **kwargs):
        """
        :param joints: two joints, start and end of the ik handle
        :param kwargs:
        :return:
        """
        super(SimpleIK, self).create_point_base(*joints, **kwargs)
        self._model.start_joint = joints[0]
        self._model.end_joint = joints[1]
        self._model.ik_handle, self._model.effector = pm.ikHandle(sj=joints[0], ee=joints[1])
        self.name_convention.rename_name_in_format(self.ik_handle, name='ikHandle')
        self.name_convention.rename_name_in_format(self.effector, name='effector')
        self.ik_handle.setParent(self.rig_system.kinematics)

    def create_point_base(self, *args, **kwargs):
        super(SimpleIK, self).create_point_base(*args, **kwargs)
        root_joints, joints = self.create.joint.point_base(*args, orient_type='point_orient')
        root_joints.setParent(self.rig_system.joints)
        self.reset_joints.append(root_joints)
        [self.joints.append(each) for each in joints]
        self.create_node_base(self.joints[0], self.joints[-1])

    def set_as_pole_vector(self, control):
        self._model.pole_vector = control
        self._model.pole_vector_constraint = pm.poleVectorConstraint(self.pole_vector, self.ik_handle, name="poleVector")
        self.name_convention.rename_name_in_format(self.pole_vector_constraint)


if __name__ == '__main__':
    simple_ik = SimpleIK()
    simple_ik.create_point_base()