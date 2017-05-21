import sys
import maya.cmds as cmds
import maya.OpenMayaUI as mui
from PySide import QtGui, QtCore
from shiboken import wrapInstance
import maya.mel as mel
import os
from RMPY.ui import RMFormGenericPropRigTool
import RMPY.RMNameConvention
from RMPY.snippets import NoisePatternRig

reload(RMFormGenericPropRigTool)
reload(NoisePatternRig)

def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QtGui.QMainWindow)

class Main(QtGui.QDialog):
    def __init__(self, NameConv=None, parent=None):
        super(Main,self).__init__(parent = getMayaWindow())
        self.ui=RMFormGenericPropRigTool.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('Generic Prop Rig Tool')
        self.ui.RigSelectionBtn.clicked.connect(self.RigSelectionBtnPressed)
        self.ui.LoadSelectionAsCntrlObjPushBtn.clicked.connect(self.LoadSelectionAsCntrlObjPushBtnPressed)
        self.ui.AddNoiseBtn.clicked.connect(self.AddNoiseBtnPressed)
        self.ui.DeleteSimpleRigBtn.clicked.connect(self.deleteSimpleRigBtnPressed)

    def RigSelectionBtnPressed(self):
        NoisePatternRig.CreateControlOnSelection(centerPivot = True)

    def LoadSelectionAsCntrlObjPushBtnPressed(self):
        Object = cmds.ls(selection = True)[0]
        self.ui.ControllineEdit.setText(Object)
    
    def AddNoiseBtnPressed(self):
        Object = cmds.ls(selection = True)[0]
        NoisePatternRig.addNoiseOnControl([Object], self.ui.ControllineEdit.text())

    def CreateGenericRigStructure(self):
        pass

    def deleteSimpleRigBtnPressed(self):
        NoisePatternRig.deleteSimpleRig()

if __name__ == '__main__':
    w = Main()
    w.show()
