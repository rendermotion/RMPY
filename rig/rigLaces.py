import pymel.core as pm
from RMPY.core import config
from RMPY.rig import rigBase

from RMPY.rig import rigObjectsOnCurve
from RMPY.rig import rigControlsForPoints


class RigLacesModel(rigBase.BaseModel):
    def __init__(self):
        super(RigLacesModel, self).__init__()
        self.clusters = None
        self.up_vector = None

        self.curve = None
        self.up_vector_curve = None

        self.rig_parent = None

        self.joints_parent = None

        self.controls_parent = None
        self.clusters_parent = None

        self.rig_outputs = None
        self.rig_up_vectors = None


class RigLaces(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', RigLacesModel())
        super(RigLaces, self).__init__(*args, **kwargs)
        self.clusters = []
        self.rig_outputs = None
        self.rig_up_vectors = None
        self.no_controls = True

    @property
    def rig_outputs(self):
        return self._model.rig_outputs

    @rig_outputs.setter
    def rig_outputs(self, value):
        self._model.rig_outputs = value

    @property
    def rig_up_vectors(self):
        return self._model.rig_up_vectors

    @rig_up_vectors.setter
    def rig_up_vectors(self, value):
        self._model.rig_up_vectors = value

    @property
    def clusters(self):
        return self._model.clusters

    @clusters.setter
    def clusters(self, cluster_list):
        self._model.clusters = cluster_list

    @property
    def up_vector(self):
        if not self._model.up_vector:
            self._model.up_vector = rigControlsForPoints.RigControlsForPoints(rig_system=self.rig_system)
        return self._model.up_vector

    @property
    def clusters_parent(self):
        return self._model.clusters_parent

    @property
    def curve(self):
        return self._model.curve

    @property
    def root_controls(self):
        return self._model.controls_parent

    @property
    def up_vector_curve(self):
        return self._model.up_vector_curve

    def create_point_base(self, *points, **kwargs):
        super(RigLaces, self).create_point_base(*points)
        self.build_points = points
        points = self.rm.dataValidators.as_pymel_nodes(points)
        controls_number = kwargs.pop('controls_number', len(points))
        kwargs['offset_by_points'] = kwargs.pop('offset_by_points', True)
        joint_number = kwargs.pop('joint_number', controls_number*2)
        periodic = kwargs.pop('periodic', False)
        single_orient_object = kwargs.pop('single_orient_object', False)
        self.no_controls = kwargs.pop('no_controls', False)
        curve = self.create.curve.point_base(*points, periodic=periodic, ep=True)

        self.name_convention.set_from_name(curve, 'laceCurve', 'name')
        curve.setParent(self.rig_system.kinematics)
        if controls_number:
            self._model.curve = self.create.curve.curve_base(curve, spans=controls_number-1)
        else:
            self._model.curve = curve

        if not single_orient_object:
            self.laces_system_multiple_rotation_controls(joint_number, **kwargs)
        else:
            self.laces_system(joint_number)

    def create_curve_base(self, curve, **kwargs):
        super(RigLaces, self).create_curve_base(curve)
        joint_number = kwargs.pop('joint_number', 6)
        num_cvs = kwargs.pop('numCvs', curve.numCVs())
        if num_cvs == curve.numCVs():
            self._model.curve = curve
        else:
            self._model.curve = self.create.curve.curve_base(curve, spans=num_cvs)
        self.laces_system_multiple_rotation_controls(joint_number, **kwargs)

    def laces_system(self, joint_number, **kwargs):
        cluster_nodes, self.clusters = self.create.cluster.curve_base(self.curve)

        rig_objects_on_curve = rigObjectsOnCurve.RigObjectsOnCurve(self.curve,
                                                                   number_of_nodes=joint_number,
                                                                   up_vector_type="object", rig_system=self.rig_system)

        joints_group = pm.group(empty=True, name="skinJoints")
        clusters_group = pm.group(empty=True, name='clusters')

        self.name_convention.rename_name_in_format(joints_group, clusters_group, useName=True)

        pm.parent(clusters_group, self.rig_system.kinematics)
        pm.parent(joints_group, self.rig_system.joints)
        for eachJoint in rig_objects_on_curve.joints:
            pm.parent(eachJoint, joints_group)
            self.joints.append(eachJoint)
            self.rig_system.settings.worldScale >> eachJoint.scaleX
            self.rig_system.settings.worldScale >> eachJoint.scaleY
            self.rig_system.settings.worldScale >> eachJoint.scaleZ

        pm.parent(self.clusters, clusters_group)
        pm.parent(rig_objects_on_curve.up_vector, self.rig_system.kinematics)

        if not self.no_controls:
            create_controls = rigControlsForPoints.RigControlsForPoints()
            create_controls.create_point_base(*self.clusters, name='controls', **kwargs)

            self._model.controls = create_controls.controls
            self._model.reset_controls = create_controls.reset_controls
            pm.parent(create_controls.reset_controls, self.rig_system.controls)

        self.up_vector.create_point_base(rig_objects_on_curve.up_vector,
                                         name="upVector", **kwargs)

        pm.parent(self.up_vector.reset_controls[0], self.rig_system.kinematics)

        self.rig_system.settings.worldScale >> self.rig_system.controls.scaleX
        self.rig_system.settings.worldScale >> self.rig_system.controls.scaleY
        self.rig_system.settings.worldScale >> self.rig_system.controls.scaleZ

        self._model.controls_parent = self.rig_system.controls
        self._model.rig_parent = self.rig_system.root
        self._model.joints_parent = joints_group
        self._model.joints = rig_objects_on_curve.joints

    def laces_system_multiple_rotation_controls(self, joint_number, **kwargs):
        offset_vector = kwargs.pop('offset_vector', [0, 1, 0])
        fk_controls = kwargs.pop('fk_controls', False)
        offset_by_points = kwargs.pop('offset_by_points')

        if offset_by_points:
            curve_distance = kwargs.pop('curve_distance', self.curve.length()/len(self.build_points))
            new_points = self.create.space_locator.node_base(*self.build_points)
            move_axis = str(f'move{config.axis_order[1].capitalize()}')
            name_convention = dict()
            name_convention[move_axis] = True
            name_convention['objectSpace'] = True
            name_convention['relative'] = True
            pm.move(curve_distance, new_points, **name_convention)
            self._model.up_vector_curve = self.create.curve.point_base(*new_points, ep=True)
            pm.delete(new_points)
        else:
            self._model.up_vector_curve = pm.duplicate(self.curve)[0]
            self.up_vector_curve.translate.set(self.up_vector_curve.translate.get() + offset_vector)

        self.name_convention.rename_name_in_format(self._model.up_vector_curve, name='upVectorCurve')
        self.up_vector_curve.setParent(self.rig_system.kinematics)
        handlers, self.clusters = self.create.cluster.curve_base(self.curve, self.up_vector_curve)
        self._model.clusters_parent = pm.group(empty=True, name='clusters')
        self.name_convention.rename_name_in_format(self.clusters_parent, useName=True)
        pm.parent(self.clusters_parent, self.rig_system.kinematics)
        pm.parent(self.clusters, self.clusters_parent)

        if not self.no_controls:
            controls_group = pm.group(empty=True, name='laceControls')
            # self.name_convention.rename_name_in_format(controls_group, name='laceControls')

            create_controls = rigControlsForPoints.RigControlsForPoints(rig_system=self.rig_system)
            create_controls.create_point_base(*self.clusters, name="control", **kwargs)
            controls_group.setParent(self.rig_system.controls)
            self.name_convention.rename_name_in_format(controls_group, self.clusters_parent, useName=True)
            self._model.reset_controls = create_controls.reset_controls
            self._model.controls = create_controls.controls
            for index, eachControl in enumerate(create_controls.reset_controls):
                if not fk_controls:
                    pm.parent(eachControl, controls_group)
                else:
                    if index == 0:
                        pm.parent(eachControl, controls_group)
                    else:
                        pm.parent(eachControl, create_controls.controls[index - 1])
            self._model.controls_parent = controls_group
        self.laces_system_based_on_two_curves(joint_number)

    def laces_system_based_on_two_curves(self, joint_number):
        self.rig_up_vectors = rigObjectsOnCurve.RigObjectsOnCurve(self.up_vector_curve, up_vector_type='world',
                                                                  number_of_nodes=joint_number,
                                                                  rig_system=self.rig_system)
        self.rig_outputs = rigObjectsOnCurve.RigObjectsOnCurve(self.curve,
                                                               up_vector_type='array',
                                                               number_of_nodes=joint_number,
                                                               object_type='joint',
                                                               up_vector_array=self.rig_up_vectors.outputs,
                                                               rig_system=self.rig_system)
        self._model.joints = self.rig_outputs.joints


if __name__ == '__main__':
    rope_root = pm.ls(u'C_tail00_reference_pnt', u'C_tail01_reference_pnt', u'C_tail02_reference_pnt',
                      u'C_tail03_reference_pnt', u'C_tail04_reference_pnt', u'C_tail05_reference_pnt')
    laces_rig = RigLaces()
    laces_rig.create_point_base(u'C_tail00_reference_pnt', u'C_tail01_reference_pnt', u'C_tail02_reference_pnt',
                                u'C_tail03_reference_pnt', u'C_tail04_reference_pnt', u'C_tail05_reference_pnt',
                                single_orient_object=False,
                                offset_axis='y', centered=True, world_align=True)