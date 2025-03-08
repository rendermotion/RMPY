import pymel.core as pm
from RMPY.rig import rigBase


class ModelSingleJoint(rigBase.BaseModel):
    def __init__(self):
        super(ModelSingleJoint, self).__init__()
        self.root_node = None


class RigSingleJoint(rigBase.RigBase):
    """
    The  single joint rig is the simplest rig you can create, it creates a control and a joint per each
    provided source locator. The control will drive the joint position.
    Every rig contains some lists inside to store the output joints, the controls and the reset groups of each one of those
    Whenever you create a control the best you can do is append this control and the reset control, to this lists.
    This lists are found on the base level of the class, so you can access them by self.joints, self.reset_joints,
    self.controls and self.resetControls

    .. code-block:: bash
       :caption: Creating a single joint based on selected locators.
       :emphasize-lines: 6

            from RMPY.rigs import rigSingleJoint
            selection = pm.ls(selection=True)
            rig_joint = rigSingleJoint.RigSingleJoint()
            rig_joint.create_point_base(*selection)
    """
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
        """
        This is the only function enabled to create a single joint rig.
        locator_list: type:spaceLocator the list of points where you want to create a single joint passed as arguments,
            the name of the points is very important since it will define the name of the output rigs.
            The naming is recalculated on each point created, so you can create multiple rigs with different
            names at the same time.

        """
        super(RigSingleJoint, self).create_point_base(*locator_list, **kwargs)
        static = kwargs.pop('static', False)
        scaleXZ = kwargs.pop('scaleXZ', False)

        for each in locator_list:
            self.setup_name_convention_node_base(each)
            reset_joint = pm.group(empty=True, name='resetJoint')

            pm.matchTransform(reset_joint, each)
            joint = pm.joint(name='joint')
            pm.matchTransform(reset_joint, joint)

            self.joints.append(joint)
            self.reset_joints.append(reset_joint)

            self.name_convention.rename_name_in_format(reset_joint, useName=True)
            self.name_convention.rename_name_in_format(joint)

            joint.setParent(reset_joint)

            reset_control, control = self.create.controls.point_base(joint, **kwargs)

            if self.reset_controls:
                if len(self.reset_controls) == 1:
                    self.reset_controls[0].setParent(self.root_node)
                reset_control.setParent(self.root_node)
            else:
                reset_control.setParent(self.rig_system.controls)

            reset_joint.setParent(self.rig_system.joints)
            self.reset_controls.append(reset_control)
            self.controls.append(control)
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









