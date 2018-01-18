# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_FacialLink.ui'
#
# Created: Wed Nov 01 23:16:45 2017
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(277, 395)
        self.verticalLayout_3 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.LinkBox = QtGui.QGroupBox(Form)
        self.LinkBox.setObjectName("LinkBox")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.LinkBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.LinkFaceBtn = QtGui.QPushButton(self.LinkBox)
        self.LinkFaceBtn.setObjectName("LinkFaceBtn")
        self.horizontalLayout_2.addWidget(self.LinkFaceBtn)
        self.LinkJawBtn = QtGui.QPushButton(self.LinkBox)
        self.LinkJawBtn.setObjectName("LinkJawBtn")
        self.horizontalLayout_2.addWidget(self.LinkJawBtn)
        self.EyeSetUpBtn = QtGui.QPushButton(self.LinkBox)
        self.EyeSetUpBtn.setObjectName("EyeSetUpBtn")
        self.horizontalLayout_2.addWidget(self.EyeSetUpBtn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addWidget(self.LinkBox)
        self.ImportBox = QtGui.QGroupBox(Form)
        self.ImportBox.setObjectName("ImportBox")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.ImportBox)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.ImpCtrlsFacialBtn = QtGui.QPushButton(self.ImportBox)
        self.ImpCtrlsFacialBtn.setObjectName("ImpCtrlsFacialBtn")
        self.horizontalLayout_3.addWidget(self.ImpCtrlsFacialBtn)
        self.ImpCtrlEyeBtn = QtGui.QPushButton(self.ImportBox)
        self.ImpCtrlEyeBtn.setObjectName("ImpCtrlEyeBtn")
        self.horizontalLayout_3.addWidget(self.ImpCtrlEyeBtn)
        self.verticalLayout_3.addWidget(self.ImportBox)
        self.CheckExistance = QtGui.QGroupBox(Form)
        self.CheckExistance.setObjectName("CheckExistance")
        self.verticalLayout = QtGui.QVBoxLayout(self.CheckExistance)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.CheckBtn = QtGui.QPushButton(self.CheckExistance)
        self.CheckBtn.setObjectName("CheckBtn")
        self.horizontalLayout.addWidget(self.CheckBtn)
        self.FaceChk = QtGui.QCheckBox(self.CheckExistance)
        self.FaceChk.setObjectName("FaceChk")
        self.horizontalLayout.addWidget(self.FaceChk)
        self.EyeChk = QtGui.QCheckBox(self.CheckExistance)
        self.EyeChk.setObjectName("EyeChk")
        self.horizontalLayout.addWidget(self.EyeChk)
        self.JawChk = QtGui.QCheckBox(self.CheckExistance)
        self.JawChk.setObjectName("JawChk")
        self.horizontalLayout.addWidget(self.JawChk)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.NodesQList = QtGui.QListWidget(self.CheckExistance)
        self.NodesQList.setObjectName("NodesQList")
        self.verticalLayout.addWidget(self.NodesQList)
        self.verticalLayout_3.addWidget(self.CheckExistance)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.LinkBox.setTitle(QtGui.QApplication.translate("Form", "Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.LinkFaceBtn.setText(QtGui.QApplication.translate("Form", "Link Face", None, QtGui.QApplication.UnicodeUTF8))
        self.LinkJawBtn.setText(QtGui.QApplication.translate("Form", "Link Jaw", None, QtGui.QApplication.UnicodeUTF8))
        self.EyeSetUpBtn.setText(QtGui.QApplication.translate("Form", "Eye Setup", None, QtGui.QApplication.UnicodeUTF8))
        self.ImportBox.setTitle(QtGui.QApplication.translate("Form", "Import", None, QtGui.QApplication.UnicodeUTF8))
        self.ImpCtrlsFacialBtn.setText(QtGui.QApplication.translate("Form", "Facial UI", None, QtGui.QApplication.UnicodeUTF8))
        self.ImpCtrlEyeBtn.setText(QtGui.QApplication.translate("Form", "Eyes UI", None, QtGui.QApplication.UnicodeUTF8))
        self.CheckExistance.setTitle(QtGui.QApplication.translate("Form", "Check existance", None, QtGui.QApplication.UnicodeUTF8))
        self.CheckBtn.setText(QtGui.QApplication.translate("Form", "Check", None, QtGui.QApplication.UnicodeUTF8))
        self.FaceChk.setText(QtGui.QApplication.translate("Form", "Face", None, QtGui.QApplication.UnicodeUTF8))
        self.EyeChk.setText(QtGui.QApplication.translate("Form", "Eyes", None, QtGui.QApplication.UnicodeUTF8))
        self.JawChk.setText(QtGui.QApplication.translate("Form", "Jaw", None, QtGui.QApplication.UnicodeUTF8))

