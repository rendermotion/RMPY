import pymel.core as pm
from RMPY.core import dataValidators
from RMPY.rig import rigBase
from RMPY.rig import rigObjectsOnCurve
from RMPY.rig import rigControlsForPoints


class BiasedControlModel(rigBase.BaseModel):
    def __init__(self, *args, **kwargs):
        super(BiasedControlModel, self).__init__(*args, **kwargs)
        self.drivers = None
        self.driver_points_parent = None
        self.biased_line = None
        self.frame_line = None
        self.result_points_parent = None
        self.result_points = []
        self.result = []
        self.connection_attribute_list = []
        self.clusters_parent = None


class BiasedControl(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(BiasedControl, self).__init__(*args, **kwargs)
        self._model = BiasedControlModel()

        self.drivers = None
        self.driver_points_parent = None
        self.biased_line = None
        self.frame_line = None
        self.result_points_parent = None
        self.result_points = []
        self.result = []
        self.connection_attribute_list = []
        self.clusters_parent = None

    def create_biased_controls(self, number_of_points, curve=None):
        if curve:
            self.biased_line = curve
        result = rigObjectsOnCurve.RigObjectsOnCurve(self.biased_line, number_of_nodes=number_of_points,
                                                     rig_system=self.rig_system
                                                     , object_type='spaceLocator', up_vector_type='scene')
        self.drivers = result.outputs
        self.driver_points_parent = pm.group(name='driverPoints', empty=True)
        pm.parent(self.drivers, self.driver_points_parent)
        self.name_convention.rename_name_in_format(self.driver_points_parent, useName=True)

        self.result_points_parent = pm.duplicate(self.driver_points_parent)[0]
        self.name_convention.rename_name_in_format(self.result_points_parent, name='resultPoints')
        for index, each in enumerate(self.result_points_parent.getChildren()):
            self.name_convention.rename_name_in_format(each, name='resultPoints', objectType='spaceLocator')
            self.name_convention.rename_name_in_format(self.drivers[index], name='driverPoints', objectType='spaceLocator')

            pm.pointConstraint(self.drivers[index], each, mo=False)
            #self.drivers[index].translateX >> each.translateX

            each.rotateX.set(0)
            each.rotateY.set(0)
            each.rotateZ.set(0)
        self.result_points = self.result_points_parent.getChildren()
        self.result = [each_point.translateX for each_point in self.result_points]
        return self.result

    def default_hieararchy(self):
        self.clusters_parent.setParent(self.rig_system.kinematics)
        self.driver_points_parent.setParent(self.rig_system.kinematics)
        self.result_points_parent.setParent(self.rig_system.kinematics)

        self.biased_line.setParent(self.rig_system.display)
        self.frame_line.setParent(self.rig_system.display)

        pm.parentConstraint(self.frame_line, self.result_points_parent)
        pm.scaleConstraint(self.frame_line, self.result_points_parent)

    def create_controls(self, curve=None):
        if not curve:
            curve = self.biased_line
        clusters_nodes, clusters = self.create.cluster.curve_base(curve)
        self.clusters_parent = pm.group(empty=True)
        self.name_convention.rename_name_in_format(self.clusters_parent, name='clusters')

        pm.parent(clusters, self.clusters_parent)
        controls_on_points = rigControlsForPoints.RigControlsForPoints()
        controls_on_points.create_point_base(*clusters, size=.1)

        self.controls = controls_on_points.controls

        for each_reset in controls_on_points.reset_controls:
            pm.parentConstraint(self.frame_line, each_reset, mo=True)
        pm.parent(controls_on_points.reset_controls, self.rig_system.controls)

    def create_biased_curve(self, curve_points=None):
        if curve_points is None:
            curve_points = [[0, 0, 0], [.25, 0, .25], [.75, 0, .75], [1, 0, 1]]

        self.biased_line = self.create.curve.point_base(*curve_points)
        self.biased_line = dataValidators.as_pymel_nodes(self.biased_line)
        self.name_convention.rename_name_in_format(self.biased_line, name='biasedCurve')
        self.frame_line = self.create.curve.point_base([0, 0, 0], [1, 0, 0],
                                                       [1, 0, 1], [0, 0, 1], [0, 0, 0],
                                                       degree=1)
        self.frame_line = dataValidators.as_pymel_nodes(self.frame_line)
        self.name_convention.rename_name_in_format(self.frame_line, name='frameCurve')

    def connect(self, connection_attribute_list):
        if len(connection_attribute_list) == len(self.result):
            self.connection_attribute_list = connection_attribute_list
            for index, each_attribute in enumerate(connection_attribute_list):
                self.result[index] >> each_attribute
        else:
            print ('Mismatch number of elements on connection attribute list and result list')

    def build(self, **kwargs):
        connection_attribute_list = kwargs.pop('connection_attribute_list', None)
        curve_points = kwargs.pop('curve_points', None)
        if connection_attribute_list:
            number_of_points = kwargs.pop('number_of_points', len(connection_attribute_list))
        else:
            number_of_points = kwargs.pop('number_of_points', 5)

        self.create_biased_curve(curve_points=curve_points)
        self.create_controls()
        self.create_biased_controls(number_of_points)
        if connection_attribute_list:
            self.connect(connection_attribute_list)
        self.default_hieararchy()


if __name__ == '__main__':
    biased = BiasedControl()
    biased.build(number_of_points=2)