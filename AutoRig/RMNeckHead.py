import pymel.core as pm
from RMPY import nameConvention

from RMPY import RMRigTools
from RMPY import RMRigShapeControls


class RMNeckHead(object):
    def __init__(self, NameConv=None):
        if not NameConv:
            self.NameConv = nameConvention.NameConvention()
        else:
            self.NameConv = NameConv
        self.rig_tools = RMRigTools.RMRigTools()
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

        pm.parent(self.rootHeadJoints, self.NeckJoints[len(self.NeckJoints) - 1])
        pm.parent(self.resetHeadControl, self.NeckControl)
        self.RootJaw, self.JawJoints = self.RMCreate2PointsJointStructure(Jaw, name="Jaw")
        pm.parent(self.RootJaw, self.HeadJoints[0])
        self.RMCleanUP()

    def RMCleanUP(self):

        self.NameConv.rename_set_from_name(self.NeckJoints[0], "sknjnt", "objectType")
        self.NameConv.rename_set_from_name(self.HeadJoints[0], "sknjnt", "objectType")
        self.NameConv.rename_set_from_name(self.JawJoints[0], "sknjnt", "objectType")

    def RMCreate2PointsJointStructure(self, ReferencePoints, name="joints"):
        root, Joints = self.rig_tools.RMCreateBonesAtPoints(ReferencePoints, ZAxisOrientation="z")
        # RMRigTools.RMAlign(ReferencePoints[0],root,3 )
        self.NameConv.rename_set_from_name(Joints, name + "Joints", "name")
        self.NameConv.rename_set_from_name(root, "resetPoint%s" % name.title() + "Joints", "name")
        return root, Joints

    def RMCreateHeadRig(self):
        headSize = RMRigTools.RMLenghtOfBone(self.HeadJoints[0])
        print '%s %s' % (self.rootHeadJoints, self.rootHeadJoints.__class__)
        resetHeadControl, headControl = RMRigShapeControls.RMImportMoveControl(self.rootHeadJoints, scale=headSize,
                                                                               name="head", Type="head")
        pm.parentConstraint(headControl, self.HeadJoints[0])
        return resetHeadControl, headControl

    def RMCreateNeckRig(self):
        resetNeckControl, NeckControl = RMRigShapeControls.RMCreateBoxCtrl(self.NeckJoints[0], name="neck")
        pm.parentConstraint(NeckControl, self.NeckJoints[0])
        return resetNeckControl, NeckControl
