import maya.cmds as cmds
from RMPY import RMRigTools
import os
from RMPY import RMNameConvention


class RMRigShapeControls(object):
    def __init__(self, NameConv=None):
        if NameConv is None:
            self.NameConv = RMNameConvention.RMNameConvention()
        else:
            self.NameConv = NameConv
        self.rigTools = RMRigTools.RMRigTools(NameConv=self.NameConv)

    def RMTurnToOne(self, curveArray):
        for eachCurve in curveArray[1:]:
            shapesInCurve = cmds.listRelatives(eachCurve, s=True, children=True)
            for eachShape in shapesInCurve:
                cmds.parent(eachShape, curveArray[0], shape=True, add=True)
                cmds.delete(eachCurve)

    def RMCreateCubeLine(self, height, length, width, centered=False, offsetX=float(0.0), offsetY=float(0.0),
                         offsetZ=float(0.0), name=""):
        if centered == True:
            offsetX = offsetX - float(height) / 2.0
        if name == "":
            defaultName = "CubeLine"
        else:
            defaultName = name
        CubeCurve = []
        pointArray = [
            [0 + offsetX, -length / 2.0 + offsetY, width / 2.0 + offsetZ],
            [0 + offsetX, -length / 2.0 + offsetY, -width / 2.0 + offsetZ],
            [height + offsetX, -length / 2.0 + offsetY, -width / 2.0 + offsetZ],
            [height + offsetX, length / 2.0 + offsetY, -width / 2.0 + offsetZ],
            [height + offsetX, length / 2.0 + offsetY, width / 2.0 + offsetZ],
            [0 + offsetX, length / 2.0 + offsetY, width / 2.0 + offsetZ],
            [0 + offsetX, length / 2.0 + offsetY, -width / 2.0 + offsetZ],
            [height + offsetX, length / 2.0 + offsetY, -width / 2.0 + offsetZ],
            [height + offsetX, -length / 2.0 + offsetY, -width / 2.0 + offsetZ],
            [height + offsetX, -length / 2.0 + offsetY, width / 2.0 + offsetZ],
            [height + offsetX, length / 2.0 + offsetY, width / 2.0 + offsetZ],
            [height + offsetX, -length / 2.0 + offsetY, width / 2.0 + offsetZ],
            [0 + offsetX, -length / 2.0 + offsetY, width / 2.0 + offsetZ],
            [0 + offsetX, length / 2.0 + offsetY, width / 2.0 + offsetZ],
            [0 + offsetX, length / 2.0 + offsetY, -width / 2.0 + offsetZ],
            [0 + offsetX, -length / 2.0 + offsetY, -width / 2.0 + offsetZ]
        ]
        curve = cmds.curve(d=1, p=pointArray, name=defaultName)
        # return CubeCurve[0]
        return curve

    def RMCreateBoxCtrl(self, Obj, Xratio=1, Yratio=1, Zratio=1, ParentBaseSize=False, customSize=0, name="",
                        centered=False):

        if name == "":
            defaultName = "BoxControl"
        else:
            defaultName = name

        Parents = cmds.listRelatives(Obj, parent=True)

        if Parents and len(Parents) != 0 and ParentBaseSize == True:
            JntLength = RMRigTools.RMLenghtOfBone(Parents[0])
            Ctrl = RMCreateCubeLine(JntLength * Xratio, JntLength * Yratio, JntLength * Zratio, name=defaultName,
                                    centered=centered)
        else:
            if customSize != 0:
                JntLength = customSize

            elif cmds.objectType(Obj) == "joint":
                JntLength = RMRigTools.RMLenghtOfBone(Obj)

            else:
                JntLength = 1
            Ctrl = RMCreateCubeLine(JntLength * Xratio, JntLength * Yratio, JntLength * Zratio, name=defaultName,
                                    centered=centered)

        if name == '' and self.NameConv.RMIsNameInFormat(Obj):
            Ctrl = self.NameConv.RMRenameBasedOnBaseName(Obj, Ctrl)
        else:
            Ctrl = self.NameConv.RMRenameBasedOnBaseName(Obj, Ctrl, {'name': Ctrl})

        Ctrl = self.NameConv.RMRenameSetFromName(Ctrl, "control", "objectType")

        RMRigTools.RMAlign(Obj, Ctrl, 3)

        ResetGroup = self.rigTools.RMCreateGroupOnObj(Ctrl)
        return ResetGroup, Ctrl

    def RMCircularControl(self, Obj, radius=1, axis="X", name=""):
        if name == '':
            defaultName = "circularControl"
        else:
            defaultName = name
        if axis in "yY":
            Ctrl, Shape = cmds.circle(normal=[0, 1, 0], radius=radius, name=defaultName)
        elif axis in "zZ":
            Ctrl, Shape = cmds.circle(normal=[0, 0, 1], radius=radius, name=defaultName)
        elif axis in "xX":
            Ctrl, Shape = cmds.circle(normal=[1, 0, 0], radius=radius, name=defaultName)

        if name == '' and self.NameConv.RMIsNameInFormat(Obj):

            Ctrl = self.NameConv.RMRenameBasedOnBaseName(Obj, Ctrl, {})
        else:
            Ctrl = self.NameConv.RMRenameBasedOnBaseName(Obj, Ctrl, {'name': Ctrl})

        Ctrl = self.NameConv.RMRenameSetFromName(Ctrl, "control", "objectType")

        RMRigTools.RMAlign(Obj, Ctrl, 3)

        ResetGroup = self.rigTools.RMCreateGroupOnObj(Ctrl)

        return ResetGroup, Ctrl

    def RMImportMoveControl(self, Obj, scale=1, name='', Type="move"):
        MoversTypeDic = {
            "move": {"filename": "ControlMover.mb", "object": "MoverControl"},
            "v": {"filename": "ControlV.mb", "object": "VControl"},
            "head": {"filename": "ControlHead.mb", "object": "HeadControl"},
            "circleDeform": {"filename": "ControlCircularDeform.mb", "object": "CircularDeform"}
        }
        print 'inside Iport move control'
        path = os.path.dirname(RMRigTools.__file__)
        RMPYPATH = os.path.split(path)
        FinalPath = os.path.join(RMPYPATH[0], "RMPY\AutoRig\RigShapes", MoversTypeDic[Type]["filename"])
        if os.path.isfile(FinalPath):
            cmds.file(FinalPath, i=True, type="mayaBinary", ignoreVersion=True, mergeNamespacesOnClash=False,
                      rpr="ControlMover", pr=False)
        else:
            print "archivo no encontrado %s , %s, %s "% (path, RMPYPATH, FinalPath)
            return None

        Ctrl = MoversTypeDic[Type]["object"]

        if cmds.objExists(Ctrl):
            if name != '':
                Ctrl = cmds.rename(Ctrl, name)

            cmds.setAttr(Ctrl + ".scale", scale, scale, scale)

            cmds.makeIdentity(Ctrl, apply=True, t=1, r=1, s=1)

            if name != '' and self.NameConv.RMIsNameInFormat(Obj):

                Ctrl = self.NameConv.RMRenameBasedOnBaseName(Obj, Ctrl, {})

            else:
                Ctrl = self.NameConv.RMRenameBasedOnBaseName(Obj, Ctrl, {'name': Ctrl})

            Ctrl = self.NameConv.RMRenameSetFromName(Ctrl, "control", "objectType")
            RMRigTools.RMAlign(Obj, Ctrl, 3)

            ParentGroup = self.rigTools.RMCreateGroupOnObj(Ctrl)
            return ParentGroup, Ctrl
        else:
            print "Error importing Shape File"
            return None


