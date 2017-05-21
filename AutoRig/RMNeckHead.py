import maya.cmds as cmds
from RMPY import RMNameConvention

reload(RMNameConvention)
from RMPY import RMRigTools

reload(RMRigTools)
from RMPY import RMRigShapeControls

reload(RMRigShapeControls)


class RMNeckHead(object):
    def __init__(self, NameConv=None):
        if not NameConv:
            self.NameConv = RMNameConvention.RMNameConvention()
        else:
            self.NameConv = NameConv
        self.rootHeadJoints = None
        self.HeadJoints = None
        self.RootNeckJoints = None
        self.NeckJoints = None
        self.resetHeadControl = None
        self.headControl = None
        self.RootJaw = None
        self.JawJoints = None

        self.NeckControl = None
        self.resetNeckControl = None

    def RMCreateHeadAndNeckRig(self, HeadRefPoints, NeckRefPoints, Jaw):

        self.rootHeadJoints, self.HeadJoints = self.RMCreate2PointsJointStructure(HeadRefPoints, name="Head")
        self.resetHeadControl, self.headControl = self.RMCreateHeadRig()

        self.RootNeckJoints, self.NeckJoints = self.RMCreate2PointsJointStructure(NeckRefPoints, name="Neck")
        self.resetNeckControl, self.NeckControl = self.RMCreateNeckRig()

        cmds.parent(self.rootHeadJoints, self.NeckJoints[len(self.NeckJoints) - 1])
        cmds.parent(self.resetHeadControl, self.NeckControl)
        self.RootJaw, self.JawJoints = self.RMCreate2PointsJointStructure(Jaw, name="Jaw")
        cmds.parent(self.RootJaw, self.HeadJoints[0])
        self.RMCleanUP()

    def RMCleanUP(self):

        self.NeckJoints[0] = self.NameConv.RMRenameSetFromName(self.NeckJoints[0], "sknjnt", "objectType")
        self.HeadJoints[0] = self.NameConv.RMRenameSetFromName(self.HeadJoints[0], "sknjnt", "objectType")
        self.JawJoints[0] = self.NameConv.RMRenameSetFromName(self.JawJoints[0], "sknjnt", "objectType")

    def RMCreate2PointsJointStructure(self, ReferencePoints, name="joints"):
        root, Joints = RMRigTools.RMCreateBonesAtPoints(ReferencePoints, ZAxisOrientation="z")
        # RMRigTools.RMAlign(ReferencePoints[0],root,3 )
        Joints = self.NameConv.RMRenameSetFromName(Joints, name + "Joints", "name")
        root = self.NameConv.RMRenameSetFromName(root, "resetPoint" + name.title() + "Joints", "name")
        return root, Joints

    def RMCreateHeadRig(self):
        headSize = RMRigTools.RMLenghtOfBone(self.HeadJoints[0])
        resetHeadControl, headControl = RMRigShapeControls.RMImportMoveControl(self.rootHeadJoints, scale=headSize,
                                                                               name="head", Type="head")
        cmds.parentConstraint(headControl, self.HeadJoints[0])
        return resetHeadControl, headControl

    def RMCreateNeckRig(self):
        resetNeckControl, NeckControl = RMRigShapeControls.RMCreateBoxCtrl(self.NeckJoints[0], name="neck")
        cmds.parentConstraint(NeckControl, self.NeckJoints[0])
        return resetNeckControl, NeckControl
