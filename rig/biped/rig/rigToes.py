from RMPY.rig import rigBase
from RMPY.rig.biped.rig import finger
from RMPY.rig import rigSingleJoint
import pymel.core as pm
from RMPY.rig.biped.rig import arm


class ToesModel(rigBase.BaseModel):
    def __init__(self):
        super(ToesModel, self).__init__()
        self.fingers = []


class Toes(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', ToesModel())
        super(Toes, self).__init__(*args, **kwargs)
        self._model.fingers = []

    @property
    def fingers(self):
        return self._model.fingers

    def create_point_base(self, toes_root, **kwargs):
        super(Toes, self).create_point_base(toes_root, **kwargs)
        toes_root = self.rm.dataValidators.as_pymel_nodes(toes_root)[0]
        fingers_root = self.create.group.point_base(toes_root, type='world')
        toes_list = toes_root.getChildren(type='transform')
        self.attach_points['root'] = fingers_root
        fingers_root.setParent(self.rig_system.kinematics)

        for each in toes_list:
            new_finger = finger.Finger(rig_system=self.rig_system)
            new_finger.create_point_base(*self.rm.descendents_list(each))
            new_finger.set_parent(fingers_root)
            self.fingers.append(new_finger)

        self.reset_joints.extend(self.fingers[0].reset_joints)
        self.reset_controls.extend(self.fingers[0].reset_controls)
        self.controls.extend(self.fingers[0].controls)

    def rename_as_skinned_joints(self, nub=True):
        super(Toes, self).rename_as_skinned_joints(nub=nub)
        for each_rig in self.fingers:
            each_rig.rename_as_skinned_joints(nub=nub)

    def set_parent(self, rig_object, **kwargs):
        super(Toes, self).set_parent(rig_object, **kwargs)
        create_hierarchy_joints = kwargs.pop('create_hierarchy_joints', False)
        output_joint_rig = kwargs.pop('output_joint_rig', None)
        for each in self.fingers:
            each._create_output_points(rig_object,
                                       create_hierarchy_joints=create_hierarchy_joints,
                                       output_joint_rig=output_joint_rig)

if __name__ == '__main__':
    toes_root_node = pm.ls('L_toes00_reference_pnt')[0]
    toes_rig = Toes()
    toes_rig.create_point_base(toes_root_node)
    toes_rig.rename_as_skinned_joints()