def RMTurnToOne(curveArray):
    for eachCurve in curveArray[1:]:
        shapesInCurve = cmds.listRelatives(eachCurve, s=True, children=True)
        for eachShape in shapesInCurve:
            cmds.parent(eachShape, curveArray[0], shape=True, add=True)
            cmds.delete(eachCurve)


def RMCreateCubeLine(height, length, width, centered=False, offsetX=0, offsetY=0, offsetZ=0, name=""):
    if centered == True:
        offsetX = offsetX - height / 2
    if name == "":
        defaultName = "CubeLine"
    else:
        defaultName = name
    CubeCurve = []
    pointArray = [
        [0 + offsetX, -length / 2 + offsetY, width / 2 + offsetZ],
        [0 + offsetX, -length / 2 + offsetY, -width / 2 + offsetZ],
        [height + offsetX, -length / 2 + offsetY, -width / 2 + offsetZ],
        [height + offsetX, length / 2 + offsetY, -width / 2 + offsetZ],
        [height + offsetX, length / 2 + offsetY, width / 2 + offsetZ],
        [0 + offsetX, length / 2 + offsetY, width / 2 + offsetZ],
        [0 + offsetX, length / 2 + offsetY, -width / 2 + offsetZ],
        [height + offsetX, length / 2 + offsetY, -width / 2 + offsetZ],
        [height + offsetX, -length / 2 + offsetY, -width / 2 + offsetZ],
        [height + offsetX, -length / 2 + offsetY, width / 2 + offsetZ],
        [height + offsetX, length / 2 + offsetY, width / 2 + offsetZ],
        [height + offsetX, -length / 2 + offsetY, width / 2 + offsetZ],
        [0 + offsetX, -length / 2 + offsetY, width / 2 + offsetZ],
        [0 + offsetX, length / 2 + offsetY, width / 2 + offsetZ],
        [0 + offsetX, length / 2 + offsetY, -width / 2 + offsetZ],
        [0 + offsetX, -length / 2 + offsetY, -width / 2 + offsetZ]
    ]
    curve = cmds.curve(d=1, p=pointArray, name=defaultName)
    # return CubeCurve[0]
    return curve


