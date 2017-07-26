# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RMCopyPosition.ui'
#
# Created: Mon Oct 31 15:31:41 2016
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
        Form.resize(239, 136)
        self.verticalLayoutWidget = QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 221, 121))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.DiskCache = QCheckBox(self.verticalLayoutWidget)
        self.DiskCache.setChecked(True)
        self.DiskCache.setObjectName("DiskCache")
        self.verticalLayout.addWidget(self.DiskCache)
        self.ResetTransformBtn = QPushButton(self.verticalLayoutWidget)
        self.ResetTransformBtn.setObjectName("ResetTransformBtn")
        self.verticalLayout.addWidget(self.ResetTransformBtn)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.GetTransformBtn = QPushButton(self.verticalLayoutWidget)
        self.GetTransformBtn.setObjectName("GetTransformBtn")
        self.horizontalLayout.addWidget(self.GetTransformBtn)
        self.SaveTransformsBtn = QPushButton(self.verticalLayoutWidget)
        self.SaveTransformsBtn.setObjectName("SaveTransformsBtn")
        self.horizontalLayout.addWidget(self.SaveTransformsBtn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.SetTransformBtn = QPushButton(self.verticalLayoutWidget)
        self.SetTransformBtn.setObjectName("SetTransformBtn")
        self.horizontalLayout_2.addWidget(self.SetTransformBtn)
        self.LoadTransformsBtn = QPushButton(self.verticalLayoutWidget)
        self.LoadTransformsBtn.setObjectName("LoadTransformsBtn")
        self.horizontalLayout_2.addWidget(self.LoadTransformsBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QApplication.translate("Form", "Form", None, -1))
        self.DiskCache.setText(QApplication.translate("Form", "AutoSave to Disk", None, -1))
        self.ResetTransformBtn.setText(QApplication.translate("Form", "Reset Transforms", None, -1))
        self.GetTransformBtn.setText(QApplication.translate("Form", "Get Transforms", None, -1))
        self.SaveTransformsBtn.setText(QApplication.translate("Form", "Save Transforms", None, -1))
        self.SetTransformBtn.setText(QApplication.translate("Form", "Set Transforms", None, -1))
        self.LoadTransformsBtn.setText(QApplication.translate("Form", "Load Transforms", None, -1))

