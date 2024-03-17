import pymel.core as pm
from RMPY.rig import rigBase


class ModelSingleJoint(rigBase.BaseModel):
    def __init__(self):
        super(ModelSingleJoint, self).__init__()
        self.root_node = None


class RigSingleJoint(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', ModelSingleJoint())
        super(RigSingleJoint, self).__init__(*args, ** kwargs)

    @property
    def root_node(self):
        if not self._model.root_node:
            self._model.root_node = pm.group(empty=True)
            self.name_convention.rename_name_in_format(self._model.root_node, name='rootNode')
            self._model.root_node.setParent(self.rig_system.controls)
            self.root = self._model.root_node

        return self._model.root_node

    def create_point_base(self, *locator_list, **kwargs):
        super(RigSingleJoint, self).create_point_base(*locator_list, **kwargs)
        static = kwargs.pop('static', False)
        scaleXZ = kwargs.pop('scaleXZ', False)

        for each in locator_list:
            reset_joint = pm.group(empty=True, name='resetJoint')
            self.rm.align(each, reset_joint)
            joint = pm.joint(name='joint')
            self.rm.align(joint, reset_joint)

            self.joints.append(joint)
            self.reset_joints.append(reset_joint)

            self.name_convention.rename_name_in_format(reset_joint, useName=True)
            self.name_convention.rename_name_in_format(joint)

            joint.setParent(reset_joint)

            reset_control, control = self.create.controls.point_base(joint, **kwargs)
            self.reset_controls.append(reset_control)
            self.controls.append(control)
            reset_control.setParent(self.root_node)
            reset_joint.setParent(self.rig_system.joints)

            if static:
                if self.name_convention.default_names['side'] == 'R':
                    control.translateX >> joint.translateX
                    control.translateY >> joint.translateY
                    self.create.connect.times_factor(control.translateZ, joint.translateZ, -1)

                    self.create.connect.times_factor(control.rotateX, joint.rotateX, -1)
                    self.create.connect.times_factor(control.rotateY, joint.rotateY, -1)
                    control.rotateZ >> joint.rotateZ





                else:
                    control.translate >> joint.translate
                    control.rotate >> joint.rotate
            else:
                self.create.constraint.node_base(control, joint, mo=True)

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
    rig_joint.create_point_base(*selection)









