from RMPY.rig.biped.rig import arm
from RMPY.rig.biped.rig import rigForwardBackwardFKSpine
from RMPY.rig.biped.rig import hand
from RMPY.rig import rigFK
from RMPY.rig.biped.rig import rig_jaw
from RMPY.rig import rigWorld
from RMPY.rig.biped.rig import neckHead
from RMPY.rig.biped.rig import rigIKFKLegFeet
from RMPY.rig import rigBase
from RMPY.rig import rigProp
from RMPY.rig.biped.rig import armSpaceSwitch
from RMPY.rig.biped.rig import legSpaceSwitch
from RMPY.rig.biped.rig import handSpaceSwitch
from RMPY.rig.biped.rig import rigEyesAim
from RMPY.rig.biped.rig import rigBreast
from RMPY.rig.biped.rig import rigToes
from RMPY.rig.biped.rig import neckHeadSpaceSwitch
from RMPY.rig.biped.rig import rigEyesSpaceSwitch
from RMPY.rig import rigSingleJoint
from RMPY.rig import rigOutput
import importlib
reload(rigOutput)


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
        self.spine = rigForwardBackwardFKSpine.RigForwardBackwardFKSpine()
        self.hip = rigFK.RigFK()
        self.cog = rigProp.RigProp()
        self.jaw = rig_jaw.Jaw()
        self.rig_world = rigWorld.RigWorld()
        self.l_arm_space_switch = armSpaceSwitch.ArmSpaceSwitch()
        self.r_arm_space_switch = armSpaceSwitch.ArmSpaceSwitch()
        self.l_leg_space_switch = legSpaceSwitch.LegSpaceSwitch()
        self.r_leg_space_switch = legSpaceSwitch.LegSpaceSwitch()
        self.l_hand_space_switch = handSpaceSwitch.HandSpaceSwitch()
        self.r_hand_space_switch = handSpaceSwitch.HandSpaceSwitch()
        self.eye_space_switch = rigEyesSpaceSwitch.EyeSpaceSwitch()
        self.neck_head_space_switch = neckHeadSpaceSwitch.NeckHeadSpaceSwitch()
        self.eyes = rigEyesAim.RigEyesAim()
        self.l_toes = rigToes.Toes()
        self.r_toes = rigToes.Toes()
        self.l_breast = rigBreast.Breast()
        self.r_breast = rigBreast.Breast()
        self.gums = rigSingleJoint.RigSingleJoint()
        self.rig_output = rigOutput.RigOutput()


