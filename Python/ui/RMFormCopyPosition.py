# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RMCopyPosition.ui'
#
# Created: Mon Sep 26 14:23:46 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(239, 136)
        self.verticalLayoutWidget = QtGui.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 221, 121))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.DiskCache = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.DiskCache.setChecked(True)
        self.DiskCache.setObjectName("DiskCache")
        self.verticalLayout.addWidget(self.DiskCache)
        self.ResetTransformBtn = QtGui.QPushButton(self.verticalLayoutWidget)
        self.ResetTransformBtn.setObjectName("ResetTransformBtn")
        self.verticalLayout.addWidget(self.ResetTransformBtn)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.GetTransformBtn = QtGui.QPushButton(self.verticalLayoutWidget)
        self.GetTransformBtn.setObjectName("GetTransformBtn")
        self.horizontalLayout.addWidget(self.GetTransformBtn)
        self.SaveTransformsBtn = QtGui.QPushButton(self.verticalLayoutWidget)
        self.SaveTransformsBtn.setObjectName("SaveTransformsBtn")
        self.horizontalLayout.addWidget(self.SaveTransformsBtn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.SetTransformBtn = QtGui.QPushButton(self.verticalLayoutWidget)
        self.SetTransformBtn.setObjectName("SetTransformBtn")
        self.horizontalLayout_2.addWidget(self.SetTransformBtn)
        self.LoadTransformsBtn = QtGui.QPushButton(self.verticalLayoutWidget)
        self.LoadTransformsBtn.setObjectName("LoadTransformsBtn")
        self.horizontalLayout_2.addWidget(self.LoadTransformsBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.DiskCache.setText(QtGui.QApplication.translate("Form", "AutoSave to Disk", None, QtGui.QApplication.UnicodeUTF8))
        self.ResetTransformBtn.setText(QtGui.QApplication.translate("Form", "Reset Transforms", None, QtGui.QApplication.UnicodeUTF8))
        self.GetTransformBtn.setText(QtGui.QApplication.translate("Form", "Get Transforms", None, QtGui.QApplication.UnicodeUTF8))
        self.SaveTransformsBtn.setText(QtGui.QApplication.translate("Form", "Save Transforms", None, QtGui.QApplication.UnicodeUTF8))
        self.SetTransformBtn.setText(QtGui.QApplication.translate("Form", "Set Transforms", None, QtGui.QApplication.UnicodeUTF8))
        self.LoadTransformsBtn.setText(QtGui.QApplication.translate("Form", "Load Transforms", None, QtGui.QApplication.UnicodeUTF8))

