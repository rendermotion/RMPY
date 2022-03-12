from RMPY.rig.quadruped.rigs import rigIKQuadLegFeet
from RMPY.rig import rigSingleJoint
from RMPY.rig import rigBase

class QuadFrontLegModel(rigBase.BaseModel):
    def __init__(self):
        super(QuadFrontLegModel, self).__init__()
        self.shoulder = None
        self.leg = None


class RigQuadFrontLeg(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', QuadFrontLegModel())
        super(RigQuadFrontLeg, self).__init__(*args, **kwargs)
        self._model.shoulder = rigSingleJoint.RigSingleJoint()
        self._model.leg = rigIKQuadLegFeet.RigIKQuadLegFeet()
        self.root = None

    @property
    def shoulder(self):
        return self._model.shoulder

    @property
    def leg(self):
        return self._model.leg

    def create_point_base(self, *args, **kwargs):
        super(RigQuadFrontLeg, self).create_point_base(*args, **kwargs)
        self.shoulder.create_point_base(args[0])
        self.leg.create_point_base(*args[1:])
        self.leg.set_parent(self.shoulder)
        self.root = self.shoulder.reset_controls[0]
        self.joints.extend(self.shoulder.joints)
        self.joints.extend(self.leg.joints)


if __name__ == '__main__':
    leg_root = [u'{}_shoulder00_reference_pnt', u'{}_clavicle00_reference_pnt', u'{}_frontLeg00_reference_pnt',
                u'{}_frontLeg01_reference_pnt', u'{}_frontPaw00_reference_pnt', u'{}_frontPawRoll00_reference_pnt',
                u'{}_frontPawToe00_reference_pnt', u'{}_frontFootLimitBack00_reference_pnt',
                u'{}_frontFootLimitOuter00_reference_pnt', u'{}_frontFootLimitInner00_reference_pnt']


    # feet_root = [u'{}_pawRoll00_reference_pnt', u'{}_pawToe00_reference_pnt',
    #              u'{}_footLimitBack00_reference_pnt', u'{}_footLimitOuter00_reference_pnt',
    #              u'{}_footLimitInner00_reference_pnt']

    root_points = [each.format('R') for each in leg_root]
    quad_front_leg = RigQuadFrontLeg()
    quad_front_leg.create_point_base(*root_points)