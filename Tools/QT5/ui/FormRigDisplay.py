# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_RigDisplay.ui'
#
# Created: Tue Mar 15 20:23:49 2022
#      by: PySide6-uic  running on PySide6 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(236, 179)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ChangeJointdrawStyle = QtWidgets.QPushButton(Form)
        self.ChangeJointdrawStyle.setMaximumSize(QtCore.QSize(100, 30))
        self.ChangeJointdrawStyle.setObjectName("ChangeJointdrawStyle")
        self.horizontalLayout.addWidget(self.ChangeJointdrawStyle)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.ChangeJointdrawStyle.setText(QtWidgets.QApplication.translate("Form", "Joint DrawStyle", None, -1))

