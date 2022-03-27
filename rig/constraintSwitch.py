import pymel.core as pm
from RMPY.rig import rigBase


class ConstraintSwitchModel(rigBase.BaseModel):
    def __init__(self):
        super(ConstraintSwitchModel, self).__init__()
        self.outputs = []
        self.list_a = []
        self.list_b = []
        self.constraints = []
        self.attribute_output_a = None
        self.attribute_output_b = None


class ConstraintSwitch(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        if 'model' not in kwargs.keys():
            kwargs['model'] = ConstraintSwitchModel()
        super(ConstraintSwitch, self).__init__(*args, **kwargs)
        self.constraint_func = {'parent': pm.parentConstraint,
                                'point': pm.pointConstraint,
                                'orient': pm.orientConstraint}

    @property
    def attribute_output_b(self):
        return self._model.attribute_output_b

    @attribute_output_b.setter
    def attribute_output_b(self, value):
        self._model.attribute_output_b = value

    @property
    def attribute_output_a(self):
        return self._model.attribute_output_a

    @attribute_output_a.setter
    def attribute_output_a(self, value):
        self._model.attribute_output_a = value

    @property
    def controls(self):
        return self._model.controls

    @controls.setter
    def controls(self, value):
        self._model.controls = value

    @property
    def outputs(self):
        return self._model.outputs

    @outputs.setter
    def outputs(self, value):
        self._model.outputs = value

    @property
    def constraints(self):
        return self._model.constraints

    @constraints.setter
    def constraints(self, value):
        self._model.constraints = value

    @property
    def list_a(self):
        return self._model.list_a

    @list_a.setter
    def list_a(self, value):
        self._model.list_a = value

    @property
    def list_b(self):
        return self._model.list_b

    @list_b.setter
    def list_b(self, value):
        self._model.list_b = value

    def build(self, list_a, list_b, **kwargs):
        control = kwargs.pop('control', None)
        self.create_list_base(list_a, list_b, **kwargs)
        if control:
            self.create_attribute_control(control, **kwargs)
            self.link_attribute_to_constraints()
            self.controls.append(control)

    def create_list_base(self, list_a, list_b, **kwargs):
        destination = kwargs.pop('destination', None)
        parent = kwargs.pop('parent', True)
        scale = kwargs.pop('scale', True)
        point = kwargs.pop('point', False)
        orient = kwargs.pop('orient', False)

        output_type = kwargs.pop('output_type', 'joint')
        root_group = pm.group(empty=True)
        self.name_convention.rename_name_in_format(root_group, name='intermediate')
        if output_type == 'group' or output_type == 'locator':
            root_group.setParent(self.rig_system.kinematics)
        else:
            root_group.setParent(self.rig_system.joints)
        if len(list_a) == len(list_b):
            for index, (constraint_a, constraint_b) in enumerate(zip(list_a, list_b)):
                if not destination:
                    if output_type == 'group':
                        output = self.create.group.point_base(constraint_a, name='intermediate')
                        output.setParent(root_group)
                    elif output_type == 'locator':
                        output = self.create.space_locator.point_base(constraint_a, name='intermediate')
                        output.setParent(root_group)
                    else:
                        if not self.joints:
                            reset, output = self.create.joint.point_base(constraint_a, name='intermediate')
                            reset.setParent(root_group)
                            self.reset_joints.append(reset)
                            self.joints.append(output[0])
                        else:
                            reset, output = self.create.joint.point_base(constraint_a, name='intermediate')
                            output[0].setParent(self.joints[-1])
                            self.joints.append(output[0])
                            pm.delete(reset)
                        self.joints[-1].segmentScaleCompensate.set(0)
                else:
                    output = destination[index]

                self.outputs.append(output)
                # self.create.constraint.define_constraints(parent=parent, scale=scale, point=point, orient=orient)
                self.create.constraint.node_base(constraint_a, output, parent=parent, scale=scale,
                                                 point=point, orient=orient)
                constraints = self.create.constraint.node_base(constraint_b, output, parent=parent, scale=scale,
                                                               point=point, orient=orient)
                # self.constraint_func[constraint_type](constraint_b, output)
                self.constraints.extend(constraints)

        else:
            print 'list_a and list_b should be the same size'

    def create_attribute_control(self, control, **kwargs):
        self.controls.append(control)
        attribute_name = kwargs.pop('attribute_name', 'space_switch')
        if attribute_name not in pm.listAttr(self.controls[0]):
            pm.addAttr(self.controls[0], ln=attribute_name, hnv=True, hxv=True, min=0, max=10, k=True)

        reverse = pm.shadingNode('reverse', asUtility=True, name="reverse")
        multiply = pm.createNode('unitConversion', name="multiplier")
        self.name_convention.rename_name_in_format(reverse)
        self.name_convention.rename_name_in_format(multiply)

        pm.connectAttr('{}.{}'.format(self.controls[0], attribute_name), "{}.input".format(multiply))
        pm.setAttr("{}.conversionFactor".format(multiply), 0.1)
        pm.connectAttr("{}.output".format(multiply), "{}.inputX".format(reverse))
        self.attribute_output_a = multiply.output
        self.attribute_output_b = reverse.outputX

    def link_attribute_to_constraints(self):
        for each_constraint in self.constraints:
            for attribute_control, weight_alias in zip([self.attribute_output_a, self.attribute_output_b],
                                                       each_constraint.getWeightAliasList()):
                attribute_control >> weight_alias


if __name__ == '__main__':
    pass