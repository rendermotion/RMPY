import pymel.core as pm
from RMPY import RMRigTools
import os
from RMPY.core import config
from RMPY import nameConvention


class RMRigShapeControls(object):
    def __init__(self, NameConv=None):
        if NameConv is None:
            self.NameConv = nameConvention.NameConvention()
        else:
            self.NameConv = NameConv
        self.rigTools = RMRigTools.RMRigTools(NameConv=self.NameConv)

    def RMTurnToOne(self, curveArray):
        for eachCurve in curveArray[1:]:
            shapesInCurve = pm.listRelatives(eachCurve, s=True, children=True)
            for eachShape in shapesInCurve:
                pm.parent(eachShape, curveArray[0], shape=True, add=True)
                pm.delete(eachCurve)

    def RMCreateCubeLine(self, height, length, width, centered=False, offsetX=float(0.0), offsetY=float(0.0),
                         offsetZ=float(0.0), name=""):
        if centered:
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
        curve = pm.curve(d=1, p=pointArray, name=defaultName)
        # return CubeCurve[0]
        return curve

    def RMCreateBoxCtrl(self, Obj, Xratio=1, Yratio=1, Zratio=1, ParentBaseSize=False, customSize=0, name="",
                        centered=False):
        Obj = RMRigTools.validate_pymel_nodes(Obj)
        if name == "":
            defaultName = "BoxControl"
        else:
            defaultName = name

        Parents = pm.listRelatives(Obj, parent=True)

        if Parents and len(Parents) != 0 and ParentBaseSize == True:
            JntLength = RMRigTools.RMLenghtOfBone(Parents[0])
            Ctrl = RMCreateCubeLine(JntLength * Xratio, JntLength * Yratio, JntLength * Zratio, name=defaultName,
                                    centered=centered)
        else:
            if customSize != 0:
                JntLength = customSize

            elif pm.objectType(Obj) == "joint":
                JntLength = RMRigTools.RMLenghtOfBone(Obj)

            else:
                JntLength = 1
            Ctrl = RMCreateCubeLine(JntLength * Xratio, JntLength * Yratio, JntLength * Zratio, name=defaultName,
                                    centered=centered)

        if name == '' and self.NameConv.is_name_in_format(Obj):
            self.NameConv.rename_based_on_base_name(Obj, Ctrl)
        else:
            self.NameConv.rename_based_on_base_name(Obj, Ctrl, name=Ctrl)

        self.NameConv.rename_set_from_name(Ctrl, "control", "objectType")

        RMRigTools.RMAlign(Obj, Ctrl, 3)

        ResetGroup = self.rigTools.RMCreateGroupOnObj(Ctrl)
        return ResetGroup, Ctrl

    def RMCircularControl(self, Obj, radius=1, axis="X", name=""):
        Obj = RMRigTools.validate_pymel_nodes(Obj)
        if name == '':
            defaultName = "circularControl"
        else:
            defaultName = name
        if axis in "yY":
            Ctrl, Shape = pm.circle(normal=[0, 1, 0], radius=radius, name=defaultName)
        elif axis in "zZ":
            Ctrl, Shape = pm.circle(normal=[0, 0, 1], radius=radius, name=defaultName)
        elif axis in "xX":
            Ctrl, Shape = pm.circle(normal=[1, 0, 0], radius=radius, name=defaultName)

        if name == 'circularControl':
            if self.NameConv.is_name_in_format(Obj):
                self.NameConv.rename_based_on_base_name(Obj, Ctrl)
            else:
                self.NameConv.rename_name_in_format(Ctrl, name=name, objectType='control')
        else:
            self.NameConv.rename_name_in_format(Ctrl, name=name, objectType='control')
        RMRigTools.RMAlign(Obj, Ctrl, 3)

        ResetGroup = self.rigTools.RMCreateGroupOnObj(Ctrl)

        return ResetGroup, Ctrl

    def RMImportMoveControl(self, Obj, scale=1, name='', Type="move"):
        Obj = RMRigTools.validate_pymel_nodes(Obj)
        MoversTypeDic = {
            "move": {"filename": "ControlMover.mb", "object": "MoverControl"},
            "v": {"filename": "ControlV.mb", "object": "VControl"},
            "head": {"filename": "ControlHead.mb", "object": "HeadControl"},
            "circleDeform": {"filename": "ControlCircularDeform.mb", "object": "CircularDeform"}
        }
        print ('inside Iport move control')
        path = os.path.dirname(RMRigTools.__file__)
        RMPYPATH = os.path.split(path)
        FinalPath = os.path.join(RMPYPATH[0], "RMPY\AutoRig\RigShapes", MoversTypeDic[Type]["filename"])
        if os.path.isfile(FinalPath):
            pm.importFile(FinalPath, i=True, type="mayaBinary", ignoreVersion=True, mergeNamespacesOnClash=False,
                    rpr="ControlMover", pr=False)
            #pm.importFile(FinalPath, i=True, type="mayaBinary", ignoreVersion=True, mergeNamespacesOnClash=False,
            #          rpr="ControlMover", pr=False)
        else:
            print ("archivo no encontrado %s , %s, %s "% (path, RMPYPATH, FinalPath))
            return None
        Ctrl = pm.ls(MoversTypeDic[Type]["object"])[0]

        if pm.objExists(Ctrl):
            if name != '':
                Ctrl = pm.rename(Ctrl, name)

            pm.setAttr(Ctrl + ".scale", scale, scale, scale)

            pm.makeIdentity(Ctrl, apply=True, t=1, r=1, s=1)

            if name != '' and self.NameConv.is_name_in_format(Obj):

                self.NameConv.rename_based_on_base_name(Obj, Ctrl)

            else:
                self.NameConv.rename_based_on_base_name(Obj, Ctrl, name=Ctrl)

            self.NameConv.rename_set_from_name(Ctrl, "control", "objectType")
            RMRigTools.RMAlign(Obj, Ctrl, 3)

            ParentGroup = self.rigTools.RMCreateGroupOnObj(Ctrl)
            return ParentGroup, Ctrl
        else:
            print ("Error importing Shape File")
            return None


