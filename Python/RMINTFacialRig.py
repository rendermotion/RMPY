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

    def CheckBtnPressed(self):
        pass

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
