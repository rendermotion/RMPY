import pymel.core as pm
from RMPY.core import dataValidators
from RMPY.core import config
import maya.api.OpenMaya as om
from RMPY.creators import group
from RMPY.core import transform
from RMPY.creators import spaceLocator
from RMPY.creators import creatorsBase


class Joint(creatorsBase.CreatorsBase):
    def __init__(self, *args, **kwargs):
        super(Joint, self).__init__(*args, **kwargs)
        self.group_creator = group.Group()

    def point_base(self, *point_array, **kwargs):
        # super(Creator, self).point_base(*point_array, **kwargs)
        """
        orient_type:
            'default': uses default maya joint orient
            'bend_orient': uses the bend vector of the orient to define joint orientation
            'point_orient': uses the axis of the point based to define orientation
        """
        custom_name = kwargs.pop('name', 'joint')
        aim_axis = kwargs.pop('aim_axis', config.axis_order[0])
        up_axis = kwargs.pop('up_axis', config.axis_order[1])
        orient_type = kwargs.pop('orient_type', 'bend_orient')
        joint_type = kwargs.pop('joint_type', 'joint')
        point_array = dataValidators.as_pymel_nodes(*point_array)
        joint_array = []

        for index, point in enumerate(point_array):
            pm.select(cl=True)
            new_joint = pm.joint(p=[0, 0, 0], name="joint")
            new_joint.segmentScaleCompensate.set(0)
            pm.matchTransform(new_joint, point)
            joint_array.append(new_joint)
            self.name_convention.rename_name_in_format(new_joint, name=custom_name, objectType=joint_type)

            if index > 0:
                new_joint.setParent(joint_array[index-1])

            pm.makeIdentity(new_joint, apply=True, t=1, r=1, s=1)

        if orient_type == 'point_orient':
            self.point_orient(*joint_array, point_list=point_array)

        elif orient_type == 'bend_orient':
            self.bend_orient(*joint_array)

        elif orient_type == 'default':
            self.default_orient(*joint_array, aim_axis=aim_axis, up_axis=up_axis)

        reset_joints = self.group_creator.point_base(joint_array[0], type="parent")

        return reset_joints, joint_array

    def point_based(self, point_array, z_axis_orientation ="Y", **kwargs):
        custom_name = kwargs.pop('name', None)
        joint_type = kwargs.pop('joint_type', 'joint')
        z_axis_orientation = config.axis_order[1]

        point_array = dataValidators.as_pymel_nodes(*point_array)
        joint_array = []

        Obj1Position = pm.xform(point_array[0], q=True, rp=True, ws=True)
        Obj2Position = pm.xform(point_array[1], q=True, rp=True, ws=True)

        V1, V2 = om.MVector(Obj1Position), om.MVector(Obj2Position)

        initVector = V1 - V2

        firstJntAngle = V1.angle(om.MVector([0, 1, 0]))

        Angle = firstJntAngle

        ParentJoint = self.RMCreateGroupOnObj(point_array[0], Type="world")

        for index in range(0, len(point_array)):

            pm.select(cl=True)

            new_joint = pm.joint(p=[0, 0, 0], name="joint")
            new_joint.segmentScaleCompensate.set(0)
            joint_array.append(new_joint)
            if not custom_name:
                joint_name = self.name_convention.get_a_short_name(str(point_array[index]))
            else:
                joint_name = custom_name
            self.name_convention.rename_name_in_format(str(new_joint),
                                                       name=joint_name,
                                                       side=self.name_convention.get_from_name(str(point_array[index]), 'side'),
                                                       objectType=joint_type)

            if index == 0:
                pm.parent(joint_array[0], ParentJoint)

            pm.matchTransform(joint_array[index], point_array[index])
            pm.makeIdentity(joint_array[index], apply=True, t=1, r=1, s=0)

            if index > 0:
                if index == 1:
                    axis_orient_joint = pm.joint()
                    pm.parent(axis_orient_joint, ParentJoint)
                    pm.matchTransform(axis_orient_joint, point_array[0])
                    pm.makeIdentity(axis_orient_joint, apply=True, t=1, r=1, s=0)

                    if z_axis_orientation in "Yy":
                        pm.xform(axis_orient_joint, translation=[0, -1, 0], objectSpace=True)

                    elif z_axis_orientation in "Xx":
                        pm.xform(axis_orient_joint, translation=[-1, 0, 0], objectSpace=True)

                    elif z_axis_orientation in "Zz":
                        pm.xform(axis_orient_joint, translation=[0, 0, -1], objectSpace=True)

                    pm.parent(joint_array[0], axis_orient_joint)
                    pm.parent(joint_array[index], joint_array[index - 1])
                    pm.joint(joint_array[index - 1], edit=True, orientJoint=config.axis_order)

                    pm.parent(joint_array[index - 1], world=True)
                    pm.delete(axis_orient_joint)
                    pm.matchTransform(ParentJoint, joint_array[index - 1])
                    pm.parent(joint_array[index - 1], ParentJoint)

                else:
                    pm.parent(joint_array[index], joint_array[index - 1])
                    pm.joint(joint_array[index - 1], edit=True, orientJoint=config.axis_order)
                # , sao="yup" )

                if index >= 2:
                    parentOrient = pm.joint(joint_array[index - 1], q=True, orientation=True)
                    # pm.joint(jointArray[index - 1], e=True, orientation=[parentOrient[0], parentOrient[1], parentOrient[2]])
                    if parentOrient[config.orient_index[0]] > 89:
                        parentOrient[config.orient_index[0]] = parentOrient[config.orient_index[0]] - 180
                        joint_array[index - 1].attr('rotate%s' % config.orient_axis_up[0]).set(180)
                        # pm.joint(jointArray[index-1], e=True, orientation=[parentOrient[0], parentOrient[1], parentOrient[2]])
                        pm.makeIdentity(joint_array[index - 1], r=True, apply=True)
                    else:
                        if parentOrient[config.orient_index[0]] < -89:
                            parentOrient[config.orient_index[0]] = parentOrient[config.orient_index[0]] + 180
                            joint_array[index - 1].attr('rotate%s' % config.orient_axis_up[0]).set(180)
                            pm.makeIdentity(joint_array[index - 1], r=True, apply=True)
                            # pm.joint(jointArray[index-1], e=True, orientation=[parentOrient[0], parentOrient[1], parentOrient[2]])

            if index == len(point_array) - 1:
                pm.matchTransform(joint_array[index], joint_array[index - 1], position=True)
                pm.makeIdentity(joint_array[index], apply=True, t=0, r=1, s=0)
            joint_array[index].rotateOrder.set(config.axis_order)
        return ParentJoint, joint_array

    def default_orient(self, *joint_list, **kwargs):
        aim_axis = kwargs.pop('aim_axis', config.axis_order[0])
        up_axis = kwargs.pop('up_axis', config.axis_order[1])
        axis = '{}{}{}'.format(aim_axis, up_axis, 'xyz'.strip(aim_axis).strip(up_axis))
        print(axis)
        for each_joint in joint_list:
            joint_child = each_joint.getChildren(type='joint')
            if joint_child:
                pm.joint(each_joint, e=True, orientJoint=axis)
            else:
                parent = each_joint.getParent()
                if parent:
                    pm.matchTransform(each_joint, parent, rotation=True)
                pm.makeIdentity(each_joint, t=False, r=True, s=False, apply=True)

    def point_orient(self, *joint_list, **kwargs):
        point_list = kwargs.pop('point_list', None)
        for each_joint, each_point in zip(joint_list, point_list):
            pm.matchTransform(each_joint, each_point, rotation=True)
            pm.makeIdentity(each_joint, t=False, r=True, s=False, apply=True)

    def bend_orient(self, *joint_list):
        space_locator = spaceLocator.SpaceLocator()
        for each_joint in joint_list:
            parent = each_joint.getParent()
            child = each_joint.getChildren(type='joint')
            if parent:
                if pm.objectType(parent) != 'joint':
                    parent = None

            if child:
                child = child[0]

            if child and parent:
                pole_vector = space_locator.pole_vector(parent, each_joint, child)

                childrens = each_joint.getChildren()
                pm.parent(childrens, None)

                transform.aim_point_based(each_joint, each_joint, child, pole_vector)
                pm.makeIdentity(each_joint, t=False, r=True, s=False, apply=True)

                pm.parent(childrens, each_joint)

                pm.delete(pole_vector)

            elif child:
                grand_child = child.getChildren(type='joint')
                if grand_child:
                    grand_child = grand_child[0]
                    pole_vector = space_locator.pole_vector(each_joint, child, grand_child)
                    childrens = each_joint.getChildren()

                    pm.parent(childrens, None)

                    transform.aim_point_based(each_joint, each_joint, child, pole_vector)
                    pm.makeIdentity(each_joint, t=False, r=True, s=False, apply=True)

                    pm.parent(childrens, each_joint)

                    pm.delete(pole_vector)
                else:
                    self.default_orient(each_joint)
            else:
                self.default_orient(each_joint)


if __name__ == '__main__':
    pass
    '''root = pm.ls('L_index01_rig_pnt')[0]
    root_finger = pm.ls('L_index01_rig_pnt')[0]
    finger_points = rm.descendants_list(root_finger)
    joints = Joint()
    joints.point_base(*finger_points, orient_type='bend_orient')'''
    joints = Joint()
    joints.point_base('C_Hip00_reference_pnt', 'C_Hip01_reference_pnt')