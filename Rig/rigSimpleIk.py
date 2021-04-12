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
        """
        Sets any given transform as a pole vector
        control (transform): The transform node that will become the pole vector.
        """
        self._model.pole_vector = control
        self._model.pole_vector_constraint = pm.poleVectorConstraint(self.pole_vector, self.ik_handle, name="poleVector")
        self.name_convention.rename_name_in_format(self.pole_vector_constraint)

    def create_pole_vector(self):
        """
        Creates a pole vector control on the correct position respect to the joint orientation.
        And sets this new control as the pole vector.
        :return:
        """
        pole_vector = self.create.space_locator.pole_vector(*self.joints)
        pm.parent(pole_vector, self.rig_system.kinematics)
        self.set_as_pole_vector(pole_vector)

    def create_controls(self):
        """
        Creates the Ik standard controls for Ik FK and pole vector if it doesn't exist.
        :return:
        """
        reset_controls,  ik_control = self.create.controls.point_base(self.ik_handle)
        self.create.constraint.node_base(ik_control, self.ik_handle)
        if self.pole_vector:
            reset_pole_vector_controls,  pole_vector_control = self.create.controls.point_base(self.pole_vector)
        self.create.constraint.node_base(pole_vector_control, self.pole_vector)
        arm_reset, arm_control = self.create.controls.point_base(self.joints[0])
        arm_control.rotate >> self.joints[0].rotate
        forearm_reset, forearm_control = self.create.controls.point_base(self.joints[1])
        forearm_control.rotate >> self.joints[1].rotate
        forearm_reset.setParent(arm_control)
        pm.parent([arm_reset, reset_pole_vector_controls, reset_controls], self.rig_system.controls)


if __name__ == '__main__':
    simple_ik = SimpleIK()
    simple_ik.create_point_base(u'L_shoulder01_reference_pnt', u'L_elbow01_reference_pnt', u'L_wrist01_reference_pnt')
    simple_ik.create_pole_vector()
    simple_ik.create_controls()