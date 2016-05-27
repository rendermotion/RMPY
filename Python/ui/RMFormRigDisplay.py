# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RMRigDisplay.ui'
#
# Created: Thu May 26 14:30:12 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(236, 179)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ChangeJointdrawStyle = QtGui.QPushButton(Form)
        self.ChangeJointdrawStyle.setMaximumSize(QtCore.QSize(100, 30))
        self.ChangeJointdrawStyle.setObjectName("ChangeJointdrawStyle")
        self.horizontalLayout.addWidget(self.ChangeJointdrawStyle)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.ChangeJointdrawStyle.setText(QtGui.QApplication.translate("Form", "Joint DrawStyle", None, QtGui.QApplication.UnicodeUTF8))

