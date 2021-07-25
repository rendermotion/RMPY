import pymel.core as pm
from RMPY.rig import rigBase


class ModelSingleJoint(rigBase.BaseModel):
    def __init__(self):
        super(ModelSingleJoint, self).__init__()


class RigSingleJoint(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(RigSingleJoint, self).__init__(*args, ** kwargs)
        self._model = ModelSingleJoint()

    def create_point_base(self, *locator_list, **kwargs):
        super(RigSingleJoint, self).create_point_base(*locator_list, **kwargs)
        static = kwargs.pop('static', False)
        scaleXZ = kwargs.pop('scaleXZ', False)

        for each in locator_list:
            reset_joint = pm.group(empty=True, name='resetJoint')
            print 'align {} {}'.format(each, reset_joint)
            self.rm.align(each, reset_joint)
            joint = pm.joint(name='joint')
            self.rm.align(joint, reset_joint)

            self.joints.append(joint)
            self.name_convention.rename_name_in_format(reset_joint, useName=True)
            self.name_convention.rename_name_in_format(joint)

            joint.setParent(reset_joint)
            reset_control, control = self.create.controls.point_base(joint, **kwargs)
            self.reset_controls.append(reset_control)
            self.controls.append(control)
            reset_control.setParent(self.rig_system.controls)
            reset_joint.setParent(self.rig_system.joints)
            if static:
                control.translate >> joint.translate
                control.rotate >> joint.rotate
            else:
                pm.parentConstraint(control, joint)

            if scaleXZ:
                pm.addAttr(control, longName='scaleXZ', at=float, k=True)
                control.scaleXZ.set(1)
                control.scaleXZ >> control.scaleX
                control.scaleXZ >> control.scaleZ
                control.scaleXZ >> joint.scaleX
                control.scaleXZ >> joint.scaleZ


if __name__ == '__main__':
    selection = pm.ls(selection=True)
    rig_joint = RigSingleJoint()
    rig_joint.create_point_base(*selection, static=True, scaleXZ=True)









