from RMPY.Tools.core.transform.QT5.ui import FormAimToPoint
import pymel.core as pm
from PySide2 import QtCore
from PySide2 import QtGui
import maya.OpenMayaUI as mui
from PySide2 import QtWidgets
from PySide2 import __version__
from shiboken2 import wrapInstance
from RMPY.Tools.QT5.ui import FormBipedRig
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from RMPY.core import transform


def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QtWidgets.QMainWindow)


class Main(MayaQWidgetDockableMixin, QtWidgets.QDialog):
    def __init__(self, NameConv=None, parent=None):
        super(Main, self).__init__(parent=getMayaWindow())
        self.ui = FormAimToPoint.Ui_aim_to_point()
        self.ui.setupUi(self)
        self.setWindowTitle('Aim to point')

        self.ui.aim_point_based_button.clicked.connect(self.aim_point_based_clicked)

    def aim_point_based_clicked(self):
        if self.ui.X_aim_axis_radio.isChecked():
            aim_axis = 'X'
        elif self.ui.Y_aim_axis_radio.isChecked():
            aim_axis = 'Y'
        elif self.ui.Z_aim_axis_radio.isChecked():
            aim_axis = 'Z'

        if self.ui.X_up_axis_radio.isChecked():
            up_axis = 'X'
        elif self.ui.Y_up_axis_radio.isChecked():
            up_axis = 'Y'
        elif self.ui.Z_up_axis_radio.isChecked():
            up_axis = 'Z'

        selection = pm.ls(selection=True)
        if len(selection) == 2:
            transform.aim_point_based(selection[0], selection[0], selection[1],
                                      aim_axis=aim_axis,
                                      up_axis=up_axis)

        if len(selection) > 2:
            transform.aim_point_based(selection[0], selection[0], selection[1], selection[2],
                                      aim_axis=aim_axis,
                                      up_axis=up_axis)


if __name__ == '__main__':
    w = Main()
    w.show()
