import maya.cmds as cmds
import maya.api.OpenMaya as om
from RMPY import RMNameConvention
from RMPY import RMRigTools
from RMPY import RMRigShapeControls
import pymel.core as pm


class RMRibbon(object):
    def __init__(self):
        self.kinematics = []
        self.joints = []
        self.controls = []
        self.baseObjects = []
        self.jointStructure = []
        self.folicules = []
        self.resetControls = []
        self.allControls = []

    def nurbPlaneBetweenObjects(self, Object01, Object02):
        VP1 = om.MVector(cmds.xform(Object01, a=True, ws=True, q=True, rp=True))
        VP2 = om.MVector(cmds.xform(Object02, a=True, ws=True, q=True, rp=True))
        longitud = VP1 - VP2
        NameConv = RMNameConvention.RMNameConvention()
        plano = cmds.nurbsPlane(ax=[0, 1, 0], p=[(longitud.length()) / 2, 0, 0], w=longitud.length(), lr=.05, d=3, u=8,
                                v=1, ch=0, name=NameConv.RMSetNameInFormat(
                {'name': "%sTo%sPlane" % (NameConv.RMGetAShortName(Object01), NameConv.RMGetAShortName(Object02)),
                 'side': NameConv.RMGetFromName(Object02, "side"), 'system': "Ribbons"}))

        RMRigTools.RMAlign(Object01, plano[0], 3)
        return plano[0]

    # nurbPlaneBetweenObjects("joint1","joint2")
    def RibbonCreation(self, Object01, Object02, foliculeNumber=5):
        print 'creating riboon in %s and %s'% (Object01, Object02)
        self.baseObjects.append(Object01)
        self.baseObjects.append(Object02)

        NameConv = RMNameConvention.RMNameConvention()
        VP1 = om.MVector(cmds.xform(Object01, a=True, ws=True, q=True, rp=True))
        VP2 = om.MVector(cmds.xform(Object02, a=True, ws=True, q=True, rp=True))
        plano = self.nurbPlaneBetweenObjects(Object01, Object02)
        planoShape = cmds.listRelatives(plano, shapes=True)[0]
        cmds.select(cl=True)
        RibbonSize = VP1 - VP2

        print "plano = %s" % plano
        print "len = %s" % RibbonSize.length()

        MainSkeleton = cmds.group(em=True, name=NameConv.RMSetNameInFormat(
            {'name': "%sTo%sRibbon" % (NameConv.RMGetAShortName(Object01), NameConv.RMGetAShortName(Object02)),
             'side': NameConv.RMGetFromName(Object02, "side"), 'system': "Ribbons"}))
        HairGroup = cmds.group(em=True, name = NameConv.RMSetNameInFormat(
            {'name': "%sTo%sHairSystem" % (NameConv.RMGetAShortName(Object01), NameConv.RMGetAShortName(Object02)),
            'side': NameConv.RMGetFromName(Object02, "side"), 'system': "Ribbons"}))

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
            NewFolicule = NameConv.RMRenameNameInFormat("follicle1", {'side':NameConv.RMGetFromName(Object02, "side")})
            folicules.append(NewFolicule)
            cmds.parent(NewFolicule, HairGroup)
        self.folicules = folicules
        cmds.delete(cmds.listRelatives(Hys, p=True))
        index = 0
        skinedJoints = cmds.group(em=True, name=NameConv.RMSetNameInFormat(
            {'name': "%sTo%sskinedJoints" % (NameConv.RMGetAShortName(Object01), NameConv.RMGetAShortName(Object02)),
             'side': NameConv.RMGetFromName (Object02, "side"), 'system': "Ribbons"}))
        for eachFolicule in folicules:
            ArrayJoints.append(cmds.joint(name=NameConv.RMSetNameInFormat(
                {'name': "%sTo%sRibbonJoints" % (NameConv.RMGetAShortName(Object01), NameConv.RMGetAShortName(Object02)),
                 'side': NameConv.RMGetFromName(Object02, "Side"), 'system': "Ribbons"})))
            RMRigTools.RMAlign(eachFolicule, ArrayJoints[index], 3)
            cmds.parentConstraint(eachFolicule, ArrayJoints[index])
            index += 1
        self.jointStructure = ArrayJoints

        controles = []
        resetControles = []
        locatorControlesList = []
        locatorLookAtList = []
        jointsLookAtList = []
        groupLookAtList = []

        GroupControls = cmds.group(empty=True, name=NameConv.RMSetNameInFormat(
            {'name': "%sTo%sControls" % (NameConv.RMGetAShortName(Object01), NameConv.RMGetAShortName(Object02)),
            'side': NameConv.RMGetFromName(Object02, "Side"), 'system': "Ribbons"}))
        GroupJoints = cmds.group(empty=True, name=NameConv.RMSetNameInFormat(
            {'name': "%sTo%sGroupJointsLookAt" % (NameConv.RMGetAShortName(Object01), NameConv.RMGetAShortName(Object02)),
            'side': NameConv.RMGetFromName(Object02, "Side"), 'system': "Ribbons"}))
        RigControls = RMRigShapeControls.RMRigShapeControls()

        self.allControls.append(GroupControls)
        self.joints.append(GroupJoints)

        for iloop in range(3):
            resetControlGroup, control = RigControls.RMCircularControl(Object01, radius=RibbonSize.length() / 3,
                                                                       name=NameConv.RMSetNameInFormat(
                                                                       {'name': "%sTo%sCtrl" % (
                                                                       NameConv.RMGetAShortName(Object01),
                                                                       NameConv.RMGetAShortName(Object02)),
                                                                       'side': NameConv.RMGetFromName(Object02, "side"),
                                                                       'objectType': 'ctrl', 'system': "Ribbons"}))
            controles.append(control)
            resetControles.append(resetControlGroup)

            locatorControl = cmds.spaceLocator(name=NameConv.RMSetNameInFormat(
                {'name':"%sTo%sLocatorCntrl" % (NameConv.RMGetAShortName(Object01), NameConv.RMGetAShortName(Object02)),
                'objectType':'spaceLocator', 'side': NameConv.RMGetFromName(Object02, "Side"), 'system': "Ribbons"}))
            locatorControlesList.append(locatorControl[0])
            RMRigTools.RMAlign(Object01, locatorControl[0], 3)

            locatorLookAt = cmds.spaceLocator(name=NameConv.RMSetNameInFormat(
                {'name': "%sTo%sLocatorLookAt" % (NameConv.RMGetAShortName(Object01), NameConv.RMGetAShortName(Object02)),
                'objectType': 'spaceLocator', 'side': NameConv.RMGetFromName(Object02, "side"), 'system': "Ribbons"}))
            locatorLookAtList.append(locatorLookAt[0])
            RMRigTools.RMAlign(Object01, locatorLookAt[0], 3)

            cmds.select(clear=True)

            jointsLookAt = cmds.joint(name=NameConv.RMSetNameInFormat(
                {'name': "%sTo%sJointsLookAt" % (NameConv.RMGetAShortName(Object01), NameConv.RMGetAShortName(Object02)),
                'objectType':'joint', 'side': NameConv.RMGetFromName(Object02, "side"), 'system':"Ribbons"}))
            jointsLookAtList.append(jointsLookAt)
            RMRigTools.RMAlign(Object01, jointsLookAt, 3)

            groupLookAt = cmds.group(empty=True, name=NameConv.RMSetNameInFormat(
                {'name': "%sTo%sGroupLookAt" % (NameConv.RMGetAShortName(Object01), NameConv.RMGetAShortName(Object02)),
                'objectType': 'transform', 'side':NameConv.RMGetFromName(Object02, "side"), 'system':"Ribbons"}))
            self.kinematics.append(groupLookAt)
            groupLookAtList.append(groupLookAt)
            RMRigTools.RMAlign(Object01, groupLookAt, 3)

            cmds.parent(groupLookAtList, MainSkeleton)

            cmds.move(RibbonSize.length() / 2 * iloop, 0, 0, resetControlGroup, r=True, os=True, moveX=True)
            cmds.move(RibbonSize.length() / 2 * iloop, 0, 0, locatorControl, r=True, os=True, moveX=True)
            cmds.move(RibbonSize.length() / 2 * iloop, 0, 1, locatorLookAt, r=True, os=True, moveXYZ=True)
            cmds.move(RibbonSize.length() / 2 * iloop, 0, 0, jointsLookAt, r=True, os=True, moveX=True)
            cmds.move(RibbonSize.length() / 2 * iloop, 0, 0, groupLookAt, r=True, os=True, moveX=True)

            cmds.parent(resetControlGroup, GroupControls)
            cmds.parent(locatorControl, groupLookAt)
            cmds.parent(locatorLookAt, groupLookAt)
            cmds.parent(jointsLookAt, GroupJoints)

            cmds.makeIdentity(control, apply=True, t=1, r=0, s=1, n=0)
            cmds.makeIdentity(jointsLookAt, apply=True, t=1, r=0, s=1, n=0)

            cmds.parentConstraint(locatorControl, jointsLookAt)
            cmds.parentConstraint(control, groupLookAt)
        print "Controles[1]:%s" % controles[1]
        print "locatorControlesList[1]:%s" % locatorControlesList[0]
        print "groupLookAtList[1]:%s" % groupLookAtList[0]
        print "locatorLookAtList:%s" % locatorLookAtList
        self.controls = controles
        self.resetControls = resetControles
        self.resetControls = resetControles
        cmds.aimConstraint(controles[1], locatorControlesList[0], aim=[1, 0, 0], upVector=[0, 0, 1], wut='object',
                           worldUpObject=locatorLookAtList[0])
        cmds.aimConstraint(controles[1], locatorControlesList[2], aim=[1, 0, 0], upVector=[0, 0, 1], wut='object',
                           worldUpObject=locatorLookAtList[2])

        cmds.parent(GroupJoints, MainSkeleton)

        cmds.select(plano, replace=True)
        print jointsLookAtList
        for eachJoint in jointsLookAtList:
            cmds.select(eachJoint, add=True)
        cmds.SmoothBindSkin()
        cmds.parent(plano, HairGroup)


if __name__ == '__main__':
    Ribbon = RMRibbon()
    Ribbon.RibbonCreation('joint1', 'joint2', foliculeNumber=4)
