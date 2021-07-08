import maya.api.OpenMaya as om
from RMPY.rig import rigBase
import pymel.core as pm


class RibonModel(rigBase.BaseModel):
    def __init__(self):
        super(RibonModel, self).__init__()
        self.base_objects = []
        self.joint_structure = []
        self.folicules = []
        self.allControls = []


class Ribon(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', RibonModel())
        super(Ribon, self).__init__(*args, **kwargs)
        self.base_objects = []
        self.joint_structure = []
        self.folicules = []
        self.all_controls = []

    def nurb_plane_between_objects(self, Object01, Object02):
        VP1 = om.MVector(pm.xform(Object01, a=True, ws=True, q=True, rp=True))
        print VP1
        VP2 = om.MVector(pm.xform(Object02, a=True, ws=True, q=True, rp=True))
        print VP2
        longitud = VP1 - VP2
        plano = pm.nurbsPlane(ax=[0, 1, 0], p=[(longitud.length()) / 2, 0, 0], w=longitud.length(), lr=.05, d=3, u=8,
                              v=1, ch=0, name="bendyPlane")
        self.name_convention.rename_name_in_format(plano, useName=True)

        pm.matchTransform(plano[0], Object01)
        return plano[0]

    # nurbPlaneBetweenObjects("joint1","joint2")
    def create_point_base(self, *args, **kwargs):
        folicule_number = kwargs.pop('folicule_number', 3)
        super(Ribon, self).create_point_base(*args, **kwargs)
        object01 = args[0]
        object02 = args[1]
        self.base_objects.append(object01)
        self.base_objects.append(object02)
        VP1 = om.MVector(pm.xform(object01, a=True, ws=True, q=True, rp=True))
        VP2 = om.MVector(pm.xform(object02, a=True, ws=True, q=True, rp=True))
        plano = self.nurb_plane_between_objects(object01, object02)
        planoShape = pm.listRelatives(plano, shapes=True)[0]
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
        nstep = 1.0 / (folicule_number - 1.0)
        hs = pm.language.Mel.eval('createNode hairSystem')
        hair_system = "hairSystem1"
        array_joints = []

        folicules = []

        for n in range(folicule_number):
            pm.language.Mel.eval(
                'createHairCurveNode("%s", "%s" ,%s ,.5 , 1 ,0 ,0 ,0 ,0 ,"" ,1.0 ,{%s} ,"" ,"" ,2 );' % (
                 hair_system, planoShape, nstep * n, n))
            NewFolicule = self.name_convention.rename_name_in_format("follicle1")
            folicules.append(NewFolicule)
            pm.parent(NewFolicule, hair_group)

        self.folicules = folicules
        pm.delete(pm.listRelatives(hair_system, p=True))
        index = 0
        skinedJoints = pm.group(em=True, name="skinedJoints")
        self.name_convention.rename_name_in_format(skinedJoints, useName=True)
        skinedJoints.setParent(self.rig_system.joints)
        for eachFolicule in folicules:
            array_joints.append(pm.joint(name="ribbonJoints"))
            self.name_convention.rename_name_in_format(array_joints[index], useName=True)
            pm.matchTransform(array_joints[index], eachFolicule)
            pm.parentConstraint(eachFolicule, array_joints[index])
            index += 1
        self.joint_structure = array_joints

        controles = []
        resetControles = []
        locatorControlesList = []
        locatorLookAtList = []
        jointsLookAtList = []
        groupLookAtList = []

        GroupJoints = pm.group(empty=True, name="groupJointsLookAt")
        self.name_convention.rename_name_in_format(GroupJoints, useName=True)

        self.joints.append(GroupJoints)

        for iloop in range(3):
            reset_control_group, control = self.create.controls.point_base(object01, type='circular',
                                                                           size=ribon_size.length() / 3,
                                                                           name='bendy')
            controles.append(control)
            resetControles.append(reset_control_group)

            locator_control = pm.spaceLocator(name="locatorCntrl")
            self.name_convention.rename_name_in_format(locator_control, useName=True)
            locatorControlesList.append(locator_control)
            pm.matchTransform(locator_control, object01)

            locatorLookAt = pm.spaceLocator(name="locatorLookAt")
            self.name_convention.rename_name_in_format(locatorLookAt,useName=True)

            locatorLookAtList.append(locatorLookAt)
            pm.matchTransform(locatorLookAt, object01)

            pm.select(clear=True)

            jointsLookAt = pm.joint(name="jointsLookAt")
            self.name_convention.rename_name_in_format(jointsLookAt, useName=True)
            jointsLookAtList.append(jointsLookAt)
            pm.matchTransform(jointsLookAt, object01)

            groupLookAt = pm.group(empty=True, name="lookAt")
            self.name_convention.rename_name_in_format(groupLookAt, useName=True)

            groupLookAt.setParent(self.rig_system.kinematics)
            groupLookAtList.append(groupLookAt)
            pm.matchTransform(groupLookAt, object01)
            for each in groupLookAtList:
                pm.parent(each, main_skeleton)

            pm.move(ribon_size.length() / 2 * iloop, 0, 0, reset_control_group, r=True, os=True, moveX=True)
            pm.move(ribon_size.length() / 2 * iloop, 0, 0, locator_control, r=True, os=True, moveX=True)
            pm.move(ribon_size.length() / 2 * iloop, 0, 1, locatorLookAt, r=True, os=True, moveXYZ=True)
            pm.move(ribon_size.length() / 2 * iloop, 0, 0, jointsLookAt, r=True, os=True, moveX=True)
            pm.move(ribon_size.length() / 2 * iloop, 0, 0, groupLookAt, r=True, os=True, moveX=True)

            pm.parent(reset_control_group, self.rig_system.controls)
            pm.parent(locator_control, groupLookAt)
            pm.parent(locatorLookAt, groupLookAt)
            pm.parent(jointsLookAt, GroupJoints)

            pm.makeIdentity(control, apply=True, t=1, r=0, s=1, n=0)
            pm.makeIdentity(jointsLookAt, apply=True, t=1, r=0, s=1, n=0)

            pm.parentConstraint(locator_control, jointsLookAt)
            pm.parentConstraint(control, groupLookAt)

        self.controls.extend(controles)
        self.reset_controls.extend(resetControles)
        pm.aimConstraint(controles[1], locatorControlesList[0], aim=[1, 0, 0], upVector=[0, 0, 1], wut='object',
                         worldUpObject=locatorLookAtList[0])
        pm.aimConstraint(controles[1], locatorControlesList[2], aim=[1, 0, 0], upVector=[0, 0, 1], wut='object',
                         worldUpObject=locatorLookAtList[2])

        pm.parent(GroupJoints, main_skeleton)

        pm.skinCluster(jointsLookAtList, plano)
        pm.parent(plano, hair_group)
        hair_system_pm = pm.ls('hairSystem1')[0]
        hair_system_pm.setParent(self.rig_system.kinematics)

if __name__ == '__main__':
    rig_ribon = Ribon()
    rig_ribon.create_point_base("L_intermediate00_shoulder_sknjnt", "L_intermediate01_shoulder_sknjnt", folicule_number = 6)
