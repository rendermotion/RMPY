# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_BlendShapeCreatorHelper.ui'
#
# Created: Tue Mar 15 20:23:49 2022
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(193, 252)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.LoadObjectBtn = QtWidgets.QPushButton(Form)
        self.LoadObjectBtn.setObjectName("LoadObjectBtn")
        self.verticalLayout.addWidget(self.LoadObjectBtn)
        self.ObjectLbl = QtWidgets.QLabel(Form)
        self.ObjectLbl.setText("")
        self.ObjectLbl.setObjectName("ObjectLbl")
        self.verticalLayout.addWidget(self.ObjectLbl)
        self.FlipWeightsBtn = QtWidgets.QPushButton(Form)
        self.FlipWeightsBtn.setObjectName("FlipWeightsBtn")
        self.verticalLayout.addWidget(self.FlipWeightsBtn)
        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.LinkSelected = QtWidgets.QPushButton(Form)
        self.LinkSelected.setObjectName("LinkSelected")
        self.verticalLayout.addWidget(self.LinkSelected)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.LoadObjectBtn.setText(QtWidgets.QApplication.translate("Form", "Load Selection", None, -1))
        self.FlipWeightsBtn.setText(QtWidgets.QApplication.translate("Form", "Flip Weights", None, -1))
        self.LinkSelected.setText(QtWidgets.QApplication.translate("Form", "Extract_Shapes", None, -1))

