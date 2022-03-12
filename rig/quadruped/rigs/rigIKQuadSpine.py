import pymel.core as pm
from RMPY.rig import rigBase
from RMPY.rig import rigSplineIK
from RMPY.rig import rigFK


class IKQuadSpineModel(rigBase.BaseModel):
    def __init__(self, *args, **kwargs):
        super(IKQuadSpineModel, self).__init__(*args, **kwargs)
        self.rig_spline_ik = None
        self.fk_spine = None


class RigIKQuadSpine(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(RigIKQuadSpine, self).__init__(*args, **kwargs)
        self._model = IKQuadSpineModel()
        self._model.rig_spline_ik = rigSplineIK.RigSplineIK(rig_system=self.rig_system)
        self._model.fk_spine = rigFK.RigFK(rig_system=self.rig_system)

    @property
    def rig_spline_ik(self):
        return self._model.rig_spline_ik

    @property
    def fk_spine(self):
        return self._model.fk_spine

    def create_point_base(self, *args, **kwargs):
        self.setup_name_convention_node_base(*args)
        hierarchize = kwargs.pop('hierarchize', True)
        kwargs['stretchy_ik'] = kwargs.pop('stretchy_ik', True)
        self.update_name_convention()
        self.rig_system.create()
        self.rig_spline_ik.create_point_base(*args, **kwargs)
        # self.rig_spline_ik.curve = self.create.curve.curve_base(self.rig_spline_ik.curve, spans=2)
        cluster_node_list, cluster_handler_list = self.create.cluster.curve_base(self.rig_spline_ik.curve)
        cluster_group = pm.group(empty=True)
        self.name_convention.rename_name_in_format(cluster_group, name='clusters')
        cluster_group.setParent(self.rig_system.kinematics)
        pm.parent(cluster_handler_list, cluster_group)
        controls_size = self.rm.point_distance(cluster_handler_list[0], cluster_handler_list[1])
        for index, reference_point in enumerate(args):
            reset_control, control = self.create.controls.point_base(reference_point, size=controls_size, centered=True)
            self.controls.append(control)
            self.reset_controls.append(reset_control)
            if hierarchize:
                if index == 0:
                    reset_control.setParent(self.rig_system.controls)
                else:
                    reset_control.setParent(self.controls[-2])
            else:
                reset_control.setParent(self.rig_system.controls)
            if index == 0:
                self.create.constraint.node_base(control, cluster_handler_list[0], mo=True)
                self.create.constraint.node_base(control, cluster_handler_list[1], mo=True)
            elif index == len(args)-1:
                self.create.constraint.node_base(control, cluster_handler_list[index + 1], mo=True)
                self.create.constraint.node_base(control, cluster_handler_list[index + 2], mo=True)
            else:
                self.create.constraint.node_base(control, cluster_handler_list[index+1], mo=True)

        self._model.joints = self.rig_spline_ik.joints
        self._model.reset_joints = self.rig_spline_ik.reset_joints
        self._model.reset_controls = self.reset_controls
        self.create.constraint.scale(self.reset_controls, self.reset_joints)
        self._model.controls = self.controls
        self.rig_spline_ik.setup_twist(self.controls[0], self.controls[-1])


if __name__ == '__main__':
    rig_spine = RigIKQuadSpine()
    spine_points = [u'C_spine00_reference_pnt', u'C_spine01_reference_pnt', u'C_spine02_reference_pnt',
                    u'C_spine03_reference_pnt', u'C_spine04_reference_pnt', u'C_spine05_reference_pnt']
    rig_spine.create_point_base(*spine_points, hierarchize=False)
