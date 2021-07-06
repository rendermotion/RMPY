from RMPY.rig.biped.parts import reverseFeet
import pymel.core as pm
from RMPY.rig import rigFK
from RMPY.rig import constraintSwitch


class IkFkFeetModel(constraintSwitch.ConstraintSwitchModel):
    def __init__(self):
        super(IkFkFeetModel, self).__init__()
        self.ik_feet = None
        self.fk_feet = None


class IkFkFeet(constraintSwitch.ConstraintSwitch):
    def __init__(self):
        super(IkFkFeet, self).__init__()
        self._model = IkFkFeetModel()
        self.ik_feet = None
        self.fk_feet = None

    @property
    def ik_feet(self):
        return self._model.ik_feet

    @ik_feet.setter
    def ik_feet(self, value):
        self._model.ik_feet = value

    @property
    def fk_feet(self):
        return self._model.fk_feet

    @fk_feet.setter
    def fk_feet(self, value):
        self._model.fk_feet = value

    def create_point_base(self, *points, **kwargs):
        control = kwargs.pop('control', None)
        if control:
            self.ik_feet = reverseFeet.RigReverseFeet(rig_system=self.rig_system)
            self.ik_feet.create_point_base(*points)
            self.fk_feet = rigFK.RigFK(rig_system=self.rig_system)
            self.fk_feet.create_point_base(*points[:3])
            self.build(self.ik_feet.joints, self.fk_feet.joints, control=control, attribute_name='IkFkSwitch')

            for each_control in self.ik_feet.controls:
                self.attribute_output_a >> each_control.visibility

            for each_control, each_joint in zip(self.fk_feet.controls, self.fk_feet.joints):
                self.attribute_output_b >> each_control.visibility
                # scale_constraints = each_joint.parentMatrix[0].listConnections(type='scaleConstraint', plugs=True)
                # scale_constraints[0].disconnect()
        else:
            print 'you should provide a control on the kwargs'


if __name__ == '__main__':
    reference_root = pm.ls(u'L_ankleFeet01_reference_pnt', u'L_ball01_reference_pnt', u'L_toe01_reference_pnt',
                           u'L_footLimitBack01_reference_pnt', u'L_footLimitOuter01_reference_pnt',
                           u'L_footLimitInner01_reference_pnt')
    reverse_feet = IkFkFeet()
    reverse_feet.create_point_base(*reference_root, control='nurbsCircle1')