import sys
import maya.cmds as cmds
import maya.OpenMayaUI as mui
from PySide import QtGui, QtCore
from shiboken import wrapInstance
import maya.mel as mel
import os
#sys.path.append(os.path.dirname(__file__))
from ui import RMFormBlendShapeEditor

reload(RMFormBlendShapeEditor)

def getMayaWindow():
	ptr = mui.MQtUtil.mainWindow()
	return wrapInstance(long(ptr), QtGui.QMainWindow)

class RMBlendShapeEditor(QtGui.QDialog):
	def __init__(self, parent=None):
		super(RMBlendShapeEditor,self).__init__(parent=getMayaWindow())
		self.ui=RMFormBlendShapeEditor.Ui_Form()
		self.ui.setupUi(self)
		self.setWindowTitle('Blend Shape Editor')
		self.ui.GetBlendshapeBtn.clicked.connect(self.GetBlendshapeBtnPressed)
		self.ui.ReplaceBlendShapeInputBtn.clicked.connect(self.ReplaceBlendShapeInputBtnPressed)
		self.ui.RebuildTargetsFromSelectionBtn.clicked.connect(self.RebuildTargetsFromSelectionBtnPressed)
		self.ui.ReplaceTargetWithSelBtn.clicked.connect(self.ReplaceTargetWithSelBtnPressed)

		'''self.ui.CreateParentGroup.clicked.connect(self.CreateParentBtnPressed)
		self.ui.JointsOnPoints.clicked.connect(self.JointsOnPointsBtnPressed)
		self.ui.AlignRotation.clicked.connect(self.AlignRotationBtnPressed)
		self.ui.AlignPosition.clicked.connect(self.AlignPositionBtnPressed)
		self.ui.AlignAll.clicked.connect(self.AlignAllBtnPressed)
		self.ui.ListConnectedJoints.clicked.connect(self.ListConnectedJointsBtnPressed)
		self.ui.SelectJoints.clicked.connect(self.SelectJointsBtnPressed)
		self.ui.SCCombineButton.clicked.connect(self.SCCombineButtonPressed)
		self.ui.AttributeTransferBtn.clicked.connect(self.AttributeTransferBtnPressed)
		
		#support Multiple selections on qwidgets
		self.ui.listWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)'''


	def GetBlendshapeBtnPressed(self):
		selection = cmds.ls(sl=True)
		print selection
		BSNode = mel.eval('''source RMDeformers.mel;
		$BSNode=GetDeformer("'''+selection[0]+'''","BlendShape");''')
		print BSNode
		#BlendShapeNodeNamelbl.setText

	def ReplaceBlendShapeInputBtnPressed(self):
		None
	def RebuildTargetsFromSelectionBtnPressed(self):
		None
	def ReplaceTargetWithSelBtnPressed(self):
		None



if __name__ == '__main__':
	w = RMBlendShapeEditor()
	w.show()
