from RMPY.rig import rigBase


class RigSpaceModel(rigBase.BaseModel):
    def __init__(self):
        super(RigSpaceModel, self).__init__()


class RigSpace(rigBase.RigBase):
    def __init__(self, reference_object, space_object, **kwargs):
        """
        It creates two transform nodes, one linked to the two objects

        Parameters
        ----------
        :param reference_object: the position of the object you want to constraint to this space,
                               a point will be created to show the position towards it is constraining,
                               the transform tip,  will be aligned in position and rotation to the reference object
        :param space_object: the root towards what you  want to constraint. a root object will be aligned to this space
                object, and constrained to it
        :param kwargs: Inherit from rigBase

        Other Parameters
        ----------
        :Keyword Arguments:
           name (string) = the name of the constraint that you want to have on the hierarchy.
        """
        super(RigSpace, self).__init__(reference_object, space_object, **kwargs)
        self._model = RigSpaceModel()
        self.name = kwargs.pop('name', 'spaceSwitch')
        self.setup_name_convention_node_base(reference_object)

        self.root = self.create.group.point_base(space_object, type='world', name=self.name)
        self.tip = self.create.group.point_base(reference_object, type='world', name=self.name)

        self.tip.setParent(self.root)
        self.root.setParent(self.rig_system.kinematics)
        self.create.constraint.parent(space_object, self.root)


if __name__ == '__main__':
    RigSpace('C_control_arm_ctr', 'C_refer_spine_pnt', name='object')



