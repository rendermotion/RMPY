from RMPY.rig.biped.rig import arm
from RMPY.rig.biped.rig import rigSpine
from RMPY.rig.biped.rig import hand
from RMPY.rig import rigFK
from RMPY.rig import rigWorld
from RMPY.rig.biped.rig import neckHead
from RMPY.rig.biped.rig import rigIKFKLegFeet
from RMPY.rig import rigBase
from RMPY.rig import rigProp
from RMPY.rig.biped.rig import armSpaceSwitch
from RMPY.rig.biped.rig import legSpaceSwitch
reload(armSpaceSwitch)
reload(legSpaceSwitch)

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
        self.jaw = rigFK.RigFK()
        self.rig_world = rigWorld.RigWorld()
        self.l_arm_space_switch = armSpaceSwitch.ArmSpaceSwitch()
        self.r_arm_space_switch = armSpaceSwitch.ArmSpaceSwitch()
        self.l_leg_space_switch = legSpaceSwitch.LegSpaceSwitch()
        self.r_leg_space_switch = legSpaceSwitch.LegSpaceSwitch()


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
        self.jaw_root = [u'C_jaw01_reference_pnt', u'C_jawTip01_reference_pnt']

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
    def rig_world(self):
        return self._model.rig_world

    @property
    def l_arm_space_switch(self):
        return self._model.l_arm_space_switch

    @property
    def r_arm_space_switch(self):
        return self._model.l_arm_space_switch
    @property
    def l_leg_space_switch(self):
        return self._model.l_leg_space_switch

    @property
    def r_leg_space_switch(self):
        return self._model.r_leg_space_switch

    @property
    def jaw(self):
        return self._model.jaw

    def build(self):
        self.spine.create_point_base(*self.spine_root)
        self.hip.create_point_base(*self.hip_root, name='hip')
        self.cog.create_point_base(self.hip_root[0], name='cog')
        self.cog.custom_world_align(self.cog.reset_controls[0])

        self.l_arm.create_point_base(*[each.format('L') for each in self.arm_root])
        self.l_arm.set_parent(self.spine)
        self.r_arm.create_point_base(*[each.format('R') for each in self.arm_root])
        self.r_arm.set_parent(self.spine)

        self.l_hand.create_point_base(*[each.format('L') for each in self.hand_root])
        self.l_hand.set_parent(self.l_arm)

        self.l_arm_space_switch.build(self.l_arm, self.rig_world)

        self.r_hand.create_point_base(*[each.format('R') for each in self.hand_root])
        self.r_hand.set_parent(self.r_arm)
        self.r_arm_space_switch.build(self.r_arm, self.rig_world)

        l_root_points = [each.format('L') for each in self.leg_root]
        l_root_points.extend([each.format('L') for each in self.feet_root])
        self.l_leg.create_point_base(*l_root_points)
        self.l_leg_space_switch.build(self.l_leg, self.rig_world)

        r_root_points = [each.format('R') for each in self.leg_root]
        r_root_points.extend([each.format('R') for each in self.feet_root])

        self.r_leg.create_point_base(*r_root_points)
        self.r_leg_space_switch.build(self.r_leg, self.rig_world)

        self.neck_head.create_point_base(*self.neck_root)
        self.jaw.create_point_base(*self.jaw_root)

        self.neck_head.set_parent(self.spine)
        self.jaw.set_parent(self.neck_head)
        self.cog.set_parent(self.rig_world)
        self.spine.set_parent(self.cog)

        self.hip.set_parent(self.cog)

        self.l_leg.set_parent(self.hip)
        self.r_leg.set_parent(self.hip)

        # setup as skinned joints
        self.jaw.rename_as_skinned_joints()
        self.spine.rename_as_skinned_joints()
        self.hip.rename_as_skinned_joints()
        self.l_arm.rename_as_skinned_joints()
        self.r_arm.rename_as_skinned_joints()
        self.l_hand.rename_as_skinned_joints()
        self.r_hand.rename_as_skinned_joints()
        self.neck_head.rename_as_skinned_joints()
        self.l_leg.rename_as_skinned_joints()
        self.r_leg.rename_as_skinned_joints()


if __name__ == '__main__':
    rig_biped = RigByped()
    rig_biped.build()








