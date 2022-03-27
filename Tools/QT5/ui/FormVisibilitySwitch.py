# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_VisibilitySwitch.ui'
#
# Created: Tue Mar 15 20:23:49 2022
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(369, 445)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.ControlObjectGroupBox = QtWidgets.QGroupBox(Form)
        self.ControlObjectGroupBox.setObjectName("ControlObjectGroupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.ControlObjectGroupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.LoadSelectionAsCntrlObjPushBtn = QtWidgets.QPushButton(self.ControlObjectGroupBox)
        self.LoadSelectionAsCntrlObjPushBtn.setObjectName("LoadSelectionAsCntrlObjPushBtn")
        self.verticalLayout.addWidget(self.LoadSelectionAsCntrlObjPushBtn)
        self.ControllineEdit = QtWidgets.QLineEdit(self.ControlObjectGroupBox)
        self.ControllineEdit.setEnabled(False)
        self.ControllineEdit.setObjectName("ControllineEdit")
        self.verticalLayout.addWidget(self.ControllineEdit)
        self.verticalLayout_3.addWidget(self.ControlObjectGroupBox)
        self.VisibilitySwitchGroupBox = QtWidgets.QGroupBox(Form)
        self.VisibilitySwitchGroupBox.setObjectName("VisibilitySwitchGroupBox")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.VisibilitySwitchGroupBox)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label = QtWidgets.QLabel(self.VisibilitySwitchGroupBox)
        self.label.setObjectName("label")
        self.verticalLayout_6.addWidget(self.label)
        self.VisibilityNameTxt = QtWidgets.QLineEdit(self.VisibilitySwitchGroupBox)
        self.VisibilityNameTxt.setObjectName("VisibilityNameTxt")
        self.verticalLayout_6.addWidget(self.VisibilityNameTxt)
        self.CreateVisibilitySwitchBtn = QtWidgets.QPushButton(self.VisibilitySwitchGroupBox)
        self.CreateVisibilitySwitchBtn.setMinimumSize(QtCore.QSize(0, 34))
        self.CreateVisibilitySwitchBtn.setObjectName("CreateVisibilitySwitchBtn")
        self.verticalLayout_6.addWidget(self.CreateVisibilitySwitchBtn)
        self.verticalLayout_3.addWidget(self.VisibilitySwitchGroupBox)
        self.VisibilityGroup = QtWidgets.QGroupBox(Form)
        self.VisibilityGroup.setObjectName("VisibilityGroup")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.VisibilityGroup)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.RemoveEnumBtn = QtWidgets.QPushButton(self.VisibilityGroup)
        self.RemoveEnumBtn.setMinimumSize(QtCore.QSize(0, 0))
        self.RemoveEnumBtn.setMaximumSize(QtCore.QSize(16777215, 100))
        self.RemoveEnumBtn.setIconSize(QtCore.QSize(16, 16))
        self.RemoveEnumBtn.setObjectName("RemoveEnumBtn")
        self.verticalLayout_2.addWidget(self.RemoveEnumBtn)
        self.ObjectSpaceListView = QtWidgets.QListWidget(self.VisibilityGroup)
        self.ObjectSpaceListView.setObjectName("ObjectSpaceListView")
        self.verticalLayout_2.addWidget(self.ObjectSpaceListView)
        self.verticalLayout_3.addWidget(self.VisibilityGroup)
        self.verticalLayout_5.addLayout(self.verticalLayout_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        self.AffectedVisibilityObjects = QtWidgets.QGroupBox(Form)
        self.AffectedVisibilityObjects.setObjectName("AffectedVisibilityObjects")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.AffectedVisibilityObjects)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.RemoveFromVisibilityBtn = QtWidgets.QPushButton(self.AffectedVisibilityObjects)
        self.RemoveFromVisibilityBtn.setMinimumSize(QtCore.QSize(0, 0))
        self.RemoveFromVisibilityBtn.setMaximumSize(QtCore.QSize(16777215, 100))
        self.RemoveFromVisibilityBtn.setIconSize(QtCore.QSize(16, 16))
        self.RemoveFromVisibilityBtn.setObjectName("RemoveFromVisibilityBtn")
        self.verticalLayout_4.addWidget(self.RemoveFromVisibilityBtn)
        self.RemoveListSelectedBtn = QtWidgets.QPushButton(self.AffectedVisibilityObjects)
        self.RemoveListSelectedBtn.setMinimumSize(QtCore.QSize(0, 0))
        self.RemoveListSelectedBtn.setMaximumSize(QtCore.QSize(16777215, 100))
        self.RemoveListSelectedBtn.setIconSize(QtCore.QSize(16, 16))
        self.RemoveListSelectedBtn.setObjectName("RemoveListSelectedBtn")
        self.verticalLayout_4.addWidget(self.RemoveListSelectedBtn)
        self.AddToVisibilitySwitchBtn = QtWidgets.QPushButton(self.AffectedVisibilityObjects)
        self.AddToVisibilitySwitchBtn.setObjectName("AddToVisibilitySwitchBtn")
        self.verticalLayout_4.addWidget(self.AddToVisibilitySwitchBtn)
        self.ConstrainedObjectListView = QtWidgets.QListWidget(self.AffectedVisibilityObjects)
        self.ConstrainedObjectListView.setObjectName("ConstrainedObjectListView")
        self.verticalLayout_4.addWidget(self.ConstrainedObjectListView)
        self.horizontalLayout_2.addWidget(self.AffectedVisibilityObjects)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.ControlObjectGroupBox.setTitle(QtWidgets.QApplication.translate("Form", "Control Object", None, -1))
        self.LoadSelectionAsCntrlObjPushBtn.setText(QtWidgets.QApplication.translate("Form", "LoadSelection as Control Object", None, -1))
        self.VisibilitySwitchGroupBox.setTitle(QtWidgets.QApplication.translate("Form", "Visibility Switch", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Form", "Visibility Switch Name", None, -1))
        self.CreateVisibilitySwitchBtn.setText(QtWidgets.QApplication.translate("Form", "Create Visibility Switch", None, -1))
        self.VisibilityGroup.setTitle(QtWidgets.QApplication.translate("Form", "Visibility Switchs", None, -1))
        self.RemoveEnumBtn.setText(QtWidgets.QApplication.translate("Form", "Remove Visibility \n"
"switch from object", None, -1))
        self.AffectedVisibilityObjects.setTitle(QtWidgets.QApplication.translate("Form", "Affected Objects", None, -1))
        self.RemoveFromVisibilityBtn.setText(QtWidgets.QApplication.translate("Form", "Remove selected \n"
"from visibility Object list", None, -1))
        self.RemoveListSelectedBtn.setText(QtWidgets.QApplication.translate("Form", "Remove list selected \n"
"from visibility Object list", None, -1))
        self.AddToVisibilitySwitchBtn.setText(QtWidgets.QApplication.translate("Form", "Add object selection \n"
"to object visibility list", None, -1))

