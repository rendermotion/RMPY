import maya.OpenMayaUI as mui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import pymel.core as pm
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from RMPY.core import config
from PySide6 import __version__
from shiboken6 import wrapInstance
from RMPY.Tools.QT6.ui import FormNameConvention
from RMPY.Tools.QT6.ui import FormSmoothSurfaces
from RMPY import nameConvention
from RMPY import RMRigTools
from RMPY.snippets import locator_at_average
from PySide6 import QtCore


def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(int(ptr), QMainWindow)


class Main(MayaQWidgetDockableMixin, QDialog):
    def __init__(self, parent=None):
        self.name_convention = nameConvention.NameConvention()
        super(Main, self).__init__(parent=getMayaWindow())
        self.ui = FormNameConvention.Ui_Form()
        self.system_backlog = config.default_reference_system_name
        self.name_backlog = 'default'
        self.ui.setupUi(self)
        self.ui.name_lineEdit.setText(self.name_backlog)
        self.setWindowTitle('Rename Tool')
        self.ui.side_comboBox.addItems(self.name_convention.validation['side'])
        self.ui.system_lineEdit.setText(config.default_reference_system_name)
        self.ui.system_lineEdit.setDisabled(True)
        object_type_list = ['auto']
        object_type_list.extend(self.name_convention.validation['objectType'])
        self.ui.objectType_comboBox.addItems(object_type_list)

    @QtCore.Slot()
    def on_rename_button_clicked(self):
        selection = pm.ls(selection=True)
        # for index, each in enumerate(selection):
        side = self.ui.side_comboBox.currentText()
        system_name = self.ui.system_lineEdit.text()
        name = self.ui.name_lineEdit.text()
        objectType = self.ui.objectType_comboBox.currentText()
        # each.full_name for each in selection[]
        if objectType == 'auto':
            self.name_convention.rename_name_in_format(*selection, side=side, system=system_name, name=name,
                                                       useName=self.ui.use_name_chkBox.isChecked())

        else:
            self.name_convention.rename_name_in_format(*selection, side=side, system=system_name, name=name,
                                                       useName=self.ui.use_name_chkBox.isChecked(),
                                                       objectType=objectType)
            print('second')

        # name_conv.rename_name_in_format(each, side=side, system=system_name, name='shoe{}'.format(chr(65+index)))
        # name_conv.rename_name_in_format(each, side=side, system=system_name, name='finger{}'.format(chr(65 + index)))

    @QtCore.Slot()
    def on_default_system_chkBox_stateChanged(self):
        if self.ui.default_system_chkBox.isChecked():
            self.system_backlog = self.ui.system_lineEdit.text()
            self.ui.system_lineEdit.setText(config.default_reference_system_name)
            self.ui.system_lineEdit.setDisabled(True)
        else:
            self.ui.system_lineEdit.setText(self.system_backlog)
            self.ui.system_lineEdit.setDisabled(False)

    @QtCore.Slot()
    def on_use_name_chkBox_stateChanged(self):
        if self.ui.use_name_chkBox.isChecked():
            self.name_backlog = self.ui.name_lineEdit.text()
            self.ui.name_lineEdit.setText('--using current name of object--')
            self.ui.name_lineEdit.setDisabled(True)
        else:
            self.ui.name_lineEdit.setText(self.name_backlog)
            self.ui.name_lineEdit.setDisabled(False)

    @QtCore.Slot()
    def on_side_push_button_clicked(self):
        selection = pm.ls(selection=True)
        side = self.ui.side_comboBox.currentText()
        for each in selection:
            self.name_convention.rename_name_in_format(each, side=side,
                                                       system=self.name_convention.get_from_name(each, 'system'),
                                                       useName=True)
        print('pushed')

    @QtCore.Slot()
    def on_name_button_clicked(self):
        pass

    @QtCore.Slot()
    def on_system_button_clicked(self):
        pass

    @QtCore.Slot()
    def on_object_type_button_clicked(self):
        pass


if __name__ == '__main__':
    w = Main()
    w.show()
