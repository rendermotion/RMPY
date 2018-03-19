import maya.api.OpenMaya as om
from RMPY import RMNameConvention
from RMPY import RMRigTools
from RMPY import RMRigShapeControls
import pymel.core as pm


class RMRibbon(object):
    def __init__(self, name_conv = None):
        if not name_conv:
            self.name_conv = RMNameConvention.RMNameConvention()
        else:
            self.name_conv = name_conv
        self.rig_controls = RMRigShapeControls.RMRigShapeControls(NameConv=name_conv)
        self.kinematics = []
        self.joints = []
        self.controls = []
        self.baseObjects = []
        self.jointStructure = []
        self.folicules = []
        self.resetControls = []
        self.allControls = []

    def nurbPlaneBetweenObjects(self, Object01, Object02):
        VP1 = om.MVector(pm.xform(Object01, a=True, ws=True, q=True, rp=True))
        VP2 = om.MVector(pm.xform(Object02, a=True, ws=True, q=True, rp=True))
        longitud = VP1 - VP2
        plano = pm.nurbsPlane(ax=[0, 1, 0], p=[(longitud.length()) / 2, 0, 0], w=longitud.length(), lr=.05, d=3, u=8,
                              v=1, ch=0, name="%sTo%sPlane" % (self.name_conv.get_a_short_name(Object01),
                                                               self.name_conv.get_a_short_name(Object02)))
        self.name_conv.set_name_in_format(plano, useName=True)

        RMRigTools.RMAlign(Object01, plano[0], 3)
        return plano[0]

    # nurbPlaneBetweenObjects("joint1","joint2")
    def RibbonCreation(self, Object01, Object02, foliculeNumber=5):
        print 'creating riboon in %s and %s'% (Object01, Object02)
        self.baseObjects.append(Object01)
        self.baseObjects.append(Object02)
        VP1 = om.MVector(pm.xform(Object01, a=True, ws=True, q=True, rp=True))
        VP2 = om.MVector(pm.xform(Object02, a=True, ws=True, q=True, rp=True))
        plano = self.nurbPlaneBetweenObjects(Object01, Object02)
        planoShape = pm.listRelatives(plano, shapes=True)[0]
        pm.select(cl=True)
        RibbonSize = VP1 - VP2

        print "plano = %s" % plano
        print "len = %s" % RibbonSize.length()

        MainSkeleton = pm.group(em=True, name="%sTo%sRibbon" % (self.name_conv.get_a_short_name(Object01),
                                                                self.name_conv.get_a_short_name(Object02)))
        self.name_conv.rename_name_in_format(MainSkeleton, {}, useName=True)
        HairGroup = pm.group(em=True, name="%sTo%sHairSystem" % (self.name_conv.get_a_short_name(Object01),
                                                                  self.name_conv.get_a_short_name(Object02)))
        self.name_conv.set_name_in_format(HairGroup, useName=True)

        nstep = 1.0 / (foliculeNumber - 1.0)
        Hys = pm.language.Mel.eval('createNode hairSystem')
        Hys = "hairSystem1"
        ArrayJoints = []
        HairSystemIndex = [0]

        folicules = []

        for n in range(foliculeNumber):
            pm.language.Mel.eval(
                'createHairCurveNode("%s", "%s" ,%s ,.5 , 1 ,0 ,0 ,0 ,0 ,"" ,1.0 ,{%s} ,"" ,"" ,2 );' % (
                Hys, planoShape, nstep * n, n))
            NewFolicule = self.name_conv.rename_name_in_format("follicle1", {})
            folicules.append(NewFolicule)
            pm.parent(NewFolicule, HairGroup)
        self.folicules = folicules
        pm.delete(pm.listRelatives(Hys, p=True))
        index = 0
        skinedJoints = pm.group(em=True, name="%sTo%sskinedJoints" % (self.name_conv.get_a_short_name(Object01),
                                                                      self.name_conv.get_a_short_name(Object02)))
        self.name_conv.rename_name_in_format(skinedJoints, useName=True)
        for eachFolicule in folicules:
            ArrayJoints.append(pm.joint(name="%sTo%sRibbonJoints" % (self.name_conv.get_a_short_name(Object01),
                                                                     self.name_conv.get_a_short_name(Object02))))
            self.name_conv.set_name_in_format(ArrayJoints[index], useName=True)
            RMRigTools.RMAlign(eachFolicule, ArrayJoints[index], 3)
            pm.parentConstraint(eachFolicule, ArrayJoints[index])
            index += 1
        self.jointStructure = ArrayJoints

        controles = []
        resetControles = []
        locatorControlesList = []
        locatorLookAtList = []
        jointsLookAtList = []
        groupLookAtList = []

        GroupControls = pm.group(empty=True, name="%sTo%sControls" % (self.name_conv.get_a_short_name(Object01),
                                                                      self.name_conv.get_a_short_name(Object02)))

        self.name_conv.rename_name_in_format(GroupControls, {}, useName=True)
        GroupJoints = pm.group(empty=True, name="%sTo%sGroupJointsLookAt" % (self.name_conv.get_a_short_name(Object01),
                                                                             self.name_conv.get_a_short_name(Object02)))
        self.name_conv.rename_name_in_format(GroupJoints, {}, useName=True)

        self.allControls.append(GroupControls)
        self.joints.append(GroupJoints)

        for iloop in range(3):
            resetControlGroup, control = self.rig_controls.RMCircularControl(Object01, radius=RibbonSize.length() / 3,
                                                                             name="%sTo%sCtrl" % (
                                                                       self.name_conv.get_a_short_name(Object01),
                                                                       self.name_conv.get_a_short_name(Object02)))
            controles.append(control)
            resetControles.append(resetControlGroup)

            locatorControl = pm.spaceLocator(name="%sTo%sLocatorCntrl" % (self.name_conv.get_a_short_name(Object01),
                                                                          self.name_conv.get_a_short_name(Object02)))
            self.name_conv.rename_name_in_format(locatorControl, {}, useName=True)
            locatorControlesList.append(locatorControl[0])
            RMRigTools.RMAlign(Object01, locatorControl[0], 3)

            locatorLookAt = pm.spaceLocator(name="%sTo%sLocatorLookAt" % (self.name_conv.get_a_short_name(Object01),
                                                                          self.name_conv.get_a_short_name(Object02)))
            self.name_conv.rename_name_in_format(locatorLookAt, {}, useName=True)

            locatorLookAtList.append(locatorLookAt[0])
            RMRigTools.RMAlign(Object01, locatorLookAt[0], 3)

            pm.select(clear=True)

            jointsLookAt = pm.joint(name="%sTo%sJointsLookAt" % (self.name_conv.get_a_short_name(Object01),
                                                                 self.name_conv.get_a_short_name(Object02)))
            self.name_conv.rename_name_in_format(jointsLookAt, {}, useName=True)
            jointsLookAtList.append(jointsLookAt)
            RMRigTools.RMAlign(Object01, jointsLookAt, 3)

            groupLookAt = pm.group(empty=True, name="%sTo%sGroupLookAt" % (self.name_conv.get_a_short_name(Object01),
                                                                           self.name_conv.get_a_short_name(Object02)))
            self.name_conv.rename_name_in_format(groupLookAt, {}, useName=True)

            self.kinematics.append(groupLookAt)
            groupLookAtList.append(groupLookAt)
            RMRigTools.RMAlign(Object01, groupLookAt, 3)

            pm.parent(groupLookAtList, MainSkeleton)

            pm.move(RibbonSize.length() / 2 * iloop, 0, 0, resetControlGroup, r=True, os=True, moveX=True)
            pm.move(RibbonSize.length() / 2 * iloop, 0, 0, locatorControl, r=True, os=True, moveX=True)
            pm.move(RibbonSize.length() / 2 * iloop, 0, 1, locatorLookAt, r=True, os=True, moveXYZ=True)
            pm.move(RibbonSize.length() / 2 * iloop, 0, 0, jointsLookAt, r=True, os=True, moveX=True)
            pm.move(RibbonSize.length() / 2 * iloop, 0, 0, groupLookAt, r=True, os=True, moveX=True)

            pm.parent(resetControlGroup, GroupControls)
            pm.parent(locatorControl, groupLookAt)
            pm.parent(locatorLookAt, groupLookAt)
            pm.parent(jointsLookAt, GroupJoints)

            pm.makeIdentity(control, apply=True, t=1, r=0, s=1, n=0)
            pm.makeIdentity(jointsLookAt, apply=True, t=1, r=0, s=1, n=0)

            pm.parentConstraint(locatorControl, jointsLookAt)
            pm.parentConstraint(control, groupLookAt)
        self.controls = controles
        self.resetControls = resetControles
        self.resetControls = resetControles
        pm.aimConstraint(controles[1], locatorControlesList[0], aim=[1, 0, 0], upVector=[0, 0, 1], wut='object',
                         worldUpObject=locatorLookAtList[0])
        pm.aimConstraint(controles[1], locatorControlesList[2], aim=[1, 0, 0], upVector=[0, 0, 1], wut='object',
                         worldUpObject=locatorLookAtList[2])

        pm.parent(GroupJoints, MainSkeleton)

        pm.select(plano, replace=True)
        print jointsLookAtList
        for eachJoint in jointsLookAtList:
            pm.select(eachJoint, add=True)
        pm.SmoothBindSkin()
        pm.parent(plano, HairGroup)


if __name__ == '__main__':
    Ribbon = RMRibbon()
    Ribbon.RibbonCreation('joint1', 'joint2', foliculeNumber=4)
