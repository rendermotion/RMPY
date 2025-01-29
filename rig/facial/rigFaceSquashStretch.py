# a specific squash and stretch rig for the face.
from RMPY.rig import rigBase
from RMPY.rig import rigObjectsOnCurve
import pymel.core as pm


class FaceSquashStretchModel(rigBase.BaseModel):
    def __init__(self):
        super(FaceSquashStretchModel, self).__init__()
        self.curve = None
        self.rig_objects_on_curve=None


class RigFaceSquashStretch(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', FaceSquashStretchModel())
        super(RigFaceSquashStretch, self).__init__(*args, **kwargs)

    def create_point_base(self, *points, **kwargs):
        super(RigFaceSquashStretch, self).create_point_base(*points, **kwargs)
        self._model.curve = self.create.curve.point_base(*points, degree=2)
        pm.parent(self.curve, self.rig_system.kinematics)
        driver_points = self.create.space_locator.node_base(*points, name='drivers')
        reset_groups = self.create.group.point_base(*driver_points, name='resetPosition')
        pm.parent(reset_groups, self.rig_system.kinematics)
        for index, each in enumerate(driver_points):
            each.worldPosition[0] >> self.curve.controlPoints[index]
        self._model.rig_objects_on_curve = rigObjectsOnCurve.RigObjectsOnCurve(rig_system=self.rig_system)
        # up_vectors = self.create.space_locator.node_base(*points, name='upVectors')
        # for driver, up in zip(driver_points, up_vectors):
        #     pm.parent(up, driver)
        #     pm.parent(driver, self.rig_system.kinematics)
        # factor = self.rm.point_distance(up_vectors[0], up_vectors[-1])
        # pm.move(factor/5, *up_vectors, moveX=True, relative=True, localSpace=True)
        self.rig_objects_on_curve.create_curve_base(self.curve, number_of_nodes=3, object_type='joint',
                                                    up_vector_type='arrayRotation',  up_vector_array=driver_points)
        self.joints.extend(self.rig_objects_on_curve.joints)
        self.reset_joints.extend(self.rig_objects_on_curve.reset_joints)
        controls_list = self.create.controls.point_base(*driver_points, centered=True)

        for reset_control, controls in controls_list:
            pm.parent(reset_control, self.rig_system.controls)
            self.reset_controls.append(reset_control)
            self.controls.append(controls)

        for control, driver in zip(self.controls, driver_points):
            self.create.connect.static_connection(pm.ls(control)[0], driver)
            # self.create.constraint.matrix_node_base(pm.ls(control)[0], driver)

        pm.parentConstraint(self.controls[0], self.reset_controls[1])
        pm.parentConstraint(self.controls[2], self.reset_controls[1])

        print(driver_points[0], driver_points[2],  reset_groups[1])
        pm.parentConstraint(driver_points[0], reset_groups[1])
        pm.parentConstraint(driver_points[2], reset_groups[1])

        curve_info = pm.createNode('curveInfo')
        divide = pm.createNode('divide')
        multiply = pm.createNode('multiply')
        self.name_convention.rename_name_in_format(curve_info, divide, multiply, name='scaleRatio')
        self.curve.worldSpace >> curve_info.inputCurve
        pm.addAttr(self.rig_system.settings, ln='squashMultiplier', k=True)
        self.rig_system.settings.squashMultiplier.set(1)
        divide.input1.set(curve_info.arcLength.get())
        curve_info.arcLength >> divide.input2
        divide.output >> multiply.input[0]
        # self.rig_system.settings.worldScale >> multiply.input[1]
        self.rig_system.settings.squashMultiplier >> multiply.input[1]
        print(self.joints)
        print(self.reset_joints)
        multiply.output >> self.reset_joints[1].scaleY
        multiply.output >> self.reset_joints[1].scaleZ


if __name__ == '__main__':
    my_rig = RigFaceSquashStretch()
    my_rig.create_point_base('C_squash00_reference_pnt', 'C_squash01_reference_pnt',  'C_squash02_reference_pnt')
    print(my_rig.zero_joint)