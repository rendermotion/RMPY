from RMPY.core import dataValidators
import pymel.core as pm
from RMPY.creators import creatorsBase


class Constraint(creatorsBase.CreatorsBase):
    def __init__(self, *args, **kwargs):
        super(Constraint, self).__init__(*args, **kwargs)
        self.constraint_type = []
        self.define_constraints(**kwargs)

    def node_base(self, *args, **kwargs):
        if len(args) >= 2:
                self.constraint(*args, constraints_list=self.constraint_type, **kwargs)
        else:
            raise AttributeError('you should provide at least 2 attributes')

    def node_list_base(self, *args, **kwargs):
        if len(args) >= 2 and len(args[0]) == len(args[1]):
            for driver, driven in zip(args[0], args[1]):
                self.constraint(driver, driven, constraints_list=self.constraint_type, **kwargs)

    def define_constraints(self, **kwargs):
        parent = kwargs.pop('parent', True)
        point = kwargs.pop('point', False)
        orient = kwargs.pop('orient', False)
        scale = kwargs.pop('scale', True)
        if parent:
            self.constraint_type.append(pm.parentConstraint)
        if point:
            self.constraint_type.append(pm.pointConstraint)
        if orient:
            self.constraint_type.append(pm.orientConstraint)
        if scale:
            self.constraint_type.append(pm.scaleConstraint)

    def constraint(self, *args, **kwargs):
        constraints = []
        for each_constraint in self.constraint_type:
            constraints.append(each_constraint(*args, **kwargs))


if __name__ == '__main__':
    selection = pm.ls(selection=True)
    constraint = Constraint()
    constraint.node_base(*selection, mo=True)
