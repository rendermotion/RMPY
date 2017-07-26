# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GenericPropRigTool.ui'
#
# Created: Mon Oct 31 15:31:45 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide import __version__
    from shiboken import wrapInstance

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(225, 219)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.RigSelectionBtn = QPushButton(Form)
        self.RigSelectionBtn.setObjectName("RigSelectionBtn")
        self.verticalLayout_2.addWidget(self.RigSelectionBtn)
        self.RigSelectionSingleCntrlBtn = QPushButton(Form)
        self.RigSelectionSingleCntrlBtn.setObjectName("RigSelectionSingleCntrlBtn")
        self.verticalLayout_2.addWidget(self.RigSelectionSingleCntrlBtn)
        self.DeleteSimpleRigBtn = QPushButton(Form)
        self.DeleteSimpleRigBtn.setObjectName("DeleteSimpleRigBtn")
        self.verticalLayout_2.addWidget(self.DeleteSimpleRigBtn)
        self.AddNoiseGrp = QGroupBox(Form)
        self.AddNoiseGrp.setObjectName("AddNoiseGrp")
        self.verticalLayout = QVBoxLayout(self.AddNoiseGrp)
        self.verticalLayout.setObjectName("verticalLayout")
        self.LoadSelectionAsCntrlObjPushBtn = QPushButton(self.AddNoiseGrp)
        self.LoadSelectionAsCntrlObjPushBtn.setObjectName("LoadSelectionAsCntrlObjPushBtn")
        self.verticalLayout.addWidget(self.LoadSelectionAsCntrlObjPushBtn)
        self.ControllineEdit = QLineEdit(self.AddNoiseGrp)
        self.ControllineEdit.setEnabled(False)
        self.ControllineEdit.setObjectName("ControllineEdit")
        self.verticalLayout.addWidget(self.ControllineEdit)
        self.AddNoiseBtn = QPushButton(self.AddNoiseGrp)
        self.AddNoiseBtn.setObjectName("AddNoiseBtn")
        self.verticalLayout.addWidget(self.AddNoiseBtn)
        self.verticalLayout_2.addWidget(self.AddNoiseGrp)

        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QApplication.translate("Form", "Form", None, -1))
        self.RigSelectionBtn.setText(QApplication.translate("Form", "Rig selection multiple controls.", None, -1))
        self.RigSelectionSingleCntrlBtn.setText(QApplication.translate("Form", "Rig selection single control", None, -1))
        self.DeleteSimpleRigBtn.setText(QApplication.translate("Form", "Delete Rig", None, -1))
        self.AddNoiseGrp.setTitle(QApplication.translate("Form", "Control Object", None, -1))
        self.LoadSelectionAsCntrlObjPushBtn.setText(QApplication.translate("Form", "LoadSelection as Control Object", None, -1))
        self.AddNoiseBtn.setText(QApplication.translate("Form", "Add noise to selectedControl", None, -1))

