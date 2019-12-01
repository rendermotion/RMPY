import sys
import maya.cmds as cmds
import maya.OpenMayaUI as mui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance
    from RMPY.Tools.QT5.ui import FormBlendShapeCreatorHelper

except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide import __version__
    from shiboken import wrapInstance
    from RMPY.Tools.QT4.ui import FormBlendShapeCreatorHelper
import maya.mel as mel
import os
from RMPY import RMblendShapesTools


def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QMainWindow)

class main(MayaQWidgetDockableMixin, QDialog):
    def __init__(self, parent=None):
        super(main,self).__init__(parent=getMayaWindow())
        self.ui=FormBlendShapeCreatorHelper.Ui_Form()
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
            RMblendShapesTools.invertCurrentPaintTargetWeights(BSNode, index)
            #invertCurrentPaintTargetWeights(BSNode,self.BSdictionary[BsName.text()]["TargetGroup"])


if __name__ == '__main__':
    w = main()
    w.show()
