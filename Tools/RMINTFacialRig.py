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
    from RMPY.Tools.QT5.ui  import FormFacialRig
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide import __version__
    from shiboken import wrapInstance
    from RMPY.Tools.QT4.ui import FormFacialRig
import maya.mel as mel
import os
from RMPY import RMblendShapesTools

reload (FormFacialRig)
from RMPY import RMRigTools
from RMPY.FacialRig import FacialConfigurationNew as FacialConfiguration

from RMPY import RMParametersManager
reload (FacialConfiguration)
reload (RMblendShapesTools)

Dictionaries = {
                 'lidShapes'        :FacialConfiguration.lidShapes,#0
                 'EyeBallPupil'     :FacialConfiguration.EyeBallPupil,#1
                 'Cristaline'       :FacialConfiguration.Cristaline,#2
                 'EyeJawJoints'     :FacialConfiguration.EyeJawJoints,#4
                 #'mouthSecondarys'  :FacialConfiguration.mouthSecondarys,#3
                 'mouth'            :FacialConfiguration.mouth,#5
                 'Cheeks'           :FacialConfiguration.Cheeks,#6
                 'mouthMover'       :FacialConfiguration.mouthMover,#7
                 'Nose'             :FacialConfiguration.Nose,#8
                 'Furrow'           :FacialConfiguration.Furrow,#9
                 #'secondaryEyeBrow' :FacialConfiguration.secondaryEyeBrow,#10
                 'EyeBrow'          :FacialConfiguration.EyeBrow
                }

 
def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QMainWindow)

class main(MayaQWidgetDockableMixin,QDialog):
    def __init__(self, parent=None):
        super(main,self).__init__(parent=getMayaWindow())
        self.ui=FormFacialRig.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('FacialRig')
        self.ui.CheckBtn.clicked.connect(self.CheckBtnPressed)
        self.ui.ImportFacialInterfaceBtn.clicked.connect(self.ImportFacialInterfaceBtnPressed)
        self.ui.DeleteAttributesBtn.clicked.connect(self.deleteAttributes)
        self.ui.ListCBx.currentIndexChanged.connect(self.comboBoxChanged)
        self.ui.renameRightBtn.clicked.connect(self.renameRightBtn)

        self.ui.LinkAllBtn.clicked.connect(self.linkAllDictionaries)

        self.ui.UsePrefixChkBx.stateChanged.connect(self.usePrefixChkBxStateChanged)
        for eachItem in sorted(Dictionaries):
            self.ui.ListCBx.addItem(eachItem)
        self.ui.LinkSelectedBtn.clicked.connect(self.connectDictionary)
        self.Manager = RMblendShapesTools.BSManager()
        
        self.ui.PrefixLineEdit.textChanged.connect(self.CheckBtnPressed)

    def usePrefixChkBxStateChanged(self):
        if self.ui.UsePrefixChkBx.checkState() == QtCore.Qt.CheckState.Checked:
            self.ui.PrefixLineEdit.setEnabled(True)
        else: 
            self.ui.PrefixLineEdit.setDisabled(True)
        self.CheckBtnPressed()        

    def renameRightBtn(self):
        selection = cmds.ls(selection=True)
        for i in selection:
            cmds.rename (i , "R" + i[1:-1])

    def comboBoxChanged(self):
        self.CheckBtnPressed()

    def connectDictionary(self):
        if self.ui.PrefixLineEdit.isEnabled():
            objectNamePrefix = self.ui.PrefixLineEdit.text()
        else:
            objectNamePrefix=''


        linkDictionary = Dictionaries[self.ui.ListCBx.currentText()]
        self.Manager.AppyBlendShapeDefinition(linkDictionary,  objectPrefix = objectNamePrefix)
    
    def linkAllDictionaries(self):
        if self.ui.PrefixLineEdit.isEnabled():
            objectNamePrefix = self.ui.PrefixLineEdit.text()
        else:
            objectNamePrefix=''

        for eachDic in Dictionaries:
            self.Manager.AppyBlendShapeDefinition(Dictionaries[eachDic],  objectPrefix = objectNamePrefix)

    def deleteAttributes(self):
        selection = cmds.ls(selection = True)
        for eachObject in selection:
            RMParametersManager.deleteAttributes(eachObject)

    def CheckBtnPressed(self):
        if self.ui.PrefixLineEdit.isEnabled():
            objectNamePrefix = self.ui.PrefixLineEdit.text()
        else:
            objectNamePrefix=''
        self.ui.listWidget.clear()
        eachDic = Dictionaries[self.ui.ListCBx.currentText()]
        for eachDefinition in eachDic:
            print eachDefinition
            if eachDic[eachDefinition]['Type'] == 'blendShapeDefinition':
                arrayPrefix =[]
                if eachDic[eachDefinition]['isSymetrical'] == True:
                    arrayPrefix = ["L","R"]
                else :
                    arrayPrefix = [""]
                for eachPrefix in arrayPrefix:
                    for eachBlendShape in sorted(eachDic[eachDefinition]['blendShapes']):
                        if not cmds.objExists(eachPrefix + objectNamePrefix + eachBlendShape):
                            self.ui.listWidget.addItem(eachPrefix+ objectNamePrefix + eachBlendShape)

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
    w = main()
    w.show()
