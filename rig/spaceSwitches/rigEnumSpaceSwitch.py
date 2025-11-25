from RMPY.rig.spaceSwitches import space
from RMPY.creators import constraint
from RMPY.rig.switches import rigEnumSwitch
import pymel.core as pm


class RigEnumSpaceSwitchModel(rigEnumSwitch.RigEnumSwitchModel):
    def __init__(self):
        super(RigEnumSpaceSwitchModel, self).__init__()
        self.space_switch = None
        self.alias_list = []
        self.space_rigs_dict = {}
        self.spaces = []
        self.constraints_dictionary = {}


class RigEnumSpaceSwitch(rigEnumSwitch.RigEnumSwitch):
    def __init__(self, *spaces, **kwargs):
        """
        :param spaces: A string list of the objects that will be represented on the scene as spaces.
        Nothing will be done with this information untill you call the add_object function.
        :param kwargs:
        """
        kwargs['model'] = kwargs.pop('model', RigEnumSpaceSwitchModel())
        super(RigEnumSpaceSwitch, self).__init__(*spaces, **kwargs)

        if self.create.constraint._user_request_redefine_constraints(**kwargs):
            self.constraints = dict(parent=kwargs.pop('parent', False),
                                    point=kwargs.pop('point', False),
                                    orient=kwargs.pop('orient', False),
                                    scale=kwargs.pop('scale', False))
            # self.create.constraint.default_constraints = self.constraints
        else:
            self.constraints = {'parent': True, 'scale': True}
            # self.create.constraint.default_constraints = {'parent': True, 'scale': True}

        self._model.spaces = spaces
        self._model.alias_list = kwargs.pop('alias_list', [])
        # self.constraint = constraint.Constraint(**self.constraints)

    @property
    def space_rigs_dict(self):
        return self._model.space_rigs_dict

    @property
    def alias_list(self):
        return self._model.alias_list

    @property
    def spaces(self):
        return self._model.spaces

    @property
    def space_switch(self):
        return self._model.space_switch

    def set_spaces(self, *args):
        for each_transform in args:
            self._set_space(each_transform)

    def _set_space(self, scene_transform):
        self.space_rigs_dict[scene_transform] = []
        for each_space, alias_name in zip(self.spaces, self.alias_list):
            self.space_rigs_dict[scene_transform].append(space.RigSpace(scene_transform, each_space,
                                                                        rig_system=self.rig_system))

    def set_switches(self):
        self.add_enum_names(*self.alias_list, attribute_name=self.attribute_name)

    def add_object(self, scene_transform, **kwargs):
        """
        Adds a new object to the constraints. This object will be constrained by the spaces and the switch of the spaces
         will be connected to the switch
        :param scene_transform:
        :param kwargs:
        :return:
        """
        kwargs.update(self.constraints)
        self.set_spaces(scene_transform)
        offset = self.create.group.point_base(scene_transform, name='spaceSwitchOffset')
        if not self.switch:
            self.set_switches()
        for each_space_rig in self.space_rigs_dict[scene_transform]:
            constraints = self.create.constraint.node_base(each_space_rig.tip, offset, **kwargs)
            self.constraints_dictionary[each_space_rig] = constraints
        self.connect_constraint(*constraints)

    def connect_constraint(self, *constraint_nodes):
        for each_constraint_node in constraint_nodes:
            for weight_alias, alias in zip(each_constraint_node.getWeightAliasList(), self.alias_list):
                self.switch[alias].attribute_output >> weight_alias

            if pm.objectType(each_constraint_node) == 'orientConstraint':
                each_constraint_node.offsetX.set(-each_constraint_node.constraintRotateX.get())
                each_constraint_node.offsetY.set(-each_constraint_node.constraintRotateY.get())
                each_constraint_node.offsetZ.set(-each_constraint_node.constraintRotateZ.get())


if __name__ == '__main__':
    '''rig_float_space = RigEnumSpaceSwitch('C_arm_ref_pnt', 'C_leg_ref_pnt',
                                         alias_list=['puntoA', 'puntoB'],
                                         attribute_name='Orient',
                                         control='nurbsCircle1', parent=False, orient=True)
    rig_float_space.add_object('pSphere1')'''

    enum_space_switch = RigEnumSpaceSwitch('C_control02_world_ctr', 'R_intermediate01_shoulder_jnt',
                                                              alias_list=['world', 'arm'],
                                                              attribute_name = 'space',
                                                              control='R_object00_palm_ctr',
                                                              orient=True)
    enum_space_switch.add_object('R_object00_palm_ctr', mo=True)