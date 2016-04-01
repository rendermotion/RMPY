import sys
import maya.cmds as cmds
import maya.OpenMayaUI as mui
from PySide import QtGui, QtCore
from shiboken import wrapInstance
import maya.mel as mel
import os
#sys.path.append(os.path.dirname(__file__))
from ui import RMFormRigTools
reload(RMFormRigTools)

def getMayaWindow():
	ptr = mui.MQtUtil.mainWindow()
	return wrapInstance(long(ptr), QtGui.QMainWindow)

class RMRigTools(QtGui.QDialog):
	def __init__(self, parent=None):
		super(RMRigTools,self).__init__(parent=getMayaWindow())
		self.ui=RMFormRigTools.Ui_Form()
		self.ui.setupUi(self)
		self.setWindowTitle('RM Maya Rig Tools')
		self.ui.RenameTool.clicked.connect(self.RenameToolBtnPressed)
		self.ui.IKOnSelection.clicked.connect(self.IKOnSelectionBtnPressed)
		self.ui.FKOnSelection.clicked.connect(self.FKOnSelectionBtnPressed)
		self.ui.CreateChildGroup.clicked.connect(self.CreateChildGroupBtnPressed)
		self.ui.CreateParentGroup.clicked.connect(self.CreateParentBtnPressed)
		self.ui.JointsOnPoints.clicked.connect(self.JointsOnPointsBtnPressed)
		self.ui.AlignRotation.clicked.connect(self.AlignRotationBtnPressed)
		self.ui.AlignPosition.clicked.connect(self.AlignPositionBtnPressed)
		self.ui.AlignAll.clicked.connect(self.AlignAllBtnPressed)
		self.ui.ListConnectedJoints.clicked.connect(self.ListConnectedJointsBtnPressed)
		self.ui.SelectJoints.clicked.connect(self.SelectJointsBtnPressed)
		self.ui.SCCombineButton.clicked.connect(self.SCCombineButtonPressed)
		self.ui.AttributeTransferBtn.clicked.connect(self.AttributeTransferBtnPressed)
		
		#support Multiple selections on qwidgets
		self.ui.listWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

	def RenameToolBtnPressed(self):
		mel.eval('source RMINTRenameTool.mel;')
	def IKOnSelectionBtnPressed(self):
		mel.eval('source RMRigIK.mel;')
		mel.eval('RMIKCreateonSelected();')
	def FKOnSelectionBtnPressed(self):
		mel.eval('source RMRigFK.mel;')
		mel.eval('RMFKCreateonSelected();')
	def CreateChildGroupBtnPressed(self):
		mel.eval('''source RMRigTools.mel;
		string $temp[]=`ls -sl`;
		RMCreateGrouponObj $temp[0] 2;''')
	def CreateParentBtnPressed(self):
		mel.eval('''source RMRigTools.mel;
		string $temp[]=`ls -sl`;
		RMCreateGrouponObj $temp[0] 1;''')
	def JointsOnPointsBtnPressed(self):
		mel.eval('''source RMRigTools.mel;
		string $temp[]=`ls -sl`;
		RMCreateBonesAtPoints $temp;''')
	def AlignPositionBtnPressed(self):
		mel.eval('''source RMRigTools.mel;
		string $temp[]=`ls -sl`;
		RMAlign $temp[1] $temp[0] 1;''')
	def AlignRotationBtnPressed(self):
		mel.eval('''source RMRigTools.mel;
		string $temp[]=`ls -sl`;
		RMAlign $temp[1] $temp[0] 2;''')
	def AlignAllBtnPressed(self):
		mel.eval('''source RMRigTools.mel;
		string $temp[]=`ls -sl`;
		RMAlign $temp[1] $temp[0] 3;''')
	def ListConnectedJointsBtnPressed(self):
		returned=mel.eval('''source RMRigSkinTools.mel;
			string $var[]=`ls -sl`;
		getSkinInfluence($var[0]);''')
		self.ui.listWidget.clear()
		for i in returned:
			self.ui.listWidget.addItem(i)
	def SelectJointsBtnPressed(self):
		Array=self.ui.listWidget.selectedItems()
		cmds.select(clear=True)
		for g in (Array):
			print g.text()
			cmds.select(g.text(),add=True)
	def SCCombineButtonPressed(self):
		mel.eval('''source RMRigShapeControls.mel;
		string $temp[]=`ls -sl`;
		RMTurnToOne $temp;''')
	def AttributeTransferBtnPressed(self):
		mel.eval('''source RMAttributes.mel;
		string $temp[]=`ls -sl`;
		TransferAllAttr $temp[0] $temp[1];''')



if __name__ == '__main__':
	w = RMRigTools()
	w.show()
