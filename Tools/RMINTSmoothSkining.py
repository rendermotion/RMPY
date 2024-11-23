import maya.cmds as cmds
import maya.OpenMayaUI as mui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import pymel.core as pm
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2 import __version__
from shiboken2 import wrapInstance
from RMPY.Tools.QT5.ui import FormRigTools_old

from RMPY import RMRigTools
from RMPY.snippets import locator_at_average


def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(int(ptr), QMainWindow)


class Main(MayaQWidgetDockableMixin, QDialog):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent=getMayaWindow())
        self.rigTools = RMRigTools.RMRigTools()
        self.ui = FormRigTools.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('Smooth skinning')
        push_button = QPushButton()
        easing_curve = QEasingCurve()
        self.ui.verticalLayout_4.addWidget(easing_curve)


if __name__ == '__main__':
    w = Main()
    w.show()
