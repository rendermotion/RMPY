from RMPY.rig.biped.rig import hand
from RMPY.rig import rigFK
from RMPY.rig import rigWorld
from RMPY.rig.biped.rig import neckHead
from RMPY.rig import rigBase
from RMPY.rig import rigProp
from RMPY.rig.quadruped.rigs import backLegSpaceSwitch
from RMPY.rig.quadruped.rigs import frontLegSpaceSwitch

from RMPY.rig.quadruped.rigs import rigIKQuadLegFeet
from RMPY.rig.quadruped.rigs import rigQuadFrontLeg
from RMPY.rig.quadruped.rigs import rigQuadSpine
from RMPY.rig.quadruped.rigs import rigTailLace
from RMPY.rig.quadruped.rigs import rigNeckSpaceSwitch
from RMPY.rig.quadruped.rigs import rigHipSpaceSwitch


class QuadrupedModel(rigBase.BaseModel):
    def __init__(self, **kwargs):
        super(QuadrupedModel, self).__init__(**kwargs)
        self.l_arm = rigQuadFrontLeg.RigQuadFrontLeg()
        self.r_arm = rigQuadFrontLeg.RigQuadFrontLeg()
        self.l_leg = rigIKQuadLegFeet.RigIKQuadLegFeet()
        self.r_leg = rigIKQuadLegFeet.RigIKQuadLegFeet()
        self.l_hand = hand.Hand()
        self.r_hand = hand.Hand()
        self.tail = rigTailLace.RigTail()
        self.neck_head = neckHead.NeckHead()
        self.spine = rigQuadSpine.RigQuadSpine()
        self.hip = rigFK.RigFK()
        self.cog = rigProp.RigProp()
        self.jaw = rigFK.RigFK()
        self.rig_world = rigWorld.RigWorld()
        self.l_arm_space_switch = frontLegSpaceSwitch.FrontLegSpaceSwitch()
        self.r_arm_space_switch = frontLegSpaceSwitch.FrontLegSpaceSwitch()
        self.l_leg_space_switch = backLegSpaceSwitch.BackLegSpaceSwitch()
        self.r_leg_space_switch = backLegSpaceSwitch.BackLegSpaceSwitch()

        self.hip_space_switch = rigHipSpaceSwitch.HipSpaceSwitch()
        self.neck_space_switch = rigNeckSpaceSwitch.NeckHeadSpaceSwitch()