class RigByped(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(RigByped, self).__init__(*args, **kwargs)
        self._model = RigBypedModel()

        self.arm_root = [u'{}_clavicle01_reference_pnt', u'{}_arm01_reference_pnt', u'{}_elbow01_reference_pnt',
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
        self.eyes_root = [u'R_eye_reference_pnt', u'L_eye_reference_pnt']

        self.breast_root = [u'{}_breast00_reference_pnt']
        self.toes_root = [u'{}_toes00_reference_grp']
        self.gums_root = [u'C_gums00_reference_pnt']

    @property
    def neck_head(self):
        return self._model.neck_head

    @property
    def gums(self):
        return self._model.gums

    @property
    def eyes(self):
        return self._model.eyes

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
    def l_hand_space_switch(self):
        return self._model.l_hand_space_switch

    @property
    def r_hand_space_switch(self):
        return self._model.r_hand_space_switch

    @property
    def l_breast(self):
        return self._model.l_breast

    @property
    def r_breast(self):
        return self._model.r_breast

    @property
    def r_toes(self):
        return self._model.r_toes

    @property
    def l_toes(self):
        return self._model.l_toes

    @property
    def jaw(self):
        return self._model.jaw

    @property
    def neck_head_space_switch(self):
        return self._model.neck_head_space_switch
    @property
    def eye_space_switch(self):
        return self._model.eye_space_switch


    def build(self):
        self.spine.create_point_base(*self.spine_root)
        self.hip.create_point_base(*self.hip_root, name='hip')
        self.cog.create_point_base(self.hip_root[0], name='cog', depth=1)
        self.cog.custom_world_align(self.cog.reset_controls[0])

        self.cog.set_parent(self.rig_world, create_hierarchy_joints=True, output_joint_rig=self.rig_output)

        self.create.constraint.node_base(self.spine.backward_root, self.hip.root, point=True)
        self.create.constraint.node_base(self.cog.tip, self.hip.root, orient=True, mo=True)
        self.hip._create_output_points(self.cog, create_hierarchy_joints=True, output_joint_rig=self.rig_output)
        self.spine.set_parent(self.cog, create_hierarchy_joints=True, output_joint_rig=self.rig_output)

        self.l_arm.create_point_base(*[each.format('L') for each in self.arm_root])
        self.l_arm.set_parent(self.spine, create_hierarchy_joints=True, output_joint_rig=self.rig_output)

        self.r_arm.create_point_base(*[each.format('R') for each in self.arm_root])
        self.r_arm.set_parent(self.spine, create_hierarchy_joints=True, output_joint_rig=self.rig_output)

        self.l_hand.create_point_base(*[each.format('L') for each in self.hand_root])
        self.l_hand.set_parent(self.l_arm, create_hierarchy_joints=True, output_joint_rig=self.rig_output)

        self.l_arm_space_switch.build(self.l_arm, self.rig_world, self.cog)
        self.l_hand_space_switch.build(self.l_hand, self.rig_world, self.l_arm)

        self.r_hand.create_point_base(*[each.format('R') for each in self.hand_root])
        self.r_hand.set_parent(self.r_arm, create_hierarchy_joints=True, output_joint_rig=self.rig_output)

        self.r_arm_space_switch.build(self.r_arm, self.rig_world, self.cog)

        self.r_hand_space_switch.build(self.r_hand, self.rig_world, self.r_arm)

        l_root_points = [each.format('L') for each in self.leg_root]
        l_root_points.extend([each.format('L') for each in self.feet_root])
        self.l_leg.create_point_base(*l_root_points)
        self.l_leg_space_switch.build(self.l_leg, self.rig_world)

        r_root_points = [each.format('R') for each in self.leg_root]
        r_root_points.extend([each.format('R') for each in self.feet_root])

        self.r_leg.create_point_base(*r_root_points)
        self.r_leg_space_switch.build(self.r_leg, self.rig_world)

        self.neck_head.create_point_base(*self.neck_root)
        # self.jaw.create_point_base(*self.jaw_root)

        # self.eyes.create_point_base(*self.eyes_root)
        # self.eye_space_switch.build(self.eyes, self.neck_head, self.rig_world)

        self.neck_head.set_parent(self.spine, create_hierarchy_joints=True, output_joint_rig=self.rig_output)

        self.neck_head_space_switch.build(self.neck_head, self.rig_world, self.cog)

        # self.gums.create_point_base(*self.gums_root)
        # self.gums.set_parent(self.neck_head)

        # self.jaw.set_parent(self.neck_head)
        #
        # self.spine.set_parent(self.cog)

        # self.eyes.set_parent(self.neck_head)

        self.l_leg.set_parent(self.hip, create_hierarchy_joints=True, output_joint_rig=self.rig_output)
        self.r_leg.set_parent(self.hip, create_hierarchy_joints=True, output_joint_rig=self.rig_output)

        # self.l_breast.create_point_base(*[each.format('L') for each in self.breast_root])
        # self.r_breast.create_point_base(*[each.format('R') for each in self.breast_root])
        # self.l_breast.set_parent(self.spine)
        # self.r_breast.set_parent(self.spine)

        # self.l_toes.create_point_base(*[each.format('L') for each in self.toes_root])
        # self.r_toes.create_point_base(*[each.format('R') for each in self.toes_root])
        # self.l_toes.set_parent(self.l_leg)
        # self.r_toes.set_parent(self.r_leg)

        # setup as skinned joints
        # self.eyes.rename_as_skinned_joints(nub=False)

        # self.jaw.rename_as_skinned_joints()

        # self.l_toes.rename_as_skinned_joints()
        # self.r_toes.rename_as_skinned_joints()

        # self.l_breast.rename_as_skinned_joints(nub=False)
        # self.r_breast.rename_as_skinned_joints(nub=False)
        # self.gums.rename_as_skinned_joints(nub=False)


if __name__ == '__main__':
    rig_biped = RigByped()
    rig_biped.build()








