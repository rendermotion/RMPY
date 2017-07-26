# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RMFacialRig.ui'
#
# Created: Mon Oct 31 15:31:48 2016
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
        Form.resize(236, 323)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.CheckBtn = QPushButton(Form)
        self.CheckBtn.setMaximumSize(QSize(70, 16777215))
        self.CheckBtn.setObjectName("CheckBtn")
        self.horizontalLayout.addWidget(self.CheckBtn)
        self.ListCBx = QComboBox(Form)
        self.ListCBx.setObjectName("ListCBx")
        self.horizontalLayout.addWidget(self.ListCBx)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.listWidget = QListWidget(Form)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.LinkAllBtn = QPushButton(Form)
        self.LinkAllBtn.setObjectName("LinkAllBtn")
        self.horizontalLayout_2.addWidget(self.LinkAllBtn)
        self.LinkSelectedBtn = QPushButton(Form)
        self.LinkSelectedBtn.setObjectName("LinkSelectedBtn")
        self.horizontalLayout_2.addWidget(self.LinkSelectedBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.ImportFacialInterfaceBtn = QPushButton(self.groupBox)
        self.ImportFacialInterfaceBtn.setObjectName("ImportFacialInterfaceBtn")
        self.verticalLayout_2.addWidget(self.ImportFacialInterfaceBtn)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.UsePrefixChkBx = QCheckBox(self.groupBox)
        self.UsePrefixChkBx.setObjectName("UsePrefixChkBx")
        self.horizontalLayout_3.addWidget(self.UsePrefixChkBx)
        self.PrefixLineEdit = QLineEdit(self.groupBox)
        self.PrefixLineEdit.setEnabled(False)
        self.PrefixLineEdit.setObjectName("PrefixLineEdit")
        self.horizontalLayout_3.addWidget(self.PrefixLineEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.renameRightBtn = QPushButton(self.groupBox)
        self.renameRightBtn.setObjectName("renameRightBtn")
        self.horizontalLayout_4.addWidget(self.renameRightBtn)
        self.createMissingBtn = QPushButton(self.groupBox)
        self.createMissingBtn.setObjectName("createMissingBtn")
        self.horizontalLayout_4.addWidget(self.createMissingBtn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.DeleteAttributesBtn = QPushButton(self.groupBox)
        self.DeleteAttributesBtn.setObjectName("DeleteAttributesBtn")
        self.verticalLayout_2.addWidget(self.DeleteAttributesBtn)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QApplication.translate("Form", "Form", None, -1))
        self.CheckBtn.setText(QApplication.translate("Form", "Check", None, -1))
        self.LinkAllBtn.setText(QApplication.translate("Form", "Link all", None, -1))
        self.LinkSelectedBtn.setText(QApplication.translate("Form", "Link selected", None, -1))
        self.groupBox.setTitle(QApplication.translate("Form", "Generic Tools", None, -1))
        self.ImportFacialInterfaceBtn.setText(QApplication.translate("Form", "Import facial interface", None, -1))
        self.UsePrefixChkBx.setText(QApplication.translate("Form", "UsePrefix", None, -1))
        self.renameRightBtn.setText(QApplication.translate("Form", "Rename right", None, -1))
        self.createMissingBtn.setText(QApplication.translate("Form", "CreateMissingAsProxy", None, -1))
        self.DeleteAttributesBtn.setText(QApplication.translate("Form", "Delete custom attributes", None, -1))

