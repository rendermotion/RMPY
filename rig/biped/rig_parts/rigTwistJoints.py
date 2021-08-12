import pymel.core as pm
import maya.api.OpenMaya as om
from RMPY.rig import rigBase
from RMPY import RMRigTools
from RMPY import RMRigShapeControls


class TwistJointsModel(rigBase.BaseModel):
    def __init__(self):
        super(TwistJointsModel, self).__init__()
        self.twist_origin = None
        self.twist_end = None


class TwistJoints(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', TwistJointsModel())
        super(TwistJoints, self).__init__(*args, **kwargs)

    def create_point_base(self, *args, **kwargs):
        super(TwistJoints, self).create_point_base(*args, **kwargs)
        self._model.twist_origin = pm.ls(args[0])[0]
        self._model.twist_end = pm.ls(args[1])[0]
        number_of_joints = kwargs.pop('number_of_joints', 2)
        look_at_axis = kwargs.pop('look_at_axis', "Y")
        self.create_twist(self.twist_origin, self.twist_end,
                          number_of_twist_bones=number_of_joints,
                          look_at_axis=look_at_axis)

        self.stretchy_twist_joints()

    @property
    def twist_origin(self):
        return self._model.twist_origin

    @property
    def twist_end(self):
        return self._model.twist_end

    def create_twist(self, twist_joint, look_at_object, number_of_twist_bones=3, look_at_axis="Y"):
        # LookAtObject = pm.listRelatives( TwistJoint,type = "transform",children=True)[]

        position_a = pm.xform(twist_joint, q=True, ws=True, rp=True)
        position_b = pm.xform(look_at_object, q=True, ws=True, rp=True)

        vector_a = om.MVector(position_a)
        vector_b = om.MVector(position_b)

        self.create_bones_between_points(vector_a, vector_b, number_of_twist_bones, align_object=twist_joint)

        Distance = RMRigTools.RMPointDistance(twist_joint, look_at_object)

        # pm.parentConstraint(twist_joint, self.reset_joints)
        self.create.constraint.node_base(twist_joint, self.reset_joints)

        # reset_point, control = RMRigShapeControls.RMCreateBoxCtrl(self.joints[0], Xratio=.1, Yratio=.1, Zratio=.1, customSize=Distance / 5, name="TwistOrigin")
        reset_point, control = self.create.controls.point_base(self.joints[0], centered=True,
                                                               size=Distance/5 * .1, name="twistOrigin")
        sign = 1
        move_distance = Distance / 5
        if "-" in look_at_axis:
            sign = -1
        if "Z" in look_at_axis or "z" in look_at_axis:
            move_list = [0, 0, move_distance * sign]
            wuv = [0, 0, sign]
        elif "Y" in look_at_axis or "y" in look_at_axis:
            move_list = [0, move_distance * sign, 0]
            wuv = [0, sign, 0]

        pm.xform(reset_point, os=True, relative=True, t=move_list)

        pm.aimConstraint(look_at_object, self.joints[0], aim=[1, 0, 0], worldUpVector=[0, 0, 1],
                         worldUpType="object", worldUpObject=control)

        twist_joint_divide = pm.shadingNode("multiplyDivide", asUtility=True,
                                            name="TwistJoint")
        self.name_convention.rename_based_on_base_name(twist_joint, twist_joint_divide,
                                                       name=self.name_convention.get_a_short_name(twist_joint_divide))
        twist_addition = pm.shadingNode("plusMinusAverage", asUtility=True,
                                        name="TwistJointAdd")
        self.name_convention.rename_based_on_base_name(twist_joint, twist_addition,
                                                       name=self.name_convention.get_a_short_name(twist_addition))
        negative_look_at_rotation = pm.shadingNode("multiplyDivide", asUtility=True)
        self.name_convention.rename_based_on_base_name(twist_joint, negative_look_at_rotation,
                                                       name="negativeLookAtRotation")
        pm.connectAttr(look_at_object + ".rotateX", negative_look_at_rotation + ".input1X")
        pm.setAttr("%s.input2X" % negative_look_at_rotation, -1)
        pm.setAttr("%s.operation" % negative_look_at_rotation, 1)
        pm.connectAttr("%s.rotateX" % self.joints[0], "%s.input1D[0]" % twist_addition)
        pm.connectAttr("%s.outputX" % negative_look_at_rotation, "%s.input1D[1]" % twist_addition)
        pm.connectAttr("%s.output1D" % twist_addition, "%s.input1X" % twist_joint_divide)

        # pm.connectAttr(self.joints[0]+".rotateX", TwistJointDivide + ".input1X") in this case the rotation of the lookatNode was not affecting
        pm.setAttr("%s.input2X" % twist_joint_divide, -(len(self.joints) - 1))
        pm.setAttr("%s.operation" % twist_joint_divide, 2)

        for eachJoint in self.joints[1:]:
            pm.connectAttr("%s.outputX" % twist_joint_divide, "%s.rotateX" % eachJoint)

        self.reset_controls.append(reset_point)
        pm.parent(self.reset_controls, self.rig_system.controls)
        self.controls.append(control)
        self.create.constraint.node_base(twist_joint, self.reset_controls[0], mo=True)

    def distance_between_points_measure(self, Point01, Point02):
        transform_start_point = "startPoint"
        transform_end_point = "endPoint"

        transform_start_point = pm.spaceLocator(name=transform_start_point)
        self.name_convention.rename_name_in_format(transform_start_point, useName=True)
        transform_end_point = pm.spaceLocator(name=transform_end_point)
        self.name_convention.rename_name_in_format(transform_end_point, useName=True)

        start_point_constraint = pm.pointConstraint(Point01, transform_start_point)
        end_point_constraint = pm.pointConstraint(Point02, transform_end_point)

        distance_node = pm.shadingNode("distanceBetween", asUtility=True, name="DistanceNode")
        self.name_convention.rename_based_on_base_name(Point01, distance_node, name=distance_node)

        pm.connectAttr("%s.worldPosition[0]" % transform_start_point, "%s.point1" % distance_node, f=True)
        pm.connectAttr("%s.worldPosition[0]" % transform_end_point, "%s.point2" % distance_node, f=True)

        return [transform_start_point, transform_end_point], distance_node

    def stretchy_twist_joints(self):
        locators, distance_node = self.distance_between_points_measure(self.twist_origin, self.twist_end)
        stretchy_reference_group = pm.group(empty=True)
        self.name_convention.rename_based_on_base_name(self.twist_origin,
                                                       stretchy_reference_group,
                                                       name="stretchyReferencePoints")
        stretchy_reference_group.setParent(self.rig_system.kinematics)
        # RMRigTools.RMParentArray(stretchy_reference_group, locators)
        pm.parent(locators, stretchy_reference_group)

        twist_joint_divide = pm.shadingNode("multiplyDivide", asUtility=True,
                                            name="StretchyTwistJoint")
        scale_compensation = pm.shadingNode("multiplyDivide", asUtility=True,
                                            name="StretchScaleCompensation")
        # self.name_convention.RMRenameNameInFormat(TwistJointDivide,{})
        self.name_convention.rename_based_on_base_name(self.twist_origin, twist_joint_divide, name=twist_joint_divide)

        pm.connectAttr("%s.distance" % distance_node, "{}.input1X".format(twist_joint_divide))
        pm.setAttr("%s.input2X" % twist_joint_divide, (len(self.joints) - 1))

        pm.connectAttr("{}.outputX".format(twist_joint_divide), "{}.input1X".format(scale_compensation))
        pm.connectAttr("{}.scaleX".format(self.twist_origin), "{}.input2X".format(scale_compensation))

        pm.setAttr("{}.operation".format(twist_joint_divide), 2)
        pm.setAttr("{}.operation".format(scale_compensation), 2)

        for eachJoint in self.joints[1:]:
            pm.connectAttr("{}.outputX".format(scale_compensation), "{}.translateX".format(eachJoint))
        # self.kinematics.append(stretchyRefGroup)

    def create_bones_between_points(self, initial_point, final_point, number_of_bones, align_object=None):
        direction_vector = final_point - initial_point
        total_length = direction_vector.length()
        step = total_length / number_of_bones
        step_vector = direction_vector.normal() * step
        locators_list = []

        for count in range(0, number_of_bones + 1):
            Locator = pm.spaceLocator()
            if align_object:
                if self.name_convention.is_name_in_format(align_object):
                    self.name_convention.rename_based_on_base_name(align_object, Locator,
                                                                   name='TwistJoint')
            locators_list.append(Locator)
            pm.xform(Locator, translation=list(initial_point + (step_vector * count)), worldSpace=True)
            # RMRigTools.RMAlign(align_object, Locator, 2)
            pm.matchTransform(Locator, align_object, position=False, rotation=True, scale=False)

        # reset_joints, joints = RMRigTools.RMCreateBonesAtPoints(locators_list)
        reset_joints, joints = self.create.joint.point_base(*locators_list, name='twist')
        self.reset_joints.append(reset_joints)
        self.reset_joints[-1].setParent(self.rig_system.joints)
        self.joints.extend(joints)
        pm.delete(locators_list)
        return self.reset_joints, self.joints


if __name__ == '__main__':
    TJ = TwistJoints()
    TJ.create_point_base("L_intermediate01_shoulder_jnt", "L_intermediate02_shoulder_jnt")








