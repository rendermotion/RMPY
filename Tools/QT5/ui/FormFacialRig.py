# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_FacialRig.ui'
#
# Created: Tue Mar 15 20:23:49 2022
#      by: PySide6-uic  running on PySide6 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(236, 323)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.CheckBtn = QtWidgets.QPushButton(Form)
        self.CheckBtn.setMaximumSize(QtCore.QSize(70, 16777215))
        self.CheckBtn.setObjectName("CheckBtn")
        self.horizontalLayout.addWidget(self.CheckBtn)
        self.ListCBx = QtWidgets.QComboBox(Form)
        self.ListCBx.setObjectName("ListCBx")
        self.horizontalLayout.addWidget(self.ListCBx)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.LinkAllBtn = QtWidgets.QPushButton(Form)
        self.LinkAllBtn.setObjectName("LinkAllBtn")
        self.horizontalLayout_2.addWidget(self.LinkAllBtn)
        self.LinkSelectedBtn = QtWidgets.QPushButton(Form)
        self.LinkSelectedBtn.setObjectName("LinkSelectedBtn")
        self.horizontalLayout_2.addWidget(self.LinkSelectedBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.ImportFacialInterfaceBtn = QtWidgets.QPushButton(self.groupBox)
        self.ImportFacialInterfaceBtn.setObjectName("ImportFacialInterfaceBtn")
        self.verticalLayout_2.addWidget(self.ImportFacialInterfaceBtn)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.UsePrefixChkBx = QtWidgets.QCheckBox(self.groupBox)
        self.UsePrefixChkBx.setObjectName("UsePrefixChkBx")
        self.horizontalLayout_3.addWidget(self.UsePrefixChkBx)
        self.PrefixLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.PrefixLineEdit.setEnabled(False)
        self.PrefixLineEdit.setObjectName("PrefixLineEdit")
        self.horizontalLayout_3.addWidget(self.PrefixLineEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.renameRightBtn = QtWidgets.QPushButton(self.groupBox)
        self.renameRightBtn.setObjectName("renameRightBtn")
        self.horizontalLayout_4.addWidget(self.renameRightBtn)
        self.createMissingBtn = QtWidgets.QPushButton(self.groupBox)
        self.createMissingBtn.setObjectName("createMissingBtn")
        self.horizontalLayout_4.addWidget(self.createMissingBtn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.DeleteAttributesBtn = QtWidgets.QPushButton(self.groupBox)
        self.DeleteAttributesBtn.setObjectName("DeleteAttributesBtn")
        self.verticalLayout_2.addWidget(self.DeleteAttributesBtn)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.CheckBtn.setText(QtWidgets.QApplication.translate("Form", "Check", None, -1))
        self.LinkAllBtn.setText(QtWidgets.QApplication.translate("Form", "Link all", None, -1))
        self.LinkSelectedBtn.setText(QtWidgets.QApplication.translate("Form", "Link selected", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("Form", "Generic Tools", None, -1))
        self.ImportFacialInterfaceBtn.setText(QtWidgets.QApplication.translate("Form", "Import facial interface", None, -1))
        self.UsePrefixChkBx.setText(QtWidgets.QApplication.translate("Form", "UsePrefix", None, -1))
        self.renameRightBtn.setText(QtWidgets.QApplication.translate("Form", "Rename right", None, -1))
        self.createMissingBtn.setText(QtWidgets.QApplication.translate("Form", "CreateMissingAsProxy", None, -1))
        self.DeleteAttributesBtn.setText(QtWidgets.QApplication.translate("Form", "Delete custom attributes", None, -1))

