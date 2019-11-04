from RMPY.rig.byped.parts import arm
from RMPY.rig.byped.parts import rigSpine
from RMPY.rig.byped.parts import hand
from RMPY.rig.byped.parts import leg
from RMPY.rig.byped.parts import neckHead
from RMPY.rig import rigBase



class RigBypedModel(rigBase.BaseModel):
    def __init__(self):
        super(RigBypedModel, self).__init__()
        self.l_arm = arm.Arm()
        self.r_arm = arm.Arm()
        self.l_leg = leg.RigIkFk()
        self.r_leg = leg.RigIkFk()
        self.l_hand = hand.Hand()
        self.r_hand = hand.Hand()
        self.neck_head = neckHead.NeckHead()
        self.spine = rigSpine.RigSpine()


class RigByped(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(RigByped, self).__init__(*args, **kwargs)
        self._model = RigBypedModel()
        self.arm_root = [u'{}_clavicle01_reference_pnt', u'{}_shoulder01_reference_pnt', u'{}_elbow01_reference_pnt',
                         u'{}_wrist01_reference_pnt']
        self.leg_root = [u'{}_leg01_reference_pnt', u'{}_Knee01_reference_pnt', u'{}_ankle01_reference_pnt',
                         u'{}_ankleFeet01_reference_pnt']

        self.fingers = [u'{}_leg01_reference_pnt', u'{}_Knee01_reference_pnt', u'{}_ankle01_reference_pnt',
                        u'{}_ankleFeet01_reference_pnt']
        self.hand_root = [u'{}_palm01_reference_pnt']

        self.spine_root = [u'C_Spine01_reference_pnt', u'C_Spine02_reference_pnt', u'C_Spine03_reference_pnt',
                           u'C_Spine04_reference_pnt', u'C_Spine05_reference_pnt']

        self.neck_root = [u'C_neck00_reference_pnt', u'C_head00_reference_pnt', u'C_headTip00_reference_pnt']

    @property
    def neck_head(self):
        return self._model.neck_head

    @property
    def spine(self):
        return self._model.spine

    @property
    def l_arm(self):
        return self._model.l_arm

    @property
    def r_arm(self):
        return self._model.r_arm

    @property
    def l_leg(self):
        return self._model.l_leg

    @property
    def r_leg(self):
        return self._model.r_leg

    @property
    def l_hand(self):
        return self._model.l_hand

    @property
    def r_hand(self):
        return self._model.r_hand

    def build(self):
        self.spine.create_point_base(*self.spine_root)

        self.l_arm.create_point_base(*[each.format('L') for each in self.arm_root])
        self.r_arm.create_point_base(*[each.format('R') for each in self.arm_root])

        self.l_hand.create_point_base(*[each.format('L') for each in self.hand_root])
        self.r_hand.create_point_base(*[each.format('R') for each in self.hand_root])

        self.l_leg.create_point_base(*[each.format('L') for each in self.leg_root])
        self.l_leg.create_point_base(*[each.format('R') for each in self.leg_root])

if __name__ == '__main__':
    rig_byped = RigByped()
    rig_byped.build()








