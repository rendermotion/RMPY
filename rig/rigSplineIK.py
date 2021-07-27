import pymel.core as pm
from RMPY.rig import rigBase
from RMPY.core import config


class RigSplineIKModel(rigBase.BaseModel):
    def __init__(self):
        super(RigSplineIKModel, self).__init__()
        self.ik = None
        self.effector = None
        self.curve = None


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
        self._model.reset_joints, self._model.joints = self.create.joint.point_base(*args, orient_type='point')
        self._model.ik, self._model.effector, self._model.curve = pm.ikHandle(startJoint=self.joints[0],
                                                                              endEffector=self.joints[-1],
                                                                              createCurve=True,
                                                                              numSpans=len(self.joints),
                                                                              solver="ikSplineSolver",
                                                                              name="splineIK")
        self.name_convention.rename_name_in_format([self.ik, self.effector, self.curve])
        self.reset_joints.setParent(self.rig_system.joints)
        self.curve.setParent(self.rig_system.kinematics)
        self.ik.setParent(self.rig_system.kinematics)

    def stretchy_ik(self):
        new_curve_info = pm.createNode('curveInfo')
        self.name_convention.rename_name_in_format(new_curve_info)
        self.curve.worldSpace[0] >> new_curve_info.inputCurve
        start_length = new_curve_info.arcLength.get()
        # start_char = ord('A')
        for index, each_joint in enumerate(self.joints[1:]):
            unit_conversion = pm.createNode('unitConversion')
            scale_multiply = pm.createNode('multiplyDivide')
            unit_conversion.conversionFactor.set(each_joint.translateX.get()/start_length)
            new_curve_info.arcLength >> unit_conversion.input
            unit_conversion.output >> scale_multiply.input1X
            scale_multiply.outputX >> each_joint.translateX
            self.reset_joints.scaleX >> scale_multiply.input2X
            scale_multiply.operation.set(2)

            # pm.addAttr(self.rig_system.settings, ln='jointScale{}'.format(chr(start_char + index)),
            #            at='double', k=True)
            # self.rig_system.settings.attr('jointScale{}'.format(chr(start_char + index))).set()

    def setup_twist(self, start_orient_object, end_orient_object):
        self.ik.dTwistControlEnable.set(True)
        self.ik.dWorldUpType.set(4)
        self.ik.dForwardAxis.set(int(config.axis_order_index[0] * 2))
        self.ik.dWorldUpAxis.set('Positive {}'.format(config.axis_order[1].upper()))
        start_orient_object.worldMatrix[0] >> self.ik.dWorldUpMatrix
        end_orient_object.worldMatrix[0] >> self.ik.dWorldUpMatrixEnd


if __name__ == '__main__':
    rig_spine = RigSplineIK()
    spine_root = pm.ls('C_Spine01_reference_pnt')[0]
    spine_points = [u'C_Spine01_reference_pnt', u'C_Spine02_reference_pnt', u'C_Spine03_reference_pnt',
                    u'C_Spine04_reference_pnt', u'C_Spine05_reference_pnt']
    rig_spine.create_point_base(*spine_points)
    rig_spine.stretchy_ik()

