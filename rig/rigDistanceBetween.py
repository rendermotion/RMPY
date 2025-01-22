from RMPY.rig import rigBase
import pymel.core as pm


class RigDistanceBetweenModel(rigBase.BaseModel):
    def __init__(self):
        super(RigDistanceBetweenModel, self).__init__()
        self.start_point = None 
        self.end_point = None
        self.distance_between = None


class RigDistanceBetween(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', RigDistanceBetweenModel())
        super(RigDistanceBetween, self).__init__(*args, **kwargs)
    @property
    def distance(self):
        return self.distance_between.distance

    def create_point_base(self, *args, **kwargs):
        constraint_to_args = kwargs.pop('constraint_to_args', True)
        self._model.start_point = pm.spaceLocator(name="startPoint")
        self.name_convention.rename_name_in_format(self.start_point, useName=True)
        self._model.end_point = pm.spaceLocator(name="endPoint")
        self.name_convention.rename_name_in_format(self.end_point, useName=True)
        self.start_point.setParent(self.rig_system.kinematics)
        self.end_point.setParent(self.rig_system.kinematics)

        if constraint_to_args:
            self.create.constraint.matrix_node_base(args[0], self.start_point)
            self.create.constraint.matrix_node_base(args[1], self.end_point)
        else:
            pm.matchTransform(self.start_point, args[0])
            pm.matchTransform(self.end_point, args[1])
        
        self._model.distance_between = pm.shadingNode("distanceBetween", asUtility=True, name="DistanceNode")
        self.name_convention.rename_name_in_format(self.distance_between, useName=True)
        
        pm.connectAttr(f"{self.start_point}.worldPosition[0]", f"{self.distance_between}.point1", f=True)
        pm.connectAttr(f"{self.end_point}.worldPosition[0]", f"{self.distance_between}.point2", f=True)


if __name__ == '__main__':
    selection = pm.ls(selection=True)
    distance_between = RigDistanceBetween()
    distance_between.create_point_base(*selection)