class RigQuadruped(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(RigQuadruped, self).__init__(*args, **kwargs)
        self._model = QuadrupedModel()

        self.arm_root = [u'{}_shoulder00_reference_pnt', u'{}_clavicle00_reference_pnt', u'{}_frontLeg00_reference_pnt',
                         u'{}_frontLeg01_reference_pnt', u'{}_frontPaw00_reference_pnt', u'{}_frontPawRoll00_reference_pnt',
                         u'{}_frontPawToe00_reference_pnt', u'{}_frontFootLimitBack00_reference_pnt',
                         u'{}_frontFootLimitOuter00_reference_pnt', u'{}_frontFootLimitInner00_reference_pnt']

        self.leg_root = [u'{}_backLeg00_reference_pnt', u'{}_backLeg01_reference_pnt',
                         u'{}_backLeg02_reference_pnt', u'{}_paw00_reference_pnt', u'{}_pawRoll00_reference_pnt',
                         u'{}_pawToe00_reference_pnt', u'{}_footLimitBack00_reference_pnt',
                         u'{}_footLimitOuter00_reference_pnt', u'{}_footLimitInner00_reference_pnt']

        self.feet_root = [u'{}_pawRoll00_reference_pnt', u'{}_pawToe00_reference_pnt',
                          u'{}_footLimitBack00_reference_pnt', u'{}_footLimitOuter00_reference_pnt',
                          u'{}_footLimitInner00_reference_pnt']

        self.fingers = [u'{}_leg01_reference_pnt', u'{}_Knee01_reference_pnt', u'{}_ankle01_reference_pnt',
                        u'{}_ankleFeet01_reference_pnt']
        self.hand_root = [u'{}_palm01_reference_pnt']
        self.hip_root = [u'C_Hip00_reference_pnt', u'C_Hip01_reference_pnt']
        self.jaw_root = [u'C_jaw01_reference_pnt', u'C_jawTip01_reference_pnt']

        self.spine_root = [u'C_spine00_reference_pnt', u'C_spine01_reference_pnt', u'C_spine02_reference_pnt',
                           u'C_spine03_reference_pnt', u'C_spine04_reference_pnt', u'C_spine05_reference_pnt']
        self.COG_root = u'C_COG_reference_pnt'
        self.neck_root = [u'C_neck00_reference_pnt', u'C_neck01_reference_pnt',
                          u'C_head00_reference_pnt', u'C_headTip00_reference_pnt']
        self.tail_root = [u'C_tail00_reference_pnt', u'C_tail01_reference_pnt', u'C_tail02_reference_pnt',
                          u'C_tail03_reference_pnt', u'C_tail04_reference_pnt', u'C_tail05_reference_pnt',
                          u'C_tail06_reference_pnt', u'C_tail07_reference_pnt', u'C_tail08_reference_pnt',
                          u'C_tail09_reference_pnt', u'C_tail10_reference_pnt', u'C_tail11_reference_pnt']

    @property
    def hip_space_switch(self):
        return self._model.hip_space_switch

    @property
    def neck_space_switch(self):
        return self._model.neck_space_switch

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

    @property
    def tail(self):
        return self._model.tail

    def build(self):
        self.spine.create_point_base(*self.spine_root)
        self.hip.create_point_base(*self.hip_root, name='hip')
        self.cog.create_point_base(self.COG_root, name='cog', centered=True)

        self.l_arm.create_point_base(*[each.format('L') for each in self.arm_root])
        self.l_arm_space_switch.build(self.l_arm, self.rig_world)
        self.r_arm.create_point_base(*[each.format('R') for each in self.arm_root])
        self.r_arm_space_switch.build(self.r_arm, self.rig_world)
        l_root_points = [each.format('L') for each in self.leg_root]
        l_root_points.extend([each.format('L') for each in self.feet_root])

        self.l_leg.create_point_base(*l_root_points)
        self.l_leg_space_switch.build(self.l_leg, self.rig_world)

        r_root_points = [each.format('R') for each in self.leg_root]
        r_root_points.extend([each.format('R') for each in self.feet_root])

        self.r_leg.create_point_base(*r_root_points)
        self.r_leg_space_switch.build(self.r_leg, self.rig_world)
        self.tail.create_point_base(*self.tail_root)

        self.spine.set_parent(self.cog)
        self.hip.set_parent(self.spine.joints[0])
        self.cog.set_parent(self.rig_world)

        self.l_leg.set_parent(self.hip)
        self.r_leg.set_parent(self.hip)
        self.l_arm.set_parent(self.spine)
        self.r_arm.set_parent(self.spine)
        self.tail.set_parent(self.hip)

        self.neck_head.create_point_base(*self.neck_root)

        self.jaw.create_point_base(*self.jaw_root)

        self.neck_head.set_parent(self.spine)
        self.jaw.set_parent(self.neck_head)
        self.cog.set_parent(self.rig_world)

        self.hip_space_switch.build(self.hip, self.spine, self.rig_world)
        self.neck_space_switch.build(self.neck_head, self.spine, self.rig_world)

        # setup as skinned joints
        self.jaw.rename_as_skinned_joints()
        self.spine.rename_as_skinned_joints()
        self.hip.rename_as_skinned_joints()
        self.l_arm.rename_as_skinned_joints()
        self.r_arm.rename_as_skinned_joints()

        self.l_hand.rename_as_skinned_joints()
        self.r_hand.rename_as_skinned_joints()
        self.l_leg.rename_as_skinned_joints()
        self.r_leg.rename_as_skinned_joints()

        self.neck_head.rename_as_skinned_joints()
        self.spine.rename_as_skinned_joints()
        self.l_leg.rename_as_skinned_joints()
        self.r_leg.rename_as_skinned_joints()
        self.tail.rename_as_skinned_joints()

        self.rig_world.settings_height = 115


if __name__ == '__main__':
    rig_biped = RigQuadruped()
    rig_biped.build()








