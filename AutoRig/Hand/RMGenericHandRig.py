from pprint import pprint as pp
from RMPY import RMRigTools

reload(RMRigTools)

from RMPY import nameConvention

reload(nameConvention)

from RMPY import RMRigShapeControls

reload(RMRigShapeControls)
import re

import pymel.core as pm
from RMPY.AutoRig.Hand import RMGenericHandStructure

reload(RMGenericHandStructure)


class RMGenericHandRig(object):
    def __init__(self, NameConv=None):
        if not NameConv:
            self.NameConv = nameConvention.NameConvention()
        else:
            self.NameConv = NameConv
        self.GHS = RMGenericHandStructure.GenericHandJointStructure(NameConv=NameConv)
        self.name_conv = RMRigTools.RMRigTools(NameConv=NameConv)
        self.fingerRoot = {
            "middle": None,
            "ring": None,
            "pinky": None,
            "index": None,
            "thumb": None
        }
        self.PalmReferencePoints = {
            "middle": None,
            "ring": None,
            "pinky": None,
            "index": None,
            "thumb": None
        }
        self.PalmFingerControlGrp = {
            "middle": None,
            "ring": None,
            "pinky": None,
            "index": None,
            "thumb": None
        }
        self.PalmResetPoint = None
        self.PalmControl = None
        self.fingerControlsReset = []
        self.fingerContols = []
        self.MainKinematics = None
        self.MainControl = None

    def CreateHandRig(self, PalmReferencePoint, PalmControl=None):
        self.CreateHandStructure(PalmReferencePoint)
        for fingers in self.GHS.fingers:
            self.CreateFingerSquareRig(fingers)

        self.CreatePalmRig(PalmControl=PalmControl)
        RMRigTools.RMParentArray(self.PalmControl, self.fingerControlsReset)
        palmLen = RMRigTools.RMPointDistance(self.PalmControl, self.GHS.fingerRoots[0])
        pm.parentConstraint(self.MainKinematics, self.GHS.palmJoint)
        pm.parentConstraint(self.MainKinematics, self.MainControl)

        self.NameConv.rename_set_from_name(self.GHS.palmJoint, "sknjnt", "objectType")
        for eachFinger in self.GHS.fingers:
            self.NameConv.rename_set_from_name(eachFinger, "sknjnt", "objectType")

        # self.PalmControl
        # RMRigShapeControls.create_box_ctrl(self.GHS.palmJoint, Yratio = .5, size = palmLen, NameConv =  NameConv)

    def CreateHandStructure(self, PalmReferencePoint):
        self.GHS.CreateHandJointStructure(PalmReferencePoint)
        self.IdentifyJoints(self.GHS.fingerRoots)

    def CreatePalmRig(self, PalmControl=None):

        if self.NameConv.get_from_name(self.GHS.palmJoint, "side") == "L":
            sideVariation = -1
        else:
            sideVariation = 1

        self.CreatePalmReferencePoints()

        if PalmControl == None:
            palmResetPoint, PalmControl = RMRigShapeControls.RMCircularControl(self.GHS.palmJoint)
        else:
            palmResetPoint = pm.group(empty=True, name="palmControl")
            self.NameConv.rename_based_on_base_name(self.GHS.palmJoint, palmResetPoint,
                                                    name=palmResetPoint)
            RMRigTools.RMAlign(self.GHS.palmJoint, palmResetPoint, 3)

        self.PalmControl = PalmControl
        self.PalmResetPoint = palmResetPoint
        self.MainControl = palmResetPoint

        # palmResetPoint = self.NameConv.RMRenameSetFromName(palmResetPoint,"palmControls","Name")

        self.RMaddPalmControls(self.PalmControl)
        RMRigTools.RMLockAndHideAttributes(self.PalmControl, "0000000000")

        pinky = self.GHS.fingerJointsByName("pinky")
        if pinky:
            self.PalmFingerControlGrp["pinky"] = self.name_conv.RMCreateGroupOnObj(pinky[0])
            RMRigTools.RMChangeRotateOrder(pinky, "yxz")
            RMRigTools.RMConnectWithLimits("%s.Spread" % self.PalmControl,
                                           '%s.rotateZ' % self.PalmFingerControlGrp["pinky"],
                                           [[-10, sideVariation * 10], [0, 0], [10, sideVariation * -60]])
        ring = self.GHS.fingerJointsByName("ring")
        if ring:
            self.PalmFingerControlGrp["ring"] = self.name_conv.RMCreateGroupOnObj(ring[0])
            RMRigTools.RMChangeRotateOrder(ring, "yxz")
            RMRigTools.RMConnectWithLimits("%s.Spread" % self.PalmControl,
                                           '%s.rotateZ' % self.PalmFingerControlGrp["ring"],
                                           [[-10, sideVariation * 5], [0, 0], [10, sideVariation * -30]])
        middle = self.GHS.fingerJointsByName("middle")
        if middle:
            self.PalmFingerControlGrp["middle"] = self.name_conv.RMCreateGroupOnObj(middle[0])
            RMRigTools.RMChangeRotateOrder(middle, "yxz")
            RMRigTools.RMConnectWithLimits("%s.Spread" % self.PalmControl,
                                           '%s.rotateZ' % self.PalmFingerControlGrp["middle"],
                                           [[-10, 0], [0, 0], [10, sideVariation * -5]])
        index = self.GHS.fingerJointsByName("index")
        if index:
            self.PalmFingerControlGrp["index"] = self.name_conv.RMCreateGroupOnObj(index[0])
            RMRigTools.RMChangeRotateOrder(index, "yxz")
            RMRigTools.RMConnectWithLimits("%s.Spread" % self.PalmControl,
                                           '%s.rotateZ' % self.PalmFingerControlGrp["index"],
                                           [[-10, sideVariation * -5], [0, 0], [10, sideVariation * 30]])
        thumb = self.GHS.fingerJointsByName("thumb")
        if thumb:
            self.PalmFingerControlGrp["thumb"] = self.name_conv.RMCreateGroupOnObj(thumb[0])
            RMRigTools.RMChangeRotateOrder(thumb, "yxz")
            RMRigTools.RMConnectWithLimits("%s.Spread" % self.PalmControl,
                                           '%s.rotateZ' % self.PalmFingerControlGrp["thumb"],
                                           [[-10, sideVariation * -10], [0, 0], [10, sideVariation * 60]])

        for eachFingerName in self.fingerRoot:
            if eachFingerName != 'thumb':
                RMRigTools.RMConnectWithLimits("%s.PalmBend" % self.PalmControl,
                                               '%s.rotateY' % self.PalmFingerControlGrp[eachFingerName],
                                               [[-10, 90], [0, 0], [10, -90]])
                RMRigTools.RMConnectWithLimits("%s.Twist" % self.PalmControl,
                                               '%s.rotateX' % self.PalmReferencePoints[eachFingerName],
                                               [[-10, sideVariation * 45], [0, 0], [10, sideVariation * -45]])

        RMRigTools.RMConnectWithLimits("%s.PalmCup" % self.PalmControl, '%s.rotateX' % self.PalmReferencePoints["pinky"],
                                       [[0, 0], [10, sideVariation * 50]])
        RMRigTools.RMConnectWithLimits("%s.PalmCup" % self.PalmControl, '%s.rotateX' % self.PalmReferencePoints["ring"],
                                       [[0, 0], [10, sideVariation * 25]])
        RMRigTools.RMConnectWithLimits("%s.PalmCup" % self.PalmControl, '%s.rotateX' % self.PalmReferencePoints["middle"],
                                       [[0, 0], [10, sideVariation * 5]])
        RMRigTools.RMConnectWithLimits("%s.PalmCup" % self.PalmControl, '%s.rotateX' % self.PalmReferencePoints["index"],
                                       [[0, 0], [10, sideVariation * -30]])
        RMRigTools.RMConnectWithLimits("%s.PalmCup" % self.PalmControl, '%s.rotateX' % self.PalmReferencePoints["thumb"],
                                       [[0, 0], [10, sideVariation * -60]])

    def CreatePalmReferencePoints(self):
        HandPalm = self.name_conv.RMCreateGroupOnObj(self.GHS.palmJoint, Type="world")
        for keys in self.fingerRoot:
            childGroup = self.name_conv.RMCreateGroupOnObj(HandPalm, Type="child")
            self.NameConv.rename_set_from_name(childGroup, keys, 'name', mode='add')
            pm.parentConstraint(childGroup, self.fingerRoot[keys], maintainOffset=True)
            self.PalmReferencePoints[keys] = childGroup

        self.MainKinematics = HandPalm

    def CreateFingerSquareRig(self, Finger):

        if self.NameConv.get_from_name(Finger[0], "side") == "L":
            sideVariation = 1
        else:
            sideVariation = -1

        BoxResetPoint, BoxControl = RMRigShapeControls.RMCreateBoxCtrl(Finger[len(Finger) - 1], ParentBaseSize=True,
                                                                       Xratio=.5, Yratio=.5, Zratio=.5)
        self.RMaddFinguerControls(BoxControl)

        pm.makeIdentity(BoxControl, apply=True, r=False, t=True, s=True, n=0)
        pm.parentConstraint(Finger[len(Finger) - 1], BoxResetPoint)

        RMRigTools.RMLockAndHideAttributes(BoxControl, "0000000000")

        RMRigTools.RMConnectWithLimits("%s.MidUD" % BoxControl, "%s.rotateY" % Finger[0],
                                       [[-10, 100], [0, 0], [10, -100]])
        RMRigTools.RMConnectWithLimits("%s.MidLR" % BoxControl, "%s.rotateZ" % Finger[0],
                                       [[-10, sideVariation * 120], [0, 0], [10, sideVariation * -127]])
        RMRigTools.RMConnectWithLimits("%s.MidTwist" % BoxControl, "%s.rotateX" % Finger[0],
                                       [[-10, sideVariation * 90], [0, 0], [10, sideVariation * -90]])
        index = 1
        for eachjoint in range(0, len(Finger) - 1):
            RMRigTools.RMConnectWithLimits("%s.UD%s" %(BoxControl, index), "%s.rotateY" % Finger[eachjoint],
                                           [[-10, 100], [0, 0], [10, -100]])
            RMRigTools.RMConnectWithLimits("%s.LR%s" % (BoxControl, index), "%s.rotateZ" % Finger[eachjoint],
                                           [[-10, sideVariation * 120], [0, 0], [10, sideVariation * -127]])
            RMRigTools.RMConnectWithLimits("%s.Twist%s" % (BoxControl, index), "%s.rotateX" % Finger[eachjoint],
                                           [[-10, sideVariation * 90], [0, 0], [10, sideVariation * -90]])
            index += 1
        self.fingerControlsReset.append(BoxResetPoint)
        self.fingerContols.append(BoxControl)

    def IdentifyJoints(self, fingerRootArray):
        for fingers in self.fingerRoot:
            for Roots in fingerRootArray:
                if re.search('%s' % fingers, '%s' % Roots):
                    self.fingerRoot[fingers] = Roots

    def IdentifyByString(self, IDstring, fingerList):
        for eachFinger in fingerList:
            if re.search(IDstring, eachFinger):
                return eachFinger

    def RMaddFinguerControls(self, Object):
        pm.addAttr(Object, at="float", ln="MidUD", hnv=1, hxv=1, h=0, k=1, smn=-10, smx=10)
        pm.addAttr(Object, at="float", ln="UD1", hnv=1, hxv=1, h=0, k=1, smn=-10, smx=10)
        pm.addAttr(Object, at="float", ln="UD2", hnv=1, hxv=1, h=0, k=1, smn=-10, smx=10)
        pm.addAttr(Object, at="float", ln="UD3", hnv=1, hxv=1, h=0, k=1, smn=-10, smx=10)
        pm.addAttr(Object, at="float", ln="MidLR", hnv=1, hxv=1, h=0, k=1, smn=-10, smx=10)
        pm.addAttr(Object, at="float", ln="LR1", hnv=1, hxv=1, h=0, k=1, smn=-10, smx=10)
        pm.addAttr(Object, at="float", ln="LR2", hnv=1, hxv=1, h=0, k=1, smn=-10, smx=10)
        pm.addAttr(Object, at="float", ln="LR3", hnv=1, hxv=1, h=0, k=1, smn=-10, smx=10)
        pm.addAttr(Object, at="float", ln="MidTwist", hnv=1, hxv=1, h=0, k=1, smn=-10, smx=10)
        pm.addAttr(Object, at="float", ln="Twist1", hnv=1, hxv=1, h=0, k=1, smn=-10, smx=10)
        pm.addAttr(Object, at="float", ln="Twist2", hnv=1, hxv=1, h=0, k=1, smn=-10, smx=10)
        pm.addAttr(Object, at="float", ln="Twist3", hnv=1, hxv=1, h=0, k=1, smn=-10, smx=10)
        pm.addAttr(Object, at="enum", ln="Secondary", k=1, en="Off:On")

    def RMaddPalmControls(self, Object):
        pm.addAttr(Object, at="float", ln="PalmBend", hnv=1, hxv=1, h=0, k=1, smn=-10, smx=10)
        pm.addAttr(Object, at="float", ln="PalmCup", hnv=1, hxv=1, h=0, k=1, smn=-10, smx=10)
        pm.addAttr(Object, at="float", ln="Spread", hnv=1, hxv=1, h=0, k=1, smn=-10, smx=10)
        pm.addAttr(Object, at="float", ln="Twist", hnv=1, hxv=1, h=0, k=1, smn=-10, smx=10)
