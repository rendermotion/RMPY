from RMPY.rig.biped.rig_parts import arm
from RMPY.rig.biped.rig_parts import rigSpine
from RMPY.rig.biped.rig_parts import hand
from RMPY.rig import rigFK
from RMPY.rig.biped.rig_parts import neckHead
from RMPY.rig.biped.rig_parts import rigIKFKLegFeet
from RMPY.rig.biped.rig_parts import rigRibonTwistJoint
from RMPY.rig import rigBase
from RMPY.rig import rigProp


class RigBypedModel(rigBase.BaseModel):
    def __init__(self, **kwargs):
        super(RigBypedModel, self).__init__(**kwargs)
        self.l_arm = arm.Arm()
        self.r_arm = arm.Arm()
        self.l_leg = rigIKFKLegFeet.RigIKKFLegFeet()
        self.r_leg = rigIKFKLegFeet.RigIKKFLegFeet()
        self.l_hand = hand.Hand()
        self.r_hand = hand.Hand()
        self.neck_head = neckHead.NeckHead()
        self.spine = rigSpine.RigSpine()
        self.hip = rigFK.RigFK()
        self.cog = rigProp.RigProp()
        self.l_twist_arm = rigRibonTwistJoint.RibbonTwistJoint()
        self.l_twist_forearm = rigRibonTwistJoint.RibbonTwistJoint()
        self.l_twist_leg = rigRibonTwistJoint.RibbonTwistJoint()
        self.l_twist_foreleg = rigRibonTwistJoint.RibbonTwistJoint()
        self.r_twist_arm = rigRibonTwistJoint.RibbonTwistJoint()
        self.r_twist_forearm = rigRibonTwistJoint.RibbonTwistJoint()
        self.r_twist_leg = rigRibonTwistJoint.RibbonTwistJoint()
        self.r_twist_foreleg = rigRibonTwistJoint.RibbonTwistJoint()


class RigByped(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(RigByped, self).__init__(*args, **kwargs)
        self._model = RigBypedModel()

        self.arm_root = [u'{}_clavicle01_reference_pnt', u'{}_shoulder01_reference_pnt', u'{}_elbow01_reference_pnt',
                         u'{}_wrist01_reference_pnt']

        self.leg_root = [u'{}_leg01_reference_pnt', u'{}_Knee01_reference_pnt', u'{}_ankle01_reference_pnt']

        self.feet_root = [u'{}_ankleFeet01_reference_pnt', u'{}_ball01_reference_pnt', u'{}_toe01_reference_pnt',
                          u'{}_footLimitBack01_reference_pnt', u'{}_footLimitOuter01_reference_pnt',
                          u'{}_footLimitInner01_reference_pnt']

        self.fingers = [u'{}_leg01_reference_pnt', u'{}_Knee01_reference_pnt', u'{}_ankle01_reference_pnt',
                        u'{}_ankleFeet01_reference_pnt']
        self.hand_root = [u'{}_palm01_reference_pnt']
        self.hip_root = [u'C_Hip00_reference_pnt', u'C_Hip01_reference_pnt']

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

    @property
    def hip(self):
        return self._model.hip

    @property
    def cog(self):
        return self._model.cog

    @property
    def l_twist_arm(self):
        return self._model.l_twist_arm

    @property
    def l_twist_forearm(self):
        return self._model.l_twist_forearm

    @property
    def l_twist_leg(self):
        return self._model.l_twist_leg

    @property
    def l_twist_foreleg(self):
        return self._model.l_twist_foreleg
    @property
    def r_twist_arm(self):
        return self._model.r_twist_arm

    @property
    def r_twist_forearm(self):
        return self._model.r_twist_forearm

    @property
    def r_twist_leg(self):
        return self._model.r_twist_leg

    @property
    def r_twist_foreleg(self):
        return self._model.r_twist_foreleg





    def build(self):
        self.spine.create_point_base(*self.spine_root)
        self.hip.create_point_base(*self.hip_root, name='hip')
        self.cog.create_point_base(self.hip_root[0], name='cog')

        self.l_arm.create_point_base(*[each.format('L') for each in self.arm_root])
        self.l_arm.set_parent(self.spine)
        self.r_arm.create_point_base(*[each.format('R') for each in self.arm_root])
        self.r_arm.set_parent(self.spine)

        self.l_hand.create_point_base(*[each.format('L') for each in self.hand_root])
        self.l_hand.set_parent(self.l_arm)
        self.r_hand.create_point_base(*[each.format('R') for each in self.hand_root])
        self.r_hand.set_parent(self.r_arm)

        l_root_points = [each.format('L') for each in self.leg_root]
        l_root_points.extend([each.format('L') for each in self.feet_root])
        self.l_leg.create_point_base(*l_root_points)

        r_root_points = [each.format('R') for each in self.leg_root]
        r_root_points.extend([each.format('R') for each in self.feet_root])
        self.r_leg.create_point_base(*r_root_points)

        self.neck_head.create_point_base(*self.neck_root)

        self.neck_head.set_parent(self.spine)

        self.spine.set_parent(self.cog)

        self.hip.set_parent(self.cog)

        self.l_leg.set_parent(self.hip)
        self.r_leg.set_parent(self.hip)

        self.l_twist_arm.create_point_base(self.l_arm.joints[2], self.l_arm.joints[3], folicule_number=5)
        self.l_twist_forearm.create_point_base(self.l_arm.joints[3], self.l_arm.joints[4], folicule_number=5)
        self.l_twist_leg.create_point_base(self.l_leg.joints[0], self.l_leg.joints[1], folicule_number=5)
        self.l_twist_foreleg.create_point_base(self.l_leg.joints[1], self.l_leg.joints[2], folicule_number=5)
        self.r_twist_arm.create_point_base(self.r_arm.joints[2], self.r_arm.joints[3], folicule_number=5)
        self.r_twist_forearm.create_point_base(self.r_arm.joints[3], self.r_arm.joints[4], folicule_number=5)
        self.r_twist_leg.create_point_base(self.r_leg.joints[0], self.r_leg.joints[1], folicule_number=5)
        self.r_twist_foreleg.create_point_base(self.r_leg.joints[1], self.r_leg.joints[2], folicule_number=5)

        # setup as skinned joints
        self.spine.rename_as_skinned_joints()
        self.hip.rename_as_skinned_joints()
        # self.l_arm.rename_as_skinned_joints()
        # self.r_arm.rename_as_skinned_joints()
        self.l_twist_arm.rename_as_skinned_joints()
        self.l_twist_forearm.rename_as_skinned_joints()
        self.r_twist_arm.rename_as_skinned_joints()
        self.r_twist_forearm.rename_as_skinned_joints()

        self.l_hand.rename_as_skinned_joints()
        self.r_hand.rename_as_skinned_joints()
        # self.l_leg.rename_as_skinned_joints()
        # self.r_leg.rename_as_skinned_joints()
        self.l_twist_leg.rename_as_skinned_joints()
        self.l_twist_foreleg.rename_as_skinned_joints()
        self.r_twist_leg.rename_as_skinned_joints()
        self.r_twist_foreleg.rename_as_skinned_joints()
        self.neck_head.rename_as_skinned_joints()
        self.spine.rename_as_skinned_joints()
        self.l_leg.rename_as_skinned_joints()
        self.r_leg.rename_as_skinned_joints()




if __name__ == '__main__':
    rig_biped = RigByped()
    rig_biped.build()








