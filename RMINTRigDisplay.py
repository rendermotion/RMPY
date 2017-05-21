import maya.cmds as cmds
import maya.OpenMayaUI as mui
from PySide import QtGui, QtCore
from shiboken import wrapInstance
import maya.mel as mel
# import os
# import sys
# sys.path.append(os.path.dirname(__file__))

from RMPY.ui import RMFormRigDisplay

reload(RMFormRigDisplay)


def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QtGui.QMainWindow)


class Main(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent=getMayaWindow())
        self.ui = RMFormRigDisplay.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('RM Maya Rig Display')
        self.ui.ChangeJointdrawStyle.clicked.connect(self.JointDrawStyle)

    def JointDrawStyle(self):
        mel.eval("source RMJointDisplay.mel;RMChangeJointDrawStyle();")


if __name__ == '__main__':
    w = Main()
    w.show()
