import sys
import maya.cmds as cmds
import maya.OpenMayaUI as mui
from PySide import QtGui, QtCore
from shiboken import wrapInstance
import maya.mel as mel
import os
import RMblendShapesTools
from ui import RMFormFacialRig
reload (RMFormFacialRig)
import RMRigTools
import FacialRig.FacialConfiguration as FacialConfiguration
reload (FacialConfiguration)
Dictionaries =  {'lisShapes'        :FacialConfiguration.lidShapes,#0
                 'EyeBallPupil'     :FacialConfiguration.EyeBallPupil,#1
                 'Cristaline'       :FacialConfiguration.Cristaline,#2
                 'mouthSecondarys'  :FacialConfiguration.mouthSecondarys,#3
                 'EyeJawJoints'     :FacialConfiguration.EyeJawJoints,#4
                 'mouth'            :FacialConfiguration.mouth,#5
                 'Cheeks'           :FacialConfiguration.Cheeks,#6
                 'mouthMover'       :FacialConfiguration.mouthMover,#7
                 'Nose'             :FacialConfiguration.Nose,#8
                 'Furrow'           :FacialConfiguration.Furrow,#9
                 'secondaryEyeBrow' :FacialConfiguration.secondaryEyeBrow,#10
                 "EyeBrow"          :FacialConfiguration.EyeBrow
                 }


def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QtGui.QMainWindow)

class RMFacialRig(QtGui.QDialog):
    def __init__(self, parent=None):
        super(RMFacialRig,self).__init__(parent=getMayaWindow())
        self.ui=RMFormFacialRig.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('FacialRig')
        self.ui.CheckBtn.clicked.connect(self.CheckBtnPressed)
        self.ui.ImportFacialInterfaceBtn.clicked.connect(self.ImportFacialInterfaceBtnPressed)
        self.ui.ListCBx.currentIndexChanged.connect(self.comboBoxChanged)
        for eachItem in sorted(Dictionaries):
            self.ui.ListCBx.addItem(eachItem)
    def comboBoxChanged(self):
        self.CheckBtnPressed()

    def CheckBtnPressed(self):
        self.ui.listWidget.clear()
        eachDic = Dictionaries[self.ui.ListCBx.currentText()]
        print eachDic
        for eachDefinition in eachDic:
            print eachDefinition
            if eachDic[eachDefinition]['Type'] == 'blendShapeDefinition':
                arrayPrefix =[]
                if eachDic[eachDefinition]['isSymetrical'] == True:
                    arrayPrefix = ["L"]
                else :
                    arrayPrefix = [""]
                for eachPrefix in arrayPrefix:
                    for eachBlendShape in sorted(eachDic[eachDefinition]['blendShapes']):
                        if not cmds.objExists(eachPrefix + eachBlendShape):
                            self.ui.listWidget.addItem(eachPrefix + eachBlendShape)


    def ImportFacialInterfaceBtnPressed(self):
        path = os.path.dirname(RMRigTools.__file__)
        RMMel=os.path.split(path)
        FinalPath = os.path.join(RMMel[0],"Python\FacialRig\RigShapes\FacialInterface.mb")

        if os.path.isfile(FinalPath):
            cmds.file( FinalPath, i=True, type="mayaBinary", ignoreVersion = True, mergeNamespacesOnClash=False, rpr="", pr = False)
        else:
            print "archivo de RigFacial No encontrado"
            return None


if __name__ == '__main__':
    w = RMFacialRig()
    w.show()
