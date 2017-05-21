from RMPY import RMRigTools

reload(RMRigTools)
import re
from RMPY import RMNameConvention

reload(RMNameConvention)

import maya.cmds as cmds


class GenericHandJointStructure(object):
    def __init__(self, NameConv=None):
        if not NameConv:
            self.NameConv = RMNameConvention.RMNameConvention()
        else:
            self.NameConv = NameConv

        self.RigTools = RMRigTools.RMRigTools()
        self.palmJoint = ""
        self.fingerRoots = []
        self.fingers = []

    def CreateHandJointStructure(self, Palm):
        referenceRoots = cmds.listRelatives(Palm, children=True, type="transform")
        palmJoint = cmds.joint(name=self.NameConv.RMGetFromName(Palm, "name"))

        RMRigTools.RMAlign(Palm, palmJoint, 3)
        palmJoint = self.NameConv.RMRenameBasedOnBaseName(Palm, palmJoint, {'system': "rig"})
        self.fingers = []

        for eachPoint in referenceRoots:
            fingerPoints = RMRigTools.RMCustomPickWalk(eachPoint, "transform", -1)
            FingerRoot, fingerJoints = self.RigTools.RMCreateBonesAtPoints(fingerPoints)
            cmds.parent(FingerRoot, palmJoint)
            self.fingerRoots.append(FingerRoot)
            self.fingers.append(fingerJoints)
        self.palmJoint = palmJoint
        if cmds.listRelatives(self.palmJoint, parent=True):
            cmds.parent(self.palmJoint, world=True)
        return palmJoint

    def fingerJointsByName(self, NameString):
        for eachFinger in self.fingers:
            stringFound = re.search(NameString, eachFinger[0])
            if stringFound:
                return eachFinger
        return None

# GHSt = GenericHandJointStructure()
# GHSt.CreateHandJointStructure("Character01_LF_palm_pnt_rfr")
