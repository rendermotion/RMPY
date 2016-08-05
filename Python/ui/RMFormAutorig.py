# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Autorig.ui'
#
# Created: Thu Aug 04 16:19:55 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(164, 135)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.CreateReferencePointsBtn = QtGui.QPushButton(Form)
        self.CreateReferencePointsBtn.setObjectName("CreateReferencePointsBtn")
        self.verticalLayout.addWidget(self.CreateReferencePointsBtn)
        self.MirrorSelectionBtn = QtGui.QPushButton(Form)
        self.MirrorSelectionBtn.setObjectName("MirrorSelectionBtn")
        self.verticalLayout.addWidget(self.MirrorSelectionBtn)
        self.pushButton_4 = QtGui.QPushButton(Form)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_4)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.CreateReferencePointsBtn.setText(QtGui.QApplication.translate("Form", "Create Reference Points", None, QtGui.QApplication.UnicodeUTF8))
        self.MirrorSelectionBtn.setText(QtGui.QApplication.translate("Form", "Mirror Selection", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_4.setText(QtGui.QApplication.translate("Form", "CreateRig", None, QtGui.QApplication.UnicodeUTF8))

