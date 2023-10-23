from RMPY.rig import rigBase
import pymel.core as pm
from RMPY.core import config


class RigPistonModel(rigBase.BaseModel):
    def __init__(self):
        super(RigPistonModel, self).__init__()
        self.distance_between = None


class RigPiston(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', RigPistonModel())
        super(RigPiston, self).__init__(*args, **kwargs)
    """
    Creates a piston rig,  2 points as input,  it will have as output 2 joints that aim at each other. 
    the root and the tip are locators on this rig that control the position of those joints, and the up Y vector will 
    define the up vector orientation of each output joint. 
    The model has the following variables:
        :var distance_between: the distance between node that measures the distance between the output joints.
    """
    @property
    def distance_between(self):
        return self._model.distance_between

    def create_point_base(self, *args, **kwargs):
        """
        This is the main function to create the piston rig.
        :param args: accepts 2 points.
        :param kwargs:
            parent_root: the root of this rig will be constrained to this node.
            parent_tip: the tip of this rig will be constrained to this node.
            do_scale: if True the aim joints will be scaled based on the distance between them.
            This scale value will be proportional to the original distance between the points, when the rig was created.
        :return:
        """
        parent_root = kwargs.pop('parent_root', None)
        parent_tip = kwargs.pop('parent_tip', None)
        do_scale = kwargs.pop('do_scale', True)
        self.root, self.tip = self.create.space_locator.node_base(*args, name='main')
        aim_root, aim_tip = self.create.group.point_base(self.root, self.tip, type='child', name='aim')
        aim_vector = [0, 0, 0]
        aim_vector[config.axis_order_index[0]] = 1
        up_vector = [0, 0, 0]
        up_vector[config.axis_order_index[1]] = 1
        root_aim_constraint = pm.aimConstraint(self.root, aim_tip, aimVector=aim_vector,
                                               upVector=up_vector,
                                               worldUpType='objectrotation',
                                               worldUpObject=self.tip)
        tip_aim_constraint = pm.aimConstraint(self.tip, aim_root, aimVector=aim_vector,
                                              upVector=up_vector,
                                              worldUpType='objectrotation',
                                              worldUpObject=self.root)
        pm.parent([self.root, self.tip],  self.rig_system.kinematics)

        reset_joints, joints = self.create.joint.point_base(aim_root)
        self.reset_joints.append(reset_joints)
        self.joints.extend(joints)
        self.create.constraint.node_base(aim_root, reset_joints)
        reset_joints, joints = self.create.joint.point_base(aim_tip)
        self.create.constraint.node_base(aim_tip, reset_joints)
        self.reset_joints.append(reset_joints)
        self.joints.extend(joints)

        pm.parent(self.reset_joints, self.rig_system.joints)
        if parent_root:
            pm.parentConstraint(parent_root, self.root)
        if parent_tip:
            pm.parentConstraint(parent_tip, self.tip)

        if do_scale:
            self._do_scale_of_joints()

    def _do_scale_of_joints(self):
        self._model.distance_between = pm.createNode('distanceBetween')
        self.root.worldPosition >> self.distance_between.point1
        self.tip.worldPosition >> self.distance_between.point2
        multiply_divide = pm.createNode('multiplyDivide')
        self.name_convention.rename_name_in_format(self.distance_between, multiply_divide, name='jointScale')
        self.distance_between.distance >> multiply_divide.input1X
        multiply_divide.input2X.set(self.distance_between.distance.get())
        multiply_divide.operation.set(2)
        for each_joint in self.joints:
            for each_axis in 'XYZ':
                multiply_divide.outputX >> each_joint.attr('scale{}'.format(each_axis))


if __name__=='__main__':
    selection = pm.ls(selection=True)
    rig_piston = RigPiston()
    rig_piston.create_point_base(*selection)
