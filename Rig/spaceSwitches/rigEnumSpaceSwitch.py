from RMPY.rig.spaceSwitches import space
from RMPY.creators import constraint
from RMPY.rig.switches import rigEnumSwitch


class RigEnumSpaceSwitchModel(rigEnumSwitch.RigEnumSwitchModel):
    def __init__(self):
        super(RigEnumSpaceSwitchModel, self).__init__(RigEnumSpaceSwitchModel)
        self.space_switch = None
        self.alias_list = []
        self.space_rigs_dict = {}
        self.spaces = []


class RigEnumSpaceSwitch(rigEnumSwitch.RigEnumSwitch):
    def __init__(self, *spaces, **kwargs):
        """
        :param spaces: A string list of the objects that will be represented on the scene as spaces.
        Nothing will be done with this information untill you call the add_object function.
        :param kwargs:
        """
        if 'model' not in kwargs.keys():
            kwargs['model'] = RigEnumSpaceSwitchModel()
        super(RigEnumSpaceSwitch, self).__init__(*spaces, **kwargs)

        self.constraints = dict(parent=kwargs.pop('parent', True),
                                point=kwargs.pop('point', False),
                                orient=kwargs.pop('orient', False),
                                scale=kwargs.pop('scale', False))
        self._model.spaces = spaces
        self._model.alias_list = kwargs.pop('alias_list', [])
        self.constraint = constraint.Constraint(**self.constraints)

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
        self.set_spaces(scene_transform)
        if not self.switch:
            self.set_switches()
        for each_space_rig in self.space_rigs_dict[scene_transform]:
            constraints = self.constraint.node_base(each_space_rig.tip, scene_transform, **kwargs)
        self.connect_constraint(*constraints)

    def connect_constraint(self, *constraint_nodes):
        for each_constraint_node in constraint_nodes:
            for weight_alias, alias in zip(each_constraint_node.getWeightAliasList(), self.alias_list):
                self.switch[alias].attribute_output >> weight_alias


if __name__ == '__main__':
    rig_float_space = RigEnumSpaceSwitch('C_arm_ref_pnt', 'C_leg_ref_pnt',
                                         alias_list=['puntoA', 'puntoB'],
                                         attribute_name='Orient',
                                         control='nurbsCircle1', parent=False, orient=True)
    rig_float_space.add_object('pSphere1')