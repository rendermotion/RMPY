import sys
import maya.cmds as cmds
import maya.OpenMayaUI as mui
from PySide import QtGui, QtCore
from shiboken import wrapInstance
import maya.mel as mel
import os
import RMUncategorized
from ui import RMFormAutorig
from AutoRig import RMAutoRig
import RMNameConvention

def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QtGui.QMainWindow)

class RMINTAutoRig(QtGui.QDialog):
    def __init__(self, NameConv=None, parent=None):
        super(RMINTAutoRig,self).__init__(parent = getMayaWindow())
        self.ui=RMFormAutorig.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('AutoRig')

        if not NameConv:
            self.NameConv = RMNameConvention.RMNameConvention()
        else:
            self.NameConv = NameConv

        self.ui.CreateRigBtn.clicked.connect(self.CreateRigBtnPressed)
        self.ui.CreateReferencePointsBtn.clicked.connect(self.CreateReferencePointsBtnPressed)
        self.ui.MirrorSelectionBtn.clicked.connect(self.MirrorSelectionBtnPressed)

    def CreateReferencePointsBtnPressed(self):
        CreateBypedPointsCommand = '''
        source "RMCreateCharacterByped.mel";
        CreateBipedCharacter(%s,<<0,0,1>>,<<0,1,0>>);
        '''%(self.ui.HeightSpnBox.value())
        mel.eval(CreateBypedPointsCommand)

    def MirrorSelectionBtnPressed(self):
        selection = cmds.ls(sl = True, type="transform")
        print selection
        self.MirrorSelection (selection)

    def CreateRigBtnPressed(self):
        BipedRig = RMAutoRig.RMBiped()
        BipedRig.CreateBipedRig()

    def MirrorSelection(self , ObjectList):
        for eachObject in ObjectList:
            ObjectTransformDic = RMUncategorized.ObjectTransformDic( [eachObject] )
            Side = self.NameConv.RMGetFromName( eachObject , "Side")
            if Side == "RH":
                OpositObject = self.NameConv.RMSetFromName( eachObject , "LF" , "Side")
                if cmds.objExists(OpositObject):
                    RMUncategorized.SetObjectTransformDic({OpositObject : ObjectTransformDic[eachObject]}, MirrorTranslateX = 1 , MirrorTranslateY = 1 , MirrorTranslateZ = -1 , MirrorRotateX = -1 , MirrorRotateY = -1 , MirrorRotateZ = 1)
            else:
                OpositObject = self.NameConv.RMSetFromName( eachObject , "RH" , "Side")
                if cmds.objExists(OpositObject):
                    RMUncategorized.SetObjectTransformDic({OpositObject : ObjectTransformDic[eachObject]}, MirrorTranslateX = 1 , MirrorTranslateY = 1 , MirrorTranslateZ = -1 , MirrorRotateX = -1 , MirrorRotateY = -1 , MirrorRotateZ = 1)
if __name__ == '__main__':
    w = RMINTAutoRig()
    w.show()
