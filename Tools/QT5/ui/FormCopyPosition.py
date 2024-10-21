# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_CopyPosition.ui'
#
# Created: Tue Mar 15 20:23:49 2022
#      by: PySide6-uic  running on PySide6 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(239, 136)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 221, 121))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.DiskCache = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.DiskCache.setChecked(True)
        self.DiskCache.setObjectName("DiskCache")
        self.verticalLayout.addWidget(self.DiskCache)
        self.ResetTransformBtn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.ResetTransformBtn.setObjectName("ResetTransformBtn")
        self.verticalLayout.addWidget(self.ResetTransformBtn)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.GetTransformBtn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.GetTransformBtn.setObjectName("GetTransformBtn")
        self.horizontalLayout.addWidget(self.GetTransformBtn)
        self.SaveTransformsBtn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.SaveTransformsBtn.setObjectName("SaveTransformsBtn")
        self.horizontalLayout.addWidget(self.SaveTransformsBtn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.SetTransformBtn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.SetTransformBtn.setObjectName("SetTransformBtn")
        self.horizontalLayout_2.addWidget(self.SetTransformBtn)
        self.LoadTransformsBtn = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.LoadTransformsBtn.setObjectName("LoadTransformsBtn")
        self.horizontalLayout_2.addWidget(self.LoadTransformsBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.DiskCache.setText(QtWidgets.QApplication.translate("Form", "AutoSave to Disk", None, -1))
        self.ResetTransformBtn.setText(QtWidgets.QApplication.translate("Form", "Reset Transforms", None, -1))
        self.GetTransformBtn.setText(QtWidgets.QApplication.translate("Form", "Get Transforms", None, -1))
        self.SaveTransformsBtn.setText(QtWidgets.QApplication.translate("Form", "Save Transforms", None, -1))
        self.SetTransformBtn.setText(QtWidgets.QApplication.translate("Form", "Set Transforms", None, -1))
        self.LoadTransformsBtn.setText(QtWidgets.QApplication.translate("Form", "Load Transforms", None, -1))

