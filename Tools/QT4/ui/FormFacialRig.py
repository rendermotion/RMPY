# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_FacialRig.ui'
#
# Created: Wed Nov 01 23:16:45 2017
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(236, 323)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.CheckBtn = QtGui.QPushButton(Form)
        self.CheckBtn.setMaximumSize(QtCore.QSize(70, 16777215))
        self.CheckBtn.setObjectName("CheckBtn")
        self.horizontalLayout.addWidget(self.CheckBtn)
        self.ListCBx = QtGui.QComboBox(Form)
        self.ListCBx.setObjectName("ListCBx")
        self.horizontalLayout.addWidget(self.ListCBx)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.listWidget = QtGui.QListWidget(Form)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.LinkAllBtn = QtGui.QPushButton(Form)
        self.LinkAllBtn.setObjectName("LinkAllBtn")
        self.horizontalLayout_2.addWidget(self.LinkAllBtn)
        self.LinkSelectedBtn = QtGui.QPushButton(Form)
        self.LinkSelectedBtn.setObjectName("LinkSelectedBtn")
        self.horizontalLayout_2.addWidget(self.LinkSelectedBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.ImportFacialInterfaceBtn = QtGui.QPushButton(self.groupBox)
        self.ImportFacialInterfaceBtn.setObjectName("ImportFacialInterfaceBtn")
        self.verticalLayout_2.addWidget(self.ImportFacialInterfaceBtn)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.UsePrefixChkBx = QtGui.QCheckBox(self.groupBox)
        self.UsePrefixChkBx.setObjectName("UsePrefixChkBx")
        self.horizontalLayout_3.addWidget(self.UsePrefixChkBx)
        self.PrefixLineEdit = QtGui.QLineEdit(self.groupBox)
        self.PrefixLineEdit.setEnabled(False)
        self.PrefixLineEdit.setObjectName("PrefixLineEdit")
        self.horizontalLayout_3.addWidget(self.PrefixLineEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.renameRightBtn = QtGui.QPushButton(self.groupBox)
        self.renameRightBtn.setObjectName("renameRightBtn")
        self.horizontalLayout_4.addWidget(self.renameRightBtn)
        self.createMissingBtn = QtGui.QPushButton(self.groupBox)
        self.createMissingBtn.setObjectName("createMissingBtn")
        self.horizontalLayout_4.addWidget(self.createMissingBtn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.DeleteAttributesBtn = QtGui.QPushButton(self.groupBox)
        self.DeleteAttributesBtn.setObjectName("DeleteAttributesBtn")
        self.verticalLayout_2.addWidget(self.DeleteAttributesBtn)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.CheckBtn.setText(QtGui.QApplication.translate("Form", "Check", None, QtGui.QApplication.UnicodeUTF8))
        self.LinkAllBtn.setText(QtGui.QApplication.translate("Form", "Link all", None, QtGui.QApplication.UnicodeUTF8))
        self.LinkSelectedBtn.setText(QtGui.QApplication.translate("Form", "Link selected", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Form", "Generic Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.ImportFacialInterfaceBtn.setText(QtGui.QApplication.translate("Form", "Import facial interface", None, QtGui.QApplication.UnicodeUTF8))
        self.UsePrefixChkBx.setText(QtGui.QApplication.translate("Form", "UsePrefix", None, QtGui.QApplication.UnicodeUTF8))
        self.renameRightBtn.setText(QtGui.QApplication.translate("Form", "Rename right", None, QtGui.QApplication.UnicodeUTF8))
        self.createMissingBtn.setText(QtGui.QApplication.translate("Form", "CreateMissingAsProxy", None, QtGui.QApplication.UnicodeUTF8))
        self.DeleteAttributesBtn.setText(QtGui.QApplication.translate("Form", "Delete custom attributes", None, QtGui.QApplication.UnicodeUTF8))

