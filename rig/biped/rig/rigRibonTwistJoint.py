from RMPY.rig.biped.rig import rigRibon
from RMPY.rig.biped.rig import rigTwistJoints
import importlib
from RMPY.rig import rigMatrixParentConstraint


class RibbonTwistJointModel(rigRibon.RibonModel):
    def __init__(self):
        super(RibbonTwistJointModel, self).__init__()
        self.rig_twist_joints = None


class RibbonTwistJoint(rigRibon.Ribon):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', RibbonTwistJointModel())
        super(RibbonTwistJoint, self).__init__(*args, **kwargs)

    @property
    def rig_twist_joints(self):
        if not self._model.rig_twist_joints:
            self._model.rig_twist_joints = rigTwistJoints.TwistJoints(rig_system=self.rig_system)
        return self._model.rig_twist_joints
        
    def create_point_base(self, *args, **kwargs):
        self.rig_twist_joints.create_point_base(*args, **kwargs)
        super(RibbonTwistJoint, self).create_point_base(*args[1:], **kwargs)
        for joints, reset_controls in zip(self.rig_twist_joints.joints, self.reset_controls):
            parent_constraint = rigMatrixParentConstraint.RigParentConstraint()
            parent_constraint.create_point_base(joints, reset_controls)
        # self.create.constraint.node_list_base(self.rig_twist_joints.joints, self.reset_controls, mo=True)


if __name__ == '__main__':
    ribbon_twist = RibbonTwistJoint()
    ribbon_twist.create_point_base('L_clavicle00_clavicle_jnt', "L_intermediate00_shoulder_jnt",
                                   "L_intermediate01_shoulder_jnt", folicule_number=5)


