# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GenericPropRigTool.ui'
#
# Created: Wed Oct 19 13:43:48 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(225, 219)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.RigSelectionBtn = QtGui.QPushButton(Form)
        self.RigSelectionBtn.setObjectName("RigSelectionBtn")
        self.verticalLayout_2.addWidget(self.RigSelectionBtn)
        self.RigSelectionSingleCntrlBtn = QtGui.QPushButton(Form)
        self.RigSelectionSingleCntrlBtn.setObjectName("RigSelectionSingleCntrlBtn")
        self.verticalLayout_2.addWidget(self.RigSelectionSingleCntrlBtn)
        self.DeleteSimpleRigBtn = QtGui.QPushButton(Form)
        self.DeleteSimpleRigBtn.setObjectName("DeleteSimpleRigBtn")
        self.verticalLayout_2.addWidget(self.DeleteSimpleRigBtn)
        self.AddNoiseGrp = QtGui.QGroupBox(Form)
        self.AddNoiseGrp.setObjectName("AddNoiseGrp")
        self.verticalLayout = QtGui.QVBoxLayout(self.AddNoiseGrp)
        self.verticalLayout.setObjectName("verticalLayout")
        self.LoadSelectionAsCntrlObjPushBtn = QtGui.QPushButton(self.AddNoiseGrp)
        self.LoadSelectionAsCntrlObjPushBtn.setObjectName("LoadSelectionAsCntrlObjPushBtn")
        self.verticalLayout.addWidget(self.LoadSelectionAsCntrlObjPushBtn)
        self.ControllineEdit = QtGui.QLineEdit(self.AddNoiseGrp)
        self.ControllineEdit.setEnabled(False)
        self.ControllineEdit.setObjectName("ControllineEdit")
        self.verticalLayout.addWidget(self.ControllineEdit)
        self.AddNoiseBtn = QtGui.QPushButton(self.AddNoiseGrp)
        self.AddNoiseBtn.setObjectName("AddNoiseBtn")
        self.verticalLayout.addWidget(self.AddNoiseBtn)
        self.verticalLayout_2.addWidget(self.AddNoiseGrp)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.RigSelectionBtn.setText(QtGui.QApplication.translate("Form", "Rig selection multiple controls.", None, QtGui.QApplication.UnicodeUTF8))
        self.RigSelectionSingleCntrlBtn.setText(QtGui.QApplication.translate("Form", "Rig selection single control", None, QtGui.QApplication.UnicodeUTF8))
        self.DeleteSimpleRigBtn.setText(QtGui.QApplication.translate("Form", "Delete Rig", None, QtGui.QApplication.UnicodeUTF8))
        self.AddNoiseGrp.setTitle(QtGui.QApplication.translate("Form", "Control Object", None, QtGui.QApplication.UnicodeUTF8))
        self.LoadSelectionAsCntrlObjPushBtn.setText(QtGui.QApplication.translate("Form", "LoadSelection as Control Object", None, QtGui.QApplication.UnicodeUTF8))
        self.AddNoiseBtn.setText(QtGui.QApplication.translate("Form", "Add noise to selectedControl", None, QtGui.QApplication.UnicodeUTF8))