def RMCreateBoxCtrl(Obj, NameConv=None, Xratio=1, Yratio=1, Zratio=1, ParentBaseSize=False, customSize=0, name="",
                    centered=False):
    if not NameConv:
        NameConv = RMNameConvention.RMNameConvention()
    if name == "":
        defaultName = "BoxControl"
    else:
        defaultName = name

    Parents = cmds.listRelatives(Obj, parent=True)

    if Parents and len(Parents) != 0 and ParentBaseSize == True:
        JntLength = RMRigTools.RMLenghtOfBone(Parents[0])
        Ctrl = RMCreateCubeLine(JntLength * Xratio, JntLength * Yratio, JntLength * Zratio, name=defaultName,
                                centered=centered)
    else:
        if customSize != 0:
            JntLength = customSize

        elif cmds.objectType(Obj) == "joint":
            JntLength = RMRigTools.RMLenghtOfBone(Obj)

        else:
            JntLength = 1
        Ctrl = RMCreateCubeLine(JntLength * Xratio, JntLength * Yratio, JntLength * Zratio, name=defaultName,
                                centered=centered)

    if name == '' and NameConv.RMIsNameInFormat(Obj):
        Ctrl = NameConv.RMRenameBasedOnBaseName(Obj, Ctrl,{})
    else:
        Ctrl = NameConv.RMRenameBasedOnBaseName(Obj, Ctrl, {'name': Ctrl})

    Ctrl = NameConv.RMRenameSetFromName(Ctrl, "control", "objectType")

    RMRigTools.RMAlign(Obj, Ctrl, 3)

    ResetGroup = RMRigTools.RMCreateGroupOnObj(Ctrl)
    return ResetGroup, Ctrl


def RMCircularControl(Obj, radius=1, NameConv=None, axis="X", name=""):
    if not NameConv:
        NameConv = RMNameConvention.RMNameConvention()
    if name == '':
        defaultName = "circularControl"
    else:
        defaultName = name
    if axis in "yY":
        Ctrl, Shape = cmds.circle(normal=[0, 1, 0], radius=radius, name=defaultName)
    elif axis in "zZ":
        Ctrl, Shape = cmds.circle(normal=[0, 0, 1], radius=radius, name=defaultName)
    elif axis in "xX":
        Ctrl, Shape = cmds.circle(normal=[1, 0, 0], radius=radius, name=defaultName)

    if name == '' and NameConv.RMIsNameInFormat(Obj):

        Ctrl = NameConv.RMRenameBasedOnBaseName(Obj, Ctrl, {})
    else:
        Ctrl = NameConv.RMRenameBasedOnBaseName(Obj, Ctrl, {'name': Ctrl})

    Ctrl = NameConv.RMRenameSetFromName(Ctrl, "control", "objectType")

    RMRigTools.RMAlign(Obj, Ctrl, 3)

    ResetGroup = RMRigTools.RMCreateGroupOnObj(Ctrl)

    return ResetGroup, Ctrl


def RMImportMoveControl(Obj, scale=1, NameConv=None, name='', Type="move"):
    MoversTypeDic = {
        "move": {"filename": "ControlMover.mb", "object": "MoverControl"},
        "v": {"filename": "ControlV.mb", "object": "VControl"},
        "head": {"filename": "ControlHead.mb", "object": "HeadControl"},
        "circleDeform": {"filename": "ControlCircularDeform.mb", "object": "CircularDeform"}
    }
    if not NameConv:
        NameConv = RMNameConvention.RMNameConvention()
    path = os.path.dirname(RMRigTools.__file__)
    RMPYPATH = os.path.split(path)
    FinalPath = os.path.join(RMPYPATH[0], "RMPY\AutoRig\RigShapes", MoversTypeDic[Type]["filename"])
    if os.path.isfile(FinalPath):
        cmds.file(FinalPath, i=True, type="mayaBinary", ignoreVersion=True, mergeNamespacesOnClash=False,
                  rpr="ControlMover", pr=False)
    else:
        print "archivo no encontrado %s , %s, %s " % (path, RMPYPATH, FinalPath)
        return None

    Ctrl = MoversTypeDic[Type]["object"]

    if cmds.objExists(Ctrl):
        if name != '':
            Ctrl = cmds.rename(Ctrl, name)

        cmds.setAttr(Ctrl + ".scale", scale, scale, scale)

        cmds.makeIdentity(Ctrl, apply=True, t=1, r=1, s=1)

        if name != '' and NameConv.RMIsNameInFormat(Obj):

            Ctrl = NameConv.RMRenameBasedOnBaseName(Obj, Ctrl, {})

        else:

            Ctrl = NameConv.RMRenameBasedOnBaseName(Obj, Ctrl, {'name': Ctrl})

        Ctrl = NameConv.RMRenameSetFromName(Ctrl, "control", "objectType")
        RMRigTools.RMAlign(Obj, Ctrl, 3)

        ParentGroup = RMRigTools.RMCreateGroupOnObj(Ctrl)
        return ParentGroup, Ctrl
    else:
        print "Error importing Shape File"
        return None
