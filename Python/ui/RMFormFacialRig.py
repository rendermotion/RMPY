# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RMFacialRig.ui'
#
# Created: Wed Oct 05 12:20:08 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(219, 286)
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
        self.ImportFacialInterfaceBtn = QtGui.QPushButton(Form)
        self.ImportFacialInterfaceBtn.setObjectName("ImportFacialInterfaceBtn")
        self.verticalLayout.addWidget(self.ImportFacialInterfaceBtn)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.CheckBtn.setText(QtGui.QApplication.translate("Form", "Check", None, QtGui.QApplication.UnicodeUTF8))
        self.ImportFacialInterfaceBtn.setText(QtGui.QApplication.translate("Form", "Import facial interface", None, QtGui.QApplication.UnicodeUTF8))

