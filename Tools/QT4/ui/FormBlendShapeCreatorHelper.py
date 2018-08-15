# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_BlendShapeCreatorHelper.ui'
#
# Created: Wed Mar 21 21:43:33 2018
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(193, 252)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.LoadObjectBtn = QtGui.QPushButton(Form)
        self.LoadObjectBtn.setObjectName("LoadObjectBtn")
        self.verticalLayout.addWidget(self.LoadObjectBtn)
        self.ObjectLbl = QtGui.QLabel(Form)
        self.ObjectLbl.setText("")
        self.ObjectLbl.setObjectName("ObjectLbl")
        self.verticalLayout.addWidget(self.ObjectLbl)
        self.FlipWeightsBtn = QtGui.QPushButton(Form)
        self.FlipWeightsBtn.setObjectName("FlipWeightsBtn")
        self.verticalLayout.addWidget(self.FlipWeightsBtn)
        self.listWidget = QtGui.QListWidget(Form)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.LinkSelected = QtGui.QPushButton(Form)
        self.LinkSelected.setObjectName("LinkSelected")
        self.verticalLayout.addWidget(self.LinkSelected)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.LoadObjectBtn.setText(QtGui.QApplication.translate("Form", "Load Selection", None, QtGui.QApplication.UnicodeUTF8))
        self.FlipWeightsBtn.setText(QtGui.QApplication.translate("Form", "Flip Weights", None, QtGui.QApplication.UnicodeUTF8))
        self.LinkSelected.setText(QtGui.QApplication.translate("Form", "Extract_Shapes", None, QtGui.QApplication.UnicodeUTF8))

