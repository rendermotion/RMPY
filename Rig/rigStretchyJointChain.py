import pymel.core as pm
from RMPY.rig import rigBase


class StretchyJointChainModel(rigBase.BaseModel):
    def __init__(self):
        super(StretchyJointChainModel, self).__init__()
        self.ik_handle = None
        self.start_point = None
        self.end_point = None


class StretchyJointChain(rigBase.RigBase):
    def __init__(self, ik_handle, **kwargs):
        if 'model' not in kwargs.keys():
            kwargs['model'] = StretchyJointChainModel()
        super(StretchyJointChain, self).__init__(ik_handle, **kwargs)
        self._model.ik_handle = ik_handle

    @property
    def ik_handle(self):
        return self._model.ik_handle

    @property
    def start_point(self):
        return self._model.start_point

    @property
    def end_point(self):
        return self._model.end_point

    def bone_chain_lenght(self):
        distancia = 0
        for index in range(1, len(self.joints)):
            distancia += self.rm.point_distance(self.joints[index - 1], self.joints[index])
        return distancia

    def identify_joints(self, ik_handle):
        end_effector = pm.ikHandle(ik_handle, q=True, endEffector=True)
        end_joint = self.rm.custom_pick_walk(end_effector, 1, maya_node_type='joint', direction="up")
        end_joint = self.rm.custom_pick_walk(end_joint[len(end_joint) - 1], 1, direction="down")
        end_joint = end_joint[1]
        start_joint = pm.ikHandle(ik_handle, q=True, startJoint=True)
        [self.joints.append(each) for each in self.rm.find_in_hierarchy(start_joint, end_joint)]

    def ik_handle_based(self):
        self.identify_joints(self.ik_handle)
        self.ik_handle.snapEnable.set(False)
        self.rig_joints_base()

    def rig_joints_base(self):
        total_distance = self.bone_chain_lenght()
        self._model.start_point = pm.spaceLocator(name="StretchyIkHandleStartPoint")
        self.name_convention.rename_name_in_format(self.start_point, useName=True)
        self._model.end_point = pm.spaceLocator(name="StretchyIkHandleEndPoint")
        self.name_convention.rename_name_in_format(self.end_point, useName=True)
        self.start_point.setParent(self.rig_system.kinematics)
        self.end_point.setParent(self.rig_system.kinematics)

        if self.reset_joints:
            pm.parent(self.start_point, self.reset_joints)
            pm.parent(self.end_point, self.reset_joints)

        pm.pointConstraint(self.joints[0], self.start_point)
        pm.pointConstraint(self.ik_handle, self.end_point)

        distance_node = pm.shadingNode("distanceBetween", asUtility=True,
                                       name="IKDistance" + self.name_convention.get_a_short_name(self.joints[-1]))
        self.name_convention.rename_based_on_base_name(self.joints[2], distance_node, name=distance_node)

        pm.connectAttr(self.start_point.worldPosition[0], distance_node.point1, f=True)
        pm.connectAttr(self.end_point.worldPosition[0], distance_node.point2, f=True)

        condition_node = pm.shadingNode("condition", asUtility=True,
                                        name="IkCondition" + self.name_convention.get_a_short_name(self.joints[2]))
        condition_node = self.name_convention.rename_based_on_base_name(self.joints[2], condition_node,
                                                                        name=condition_node)
        pm.connectAttr(distance_node + ".distance", condition_node + ".colorIfFalseR", f=True)
        pm.connectAttr(distance_node + ".distance", condition_node + ".secondTerm", f=True)
        pm.setAttr(condition_node + ".operation", 3)
        pm.setAttr(condition_node + ".firstTerm", total_distance)
        pm.setAttr(condition_node + ".colorIfTrueR", total_distance)
        multiply_divide = pm.shadingNode("multiplyDivide", asUtility=True,
                                         name="IKStretchMultiply" + self.name_convention.get_a_short_name(
                                             self.joints[2]))
        self.name_convention.rename_based_on_base_name(self.joints[2], multiply_divide, name=multiply_divide)

        pm.connectAttr(condition_node + ".outColorR", multiply_divide + ".input1X", f=True)
        pm.setAttr(multiply_divide + ".input2X", total_distance)
        pm.setAttr(multiply_divide + ".operation", 2)

        # self.rig_space_switch.AddNumericParameter(self.controls_dict['ikHandle'], Name="StretchyIK")
        pm.addAttr(self.ik_handle, ln="stretchyIK", at='float', min=0, max=10, k=True)
        ik_switch_divide = pm.shadingNode("multiplyDivide", asUtility=True,
                                          name="IkSwitchDivide" + self.name_convention.get_a_short_name(self.joints[2]))
        self.name_convention.rename_based_on_base_name(self.joints[2], ik_switch_divide, name=ik_switch_divide)
        pm.connectAttr("%s.stretchyIK" % self.ik_handle, ik_switch_divide + ".input1X")
        pm.setAttr(ik_switch_divide + ".input2X", 10)
        pm.setAttr(ik_switch_divide + ".operation", 2)

        ik_switchblend_two_attr = pm.shadingNode("blendTwoAttr", asUtility=True,
                                                 name="IkSwitchBlendTwoAttr{}".format(
                                                     self.name_convention.get_a_short_name(self.joints[2])))
        self.name_convention.rename_based_on_base_name(self.joints[2], ik_switchblend_two_attr,
                                                       name=ik_switchblend_two_attr)

        pm.connectAttr(multiply_divide.outputX, ik_switchblend_two_attr.input[1], force=True)
        ik_switchblend_two_attr.input[0].set(1)
        pm.connectAttr(ik_switch_divide.outputX, ik_switchblend_two_attr.attributesBlender, force=True)

        for joints in self.joints[:-1]:
            pm.connectAttr(ik_switchblend_two_attr.output, '{}.scaleX'.format(joints))