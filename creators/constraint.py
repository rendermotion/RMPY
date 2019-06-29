from RMPY.core import dataValidators
import pymel.core as pm
from RMPY.creators import creatorsBase


class Constraint(creatorsBase.CreatorBase):
    def __init__(self, *args, **kwargs):
        super(Constraint, self).__init__(**kwargs)

    def node_base(self, *args, **kwargs):
        parent = kwargs.pop('parent', True)
        point = kwargs.pop('point', False)
        orient = kwargs.pop('orient', False)
        scale = kwargs.pop('scale', True)
        constraint_type = []

        if parent:
            constraint_type.append(pm.parentConstraint)
        if point:
            constraint_type.append(pm.pointConstraint)
        if orient:
            constraint_type.append(pm.orientConstraint)
        if scale:
            constraint_type.append(pm.scaleConstraint)

        if len(args) >= 2:
            if parent:
                for each in args[1:]:
                    pm.parentConstraint()
            if len(args) == 2:
                if args[0].__class__ is not list and args[1].__class__ is not list:
                    self.constraint(args[0], args[1],
                                    constraints_list=constraint_type)
                    
        else:
            raise AttributeError('you should provide at least 2 attributes')