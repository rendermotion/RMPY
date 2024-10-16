import sys
import maya.cmds as cmds
import maya.OpenMayaUI as mui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6 import __version__
from shiboken6 import wrapInstance
from RMPY.Tools.QT5.ui import FormGenericPropRig


import maya.mel as mel
import os

import RMPY.nameConvention
from RMPY.snippets import NoisePatternRig


def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(int(ptr), QMainWindow)

class main(MayaQWidgetDockableMixin, QDialog):
    def __init__(self, NameConv=None, parent=None):
        super(main,self).__init__(parent=getMayaWindow())
        self.ui=FormGenericPropRig.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('Generic Prop Rig Tool')
        self.ui.RigSelectionBtn.clicked.connect(self.RigSelectionBtnPressed)
        self.ui.LoadSelectionAsCntrlObjPushBtn.clicked.connect(self.LoadSelectionAsCntrlObjPushBtnPressed)
        self.ui.AddNoiseBtn.clicked.connect(self.AddNoiseBtnPressed)
        self.ui.DeleteSimpleRigBtn.clicked.connect(self.deleteSimpleRigBtnPressed)

    def RigSelectionBtnPressed(self):
        NoisePatternRig.CreateControlOnSelection(centerPivot = True)

    def LoadSelectionAsCntrlObjPushBtnPressed(self):
        Object = cmds.ls(selection=True)[0]
        self.ui.ControllineEdit.setText(Object)
    
    def AddNoiseBtnPressed(self):
        Object = cmds.ls(selection=True)[0]
        NoisePatternRig.addNoiseOnControl([Object], self.ui.ControllineEdit.text())

    def CreateGenericRigStructure(self):
        pass

    def deleteSimpleRigBtnPressed(self):
        NoisePatternRig.deleteSimpleRig()

if __name__ == '__main__':
    w = main()
    w.show()
