import sys
import maya.cmds as cmds
import maya.OpenMayaUI as mui
from PySide import QtGui, QtCore
from shiboken import wrapInstance
import maya.mel as mel
import os
import RMRigTools
from AutoRig import RMGenericJointRig
from GenericRig import RMProgressiveConstraint
from GenericRig import RMUnfoldRig

#sys.path.append(os.path.dirname(__file__))
from ui import RMFormRigTools
import RMUncategorized
reload(RMFormRigTools)
reload (RMGenericJointRig)
reload(RMProgressiveConstraint)

from AutoRig import RMRigFK

def getMayaWindow():
	ptr = mui.MQtUtil.mainWindow()
	return wrapInstance(long(ptr), QtGui.QMainWindow)

class RMINTRigTools(QtGui.QDialog):
	def __init__(self, parent=None):
		super(RMINTRigTools,self).__init__(parent=getMayaWindow())
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
		self.ui.ExtractGeoBtn.clicked.connect(self.ExtractGeoFunct)
		self.ui.GenericJointChainRigBtn.clicked.connect(self.GenericJointChainRigBtnPressed)
		self.ui.OrientNubButton.clicked.connect(self.OrientNubButtonPressed)
		self.ui.unfoldRigBtn.clicked.connect(self.unfoldRigBtnPressed)

		self.ui.ProgressiveConstraintButton.clicked.connect(self.ProgressiveConstraintButtonPressed)
		
		#self.ui.ConstShapeLblBtn.clicked.connect(self.AttributeTransferBtnPressed)

		#support Multiple selections on qwidgets
		self.ui.listWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

	def unfoldRigBtnPressed(self):
		selection = cmds.ls(selection=True)
		RMUnfoldRig.SpiralOfPointsStraight(self.ui.initRadiusSpnBx.value(),self.ui.endRadiusSpnBx.value(), self.ui.NumberOfPointsSpnBx.value(),selection[0],selection[1])

	def RenameToolBtnPressed(self):
		mel.eval('source RMINTRenameTool.mel;')
	def IKOnSelectionBtnPressed(self):
		mel.eval('source RMRigIK.mel;')
		mel.eval('RMIKCreateonSelected();')
	def FKOnSelectionBtnPressed(self):
		#mel.eval('source RMRigFK.mel;')
		#mel.eval('RMFKCreateonSelected();')
		FKM = RMRigFK.RMRigFK()
		FKM.createOnSelection()
	def CreateChildGroupBtnPressed(self):
		mel.eval('''source RMRigTools.mel;
		string $temp[]=`ls -sl`;
		RMCreateGrouponObj $temp[0] 2;''')

	def GenericJointChainRigBtnPressed(self):
		selection = cmds.ls(selection = True)
		GJR = RMGenericJointRig.RMGenericJointChainRig()
		GJR.CreateJointChainRig(selection[0],UDaxis = "Z")
	def OrientNubButtonPressed(self):
		selection = cmds.ls(selection = True)
		RMGenericJointRig.lastTwoJointsInChain(selection)

	def CreateParentBtnPressed(self):
		selection = cmds.ls( selection = True)
		paretnType =''
		if selection:
			if self.ui.parentRadio.isChecked() == True:
				paretnType ='parent'
			if self.ui.worldRadio.isChecked() == True:
				paretnType ='world'
			if self.ui.insertedRadio.isChecked() == True:
				paretnType ='inserted'
		
		for eachObject in selection:
			RMRigTools.RMCreateGroupOnObj(eachObject,Type = paretnType)
	def ProgressiveConstraintButtonPressed(self):
		selection = cmds.ls( selection = True)
		ConstraintType ='parent'
		if selection:
			if self.ui.CnstParentRadio.isChecked() == True:
				ConstraintType ='parent'
			if self.ui.CnstOrientRadio.isChecked() == True:
				ConstraintType ='orient'
			if self.ui.CnstPointRadio.isChecked() == True:
				ConstraintType ='point'
		if self.ui.mantainOffsetChk.isChecked() == True:
			mo = True 
		else: 
			mo = False
		deepth=self.ui.ProgressiveDepthSpinBox.value()

		RMProgressiveConstraint.deepthProgressiveconstraint( deepth, selection, constraintType = ConstraintType, mo = mo)

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
		self.ui.listWidget.clear()
		selection = cmds.ls(sl = True)
		for eachObject in selection: 
			returned=mel.eval('''source RMRigSkinTools.mel;
			getSkinInfluence("'''+eachObject+ '''");''')
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

	def ExtractGeoFunct(self):
		RMUncategorized.ExtractGeometry()

if __name__ == '__main__':
	w = RMINTRigTools()
	w.show()
