# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_GenericPropRig.ui'
#
# Created: Wed Nov 01 23:16:45 2017
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(225, 219)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.RigSelectionBtn = QtWidgets.QPushButton(Form)
        self.RigSelectionBtn.setObjectName("RigSelectionBtn")
        self.verticalLayout_2.addWidget(self.RigSelectionBtn)
        self.RigSelectionSingleCntrlBtn = QtWidgets.QPushButton(Form)
        self.RigSelectionSingleCntrlBtn.setObjectName("RigSelectionSingleCntrlBtn")
        self.verticalLayout_2.addWidget(self.RigSelectionSingleCntrlBtn)
        self.DeleteSimpleRigBtn = QtWidgets.QPushButton(Form)
        self.DeleteSimpleRigBtn.setObjectName("DeleteSimpleRigBtn")
        self.verticalLayout_2.addWidget(self.DeleteSimpleRigBtn)
        self.AddNoiseGrp = QtWidgets.QGroupBox(Form)
        self.AddNoiseGrp.setObjectName("AddNoiseGrp")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.AddNoiseGrp)
        self.verticalLayout.setObjectName("verticalLayout")
        self.LoadSelectionAsCntrlObjPushBtn = QtWidgets.QPushButton(self.AddNoiseGrp)
        self.LoadSelectionAsCntrlObjPushBtn.setObjectName("LoadSelectionAsCntrlObjPushBtn")
        self.verticalLayout.addWidget(self.LoadSelectionAsCntrlObjPushBtn)
        self.ControllineEdit = QtWidgets.QLineEdit(self.AddNoiseGrp)
        self.ControllineEdit.setEnabled(False)
        self.ControllineEdit.setObjectName("ControllineEdit")
        self.verticalLayout.addWidget(self.ControllineEdit)
        self.AddNoiseBtn = QtWidgets.QPushButton(self.AddNoiseGrp)
        self.AddNoiseBtn.setObjectName("AddNoiseBtn")
        self.verticalLayout.addWidget(self.AddNoiseBtn)
        self.verticalLayout_2.addWidget(self.AddNoiseGrp)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.RigSelectionBtn.setText(QtWidgets.QApplication.translate("Form", "Rig selection multiple controls.", None, -1))
        self.RigSelectionSingleCntrlBtn.setText(QtWidgets.QApplication.translate("Form", "Rig selection single control", None, -1))
        self.DeleteSimpleRigBtn.setText(QtWidgets.QApplication.translate("Form", "Delete Rig", None, -1))
        self.AddNoiseGrp.setTitle(QtWidgets.QApplication.translate("Form", "Control Object", None, -1))
        self.LoadSelectionAsCntrlObjPushBtn.setText(QtWidgets.QApplication.translate("Form", "LoadSelection as Control Object", None, -1))
        self.AddNoiseBtn.setText(QtWidgets.QApplication.translate("Form", "Add noise to selectedControl", None, -1))

