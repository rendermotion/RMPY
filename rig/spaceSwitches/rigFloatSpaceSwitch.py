from RMPY.rig.switches import rigFloatSwitch
from RMPY.rig.spaceSwitches import space
from RMPY.creators import constraint


class RigFloatSpaceSwitch(rigFloatSwitch.FloatSwitch):
    def __init__(self, space_a, space_b, **kwargs):
        super(RigFloatSpaceSwitch, self).__init__(space_a, space_b, **kwargs)

        self.constraints = dict(parent=kwargs.pop('parent', True),
                                point=kwargs.pop('point', False),
                                orient=kwargs.pop('orient', False),
                                scale=kwargs.pop('scale', False))
        self.constraint = constraint.Constraint(**self.constraints)
        self.spaces = [space_a, space_b]
        self.space_rigs_dict = {}

    def set_spaces(self, *args):
        for each_transform in args:
            self._set_space(each_transform)

    def _set_space(self, scene_transform):
        self.space_rigs_dict[scene_transform] = []
        for each_space in self.spaces:
            self.space_rigs_dict[scene_transform].append(space.RigSpace(scene_transform, each_space,
                                                                        rig_system=self.rig_system))

    def add_object(self, scene_transform, **kwargs):
        """
        Adds a new object to the constraints. This object will be constrained by the spaces and the switch of the spaces
        will be connected to the switch.
        :param scene_transform: The new object that will be constraned
        :param kwargs: kwargs that will be passed to the constraint like the mo flag.
        :return : None
        """
        self.set_spaces(scene_transform)
        for each_space_rig in self.space_rigs_dict[scene_transform]:
            constraints = self.constraint.node_base(each_space_rig.tip, scene_transform, **kwargs)
        self.connect_constraint(*constraints)

    def connect_constraint(self, *constraint_nodes):

        for each_constraint_node in constraint_nodes:
            weight_alias = each_constraint_node.getWeightAliasList()
            print weight_alias
            self.attribute_output >> weight_alias[0]
            self.attribute_output_false >> weight_alias[1]


if __name__ == '__main__':
    rig_float_space = RigFloatSpaceSwitch('C_ball00_pSphere_msh', 'C_cube00_pCube_msh', attribute_name='Orient',
                                          control='L_main_arm_ctrl', parent=False, orient=True)
    rig_float_space.add_object('L_armor_mover_pnt')




