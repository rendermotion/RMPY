from RMPY.rig import rigBase
from RMPY.rig import rigSingleJoint
import pymel.core as pm


class RigFromHierarchyModel(rigSingleJoint.ModelSingleJoint):
    def __init__(self):
        super(RigFromHierarchyModel, self).__init__()
        self.rig_children = []



class RigFromHierarchy(rigSingleJoint.RigSingleJoint):# rigBase.RigBase
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', RigFromHierarchyModel())
        super(RigFromHierarchy, self).__init__(*args, **kwargs)
    def create_point_base(self, *points, **kwargs):
        for each in points:
            super(RigFromHierarchy, self).create_point_base(each, **kwargs)
            if each.getChildren(type='transform'):
                self.rig_children.append(RigFromHierarchy(rig_system = self.rig_system))
                self.rig_children[-1].create_point_base(*each.getChildren(type='transform'))
                self.rig_children[-1].set_parent(self)


if __name__ == '__main__':
    my_rig = RigFromHierarchy()
    my_rig.create_point_base(*pm.ls('C_base00_reference_pnt'))
