import pymel.core as pm
from RMPY.creators import creatorsBase


class Constraint(creatorsBase.CreatorsBase):
    def __init__(self, *args, **kwargs):
        super(Constraint, self).__init__(*args, **kwargs)
        self.constraint_type = []
        self.define_constraints(**kwargs)

    def node_base(self, *args, **kwargs):
        super(Constraint, self).node_base(*args, **kwargs)
        if len(args) >= 2:
                return self.constraint(*args, **kwargs)
        else:
            raise AttributeError('you should provide at least 2 attributes')

    def node_list_base(self, *args, **kwargs):
        constraints_created = []
        if len(args) >= 2 and len(args[0]) == len(args[1]):
            for driver, driven in zip(args[0], args[1]):
                constraints_created.append(self.constraint(driver, driven, **kwargs))
        else:
            self.constraint_different_len_lists(*args, **kwargs)

        return constraints_created

    def point(self, *args, **kwargs):
        self.define_constraints(point=True, scale=False, parent=False, orient=False)
        return self.node_base(*args, **kwargs)

    def parent(self, *args, **kwargs):
        self.define_constraints(point=False, scale=False, parent=True, orient=False)
        return self.node_base(*args, **kwargs)

    def scale(self, *args, **kwargs):
        self.define_constraints(point=False, scale=True, parent=False, orient=False)
        return self.node_base(*args, **kwargs)

    def orient(self, *args, **kwargs):
        self.define_constraints(point=False, scale=False, parent=False, orient=True)
        return self.node_base(*args, **kwargs)

    def define_constraints(self, **kwargs):
        parent = kwargs.pop('parent', True)
        point = kwargs.pop('point', False)
        orient = kwargs.pop('orient', False)
        scale = kwargs.pop('scale', True)
        self.constraint_type = []
        if parent:
            self.constraint_type.append(pm.parentConstraint)
        if point:
            self.constraint_type.append(pm.pointConstraint)
        if orient:
            self.constraint_type.append(pm.orientConstraint)
        if scale:
            self.constraint_type.append(pm.scaleConstraint)

    def constraint(self, *args, **kwargs):
        print args[0]
        if args[0].__class__ is list:
            name = kwargs.pop('name', self.name_convention.get_a_short_name(args[0][0]))
        else:
            name = kwargs.pop('name', self.name_convention.get_a_short_name(args[0]))
        constraints_list = []
        for each_constraint in self.constraint_type:
            new_constraint = each_constraint(*args, **kwargs)
            constraints_list.append(new_constraint)
            self.name_convention.rename_name_in_format(new_constraint, name=name)
        return constraints_list

    def constraint_different_len_lists(self, drivers, driven, **kwargs):
        step_constraint = (float(len(drivers)) - 1.0) / (len(driven) - 1)
        for index, each in enumerate(driven):
            constraint_weight_value = step_constraint * index
            if int(constraint_weight_value) and constraint_weight_value % int(constraint_weight_value) == 0:
                self.constraint(drivers[int(constraint_weight_value)], each, w=1.0, **kwargs)
            else:
                if constraint_weight_value >= 1:
                    print constraint_weight_value
                    constraint_value = constraint_weight_value % int(constraint_weight_value)
                else:
                    constraint_value = constraint_weight_value
                self.constraint(drivers[int(constraint_weight_value)], each, w=1.0 - constraint_value, **kwargs)
                self.constraint(drivers[int(constraint_weight_value) + 1], each, w=constraint_value, **kwargs)


if __name__ == '__main__':
    locators = pm.ls('locator*', type='transform')
    nurbs_curves = pm.ls('nurb*', type='transform')
    selection = pm.ls(selection=True)
    constraint = Constraint()
    constraint.node_list_base(nurbs_curves, locators, mo=False)