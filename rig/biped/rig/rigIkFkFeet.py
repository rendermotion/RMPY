from RMPY.rig.biped.rig import reverseFeet
import pymel.core as pm
from RMPY.rig import rigFK
from RMPY.rig import constraintSwitch


class IkFkFeetModel(constraintSwitch.ConstraintSwitchModel):
    def __init__(self):
        super(IkFkFeetModel, self).__init__()
        self.ik_feet = None
        self.fk_feet = None


class IkFkFeet(constraintSwitch.ConstraintSwitch):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', IkFkFeetModel())
        super(IkFkFeet, self).__init__(*args, **kwargs)

    @property
    def ik_feet(self):
        return self._model.ik_feet

    @property
    def fk_feet(self):
        return self._model.fk_feet

    def create_point_base(self, *points, **kwargs):
        control = kwargs.pop('control', None)
        if control:
            self._model.ik_feet = reverseFeet.RigReverseFeet(rig_system=self.rig_system)
            self.ik_feet.create_point_base(*points)
            self._model.fk_feet = rigFK.RigFK(rig_system=self.rig_system)
            self.fk_feet.create_point_base(*points[:3], orient_type='point_orient')
            self.build(self.ik_feet.joints, self.fk_feet.joints, control=control, attribute_name='IkFkSwitch')

            for each_control in self.ik_feet.controls:
                self.attribute_output_a >> each_control.visibility

            for each_control, each_joint in zip(self.fk_feet.controls, self.fk_feet.joints):
                self.attribute_output_b >> each_control.visibility
                # scale_constraints = each_joint.parentMatrix[0].listConnections(type='scaleConstraint', plugs=True)
                # scale_constraints[0].disconnect()
        else:
            print('you should provide a control on the kwargs')


if __name__ == '__main__':
    reference_points_quadruped = pm.ls(u'L_paw00_reference_pnt', u'L_pawRoll00_reference_pnt',
                                       u'L_pawToe00_reference_pnt',
                                       u'L_footLimitBack00_reference_pnt', u'L_footLimitOuter00_reference_pnt',
                                       u'L_footLimitInner00_reference_pnt')

    reference_root = pm.ls(u'L_ankleFeet01_reference_pnt', u'L_ball01_reference_pnt',
                                       u'L_toe01_reference_pnt', u'L_footLimitBack01_reference_pnt',
                                       u'L_footLimitOuter01_reference_pnt', u'L_footLimitInner01_reference_pnt')
    reverse_feet = IkFkFeet()
    reverse_feet.create_point_base(*reference_points_quadruped, control='nurbsCircle1')