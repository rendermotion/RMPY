import maya.cmds as cmds
import maya.OpenMayaUI as mui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance
    from RMPY.Tools.QT5.ui  import FormRigDisplay
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide import __version__
    from shiboken import wrapInstance
    from RMPY.Tools.QT4.ui import FormRigDisplay
import maya.mel as mel
# import os
# import sys
# sys.path.append(os.path.dirname(__file__))

def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(int(ptr), QMainWindow)


class main(MayaQWidgetDockableMixin, QDialog):
    def __init__(self, parent=None):
        super(main, self).__init__(parent=getMayaWindow())
        self.ui = FormRigDisplay.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('RM Maya Rig Display')
        self.ui.ChangeJointdrawStyle.clicked.connect(self.JointDrawStyle)

    def JointDrawStyle(self):
        mel.eval("source RMJointDisplay.mel;RMChangeJointDrawStyle();")

if __name__ == '__main__':
    w = main()
    w.show()
