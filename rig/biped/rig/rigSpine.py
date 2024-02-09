import pymel.core as pm
from RMPY.rig import rigBase
from RMPY.rig import rigSplineIK
from RMPY.rig import rigFK


class SpineModel(rigBase.BaseModel):
    def __init__(self, *args, **kwargs):
        super(SpineModel, self).__init__(*args, **kwargs)
        self.rig_spline_ik = None


class RigSpine(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(RigSpine, self).__init__(*args, **kwargs)
        self._model = SpineModel()
        self.rig_spline_ik = rigSplineIK.RigSplineIK(rig_system=self.rig_system)
        self.fk_spine = rigFK.RigFK(rig_system=self.rig_system)

    @property
    def rig_spline_ik(self):
        return self._model.rig_spline_ik

    @rig_spline_ik.setter
    def rig_spline_ik(self, value):
        self._model.rig_spline_ik = value

    def create_point_base(self, *args, **kwargs):
        self.setup_name_convention_node_base(*args)
        self.update_name_convention()
        self.rig_system.create()
        self.rig_spline_ik.create_point_base(*args, **kwargs)
        self.rig_spline_ik._stretchy_ik()
        self.rig_spline_ik.curve = self.create.curve.curve_base(self.rig_spline_ik.curve, spans=2)
        cluster_node_list, cluster_handler_list = self.create.cluster.curve_base(self.rig_spline_ik.curve)
        cluster_group = pm.group(empty=True)
        self.name_convention.rename_name_in_format(cluster_group, name='clusters')
        cluster_group.setParent(self.rig_system.kinematics)
        pm.parent(cluster_handler_list, cluster_group)

        for index, (each_cluster, reference_point) in enumerate(zip(cluster_handler_list, args)):
            if index + 1 < len(cluster_handler_list):
                reset_control, control = self.create.controls.point_base(
                    reference_point, size=self.rm.point_distance(each_cluster, cluster_handler_list[index + 1])) # centered=True
            else:
                reset_control, control = self.create.controls.point_base(
                    reference_point,
                    size=self.rm.point_distance(each_cluster, cluster_handler_list[index - 1]))

            self.controls.append(control)
            self.reset_controls.append(reset_control)
            if index == 0:
                reset_control.setParent(self.rig_system.controls)
            else:
                reset_control.setParent(self.controls[-2])
            self.create.constraint.node_base(control, each_cluster)

        self._model.joints = self.rig_spline_ik.joints
        self._model.reset_joints = self.rig_spline_ik.reset_joints
        self._model.reset_controls = self.reset_controls
        self.create.constraint.scale(self.reset_controls, self.reset_joints)
        self._model.controls = self.controls
        self.rig_spline_ik.setup_twist(self.controls[0], self.controls[-1])


if __name__ == '__main__':
    rig_spine = RigSpine()
    spine_points = [u'C_spine01_reference_pnt', u'C_spine02_reference_pnt', u'C_spine03_reference_pnt',
                    u'C_spine04_reference_pnt', u'C_spine05_reference_pnt']
    rig_spine.create_point_base(*spine_points)
