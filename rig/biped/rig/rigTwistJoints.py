import pymel.core as pm
import maya.api.OpenMaya as om
from RMPY.rig import rigBase
from RMPY import RMRigTools
from RMPY.rig import rigDistanceBetween
from RMPY.rig import rigMatrixParentConstraint


class TwistJointsModel(rigBase.BaseModel):
    def __init__(self):
        super(TwistJointsModel, self).__init__()
        self.twist_origin = None
        self.twist_end = None
        self.control_parent = None
        self.rig_distance_between = None


class TwistJoints(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', TwistJointsModel())
        super(TwistJoints, self).__init__(*args, **kwargs)

    def create_point_base(self, *args, **kwargs):
        super(TwistJoints, self).create_point_base(*args, **kwargs)

        self._model.control_parent = pm.ls(args[0])[0]
        self._model.twist_origin = pm.ls(args[1])[0]
        self._model.twist_end = pm.ls(args[2])[0]

        number_of_joints = kwargs.pop('number_of_joints', 2)
        look_at_axis = kwargs.pop('look_at_axis', "Z")

        self.create_twist(self.control_parent, self.twist_origin, self.twist_end,
                          number_of_twist_bones=number_of_joints,
                          look_at_axis=look_at_axis)

    @property
    def control_parent(self):
        return self._model.control_parent

    @property
    def twist_origin(self):
        return self._model.twist_origin

    @property
    def twist_end(self):
        return self._model.twist_end

    def create_twist(self, control_parent, twist_joint, twist_end_object, number_of_twist_bones=3, look_at_axis="Z"):
        # LookAtObject = pm.listRelatives( TwistJoint,type = "transform",children=True)[]
        twist_joint = pm.ls(twist_joint)[0]
        twist_end_object = pm.ls(twist_end_object)[0]
        control_parent = pm.ls(control_parent)[0]

        self.create_bones_between_points(twist_joint, twist_end_object, number_of_twist_bones, align_object=twist_joint)
        self.stretchy_twist_joints()
        rig_distance = self.rig_distance_between.distance.get()

        # pm.parentConstraint(twist_joint, self.reset_joints[0])
        # twist_joint.scale >> self.reset_joints[0].scale

        # self.create.constraint.node_base(twist_joint, self.reset_joints, mo=True)
        # self.create.constraint.matrix_node_base(twist_joint, self.reset_joints[0], mo=True)
        constraint = rigMatrixParentConstraint.RigParentConstraint()
        constraint.create_point_base(twist_joint, self.reset_joints[0], mo=False)

        # reset_point, control = RMRigShapeControls.RMCreateBoxCtrl(self.joints[0], Xratio=.1, Yratio=.1, Zratio=.1,
        # customSize=Distance / 5, name="TwistOrigin")

        # Creating an up vector control for the root of the twist
        reset_control, control = self.create.controls.point_base(self.joints[0], centered=True,
                                                                 size=rig_distance/5 * .1, name="twistOrigin")
        self.reset_controls.append(reset_control)

        move_vector = self.vector_from_axis(look_at_axis, length=rig_distance / 5)

        pm.xform(reset_control, os=True, relative=True, translation=move_vector)
        pm.aimConstraint(twist_end_object, self.joints[0],
                         aim=[1, 0, 0], worldUpVector=[0, 0, 1],
                         worldUpType="object", worldUpObject=control)
        pm.parent(self.reset_controls, self.rig_system.controls)
        self.controls.append(control)
        self.create.constraint.matrix_node_base(control_parent, self.reset_controls[0], mo=True)

        # creating a point aligned with the look at object that keeps track of the rotation
        aim_offset_sum = pm.createNode('sum', name='aimOffset')
        aim_offset_sum.input[0].set(rig_distance / 5)
        self.rig_distance_between.distance >> aim_offset_sum.input[1]

        end_look_at = self.create.space_locator.point_base(twist_end_object, name='endLookAt')
        end_look_at.setParent(self.reset_joints)
        pm.matchTransform(end_look_at, self.reset_joints, rotation=True, position=False, scale=False)
        end_aim_object = pm.duplicate(end_look_at)[0]
        self.name_convention.rename_name_in_format(end_aim_object, name='endAim')
        # pm.move(end_aim_object, rig_distance / 5, moveX=True, localSpace=True, relative=True)

        self.rig_distance_between.distance >> end_look_at.translateX
        aim_offset_sum.output >> end_aim_object.translateX

        pm.aimConstraint(end_aim_object, end_look_at,
                         aim=[1, 0, 0], worldUpVector=[0, 0, 1],
                         worldUpType="objectrotation", worldUpObject=twist_end_object)

        twist_joint_divide = pm.shadingNode("multiplyDivide", asUtility=True, name="TwistJointDiv")
        twist_addition = pm.shadingNode("plusMinusAverage", asUtility=True, name="TwistJointAdd")
        negative_look_at_rotation = pm.shadingNode("multiplyDivide", asUtility=True, name="negativeLookAtRotation")
        self.name_convention.rename_name_in_format(twist_addition, twist_joint_divide, negative_look_at_rotation,
                                                   useName=True)

        pm.connectAttr(f"{end_look_at}.rotateX", f"{negative_look_at_rotation}.input1X")
        pm.setAttr(f"{negative_look_at_rotation}.input2X", -1)
        pm.setAttr(f"{negative_look_at_rotation}.operation", 1)
        pm.connectAttr(f"{self.joints[0]}.rotateX", f"{twist_addition}.input1D[0]")
        pm.connectAttr(f"{negative_look_at_rotation}.outputX", f"{twist_addition}.input1D[1]")
        pm.connectAttr(f"{twist_addition}.output1D", f"{twist_joint_divide}.input1X")

        # pm.connectAttr("%s.rotateX" % self.joints[0], "%s.input1X" % twist_joint_divide)
        # pm.connectAttr(self.joints[0]+".rotateX", TwistJointDivide + ".input1X")

        # in this case the rotation of the lookatNode was not affecting
        pm.setAttr("%s.input2X" % twist_joint_divide, -(len(self.joints) - 1))
        pm.setAttr("%s.operation" % twist_joint_divide, 2)

        for eachJoint in self.joints[1:]:
            pm.connectAttr(f"{twist_joint_divide}.outputX", f"{eachJoint}.rotateX")



        # self.create.constraint.node_base(control_parent, self.reset_controls[0], mo=True)

    def stretchy_twist_joints(self):
        self._model.rig_distance_between = rigDistanceBetween.RigDistanceBetween(rig_system=self.rig_system)
        self.rig_distance_between.create_point_base(self.twist_origin, self.twist_end)
        twist_joint_divide = pm.shadingNode("multiplyDivide", asUtility=True)
        scale_compensation = pm.shadingNode("multiplyDivide", asUtility=True,
                                            name="StretchScaleCompensation")
        self.name_convention.rename_name_in_format(twist_joint_divide, name="StretchyTwistJoint")

        pm.connectAttr(self.rig_distance_between.distance, f"{twist_joint_divide}.input1X")
        pm.setAttr(f"{twist_joint_divide}.input2X", (len(self.joints) - 1))

        pm.connectAttr(f"{twist_joint_divide}.outputX", f"{scale_compensation}.input1X")
        pm.connectAttr(f"{self.reset_joints[0]}.scaleX", f"{scale_compensation}.input2X")
        #                                 twist_origin
        pm.setAttr("{}.operation".format(twist_joint_divide), 2)
        pm.setAttr("{}.operation".format(scale_compensation), 2)

        for eachJoint in self.joints[1:]:
            pm.connectAttr("{}.outputX".format(scale_compensation), "{}.translateX".format(eachJoint))

    def create_bones_between_points(self, initial_object, final_object, number_of_bones, align_object=None):
        """
         Creates a number_of_bones between the initial and final point, which are positions in space
        """
        position_a = pm.xform(initial_object, q=True, ws=True, rp=True)
        position_b = pm.xform(final_object, q=True, ws=True, rp=True)
        initial_point = om.MVector(position_a)
        final_point = om.MVector(position_b)

        direction_vector = final_point - initial_point
        total_length = direction_vector.length()
        step = total_length / number_of_bones
        step_vector = direction_vector.normal() * step
        locators_list = []

        for count in range(0, number_of_bones + 1):
            space_locator = pm.spaceLocator()
            locators_list.append(space_locator)
            if align_object:
                if self.name_convention.is_name_in_format(align_object):
                    self.name_convention.rename_based_on_base_name(align_object, space_locator, name='TwistJoint')
                pm.xform(space_locator, translation=list(initial_point + (step_vector * count)), worldSpace=True)
                pm.matchTransform(space_locator, align_object, position=False, rotation=True, scale=False)
            else:
                self.name_convention.rename_name_in_format(space_locator, name='TwistJoint')
                self.transform.aim_point_based(space_locator, initial_object, final_object, use_destination_up_axis=True)
                pm.xform(space_locator, translation=list(initial_point + (step_vector * count)), worldSpace=True)

        reset_joints, joints = self.create.joint.point_base(*locators_list, name='twist', orient_type='point_orient')
        self.reset_joints.append(reset_joints)
        self.reset_joints[-1].setParent(self.rig_system.joints)
        self.joints.extend(joints)
        pm.delete(locators_list)
        return self.reset_joints, self.joints

    def vector_from_axis(self, axis, length=1):
        sign = 1
        if "-" in axis:
            sign = -1
        if "Z" in axis or "z" in axis:
            result_vector = [0, 0, length * sign]
        elif "Y" in axis or "y" in axis:
            result_vector = [0, length * sign, 0]
        else:
            result_vector = [length * sign, 0, 0]
        return result_vector


if __name__ == '__main__':
    TJ = TwistJoints()
    # TJ.create_bones_between_points('C_fk00_neck_jnt', 'C_fk00_head_jnt', 3)
    TJ.create_point_base('C_joints00_neck_grp', 'C_fk00_neck_jnt', 'C_fk00_head_jnt')








