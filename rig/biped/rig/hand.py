from RMPY.rig import rigBase
from RMPY.rig.biped.rig import finger
from RMPY.rig import rigSingleJoint
import pymel.core as pm
from RMPY.rig.biped.rig import arm
from RMPY.core import config


class HandModel(rigBase.BaseModel):
    def __init__(self):
        super(HandModel, self).__init__()
        self.fingers = []


class Hand(rigSingleJoint.RigSingleJoint):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', HandModel())
        super(Hand, self).__init__(*args, **kwargs)

    @property
    def fingers(self):
        return self._model.fingers

    @fingers.setter
    def fingers(self, value):
        self._model.fingers = value

    def create_point_base(self, *args, **kwargs):
        args = self.rm.dataValidators.as_pymel_nodes(args)
        super(Hand, self).create_point_base(args[0], name='main')
        for each in args[0].getChildren(type='transform'):
            new_finger = finger.Finger()
            new_finger.create_point_base(*self.rm.descendents_list(each))
            new_finger.set_parent(self.joints[-1])
            # self.create.constraint.node_base(self.joints[-1], new_finger.reset_controls[0], mo=True)
            self.fingers.append(new_finger)

    def rename_as_skinned_joints(self, nub=True):
        super(Hand, self).rename_as_skinned_joints(nub=nub)
        for each_rig in self.fingers:
            each_rig.rename_as_skinned_joints(nub=nub)
        # self.palm.rename_as_skinned_joints(nub=False)

    def set_parent(self, rig_object, **kwargs):
        """
        This is the default function to parent modules, when you set parent an object it will look for the
        root on the dictionary attachments. If this has not being asigned the default value will be the first element
        of the list rig_reset_controls. So you can asign what ever point you want to be the driver of all the rig
        or let the rig find it by itself.
        :param rig_object: object or rig that you expect to be the parent of the module.
        :return:
        """
        create_hierarchy_joints = kwargs.pop('create_hierarchy_joints', False)
        output_joint_rig = kwargs.pop('output_joint_rig', None)
        # self.create.constraint.define_constraints(point=True, scale=True, parent=False, orient=False)
        # print type(rig_object).__mro__
        if arm.Arm in type(rig_object).__mro__:
            # print '{} in constraining {} {}'.format(self.create.constraint.constraint_type, rig_object.tip, self.root)
            self.create.constraint.point(rig_object.tip, self.root, mo=True, **kwargs)
            # self.create.constraint.define_constraints(point=False, scale=False, parent=False, orient=True)
            if self.name_convention.get_from_name(self.controls[0], 'side') == 'R' and config.mirror_controls:
                self.create.connect.times_factor(self.controls[0].rotateX, rig_object.tip.rotateX, -1)
            else:
                self.controls[0].rotateX >> rig_object.tip.rotateX

            # self.create.constraint.orient(self.tip, rig_object.tip, mo=True, **kwargs)
        else:
            try:
                self.create.constraint.node_base(rig_object, self.root, mo=True, **kwargs)
            except AttributeError():
                raise AttributeError('not valid object to parent')
        self._create_output_points(rig_object,
                                   create_hierarchy_joints=create_hierarchy_joints,
                                   output_joint_rig=output_joint_rig)
        for each in self.fingers:
            each._create_output_points(self,
                                       create_hierarchy_joints=create_hierarchy_joints,
                                       output_joint_rig=output_joint_rig)


if __name__ == '__main__':
    palm_root = pm.ls('L_palm01_reference_pnt')[0]
    hand = Hand()
    hand.create_point_base(palm_root)