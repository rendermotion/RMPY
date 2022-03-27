import maya.api.OpenMaya as om
from RMPY.rig import rigBase
import pymel.core as pm


class RibonModel(rigBase.BaseModel):
    def __init__(self):
        super(RibonModel, self).__init__()
        self.base_objects = []
        self.follicules = []
        self.allControls = []


class Ribon(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', RibonModel())
        super(Ribon, self).__init__(*args, **kwargs)
        self.base_objects = []
        self.all_controls = []

    @property
    def follicules(self):
        return self._model.follicules

    def nurb_plane_between_objects(self, object_a, object_b):
        vector_a = om.MVector(pm.xform(object_a, a=True, ws=True, q=True, rp=True))
        vector_b = om.MVector(pm.xform(object_b, a=True, ws=True, q=True, rp=True))
        length = vector_a - vector_b
        plano = pm.nurbsPlane(ax=[0, 1, 0], p=[(length.length()) / 2, 0, 0], w=length.length(), lr=.05, d=3, u=8,
                              v=1, ch=0, name="bendyPlane")
        self.name_convention.rename_name_in_format(plano[0], useName=True)

        pm.matchTransform(plano[0], object_a)
        return plano[0]

    # nurbPlaneBetweenObjects("joint1","joint2")
    def create_point_base(self, *args, **kwargs):
        folicule_number = kwargs.pop('folicule_number', 3)
        super(Ribon, self).create_point_base(*args, **kwargs)
        object_a = args[0]
        object_b = args[1]
        self.base_objects.append(object_a)
        self.base_objects.append(object_b)
        VP1 = om.MVector(pm.xform(object_a, a=True, ws=True, q=True, rp=True))
        VP2 = om.MVector(pm.xform(object_b, a=True, ws=True, q=True, rp=True))

        plane = self.nurb_plane_between_objects(object_a, object_b)

        plane_shape = pm.listRelatives(plane, shapes=True)[0]
        pm.select(cl=True)
        ribon_size = VP1 - VP2

        # print "plano = %s" % plano
        # print "len = %s" % ribon_size.length()

        main_skeleton = pm.group(em=True, name="ribon")
        self.name_convention.rename_name_in_format(main_skeleton, useName=True)
        main_skeleton.setParent(self.rig_system.kinematics)
        hair_group = pm.group(em=True, name="hairSystem")
        self.name_convention.rename_name_in_format(hair_group, useName=True)
        hair_group.setParent(self.rig_system.kinematics)

        for each in range(folicule_number):
            self.create.follicle.surface_base(plane, u_value=1.0 / (folicule_number - 1) * each)
            new_follicule = self.create.follicle.transform
            self.follicules.append(new_follicule)
            pm.parent(new_follicule, hair_group)

        skin_joints = pm.group(em=True, name="ribbonJoints")
        self.name_convention.rename_name_in_format(skin_joints, useName=True)
        skin_joints.setParent(self.rig_system.joints)

        for each_follicle in self.follicules:
            self.joints.append(pm.joint(name="ribbonJoints"))
            self.name_convention.rename_name_in_format(self.joints[-1], useName=True)
            self.create.constraint.node_base(each_follicle, self.joints[-1])
            self.joints[-1].segmentScaleCompensate.set(0)

        locator_controls_list = []
        locator_look_at_list = []
        joints_look_at_list = []
        group_look_at_list = []

        group_joints = pm.group(empty=True, name="groupJointsLookAt")
        self.name_convention.rename_name_in_format(group_joints, useName=True)

        # self.joints.append(group_joints)

        for iloop in range(3):
            reset_control_group, control = self.create.controls.point_base(object_a, type='circular',
                                                                           size=ribon_size.length() / 3,
                                                                           name='bendy')
            self.controls.append(control)
            self.reset_controls.append(reset_control_group)

            locator_control = pm.spaceLocator(name="locatorCntrl")
            self.name_convention.rename_name_in_format(locator_control, useName=True)
            locator_controls_list.append(locator_control)
            pm.matchTransform(locator_control, object_a)

            locator_look_at = pm.spaceLocator(name="locatorLookAt")
            self.name_convention.rename_name_in_format(locator_look_at, useName=True)

            locator_look_at_list.append(locator_look_at)
            pm.matchTransform(locator_look_at, object_a)

            pm.select(clear=True)

            joints_look_at = pm.joint(name="jointsLookAt")
            self.name_convention.rename_name_in_format(joints_look_at, useName=True)
            joints_look_at_list.append(joints_look_at)
            pm.matchTransform(joints_look_at, object_a)

            group_look_at = pm.group(empty=True, name="lookAt")
            self.name_convention.rename_name_in_format(group_look_at, useName=True)

            group_look_at.setParent(self.rig_system.kinematics)
            group_look_at_list.append(group_look_at)
            pm.matchTransform(group_look_at, object_a)
            for each in group_look_at_list:
                pm.parent(each, main_skeleton)

            pm.move(ribon_size.length() / 2 * iloop, 0, 0, reset_control_group, r=True, os=True, moveX=True)
            pm.move(ribon_size.length() / 2 * iloop, 0, 0, locator_control, r=True, os=True, moveX=True)
            pm.move(ribon_size.length() / 2 * iloop, 0, 1, locator_look_at, r=True, os=True, moveXYZ=True)
            pm.move(ribon_size.length() / 2 * iloop, 0, 0, joints_look_at, r=True, os=True, moveX=True)
            pm.move(ribon_size.length() / 2 * iloop, 0, 0, group_look_at, r=True, os=True, moveX=True)

            pm.parent(reset_control_group, self.rig_system.controls)
            pm.parent(locator_control, group_look_at)
            pm.parent(locator_look_at, group_look_at)
            pm.parent(joints_look_at, group_joints)

            pm.makeIdentity(control, apply=True, t=1, r=0, s=1, n=0)
            pm.makeIdentity(joints_look_at, apply=True, t=1, r=0, s=1, n=0)

            self.create.constraint.node_base(locator_control, joints_look_at)
            self.create.constraint.node_base(control, group_look_at)

        pm.aimConstraint(self.controls[1], locator_controls_list[0], aim=[1, 0, 0], upVector=[0, 0, 1], wut='object',
                         worldUpObject=locator_look_at_list[0])

        pm.aimConstraint(self.controls[1], locator_controls_list[2], aim=[1, 0, 0], upVector=[0, 0, 1], wut='object',
                         worldUpObject=locator_look_at_list[2])

        self.create.constraint.define_constraints(parent=False, scale=True)
        self.create.constraint.node_list_base(self.controls, self.follicules, mo=False)
        self.create.constraint.define_constraints(parent=True, scale=True)
        pm.parent(group_joints, main_skeleton)
        pm.parent(plane, hair_group)
        pm.skinCluster(joints_look_at_list, plane)

    def set_parent(self, *args, **kwargs):
        """
        :param args: three objects should be provided regularly a twist joint rig to control the rotation of the joints
        :param kwargs:
        :return:
        """
        for each in args:
            self.create.constraint.node_base(args[0], self.reset_controls[0], mo=True)
            self.create.constraint.node_base(args[1], self.reset_controls[1], mo=True)
            self.create.constraint.node_base(args[2], self.reset_controls[2], mo=True)


if __name__ == '__main__':
    rig_ribbon = Ribon()
    rig_ribbon.create_point_base("R_intermediate01_shoulder_jnt",
                                 "R_intermediate02_shoulder_jnt", folicule_number=5)
    # rig_ribon.set_parent("L_intermediate00_shoulder_sknjnt", "L_intermediate01_shoulder_sknjnt")
