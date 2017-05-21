import maya.cmds as cmds
from RMPY import RMRigTools
from RMPY import RMNameConvention
from RMPY import RMRigShapeControls

import re


class RMGenericJointChainRig(object):
    def __init__(self, NameConv=None):
        if NameConv:
            self.NameConv = NameConv
        else:
            self.NameConv = RMNameConvention.RMNameConvention()

    def CreateJointChainRig(self, node, UDaxis="Y"):
        jointChain = RMRigTools.RMCustomPickWalk(node, "joint", -1)
        print jointChain
        self.CreateJointChainSquareRig(jointChain, UDaxis=UDaxis)

    def CreateJointChainSquareRig(self, JointChain, UDaxis="Y"):
        if self.NameConv.RMIsNameInFormat(JointChain[0]):
            if self.NameConv.RMGetFromName(JointChain[0], "Side") == "LF":
                sideVariation = 1
            else:
                sideVariation = -1
        else:
            sideVariation = 1

        if UDaxis in ["Y", "Z"]:
            BoxResetPoint, BoxControl = RMRigShapeControls.RMCreateBoxCtrl(JointChain[len(JointChain) - 1],
                                                                           ParentBaseSize=True, Xratio=.5, Yratio=.5,
                                                                           Zratio=.5)
            self.addChainParameters(BoxControl, len(JointChain) - 1)

            cmds.makeIdentity(BoxControl, apply=True, r=False, t=True, s=True, n=0)

            cmds.parentConstraint(JointChain[len(JointChain) - 1], BoxResetPoint)

            RMRigTools.RMLockAndHideAttributes(BoxControl, "0000000000")

            if UDaxis == "Y":
                LRaxis = "Z"
            elif UDaxis == "Z":
                LRaxis = "Y"
            for eachjoint in range(len(JointChain) - 1):
                RMRigTools.RMConnectWithLimits(BoxControl + ".UD" + str(eachjoint + 1),
                                               JointChain[eachjoint] + (".rotate%s" % UDaxis),
                                               [[-10, 100], [0, 0], [10, -100]])
                RMRigTools.RMConnectWithLimits(BoxControl + ".LR" + str(eachjoint + 1),
                                               JointChain[eachjoint] + (".rotate%s" % LRaxis),
                                               [[-10, sideVariation * 100], [0, 0], [10, sideVariation * -100]])
                RMRigTools.RMConnectWithLimits(BoxControl + ".Twist" + str(eachjoint + 1),
                                               JointChain[eachjoint] + ".rotateX",
                                               [[-10, sideVariation * 100], [0, 0], [10, sideVariation * -100]])
        else:
            print "Not Valid UD Axis Provided"

    def addChainParameters(self, control, number, UD=True, LR=True, Twist=True, smn=-10, smx=10):
        for element in range(number):
            if UD == True:
                cmds.addAttr(control, at="float", ln=("UD%s" % (element + 1)), hnv=1, hxv=1, h=0, k=1, smn=smn, smx=smx)
        for element in range(number):
            if LR == True:
                cmds.addAttr(control, at="float", ln=("LR%s" % (element + 1)), hnv=1, hxv=1, h=0, k=1, smn=smn, smx=smx)
        for element in range(number):
            if Twist == True:
                cmds.addAttr(control, at="float", ln=("Twist%s" % (element + 1)), hnv=1, hxv=1, h=0, k=1, smn=smn,
                             smx=smx)


def setInName(selection):
    NameConv = RMNameConvention.RMNameConvention()
    for eachObject in selection:
        childJoints = RMRigTools.RMCustomPickWalk(eachObject, "joint", -1)
        for eachJoint in childJoints:
            Name = eachJoint.split("_")
            Value = re.split(r"([0-9]+$)", Name[len(Name) - 1])
            NewName = Value[0]
            cmds.rename(eachJoint,
                        NameConv.RMSetNameInFormat(Name=NewName, Side="RH", Type=NameConv.RMGuessObjType(eachJoint)))


def lastTwoJointsInChain(selection):
    for eachObject in selection:
        childJoints = RMRigTools.RMCustomPickWalk(eachObject, "joint", -1)
        RMRigTools.RMAlign(childJoints[len(childJoints) - 2], childJoints[len(childJoints) - 1], 2)


if __name__ == '__main__':
    selection = cmds.ls(selection=True)
    GJR = RMGenericJointChainRig()
    GJR.CreateJointChainRig(selection[0], UDaxis="Z")
# setInName (selection)
# lastTwoJointsInChain(selection)
