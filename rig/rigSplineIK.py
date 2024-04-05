import pymel.core as pm
from RMPY.rig import rigBase
from RMPY.core import config
from RMPY.rig import rigSingleJoint


class RigSplineIKModel(rigBase.BaseModel):
    def __init__(self):
        super(RigSplineIKModel, self).__init__()
        self.ik = None
        self.effector = None
        self.curve = None
        self.up_vector_rig = None


class RigSplineIK(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', RigSplineIKModel())
        super(RigSplineIK, self).__init__(*args, **kwargs)

    @property
    def ik(self):
        return self._model.ik

    @ik.setter
    def ik(self, value):
        self._model.ik = value

    @property
    def effector(self):
        return self._model.effector

    @effector.setter
    def effector(self, value):
        self._model.effector = value

    @property
    def curve(self):
        return self._model.curve

    @curve.setter
    def curve(self, value):
        self._model.curve = value

    def create_point_base(self, *args, **kwargs):
        super(RigSplineIK, self).create_point_base(*args, **kwargs)
        equidistant_points = kwargs.pop('equidistant_points', False)
        create_up_vectors = kwargs.pop('create_up_vectors', False)
        if equidistant_points:
            number_of_joints = kwargs.pop('number_of_joints', 10)
            self._create_equidistant_joints(number_of_joints)
        else:
            self._model.reset_joints, self._model.joints = self.create.joint.point_base(*args, orient_type='point_orient')
        self._model.curve = kwargs.pop('curve', None)
        stretchy_ik = kwargs.pop('stretchy_ik', True)
        if not self.curve:
            self.curve = self.create.curve.point_base(*pm.ls(args), ep=True)
        self._spline_ik_creation(stretchy_ik)
        if create_up_vectors:
            self._create_up_vectors()

    def create_curve_base(self, curve, **kwargs):
        number_of_joints = kwargs.pop('number_of_joints', 10)
        create_up_vectors = kwargs.pop('create_up_vectors', False)
        distance_between_joints = kwargs.pop('create_up_vectors', curve.length()/(number_of_joints-1))
        super(RigSplineIK, self).create_point_base(curve, **kwargs)

        self._create_equidistant_joints(number_of_joints, distance_between=distance_between_joints)
        stretchy_ik = kwargs.pop('stretchy_ik', True)
        self.curve = curve
        self._spline_ik_creation(stretchy_ik=stretchy_ik)
        if create_up_vectors:
            self._create_up_vectors()

    def _spline_ik_creation(self, stretchy_ik=False):
        self.root = self.curve
        self._model.ik, self._model.effector,  = pm.ikHandle(startJoint=self.joints[0],
                                                             endEffector=self.joints[-1],
                                                             createCurve=False,
                                                             curve=self.curve,
                                                             numSpans=len(self.joints),
                                                             solver="ikSplineSolver",
                                                             name="splineIK")

        self.name_convention.rename_name_in_format(self.ik, self.effector, self.curve)
        pm.parent(self.reset_joints, self.rig_system.joints)
        self.curve.setParent(self.rig_system.kinematics)
        self.ik.setParent(self.rig_system.kinematics)
        if stretchy_ik:
            self._stretchy_ik()
        else:
            self._non_stretchy_lenght()


    def _create_equidistant_joints(self, number_of_joints, distance_between=1):
        pm.select(clear=True)
        vector = pm.datatypes.Vector(0, 0, 0)
        vector[config.axis_order_index[0]] = 1 * distance_between
        self.reset_joints.append(pm.group(empty=True))
        for index in range(number_of_joints):
            new_joint = pm.joint(position=vector*float(index))
            self.joints.append(new_joint)
        self.name_convention.rename_name_in_format(*self.joints)
        self.name_convention.rename_name_in_format(*self.reset_joints, name='resetJoints')
        pm.parent(self.reset_joints[0], self.rig_system.joints)

    def _non_stretchy_lenght(self):
        pm.addAttr(self.rig_system.settings, ln='ropeLength', k=True)
        scale_division = pm.createNode('multiplyDivide')
        self.rig_system.settings.ropeLength.set(self.curve.length())
        self.rig_system.settings.ropeLength >> scale_division.input1X
        scale_division.operation.set(2)
        self.name_convention.rename_name_in_format(scale_division, name='curveLength')
        scale_division.input2X.set(len(self.joints)-1)
        for each_joint in self.joints[1:]:
            scale_division.outputX >> each_joint.translateX

    def _stretchy_ik(self):
        new_curve_info = pm.createNode('curveInfo')
        self.name_convention.rename_name_in_format(new_curve_info)
        self.curve.worldSpace[0] >> new_curve_info.inputCurve
        start_length = new_curve_info.arcLength.get()
        # start_char = ord('A')
        unit_conversion = pm.createNode('unitConversion')
        scale_multiply = pm.createNode('multiplyDivide')
        self.name_convention.rename_name_in_format(unit_conversion, scale_multiply, name='stretchyIK')
        unit_conversion.conversionFactor.set(1.0/len(self.joints))
        new_curve_info.arcLength >> unit_conversion.input
        for each_joint in self.joints[1:]:
            unit_conversion.output >> each_joint.translateX

            # pm.addAttr(self.rig_system.settings, ln='jointScale{}'.format(chr(start_char + index)),
            #            at='double', k=True)
            # self.rig_system.settings.attr('jointScale{}'.format(chr(start_char + index))).set()
    def _create_up_vectors(self):
        self._model.up_vector_rig = rigSingleJoint.RigSingleJoint()
        reset_control, control = self.create.controls.point_base(self.joints[0], name='upVectorStart', centered=True)
        self.reset_controls.append(reset_control)
        self.controls.append(control)
        reset_control, control = self.create.controls.point_base(self.joints[-2], name='upVectorEnd', centered=True)
        self.reset_controls.append(reset_control)
        pm.parent(self.reset_controls, self.rig_system.controls)
        self.controls.append(control)
        self.create.motion_path.node_base(*self.reset_controls, curve=self.curve)
        self._setup_twist()

    def _setup_twist(self):
        self.ik.dTwistControlEnable.set(True)
        self.ik.dWorldUpType.set(4)
        self.ik.dForwardAxis.set(int(config.axis_order_index[0] * 2))
        self.ik.dWorldUpAxis.set('Positive {}'.format(config.axis_order[1].upper()))
        self.controls[0].worldMatrix[0] >> self.ik.dWorldUpMatrix
        self.controls[1].worldMatrix[0] >> self.ik.dWorldUpMatrixEnd


if __name__ == '__main__':
    rig_spine = RigSplineIK()
    # spine_root = pm.ls('C_Spine01_reference_pnt')[0]
    spine_points = pm.ls('C_chain00_reference_grp')[0]

    rig_spine.create_point_base(*spine_points.getChildren(), stretchy_ik=True, create_up_vectors=True)


