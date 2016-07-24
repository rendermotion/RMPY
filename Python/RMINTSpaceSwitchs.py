import sys
import maya.cmds as cmds
import maya.OpenMayaUI as mui
from PySide import QtGui, QtCore
from shiboken import wrapInstance
import maya.mel as mel
import os

from ui import RMFormSpaceSwitch
from AutoRig import RMSpaceSwitch


def getMayaWindow():
	ptr = mui.MQtUtil.mainWindow()
	return wrapInstance(long(ptr), QtGui.QMainWindow)

class RMSpaceSwitchTool(QtGui.QDialog):
	def __init__(self, parent=None):
		super(RMSpaceSwitchTool,self).__init__(parent=getMayaWindow())

		self.ui=RMFormSpaceSwitch.Ui_Form()
		self.ui.setupUi(self)
		self.setWindowTitle('Space Switch Tool')
		self.RMSpaceSwitch = RMSpaceSwitch.RMSpaceSwitch()
		

		
		self.ui.LinkFaceBtn.clicked.connect(self.Link)
		self.ui.LinkJawBtn.clicked.connect(self.JawSetup)
		self.ui.EyeSetUpBtn.clicked.connect(self.SetupEyes)

		self.ui.ImpCtrlsFacialBtn.clicked.connect(self.importFacialControls)
		self.ui.ImpCtrlEyeBtn.clicked.connect(self.importFacialControls)
		self.ui.CheckBtn.clicked.connect(self.CheckExistance)

if __name__ == '__main__':
	w = RMFacialLink()
	w.show()