def RMTurnToOne(curveArray):
    for eachCurve in curveArray[1:]:
        shapesInCurve = pm.listRelatives(eachCurve, s=True, children=True)
        for eachShape in shapesInCurve:
            pm.parent(eachShape, curveArray[0], shape=True, add=True)
            pm.delete(eachCurve)

def fixShapeName(object_list):
    """
    :param object_list: receives a list of an object name, and renames the shapes to match the objects name.
    :return:no return value 
    """
    for each_object in object_list:
        shapes = each_object.getShapes()
        for each_shape in shapes:
            index = 0
            if each_shape.intermediateObject.get():
                print ('found intermediate')
            else:
                print ('found Shape')
                if index > 0:
                    each_shape.rename('%sShape%s' % (each_object, index))
                else:
                    each_shape.rename('%sShape' % (each_object))
                index += 1

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
    curve = pm.curve(d=1, p=pointArray, name=defaultName)
    # return CubeCurve[0]
    return curve


def RMCreateBoxCtrl(Obj, NameConv=None, Xratio=1, Yratio=1, Zratio=1, ParentBaseSize=False, customSize=0, name="",
                    centered=False):
    if not NameConv:
        NameConv = nameConvention.NameConvention()
    if name == "":
        defaultName = "BoxControl"
    else:
        defaultName = name

    Parents = pm.listRelatives(Obj, parent=True)

    if Parents and len(Parents) != 0 and ParentBaseSize == True:
        JntLength = RMRigTools.RMLenghtOfBone(Parents[0])
        Ctrl = RMCreateCubeLine(JntLength * Xratio, JntLength * Yratio, JntLength * Zratio, name=defaultName,
                                centered=centered)
    else:
        if customSize != 0:
            JntLength = customSize

        elif pm.objectType(Obj) == "joint":
            JntLength = RMRigTools.RMLenghtOfBone(Obj)

        else:
            JntLength = 1
        Ctrl = RMCreateCubeLine(JntLength * Xratio, JntLength * Yratio, JntLength * Zratio, name=defaultName,
                                centered=centered)

    if name == '' and NameConv.is_name_in_format(Obj):
        NameConv.rename_based_on_base_name(Obj, Ctrl)
    else:
        NameConv.rename_based_on_base_name(Obj, Ctrl, name = Ctrl)

    NameConv.rename_set_from_name(Ctrl, "control", "objectType")

    RMRigTools.RMAlign(Obj, Ctrl, 3)

    ResetGroup = RMRigTools.RMCreateGroupOnObj(Ctrl)
    return ResetGroup, Ctrl


