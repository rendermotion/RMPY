# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RMVisibilityTool.ui'
#
# Created: Mon Oct 31 15:31:44 2016
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
        Form.resize(369, 445)
        self.horizontalLayout_2 = QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.ControlObjectGroupBox = QGroupBox(Form)
        self.ControlObjectGroupBox.setObjectName("ControlObjectGroupBox")
        self.verticalLayout = QVBoxLayout(self.ControlObjectGroupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.LoadSelectionAsCntrlObjPushBtn = QPushButton(self.ControlObjectGroupBox)
        self.LoadSelectionAsCntrlObjPushBtn.setObjectName("LoadSelectionAsCntrlObjPushBtn")
        self.verticalLayout.addWidget(self.LoadSelectionAsCntrlObjPushBtn)
        self.ControllineEdit = QLineEdit(self.ControlObjectGroupBox)
        self.ControllineEdit.setEnabled(False)
        self.ControllineEdit.setObjectName("ControllineEdit")
        self.verticalLayout.addWidget(self.ControllineEdit)
        self.verticalLayout_3.addWidget(self.ControlObjectGroupBox)
        self.VisibilitySwitchGroupBox = QGroupBox(Form)
        self.VisibilitySwitchGroupBox.setObjectName("VisibilitySwitchGroupBox")
        self.verticalLayout_6 = QVBoxLayout(self.VisibilitySwitchGroupBox)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label = QLabel(self.VisibilitySwitchGroupBox)
        self.label.setObjectName("label")
        self.verticalLayout_6.addWidget(self.label)
        self.VisibilityNameTxt = QLineEdit(self.VisibilitySwitchGroupBox)
        self.VisibilityNameTxt.setObjectName("VisibilityNameTxt")
        self.verticalLayout_6.addWidget(self.VisibilityNameTxt)
        self.CreateVisibilitySwitchBtn = QPushButton(self.VisibilitySwitchGroupBox)
        self.CreateVisibilitySwitchBtn.setMinimumSize(QSize(0, 34))
        self.CreateVisibilitySwitchBtn.setObjectName("CreateVisibilitySwitchBtn")
        self.verticalLayout_6.addWidget(self.CreateVisibilitySwitchBtn)
        self.verticalLayout_3.addWidget(self.VisibilitySwitchGroupBox)
        self.VisibilityGroup = QGroupBox(Form)
        self.VisibilityGroup.setObjectName("VisibilityGroup")
        self.verticalLayout_2 = QVBoxLayout(self.VisibilityGroup)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.RemoveEnumBtn = QPushButton(self.VisibilityGroup)
        self.RemoveEnumBtn.setMinimumSize(QSize(0, 0))
        self.RemoveEnumBtn.setMaximumSize(QSize(16777215, 100))
        self.RemoveEnumBtn.setIconSize(QSize(16, 16))
        self.RemoveEnumBtn.setObjectName("RemoveEnumBtn")
        self.verticalLayout_2.addWidget(self.RemoveEnumBtn)
        self.ObjectSpaceListView = QListWidget(self.VisibilityGroup)
        self.ObjectSpaceListView.setObjectName("ObjectSpaceListView")
        self.verticalLayout_2.addWidget(self.ObjectSpaceListView)
        self.verticalLayout_3.addWidget(self.VisibilityGroup)
        self.verticalLayout_5.addLayout(self.verticalLayout_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        self.AffectedVisibilityObjects = QGroupBox(Form)
        self.AffectedVisibilityObjects.setObjectName("AffectedVisibilityObjects")
        self.verticalLayout_4 = QVBoxLayout(self.AffectedVisibilityObjects)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.RemoveFromVisibilityBtn = QPushButton(self.AffectedVisibilityObjects)
        self.RemoveFromVisibilityBtn.setMinimumSize(QSize(0, 0))
        self.RemoveFromVisibilityBtn.setMaximumSize(QSize(16777215, 100))
        self.RemoveFromVisibilityBtn.setIconSize(QSize(16, 16))
        self.RemoveFromVisibilityBtn.setObjectName("RemoveFromVisibilityBtn")
        self.verticalLayout_4.addWidget(self.RemoveFromVisibilityBtn)
        self.RemoveListSelectedBtn = QPushButton(self.AffectedVisibilityObjects)
        self.RemoveListSelectedBtn.setMinimumSize(QSize(0, 0))
        self.RemoveListSelectedBtn.setMaximumSize(QSize(16777215, 100))
        self.RemoveListSelectedBtn.setIconSize(QSize(16, 16))
        self.RemoveListSelectedBtn.setObjectName("RemoveListSelectedBtn")
        self.verticalLayout_4.addWidget(self.RemoveListSelectedBtn)
        self.AddToVisibilitySwitchBtn = QPushButton(self.AffectedVisibilityObjects)
        self.AddToVisibilitySwitchBtn.setObjectName("AddToVisibilitySwitchBtn")
        self.verticalLayout_4.addWidget(self.AddToVisibilitySwitchBtn)
        self.ConstrainedObjectListView = QListWidget(self.AffectedVisibilityObjects)
        self.ConstrainedObjectListView.setObjectName("ConstrainedObjectListView")
        self.verticalLayout_4.addWidget(self.ConstrainedObjectListView)
        self.horizontalLayout_2.addWidget(self.AffectedVisibilityObjects)

        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QApplication.translate("Form", "Form", None, -1))
        self.ControlObjectGroupBox.setTitle(QApplication.translate("Form", "Control Object", None, -1))
        self.LoadSelectionAsCntrlObjPushBtn.setText(QApplication.translate("Form", "LoadSelection as Control Object", None, -1))
        self.VisibilitySwitchGroupBox.setTitle(QApplication.translate("Form", "Visibility Switch", None, -1))
        self.label.setText(QApplication.translate("Form", "Visibility Switch Name", None, -1))
        self.CreateVisibilitySwitchBtn.setText(QApplication.translate("Form", "Create Visibility Switch", None, -1))
        self.VisibilityGroup.setTitle(QApplication.translate("Form", "Visibility Switchs", None, -1))
        self.RemoveEnumBtn.setText(QApplication.translate("Form", "Remove Visibility \n"
"switch from object", None, -1))
        self.AffectedVisibilityObjects.setTitle(QApplication.translate("Form", "Affected Objects", None, -1))
        self.RemoveFromVisibilityBtn.setText(QApplication.translate("Form", "Remove selected \n"
"from visibility Object list", None, -1))
        self.RemoveListSelectedBtn.setText(QApplication.translate("Form", "Remove list selected \n"
"from visibility Object list", None, -1))
        self.AddToVisibilitySwitchBtn.setText(QApplication.translate("Form", "Add object selection \n"
"to object visibility list", None, -1))

