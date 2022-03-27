# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_SpaceSwitch.ui'
#
# Created: Tue Mar 15 20:23:49 2022
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(505, 553)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.CreateSpaceSwitchBtn = QtWidgets.QPushButton(Form)
        self.CreateSpaceSwitchBtn.setMinimumSize(QtCore.QSize(0, 34))
        self.CreateSpaceSwitchBtn.setObjectName("CreateSpaceSwitchBtn")
        self.horizontalLayout.addWidget(self.CreateSpaceSwitchBtn)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
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
        self.ObjectSpaceGroup = QtWidgets.QGroupBox(Form)
        self.ObjectSpaceGroup.setObjectName("ObjectSpaceGroup")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.ObjectSpaceGroup)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.RemoveFromObjectSpaceBtn = QtWidgets.QPushButton(self.ObjectSpaceGroup)
        self.RemoveFromObjectSpaceBtn.setMinimumSize(QtCore.QSize(0, 0))
        self.RemoveFromObjectSpaceBtn.setMaximumSize(QtCore.QSize(16777215, 100))
        self.RemoveFromObjectSpaceBtn.setIconSize(QtCore.QSize(16, 16))
        self.RemoveFromObjectSpaceBtn.setObjectName("RemoveFromObjectSpaceBtn")
        self.verticalLayout_2.addWidget(self.RemoveFromObjectSpaceBtn)
        self.AddToObjectSpacePushBtn = QtWidgets.QPushButton(self.ObjectSpaceGroup)
        self.AddToObjectSpacePushBtn.setObjectName("AddToObjectSpacePushBtn")
        self.verticalLayout_2.addWidget(self.AddToObjectSpacePushBtn)
        self.ObjectSpaceListView = QtWidgets.QListWidget(self.ObjectSpaceGroup)
        self.ObjectSpaceListView.setObjectName("ObjectSpaceListView")
        self.verticalLayout_2.addWidget(self.ObjectSpaceListView)
        self.verticalLayout_3.addWidget(self.ObjectSpaceGroup)
        self.verticalLayout_5.addLayout(self.verticalLayout_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        self.ConstrainedObjectSpaceSwitch = QtWidgets.QGroupBox(Form)
        self.ConstrainedObjectSpaceSwitch.setObjectName("ConstrainedObjectSpaceSwitch")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.ConstrainedObjectSpaceSwitch)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.RemoveFromConstrainedBtn = QtWidgets.QPushButton(self.ConstrainedObjectSpaceSwitch)
        self.RemoveFromConstrainedBtn.setMinimumSize(QtCore.QSize(0, 0))
        self.RemoveFromConstrainedBtn.setMaximumSize(QtCore.QSize(16777215, 100))
        self.RemoveFromConstrainedBtn.setIconSize(QtCore.QSize(16, 16))
        self.RemoveFromConstrainedBtn.setObjectName("RemoveFromConstrainedBtn")
        self.verticalLayout_4.addWidget(self.RemoveFromConstrainedBtn)
        self.AddToConstrainListPushBtn = QtWidgets.QPushButton(self.ConstrainedObjectSpaceSwitch)
        self.AddToConstrainListPushBtn.setObjectName("AddToConstrainListPushBtn")
        self.verticalLayout_4.addWidget(self.AddToConstrainListPushBtn)
        self.ConstrainedObjectListView = QtWidgets.QListWidget(self.ConstrainedObjectSpaceSwitch)
        self.ConstrainedObjectListView.setObjectName("ConstrainedObjectListView")
        self.verticalLayout_4.addWidget(self.ConstrainedObjectListView)
        self.horizontalLayout_2.addWidget(self.ConstrainedObjectSpaceSwitch)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.CreateSpaceSwitchBtn.setText(QtWidgets.QApplication.translate("Form", "Create SpaceSwitch", None, -1))
        self.ControlObjectGroupBox.setTitle(QtWidgets.QApplication.translate("Form", "Control Object", None, -1))
        self.LoadSelectionAsCntrlObjPushBtn.setText(QtWidgets.QApplication.translate("Form", "LoadSelection as Control Object", None, -1))
        self.ObjectSpaceGroup.setTitle(QtWidgets.QApplication.translate("Form", "Object Space", None, -1))
        self.RemoveFromObjectSpaceBtn.setText(QtWidgets.QApplication.translate("Form", "Remove selected \n"
"from object space list", None, -1))
        self.AddToObjectSpacePushBtn.setText(QtWidgets.QApplication.translate("Form", "Add object selection \n"
"to object space list", None, -1))
        self.ConstrainedObjectSpaceSwitch.setTitle(QtWidgets.QApplication.translate("Form", "Constrained objects", None, -1))
        self.RemoveFromConstrainedBtn.setText(QtWidgets.QApplication.translate("Form", "Remove selected \n"
"from constrained Object list", None, -1))
        self.AddToConstrainListPushBtn.setText(QtWidgets.QApplication.translate("Form", "Add object selection \n"
"to object constrained list", None, -1))

