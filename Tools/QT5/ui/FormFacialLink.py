# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_FacialLink.ui'
#
# Created: Thu Sep  9 23:13:52 2021
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(277, 395)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.LinkBox = QtWidgets.QGroupBox(Form)
        self.LinkBox.setObjectName("LinkBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.LinkBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.LinkFaceBtn = QtWidgets.QPushButton(self.LinkBox)
        self.LinkFaceBtn.setObjectName("LinkFaceBtn")
        self.horizontalLayout_2.addWidget(self.LinkFaceBtn)
        self.LinkJawBtn = QtWidgets.QPushButton(self.LinkBox)
        self.LinkJawBtn.setObjectName("LinkJawBtn")
        self.horizontalLayout_2.addWidget(self.LinkJawBtn)
        self.EyeSetUpBtn = QtWidgets.QPushButton(self.LinkBox)
        self.EyeSetUpBtn.setObjectName("EyeSetUpBtn")
        self.horizontalLayout_2.addWidget(self.EyeSetUpBtn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addWidget(self.LinkBox)
        self.ImportBox = QtWidgets.QGroupBox(Form)
        self.ImportBox.setObjectName("ImportBox")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.ImportBox)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.ImpCtrlsFacialBtn = QtWidgets.QPushButton(self.ImportBox)
        self.ImpCtrlsFacialBtn.setObjectName("ImpCtrlsFacialBtn")
        self.horizontalLayout_3.addWidget(self.ImpCtrlsFacialBtn)
        self.ImpCtrlEyeBtn = QtWidgets.QPushButton(self.ImportBox)
        self.ImpCtrlEyeBtn.setObjectName("ImpCtrlEyeBtn")
        self.horizontalLayout_3.addWidget(self.ImpCtrlEyeBtn)
        self.verticalLayout_3.addWidget(self.ImportBox)
        self.CheckExistance = QtWidgets.QGroupBox(Form)
        self.CheckExistance.setObjectName("CheckExistance")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.CheckExistance)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.CheckBtn = QtWidgets.QPushButton(self.CheckExistance)
        self.CheckBtn.setObjectName("CheckBtn")
        self.horizontalLayout.addWidget(self.CheckBtn)
        self.FaceChk = QtWidgets.QCheckBox(self.CheckExistance)
        self.FaceChk.setObjectName("FaceChk")
        self.horizontalLayout.addWidget(self.FaceChk)
        self.EyeChk = QtWidgets.QCheckBox(self.CheckExistance)
        self.EyeChk.setObjectName("EyeChk")
        self.horizontalLayout.addWidget(self.EyeChk)
        self.JawChk = QtWidgets.QCheckBox(self.CheckExistance)
        self.JawChk.setObjectName("JawChk")
        self.horizontalLayout.addWidget(self.JawChk)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.NodesQList = QtWidgets.QListWidget(self.CheckExistance)
        self.NodesQList.setObjectName("NodesQList")
        self.verticalLayout.addWidget(self.NodesQList)
        self.verticalLayout_3.addWidget(self.CheckExistance)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.LinkBox.setTitle(QtWidgets.QApplication.translate("Form", "Connect", None, -1))
        self.LinkFaceBtn.setText(QtWidgets.QApplication.translate("Form", "Link Face", None, -1))
        self.LinkJawBtn.setText(QtWidgets.QApplication.translate("Form", "Link Jaw", None, -1))
        self.EyeSetUpBtn.setText(QtWidgets.QApplication.translate("Form", "Eye Setup", None, -1))
        self.ImportBox.setTitle(QtWidgets.QApplication.translate("Form", "Import", None, -1))
        self.ImpCtrlsFacialBtn.setText(QtWidgets.QApplication.translate("Form", "Facial UI", None, -1))
        self.ImpCtrlEyeBtn.setText(QtWidgets.QApplication.translate("Form", "Eyes UI", None, -1))
        self.CheckExistance.setTitle(QtWidgets.QApplication.translate("Form", "Check existance", None, -1))
        self.CheckBtn.setText(QtWidgets.QApplication.translate("Form", "Check", None, -1))
        self.FaceChk.setText(QtWidgets.QApplication.translate("Form", "Face", None, -1))
        self.EyeChk.setText(QtWidgets.QApplication.translate("Form", "Eyes", None, -1))
        self.JawChk.setText(QtWidgets.QApplication.translate("Form", "Jaw", None, -1))

