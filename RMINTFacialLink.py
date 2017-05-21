import sys
import maya.cmds as cmds
import maya.OpenMayaUI as mui
from PySide import QtGui, QtCore
from shiboken import wrapInstance
import maya.mel as mel
import os
from RMPY.ui import RMFormFacialLink
from RMPY.FacialRig import GenericFacialRig

reload(GenericFacialRig)
from RMPY import RMUncategorized


def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QtGui.QMainWindow)


class Main(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent=getMayaWindow())
        self.ui = RMFormFacialLink.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('Facial Link')

        self.FacialRig = GenericFacialRig.GenericFacial()

        self.ui.LinkFaceBtn.clicked.connect(self.Link)
        self.ui.LinkJawBtn.clicked.connect(self.JawSetup)
        self.ui.EyeSetUpBtn.clicked.connect(self.SetupEyes)

        self.ui.ImpCtrlsFacialBtn.clicked.connect(self.importFacialControls)
        self.ui.ImpCtrlEyeBtn.clicked.connect(self.importFacialControls)
        self.ui.CheckBtn.clicked.connect(self.CheckExistance)

    def importFacialControls(self):
        path = os.path.dirname(RMUncategorized.__file__)
        RMMel = os.path.split(path)
        FinalPath = os.path.join(RMMel[0], "Mel", "FacialControlsV2.mb")
        if os.path.isfile(FinalPath):
            cmds.file(FinalPath, i=True, type="mayaBinary", ignoreVersion=True, mergeNamespacesOnClash=False,
                      rpr="FacialControls", pr=False)
        else:
            print "archivo no encontrado"

    def Link(self):
        self.FacialRig.LinkFacial()

    def JawSetup(self):
        self.FacialRig.JawSetup()

    def SetupEyes(self):
        self.FacialRig.SetupEyes()

    def CheckExistance(self):
        self.FacialRig.checkExistance()
        self.ui.NodesQList.clear()
        self.addToList(self.FacialRig.FaceBlendShapeDic)
        self.addToList(self.FacialRig.IntermediateBlendShapeDic)
        self.addToList(self.FacialRig.JawDic)
        self.addToList(self.FacialRig.EyesDic)

    def addToList(self, Dictionary):
        for keys in sorted(Dictionary):
            if Dictionary[keys]["Exists"] == False:
                self.ui.NodesQList.addItem(keys)


if __name__ == '__main__':
    w = Main()
    w.show()
