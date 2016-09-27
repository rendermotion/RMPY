import sys
import maya.cmds as cmds
import maya.OpenMayaUI as mui
from PySide import QtGui, QtCore
from shiboken import wrapInstance
import maya.mel as mel
import os
import RMUncategorized
from AutoRig import RMLaces
from ui import RMFormLaces
from snippets import MultiPathObjects
reload(RMFormLaces)
reload(RMLaces)

def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QtGui.QMainWindow)

class RMINTLacesTool(QtGui.QDialog):
    def __init__ (self, NameConv=None, parent=None):
        super(RMINTLacesTool,self).__init__(parent = getMayaWindow())
        self.isShapeSelected = False
        self.ui = RMFormLaces.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('RM Laces')
        self.ui.LoadShapeBtn.clicked.connect(self.LoadShapeBtnPressed)
        self.ui.CreateControlsBtn.clicked.connect(self.CreateControlsBtnPressed)
        self.NumCvs = None
        self.ui.ControlCurveBtn.clicked.connect(self.ControlCurveBtnPressed)
        self.ui.PathCurveBtn.clicked.connect(self.PathCurveBtnPressed)
        self.ui.pushButton.clicked.connect(self.ProgressiveLinkBtnPressed)

    def PathCurveBtnPressed(self):
        selection = cmds.ls(selection = True)
        if selection and len(selection)>=1:
            self.ui.PathCurveLbl.setText(selection[0])
    
    def ControlCurveBtnPressed(self):
        selection = cmds.ls(selection = True)
        if selection and len(selection)>=1:
            self.ui.ControlCurveLbl.setText(selection[0])
    def ProgressiveLinkBtnPressed(self):
        objectArray = cmds.ls(sl=True)
        MultiPathObjects.pathFollow(self.ui.PathCurveLbl.text(),self.ui.ControlCurveLbl.text(),objectArray)

    def LoadShapeBtnPressed(self):
        selection = cmds.ls(selection = True)[0]
        self.isShapeSelected = True
        self.ui.CurrentShapeLbl.setText(selection)
        form = cmds.getAttr (selection+".form")
        spans = cmds.getAttr (selection + ".spans")
        if form == 2:   
            CVs = spans
        else:
            CVs = spans + 3
        self.NumCvs=CVs
        self.ui.CurrentShapeControlsLbl.setText("Current Controls Number %s"%CVs)
    
    def CreateControlsBtnPressed(self):
        laces = RMLaces.RMlaces()
        if self.ui.RebuildCurveChk.isChecked() == True:
            laces.RebuildWithNCVs(self.ui.NumberOfSpansSpnBx.value(),self.ui.CurrentShapeLbl.text())
        else: 
            laces.RebuildWithNCVs(self.NumCvs,self.ui.CurrentShapeLbl.text())

        if self.ui.Mode.isChecked() == True:
            laces.RMlacesSystem( self.ui.NumberOfJoints.value() , curve = self.ui.CurrentShapeLbl.text())    
        else:
            laces.RMlacesSystemMultipleRotationControls(self.ui.NumberOfJoints.value() , curve = self.ui.CurrentShapeLbl.text())
if __name__ == '__main__':
    w = RMINTLacesTool()
    w.show()





