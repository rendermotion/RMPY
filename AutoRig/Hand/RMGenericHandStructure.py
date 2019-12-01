from RMPY import RMRigTools

import re
from RMPY import nameConvention


import pymel.core as pm


class GenericHandJointStructure(object):
    def __init__(self, NameConv=None):
        if not NameConv:
            self.NameConv = nameConvention.NameConvention()
        else:
            self.NameConv = NameConv

        self.rig_tools = RMRigTools.RMRigTools(NameConv=self.NameConv)
        self.palmJoint = ""
        self.fingerRoots = []
        self.fingers = []

    def CreateHandJointStructure(self, Palm):
        referenceRoots = pm.listRelatives(Palm, children=True, type="transform")
        palmJoint = pm.joint(name=self.NameConv.get_from_name(Palm, "name"))

        RMRigTools.RMAlign(Palm, palmJoint, 3)
        self.NameConv.rename_based_on_base_name(Palm, palmJoint, system="rig")
        self.fingers = []

        for eachPoint in referenceRoots:
            fingerPoints = RMRigTools.RMCustomPickWalk(eachPoint, "transform", -1)
            FingerRoot, fingerJoints = self.rig_tools.RMCreateBonesAtPoints(fingerPoints)
            pm.parent(FingerRoot, palmJoint)
            self.fingerRoots.append(FingerRoot)
            self.fingers.append(fingerJoints)
        self.palmJoint = palmJoint
        if pm.listRelatives(self.palmJoint, parent=True):
            pm.parent(self.palmJoint, world=True)
        return palmJoint

    def fingerJointsByName(self, NameString):
        for eachFinger in self.fingers:
            stringFound = re.search('%s' % NameString, '%s' % eachFinger[0])
            if stringFound:
                return eachFinger
        return None

# GHSt = GenericHandJointStructure()
# GHSt.CreateHandJointStructure("Character01_LF_palm_pnt_rfr")
