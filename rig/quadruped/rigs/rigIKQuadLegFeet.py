from RMPY.rig import rigIKFK
from RMPY.rig.biped.rig import rigIkFkFeet
from RMPY.rig import rigBase
from RMPY.rig.biped.rig import reverseFeet
from RMPY.rig.quadruped.rigs import rigIKQuadLeg
reload(rigIKQuadLeg)


class RigIKQuadLegFeetModel(rigBase.BaseModel):
    def __init__(self):
        super(RigIKQuadLegFeetModel, self).__init__()
        self.leg = None
        self.feet = None


class RigIKQuadLegFeet(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', RigIKQuadLegFeetModel())
        super(RigIKQuadLegFeet, self).__init__(*args, **kwargs)

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

    def create_point_base(self, *points, **kwargs):
        """
        :param points: the points to create the leg, should be 5 points
        :param kwargs: no kwargs expected
        :return:
        """
        print points[:4]
        print points[3:]
        self._model.leg = rigIKQuadLeg.IKQuadLeg(rig_system=self.rig_system)
        self._model.feet = reverseFeet.RigReverseFeet(rig_system=self.rig_system)

        self.leg.create_point_base(*points[:4])

        self.feet.create_point_base(*points[3:], control=self.leg.controls_dict['ikHandle'])

        l_point_constraint = self.create.constraint.point(self.feet.up_ik.joints[-1],
                                                          self.leg.rig_leg_palm.root, mo=True)
        l_point_constraint[0].getWeightAliasList()[0].set(0)

        self.feet.set_parent(self.leg.controls_dict['ikHandle'])

        self.create.constraint.node_base(self.leg.tip, self.feet.attachment_ik_leg, mo=True)

        self.attach_points['root'] = self.leg.root
        self.attach_points['tip'] = self.feet.tip

        # self.create.constraint.orient(self.feet.joints[0], self.leg.joints[-1], mo=True)
        # self.create.constraint.define_constraints(point=False, scale=True, parent=True, orient=False)

        self.joints.extend(self.feet.joints)


if __name__ == '__main__':
    leg_root = [u'{}_backLeg00_reference_pnt', u'{}_backLeg01_reference_pnt',
                u'{}_backLeg02_reference_pnt', u'{}_paw00_reference_pnt']
    # u'{}_ankleFeet01_reference_pnt'
    feet_root = [u'{}_pawRoll00_reference_pnt', u'{}_pawToe00_reference_pnt',
                 u'{}_footLimitBack00_reference_pnt', u'{}_footLimitOuter00_reference_pnt',
                 u'{}_footLimitInner00_reference_pnt']

    root_points = [each.format('L') for each in leg_root]
    root_points.extend([each.format('L') for each in feet_root])

    rig_leg_ik_fk = RigIKQuadLegFeet()
    rig_leg_ik_fk.create_point_base(*root_points)

