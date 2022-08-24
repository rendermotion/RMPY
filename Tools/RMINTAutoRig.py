import maya.cmds as cmds
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.OpenMayaUI as mui
try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance
    from RMPY.Tools.QT5.ui import FormBipedRig

except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide import __version__
    from shiboken import wrapInstance
    from RMPY.Tools.QT4.ui import FormBipedRig

import maya.mel as mel
import pymel.core as pm
import os
from RMPY import RMUncategorized
from RMPY.AutoRig import RMAutoRig
from RMPY import nameConvention
from RMPY.AutoRig.snippets import CorrectPoleVectorsOrientation
from RMPY.AutoRig.snippets import RedoClavicleSpaceSwitch
from RMPY.AutoRig.snippets import SkeletonHands
from RMPY.AutoRig.snippets import supportScaleOnRig
from RMPY.snippets import ChangeNameConvention


from RMPY.AutoRig.snippets import FetTipRotation
def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QMainWindow)


class Main(MayaQWidgetDockableMixin, QDialog):
    def __init__(self, NameConv=None, parent=None):
        super(Main, self).__init__(parent = getMayaWindow())
        self.ui=FormBipedRig.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('AutoRig')

        if not NameConv:
            self.NameConv = nameConvention.NameConvention()
        else:
            self.NameConv = NameConv

        self.ui.CreateRigBtn.clicked.connect(self.CreateRigBtnPressed)
        self.ui.CreateReferencePointsBtn.clicked.connect(self.CreateReferencePointsBtnPressed)
        self.ui.MirrorSelectionBtn.clicked.connect(self.MirrorSelectionBtnPressed)
        self.ui.ClavicleSpaceSwitchBtn.clicked.connect(self.ClavicleSpaceSwitchBtnPressed)
        self.ui.PoleVectorBtn.clicked.connect(self.PoleVectorBtnPressed)
        self.ui.SkeletonHandsBtn.clicked.connect(self.SkeletonHandsBtnPressed)
        self.ui.supportScaleRigBtn.clicked.connect(self.supportScaleRigBtnPressed)
        self.ui.feetOrientationBtn.clicked.connect(self.feetOrientationBtnPressed)

    def feetOrientationBtnPressed(self):
        FeetTipRotation.FetTipRotationCorrect(side="LF")
        FeetTipRotation.FetTipRotationCorrect(side="RH")

        FeetTipRotation.fetAnkleRotationCorrect(side="LF")
        FeetTipRotation.fetAnkleRotationCorrect(side="RH")

    def CreateReferencePointsBtnPressed(self):
        CreateBypedPointsCommand = '''
        source "RMCreateCharacterByped.mel";
        CreateBipedCharacter(%s,<<0,0,1>>,<<0,1,0>>);
        ''' % (self.ui.HeightSpnBox.value())
        mel.eval(CreateBypedPointsCommand)
        selection = pm.ls('Character01_MD_Spine_pnt_rfr')
        ChangeNameConvention.changeNameConv(selection)
        pm.rename('C_object01_rig_UDF', 'C_headTip01_rig_pnt')

    def supportScaleRigBtnPressed(self):
        supportScaleOnRig.supportScaleOnRig()

    def MirrorSelectionBtnPressed(self):
        selection = cmds.ls(sl = True, type="transform")
        print selection
        self.MirrorSelection (selection)

    def CreateRigBtnPressed(self):
        FormBipedRig = RMAutoRig.RMBiped()
        FormBipedRig.CreateBipedRig()

    def MirrorSelection(self , ObjectList):
        for eachObject in ObjectList:
            ObjectTransformDic = RMUncategorized.ObjectTransformDic([eachObject])
            Side = self.NameConv.get_from_name(eachObject, "side")
            if Side == "R":
                OpositObject = self.NameConv.set_from_name(eachObject, "L", "side")
                if cmds.objExists(OpositObject):
                    RMUncategorized.SetObjectTransformDic({OpositObject: ObjectTransformDic[eachObject]}, MirrorTranslateX = 1 , MirrorTranslateY = 1 , MirrorTranslateZ = -1 , MirrorRotateX = -1 , MirrorRotateY = -1 , MirrorRotateZ = 1)
                else:
                    print 'object not found %s'%OpositObject
            else:
                OpositObject = self.NameConv.set_from_name(eachObject, "R", "side")
                if cmds.objExists(OpositObject):
                    RMUncategorized.SetObjectTransformDic({OpositObject : ObjectTransformDic[eachObject]}, MirrorTranslateX = 1 , MirrorTranslateY = 1 , MirrorTranslateZ = -1 , MirrorRotateX = -1 , MirrorRotateY = -1 , MirrorRotateZ = 1)
                else:
                    print 'object not found %s' % OpositObject
    def ClavicleSpaceSwitchBtnPressed(self):
        RedoClavicleSpaceSwitch.clavicleSpaceSwitch()
    def PoleVectorBtnPressed(self):
        CorrectPoleVectorsOrientation.correctPoleVectors()
    def SkeletonHandsBtnPressed(self):
        SkeletonHands.skeletonHands()
if __name__ == '__main__':
    w = Main()
    w.show()
