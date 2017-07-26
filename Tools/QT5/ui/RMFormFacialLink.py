# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FacialLink.ui'
#
# Created: Mon Oct 31 15:31:42 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide import __version__
    from shiboken import wrapInstance

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(277, 395)
        self.verticalLayout_3 = QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.LinkBox = QGroupBox(Form)
        self.LinkBox.setObjectName("LinkBox")
        self.verticalLayout_2 = QVBoxLayout(self.LinkBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.LinkFaceBtn = QPushButton(self.LinkBox)
        self.LinkFaceBtn.setObjectName("LinkFaceBtn")
        self.horizontalLayout_2.addWidget(self.LinkFaceBtn)
        self.LinkJawBtn = QPushButton(self.LinkBox)
        self.LinkJawBtn.setObjectName("LinkJawBtn")
        self.horizontalLayout_2.addWidget(self.LinkJawBtn)
        self.EyeSetUpBtn = QPushButton(self.LinkBox)
        self.EyeSetUpBtn.setObjectName("EyeSetUpBtn")
        self.horizontalLayout_2.addWidget(self.EyeSetUpBtn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addWidget(self.LinkBox)
        self.ImportBox = QGroupBox(Form)
        self.ImportBox.setObjectName("ImportBox")
        self.horizontalLayout_3 = QHBoxLayout(self.ImportBox)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.ImpCtrlsFacialBtn = QPushButton(self.ImportBox)
        self.ImpCtrlsFacialBtn.setObjectName("ImpCtrlsFacialBtn")
        self.horizontalLayout_3.addWidget(self.ImpCtrlsFacialBtn)
        self.ImpCtrlEyeBtn = QPushButton(self.ImportBox)
        self.ImpCtrlEyeBtn.setObjectName("ImpCtrlEyeBtn")
        self.horizontalLayout_3.addWidget(self.ImpCtrlEyeBtn)
        self.verticalLayout_3.addWidget(self.ImportBox)
        self.CheckExistance = QGroupBox(Form)
        self.CheckExistance.setObjectName("CheckExistance")
        self.verticalLayout = QVBoxLayout(self.CheckExistance)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.CheckBtn = QPushButton(self.CheckExistance)
        self.CheckBtn.setObjectName("CheckBtn")
        self.horizontalLayout.addWidget(self.CheckBtn)
        self.FaceChk = QCheckBox(self.CheckExistance)
        self.FaceChk.setObjectName("FaceChk")
        self.horizontalLayout.addWidget(self.FaceChk)
        self.EyeChk = QCheckBox(self.CheckExistance)
        self.EyeChk.setObjectName("EyeChk")
        self.horizontalLayout.addWidget(self.EyeChk)
        self.JawChk = QCheckBox(self.CheckExistance)
        self.JawChk.setObjectName("JawChk")
        self.horizontalLayout.addWidget(self.JawChk)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.NodesQList = QListWidget(self.CheckExistance)
        self.NodesQList.setObjectName("NodesQList")
        self.verticalLayout.addWidget(self.NodesQList)
        self.verticalLayout_3.addWidget(self.CheckExistance)

        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QApplication.translate("Form", "Form", None, -1))
        self.LinkBox.setTitle(QApplication.translate("Form", "Connect", None, -1))
        self.LinkFaceBtn.setText(QApplication.translate("Form", "Link Face", None, -1))
        self.LinkJawBtn.setText(QApplication.translate("Form", "Link Jaw", None, -1))
        self.EyeSetUpBtn.setText(QApplication.translate("Form", "Eye Setup", None, -1))
        self.ImportBox.setTitle(QApplication.translate("Form", "Import", None, -1))
        self.ImpCtrlsFacialBtn.setText(QApplication.translate("Form", "Facial UI", None, -1))
        self.ImpCtrlEyeBtn.setText(QApplication.translate("Form", "Eyes UI", None, -1))
        self.CheckExistance.setTitle(QApplication.translate("Form", "Check existance", None, -1))
        self.CheckBtn.setText(QApplication.translate("Form", "Check", None, -1))
        self.FaceChk.setText(QApplication.translate("Form", "Face", None, -1))
        self.EyeChk.setText(QApplication.translate("Form", "Eyes", None, -1))
        self.JawChk.setText(QApplication.translate("Form", "Jaw", None, -1))

