from RMPY.rig import rigIKFK
from RMPY.rig.biped.rig import rigIkFkFeet
from RMPY.rig import rigBase
from RMPY.rig.biped.rig import rigRibonTwistJoint
import pymel.core as pm
import maya.api.OpenMaya as om


class RigIKKFLegFeetModel(rigBase.BaseModel):
    def __init__(self):
        super(RigIKKFLegFeetModel, self).__init__()
        self.leg = None
        self.feet = None


class RigIKKFLegFeet(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', RigIKKFLegFeetModel())
        super(RigIKKFLegFeet, self).__init__(*args, **kwargs)

    @property
    def leg(self):
        return self._model.leg

    @property
    def feet(self):
        return self._model.feet

    @property
    def twist_leg(self):
        return self._model.twist_leg

    @property
    def twist_foreleg(self):
        return self._model.twist_foreleg

    def create_point_base(self, *args, **kwargs):
        """
        :param points: the points to create the leg, should be 5 points
        :param kwargs: no kwargs expected
        :return:
        """
        super(RigIKKFLegFeet, self).create_point_base(*args, **kwargs)
        align_args = []
        for each in args:
            align_args.append(self.create.space_locator.node_base(each)[0])
            self.name_convention.rename_name_in_format(align_args[-1], name=self.name_convention.get_a_short_name(each),
                                                       system='reference')

        arm_position_vector = om.MVector(pm.xform(align_args[0], q=True, ws=True, rp=True))
        elbow_position_vector = om.MVector(pm.xform(align_args[1], q=True, ws=True, rp=True))
        wrist_position_vector = om.MVector(pm.xform(align_args[2], q=True, ws=True, rp=True))
        args = align_args
        up_vector = (arm_position_vector - elbow_position_vector) ^ (arm_position_vector - wrist_position_vector) * -1
        for index, each in enumerate(args[0:3]):
            self.transform.aim_point_based(each, each, args[index + 1],
                                           use_vector_as_up_axis=(up_vector.x, up_vector.y, up_vector.z), up_axis='z')
        pm.matchTransform(args[2], args[1], rotation=True, position=False, scale=False)

        self._model.leg = rigIKFK.RigIkFk(rig_system=self.rig_system)
        self._model.feet = rigIkFkFeet.IkFkFeet(rig_system=self.rig_system)
        self._model.twist_leg = rigRibonTwistJoint.RibbonTwistJoint(rig_system=self.rig_system)
        self._model.twist_foreleg = rigRibonTwistJoint.RibbonTwistJoint(rig_system=self.rig_system)

        self.leg.create_point_base(*args[:3])
        self.feet.create_point_base(*args[3:], control=self.leg.switch_control_rig.controls[0])

        l_point_constraint = self.create.constraint.point(self.feet.ik_feet.up_ik.joints[-1],
                                                          self.leg.ik_rig.ik_handle, mo=True)

        l_point_constraint[0].getWeightAliasList()[0].set(0)

        self.feet.ik_feet.set_parent(self.leg.ik_rig.controls[0])
        self.feet.fk_feet.set_parent(self.leg.fk_rig)
        self.create.constraint.node_base(self.leg.ik_rig.tip, self.feet.ik_feet.attachment_ik_leg, mo=True)
        self.create.constraint.node_base(self.leg.ik_rig.controls_dict['ikHandle'],
                                         self.feet.ik_feet.reset_controls[0], mo=True)

        self.attach_points['root'] = self.leg.root
        self.attach_points['tip'] = self.feet.tip

        self.create.constraint.orient(self.feet.joints[0], self.leg.joints[-1], mo=True)

        # self.create.constraint.define_constraints(point=False, scale=True, parent=True, orient=False)

        self.twist_leg.create_point_base(self.root, self.leg.joints[0], self.leg.joints[1],
                                         folicule_number=5)
        self.twist_foreleg.create_point_base(self.leg.joints[1], self.leg.joints[1], self.leg.joints[2],
                                             folicule_number=5)
        # self.joints.extend(self.leg.joints)
        self.joints.extend(self.twist_leg.joints)
        self.joints.extend(self.twist_foreleg.joints)
        self.joints.extend(self.feet.joints)
        pm.delete(align_args)


if __name__ == '__main__':
    leg_root = [u'{}_leg01_reference_pnt', u'{}_Knee01_reference_pnt', u'{}_ankle01_reference_pnt']
    # u'{}_ankleFeet01_reference_pnt'
    feet_root = [u'{}_ankleFeet01_reference_pnt', u'{}_ball01_reference_pnt', u'{}_toe01_reference_pnt',
                 u'{}_footLimitBack01_reference_pnt', u'{}_footLimitOuter01_reference_pnt',
                 u'{}_footLimitInner01_reference_pnt']
    root_points = [each.format('R') for each in leg_root]
    root_points.extend([each.format('R') for each in feet_root])

    rig_leg_ik_fk = RigIKKFLegFeet()
    rig_leg_ik_fk.create_point_base(*root_points)

