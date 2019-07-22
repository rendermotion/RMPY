from RMPY.rig import rigBase
import pymel.core as pm
reload(rigBase)


class LineBetweenPointsModel(rigBase.BaseModel):
    def __init__(self):
        super(LineBetweenPointsModel, self).__init__()
        self.curve = None
        self.clusters = []


class LineBetweenPoints(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(LineBetweenPoints, self).__init__(*args, **kwargs)
        self._model = LineBetweenPointsModel()
        self.curve = None
        self.clusters = []
        
    @property
    def curve(self):
        return self._model.curve

    @curve.setter
    def curve(self, value):
        self._model.curve = value

    @property
    def clusters(self):
        return self._model.clusters

    @clusters.setter
    def clusters(self, value):
        if value.__class__ == list:
            self._model.clusters = value
        else:
            raise AttributeError('the attribute type should be a list')

    def create_point_base(self, *points, **kwargs):
        super(LineBetweenPoints, self).create_point_base(*points, **kwargs)
        self.curve = pm.curve(degree=1, p=[[0, 0, 0], [0, 0, 0]])
        self.name_convention.rename_based_on_base_name(points[0], self.curve, name="lineBetween")
        cluster_nodes, self.clusters = self.create.cluster.curve_base(self.curve)

        data_group = pm.group(em=True)
        self.name_convention.rename_name_in_format(data_group, name="lineBetweenData")
        data_group.setParent(self.rig_system.kinematics)

        for point, cluster in zip(points, self.clusters):
            self.create.constraint.parent(point, cluster, name="lineBetween", mo=False)
            pm.parent(cluster, data_group)
        pm.parent(self.curve, data_group)
        return data_group, self.curve


if __name__ == '__main__':
    source_points = pm.ls('C_Spine04_rig_pnt', 'C_Spine03_rig_pnt')
    line_between_points = LineBetweenPoints()
    line_between_points.create_point_base(*source_points)