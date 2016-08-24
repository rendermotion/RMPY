# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Autorig.ui'
#
# Created: Tue Aug 16 15:51:40 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(144, 128)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.heightLabel = QtGui.QLabel(Form)
        self.heightLabel.setMinimumSize(QtCore.QSize(20, 0))
        self.heightLabel.setMaximumSize(QtCore.QSize(50, 16777215))
        self.heightLabel.setTextFormat(QtCore.Qt.PlainText)
        self.heightLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.heightLabel.setObjectName("heightLabel")
        self.horizontalLayout.addWidget(self.heightLabel)
        self.HeightSpnBox = QtGui.QDoubleSpinBox(Form)
        self.HeightSpnBox.setMaximum(1000000.0)
        self.HeightSpnBox.setProperty("value", 75.0)
        self.HeightSpnBox.setObjectName("HeightSpnBox")
        self.horizontalLayout.addWidget(self.HeightSpnBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.CreateReferencePointsBtn = QtGui.QPushButton(Form)
        self.CreateReferencePointsBtn.setObjectName("CreateReferencePointsBtn")
        self.verticalLayout.addWidget(self.CreateReferencePointsBtn)
        self.MirrorSelectionBtn = QtGui.QPushButton(Form)
        self.MirrorSelectionBtn.setObjectName("MirrorSelectionBtn")
        self.verticalLayout.addWidget(self.MirrorSelectionBtn)
        self.CreateRigBtn = QtGui.QPushButton(Form)
        self.CreateRigBtn.setObjectName("CreateRigBtn")
        self.verticalLayout.addWidget(self.CreateRigBtn)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.heightLabel.setText(QtGui.QApplication.translate("Form", "Height", None, QtGui.QApplication.UnicodeUTF8))
        self.CreateReferencePointsBtn.setText(QtGui.QApplication.translate("Form", "Create Reference Points", None, QtGui.QApplication.UnicodeUTF8))
        self.MirrorSelectionBtn.setText(QtGui.QApplication.translate("Form", "Mirror Selection", None, QtGui.QApplication.UnicodeUTF8))
        self.CreateRigBtn.setText(QtGui.QApplication.translate("Form", "CreateRig", None, QtGui.QApplication.UnicodeUTF8))