def RMCircularControl(Obj, radius=1, NameConv=None, axis="X", name=""):
    Obj = RMRigTools.validate_pymel_nodes(Obj)
    if not NameConv:
        NameConv = nameConvention.NameConvention()
    if name == '':
        defaultName = "circularControl"
    else:
        defaultName = name
    if axis in "yY":
        Ctrl, Shape = pm.circle(normal=[0, 1, 0], radius=radius, name=defaultName)
    elif axis in "zZ":
        Ctrl, Shape = pm.circle(normal=[0, 0, 1], radius=radius, name=defaultName)
    elif axis in "xX":
        Ctrl, Shape = pm.circle(normal=[1, 0, 0], radius=radius, name=defaultName)

    if name == '' and NameConv.is_name_in_format(Obj):

        NameConv.rename_based_on_base_name(Obj, Ctrl)
    else:
        NameConv.rename_based_on_base_name(Obj, Ctrl, name=Ctrl)

    NameConv.rename_set_from_name(Ctrl, "control", "objectType")

    RMRigTools.RMAlign(Obj, Ctrl, 3)

    ResetGroup = RMRigTools.RMCreateGroupOnObj(Ctrl)

    return ResetGroup, Ctrl


def RMImportMoveControl(Obj, scale=1, NameConv=None, name='', Type="move"):
    Obj = RMRigTools.validate_pymel_nodes(Obj)
    MoversTypeDic = {
        "move": {"filename": "ControlMover.mb", "object": "MoverControl"},
        "v": {"filename": "ControlV.mb", "object": "VControl"},
        "head": {"filename": "ControlHead.mb", "object": "HeadControl"},
        "circleDeform": {"filename": "ControlCircularDeform.mb", "object": "CircularDeform"}
    }
    if not NameConv:
        NameConv = nameConvention.NameConvention()
    path = os.path.dirname(RMRigTools.__file__)
    RMPYPATH = os.path.split(path)
    FinalPath = os.path.join(RMPYPATH[0], "RMPY\AutoRig\RigShapes", MoversTypeDic[Type]["filename"])
    if os.path.isfile(FinalPath):
        print ('ready  to import')
        pm.importFile(FinalPath, i=True, type="mayaBinary", ignoreVersion=True, mergeNamespacesOnClash=False,
                  rpr="ControlMover", pr=False)
        print ('imported !!')
    else:
        print ("archivo no encontrado %s , %s, %s " % (path, RMPYPATH, FinalPath))
        return None

    Ctrl = pm.ls(MoversTypeDic[Type]["object"])[0]
    if pm.objExists(Ctrl):
        if name != '':
            Ctrl = pm.rename(Ctrl, name)

        pm.setAttr(Ctrl + ".scale", scale, scale, scale)

        pm.makeIdentity(Ctrl, apply=True, t=1, r=1, s=1)

        if name != '' and NameConv.is_name_in_format(Obj):

            NameConv.rename_based_on_base_name(Obj, Ctrl)

        else:

            NameConv.rename_based_on_base_name(Obj, Ctrl, name = Ctrl)
        NameConv.rename_set_from_name(Ctrl, "control", "objectType")

        RMRigTools.RMAlign(Obj, Ctrl, 3)

        ParentGroup = RMRigTools.RMCreateGroupOnObj(Ctrl)
        return ParentGroup, Ctrl
    else:
        print ("Error importing Shape File")
        return None

if __name__=='__main__':
    selection = pm.ls('Character01_MD_neck_pnt_rfr')[0]
    shapeControls = RMRigShapeControls()
    shapeControls.RMImportMoveControl(selection)

