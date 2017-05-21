import sys
import maya.cmds as cmds
import maya.OpenMayaUI as mui
from PySide import QtGui, QtCore
from shiboken import wrapInstance
import maya.mel as mel
import os
from RMPY import RMblendShapesTools
reload (RMblendShapesTools)
from RMPY.ui import RMFormBSCreatorHelper

def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QtGui.QMainWindow)

class Main(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Main,self).__init__(parent=getMayaWindow())
        self.ui=RMFormBSCreatorHelper.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('Blend Shape Creator Helper')
        self.ui.LoadObjectBtn.clicked.connect(self.loadObjectBtnPressed)
        self.ui.FlipWeightsBtn.clicked.connect(self.FlipWeightsBtnPressed)
        self.BSdictionary = None

    def loadObjectBtnPressed(self):
        selection = cmds.ls(selection = True)
        BSNodeArray = mel.eval('''source RMDeformers.mel;\nstring $BSNode[]=GetDeformer("'''+selection[0]+'''","blendShape");''')
        if len(BSNodeArray) > 0:
            self.ui.ObjectLbl.setText(BSNodeArray[0])
            self.BSdictionary = RMblendShapesTools.RMblendShapeTargetDic( BSNodeArray[0])
            print self.BSdictionary
            self.ui.listWidget.clear()
            for keys in sorted(self.BSdictionary):
                self.ui.listWidget.addItem(keys)

            if len(self.BSdictionary.keys()) >= 1:
                self.ui.listWidget.setCurrentRow(0)
        else:
            print "No Blendshape Node found"

    def FlipWeightsBtnPressed(self):
        BSNode = self.ui.ObjectLbl.text()
        BsName = self.ui.listWidget.currentItem()

        if BSNode!= "":
            print self.BSdictionary[BsName.text()]["TargetGroup"]
            print "BSNode:%s"%BSNode
            print "TargerEdited:%s"%self.BSdictionary[BsName.text()]["TargetGroup"]
            index = self.BSdictionary[BsName.text()]["TargetGroup"]
            RMblendShapesTools.copyCurrentPaintTargetWeights(BSNode, index,index)
            #invertCurrentPaintTargetWeights(BSNode,self.BSdictionary[BsName.text()]["TargetGroup"])


if __name__ == '__main__':
    w = Main()
    w.show()
