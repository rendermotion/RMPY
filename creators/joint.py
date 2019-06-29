import pymel.core as pm
from RMPY.core import dataValidators
from RMPY.core import config
from RMPY.core import transform
import maya.api.OpenMaya as om
from RMPY.creators import group
from RMPY import RMNameConvention
from RMPY.core import transform
from RMPY.creators import spaceLocator
from RMPY.creators import creatorsBase

reload(group)
reload(transform)
reload(spaceLocator)
reload(creatorsBase)


class Joint(creatorsBase.Creator):
    def __init__(self, *args, **kwargs):
        super(Joint, self).__init__(*args, **kwargs)
        self.group_creator = group.Creator()

    def point_base(self, *point_array, **kwargs):
        #super(Creator, self).point_base(*point_array, **kwargs)
        """
        orient_type:
            'default': uses default maya joint orient
            'bend_orient': uses the bend vector of the orient to define joint orientation
            'point_orient': uses the axis of the point based to define orientation
        """
        aim_axis = kwargs.pop('aim_axis', config.orient_axis[0])
        up_axis = kwargs.pop('up_axis', config.orient_axis[1])
        orient_type = kwargs.pop('orient_type', 'bend_orient')

        point_array = dataValidators.as_pymel_nodes(point_array)
        joint_array = []

        for index, point in enumerate(point_array):
            pm.select(cl=True)
            new_joint = pm.joint(p=[0, 0, 0], name="joint")

            transform.align(point, new_joint)

            joint_array.append(new_joint)

            self.name_convention.rename_name_in_format(new_joint, name='joint')

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

    def point_based(self, PointArray, ZAxisOrientation = "Y"):
        ZAxisOrientation = config.orient_axis[1]

        PointArray = dataValidators.as_pymel_nodes(PointArray)
        jointArray = []

        Obj1Position = pm.xform(PointArray[0], q=True, rp=True, ws=True)
        Obj2Position = pm.xform(PointArray[1], q=True, rp=True, ws=True)

        V1, V2 = om.MVector(Obj1Position), om.MVector(Obj2Position)

        initVector = V1 - V2

        firstJntAngle = V1.angle(om.MVector([0, 1, 0]))

        Angle = firstJntAngle

        ParentJoint = self.RMCreateGroupOnObj(PointArray[0], Type="world")

        for index in range(0, len(PointArray)):

            pm.select(cl=True)

            newJoint = pm.joint(p=[0, 0, 0], name="joint")
            jointArray.append(newJoint)
            self.name_convention.rename_name_in_format(str(newJoint),
                                                 name=self.name_convention.get_a_short_name(str(PointArray[index])),
                                                 side=self.name_convention.get_from_name(str(PointArray[index]), 'side'))

            if index == 0:
                pm.parent(jointArray[0], ParentJoint)

            transform.align(PointArray[index], jointArray[index])
            pm.makeIdentity(jointArray[index], apply=True, t=1, r=1, s=0)

            if (index > 0):
                if index == 1:
                    AxisOrientJoint = pm.joint()
                    pm.parent(AxisOrientJoint, ParentJoint)
                    transform.align(PointArray[0], AxisOrientJoint)
                    pm.makeIdentity(AxisOrientJoint, apply=True, t=1, r=1, s=0)

                    if ZAxisOrientation in "Yy":
                        pm.xform(AxisOrientJoint, translation=[0, -1, 0], objectSpace=True)

                    elif ZAxisOrientation in "Xx":
                        pm.xform(AxisOrientJoint, translation=[-1, 0, 0], objectSpace=True)

                    elif ZAxisOrientation in "Zz":
                        pm.xform(AxisOrientJoint, translation=[0, 0, -1], objectSpace=True)

                    pm.parent(jointArray[0], AxisOrientJoint)
                    pm.parent(jointArray[index], jointArray[index - 1])
                    pm.joint(jointArray[index - 1], edit=True, orientJoint=config.orient_axis)

                    pm.parent(jointArray[index - 1], world=True)
                    pm.delete(AxisOrientJoint)
                    transform.align(jointArray[index - 1], ParentJoint)
                    pm.parent(jointArray[index - 1], ParentJoint)

                else:
                    pm.parent(jointArray[index], jointArray[index - 1])
                    pm.joint(jointArray[index - 1], edit=True, orientJoint=config.orient_axis)
                # , sao="yup" )

                if index >= 2:
                    parentOrient = pm.joint(jointArray[index - 1], q=True, orientation=True)
                    # pm.joint(jointArray[index - 1], e=True, orientation=[parentOrient[0], parentOrient[1], parentOrient[2]])
                    if parentOrient[config.orient_index[0]] > 89:
                        parentOrient[config.orient_index[0]] = parentOrient[config.orient_index[0]] - 180
                        jointArray[index - 1].attr('rotate%s' % config.orient_axis_up[0]).set(180)
                        # pm.joint(jointArray[index-1], e=True, orientation=[parentOrient[0], parentOrient[1], parentOrient[2]])
                        pm.makeIdentity(jointArray[index - 1], r=True, apply=True)
                    else:
                        if parentOrient[config.orient_index[0]] < -89:
                            parentOrient[config.orient_index[0]] = parentOrient[config.orient_index[0]] + 180
                            jointArray[index - 1].attr('rotate%s' % config.orient_axis_up[0]).set(180)
                            pm.makeIdentity(jointArray[index - 1], r=True, apply=True)
                            # pm.joint(jointArray[index-1], e=True, orientation=[parentOrient[0], parentOrient[1], parentOrient[2]])

            if index == len(PointArray) - 1:
                transform.align(jointArray[index - 1], jointArray[index], rotate=False)
                pm.makeIdentity(jointArray[index], apply=True, t=0, r=1, s=0)
            jointArray[index].rotateOrder.set(config.orient_axis)
        return ParentJoint, jointArray

    def default_orient(self, *joint_list, **kwargs):
        aim_axis = kwargs.pop('aim_axis', config.orient_axis[0])
        up_axis = kwargs.pop('up_axis', config.orient_axis[1])
        axis = '%s%s%s' % (aim_axis, up_axis, filter(lambda ch: ch not in '%s%s' % (aim_axis, up_axis), 'xyz'))
        for each_joint in joint_list:
            joint_child = each_joint.getChildren(type='joint')
            if joint_child:
                pm.joint(each_joint, e=True, orientJoint=axis)
            else:
                parent = each_joint.getParent()
                if parent:
                    transform.align(parent, each_joint, translate=False)
                pm.makeIdentity(each_joint, t=False, r=True, s=False, apply=True)

    def point_orient(self, *joint_list, **kwargs):
        point_list = kwargs.pop('point_list', None)
        for each_joint, each_point in zip(joint_list, point_list):
            transform.align(each_point, each_joint, translate=False)
            pm.makeIdentity(each_joint, t=False, r=True, s=False, apply=True)

    def bend_orient(self, *joint_list):
        space_locator = spaceLocator.Creator()
        for each_joint in joint_list:
            print 'each_joint'
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
    root = pm.ls('L_bodyWing00_reference_GRP')[0]
    joints = Joint()
    joints.point_base(*root.getChildren(), orient_type='bend_orient')