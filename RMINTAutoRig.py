import sys
import maya.cmds as cmds
import maya.OpenMayaUI as mui
from PySide import QtGui, QtCore
#RMB08
#627tpw
try:
    from shiboken import wrapInstance
except:
    from shiboken2 import wrapInstance 
import maya.mel as mel
import os
import RMPY.RMUncategorized
from RMPY.ui import RMFormAutorig
from RMPY.AutoRig import RMAutoRig
from RMPY import RMNameConvention
from RMPY.AutoRig.snippets import CorrectPoleVectorsOrientation
from RMPY.AutoRig.snippets import RedoClavicleSpaceSwitch
from RMPY.AutoRig.snippets import SkeletonHands
from RMPY.AutoRig.snippets import supportScaleOnRig
from RMPY.AutoRig.snippets import FetTipRotation
reload(RMAutoRig)
#reload(RMFormAutorig)
def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QtGui.QMainWindow)

class Main(QtGui.QDialog):
    def __init__(self, NameConv=None, parent=None):
        super(Main, self).__init__(parent = getMayaWindow())
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
        self.ui.ClavicleSpaceSwitchBtn.clicked.connect(self.ClavicleSpaceSwitchBtnPressed)
        self.ui.PoleVectorBtn.clicked.connect(self.PoleVectorBtnPressed)
        self.ui.SkeletonHandsBtn.clicked.connect(self.SkeletonHandsBtnPressed)
        self.ui.supportScaleRigBtn.clicked.connect(self.supportScaleRigBtnPressed)
        self.ui.feetOrientationBtn.clicked.connect(self.feetOrientationBtnPressed)

    def feetOrientationBtnPressed(self):
        FeetTipRotation.FetTipRotationCorrect(side="LF")
        FeetTipRotation.FetTipRotationCorrect(side="RH")

        FeetTipRotation.fetAnkleRotationCorrect(side="LF")
        FeetTipRotation.fetAnkleRotationCorrect(side="RH")

    def CreateReferencePointsBtnPressed(self):
        CreateBypedPointsCommand = '''
        source "RMCreateCharacterByped.mel";
        CreateBipedCharacter(%s,<<0,0,1>>,<<0,1,0>>);
        '''%(self.ui.HeightSpnBox.value())
        mel.eval(CreateBypedPointsCommand)
    def supportScaleRigBtnPressed(self):
        supportScaleOnRig.supportScaleOnRig()

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
    def ClavicleSpaceSwitchBtnPressed(self):
        RedoClavicleSpaceSwitch.clavicleSpaceSwitch()
    def PoleVectorBtnPressed(self):
        CorrectPoleVectorsOrientation.correctPoleVectors()
    def SkeletonHandsBtnPressed(self):
        SkeletonHands.skeletonHands()
if __name__ == '__main__':
    w = Main()
    w.show()
