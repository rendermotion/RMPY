import maya.cmds as cmds
from RMPY import RMRigTools
from RMPY import RMRigShapeControls
from RMPY import RMNameConvention
reload(RMRigShapeControls)


class RMRigFK(object):
    def __init__(self, NameConv=None):
        self.joints = None
        self.controls = []
        self.rootControls = None
        self.rootJoints = None
        self.ShapeControls = RMRigShapeControls.RMRigShapeControls()

    def createOnSelection(self, controlShape="cube"):
        selection = cmds.ls(selection=True)

        self.createFKControlsOnListPoints(selection, controlShape=controlShape)

    def createFKControlsOnListPoints(self, ListPoints, controlShape="cube"):
        self.rootJoints, jointArray = RMRigTools.RMCreateBonesAtPoints(ListPoints)

        index = 0
        for eachJoint in jointArray[:-1]:
            if controlShape == "cube":
                ResetGroup, Ctrl = self.ShapeControls.RMCreateBoxCtrl(eachJoint)
            else:
                ResetGroup, Ctrl = self.ShapeControls.RMCircularControl(eachJoint)
            if index == 0:
                self.rootControls = ResetGroup
                prevControl = Ctrl
            else:
                cmds.parent(ResetGroup, prevControl)
                prevControl = Ctrl
            self.controls.append(Ctrl)
            cmds.parentConstraint(Ctrl, eachJoint, mo=False)
            index += 1
