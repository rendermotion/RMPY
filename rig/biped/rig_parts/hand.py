from RMPY.rig import rigBase
from RMPY.rig.biped.rig_parts import finger
from RMPY.rig import rigSingleJoint
import pymel.core as pm


class HandModel(rigBase.BaseModel):
    def __init__(self):
        super(HandModel, self).__init__()
        self.fingers = []
        self.palm = rigSingleJoint.RigSingleJoint()


class Hand(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(Hand, self).__init__(*args, **kwargs)
        self._model = HandModel()
        self.fingers = []
        self.joints = []
        self.reset_joints = []
        self.reset_controls = []
        self.controls = []

    @property
    def fingers(self):
        return self._model.fingers

    @fingers.setter
    def fingers(self, value):
        self._model.fingers = value

    @property
    def palm(self):
        return self._model.palm

    def create_point_base(self, *args, **kwargs):
        args = self.rm.dataValidators.as_pymel_nodes(args)
        self.palm.create_point_base(args[0])
        for each in args[0].getChildren(type='transform'):
            new_finger = finger.Finger()
            print self.rm.descendents_list(each)
            new_finger.create_point_base(*self.rm.descendents_list(each))
            self.create.constraint.node_base(self.palm.joints[-1], new_finger.reset_controls[0], mo=True)
            self.fingers.append(new_finger)

        self.joints = self.palm.joints
        self.reset_joints = self.palm.reset_joints
        self.reset_controls = self.palm.reset_controls
        self.controls = self.palm.controls

    def rename_as_skinned_joints(self, nub=True):
        super(Hand, self).rename_as_skinned_joints(nub=nub)
        for each_rig in self.fingers:
            each_rig.rename_as_skinned_joints(nub=nub)
        self.palm.rename_as_skinned_joints(nub=False)


if __name__ == '__main__':
    palm_root = pm.ls('L_palm01_reference_pnt')[0]
    print palm_root
    hand = Hand()
    hand.create_point_base(palm_root)