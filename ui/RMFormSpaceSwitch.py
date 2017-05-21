# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RMSpaceSwitchTool.ui'
#
# Created: Mon Oct 31 15:31:42 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(505, 553)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.CreateSpaceSwitchBtn = QtGui.QPushButton(Form)
        self.CreateSpaceSwitchBtn.setMinimumSize(QtCore.QSize(0, 34))
        self.CreateSpaceSwitchBtn.setObjectName("CreateSpaceSwitchBtn")
        self.horizontalLayout.addWidget(self.CreateSpaceSwitchBtn)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.ControlObjectGroupBox = QtGui.QGroupBox(Form)
        self.ControlObjectGroupBox.setObjectName("ControlObjectGroupBox")
        self.verticalLayout = QtGui.QVBoxLayout(self.ControlObjectGroupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.LoadSelectionAsCntrlObjPushBtn = QtGui.QPushButton(self.ControlObjectGroupBox)
        self.LoadSelectionAsCntrlObjPushBtn.setObjectName("LoadSelectionAsCntrlObjPushBtn")
        self.verticalLayout.addWidget(self.LoadSelectionAsCntrlObjPushBtn)
        self.ControllineEdit = QtGui.QLineEdit(self.ControlObjectGroupBox)
        self.ControllineEdit.setEnabled(False)
        self.ControllineEdit.setObjectName("ControllineEdit")
        self.verticalLayout.addWidget(self.ControllineEdit)
        self.verticalLayout_3.addWidget(self.ControlObjectGroupBox)
        self.ObjectSpaceGroup = QtGui.QGroupBox(Form)
        self.ObjectSpaceGroup.setObjectName("ObjectSpaceGroup")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.ObjectSpaceGroup)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.RemoveFromObjectSpaceBtn = QtGui.QPushButton(self.ObjectSpaceGroup)
        self.RemoveFromObjectSpaceBtn.setMinimumSize(QtCore.QSize(0, 0))
        self.RemoveFromObjectSpaceBtn.setMaximumSize(QtCore.QSize(16777215, 100))
        self.RemoveFromObjectSpaceBtn.setIconSize(QtCore.QSize(16, 16))
        self.RemoveFromObjectSpaceBtn.setObjectName("RemoveFromObjectSpaceBtn")
        self.verticalLayout_2.addWidget(self.RemoveFromObjectSpaceBtn)
        self.AddToObjectSpacePushBtn = QtGui.QPushButton(self.ObjectSpaceGroup)
        self.AddToObjectSpacePushBtn.setObjectName("AddToObjectSpacePushBtn")
        self.verticalLayout_2.addWidget(self.AddToObjectSpacePushBtn)
        self.ObjectSpaceListView = QtGui.QListWidget(self.ObjectSpaceGroup)
        self.ObjectSpaceListView.setObjectName("ObjectSpaceListView")
        self.verticalLayout_2.addWidget(self.ObjectSpaceListView)
        self.verticalLayout_3.addWidget(self.ObjectSpaceGroup)
        self.verticalLayout_5.addLayout(self.verticalLayout_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        self.ConstrainedObjectSpaceSwitch = QtGui.QGroupBox(Form)
        self.ConstrainedObjectSpaceSwitch.setObjectName("ConstrainedObjectSpaceSwitch")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.ConstrainedObjectSpaceSwitch)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.RemoveFromConstrainedBtn = QtGui.QPushButton(self.ConstrainedObjectSpaceSwitch)
        self.RemoveFromConstrainedBtn.setMinimumSize(QtCore.QSize(0, 0))
        self.RemoveFromConstrainedBtn.setMaximumSize(QtCore.QSize(16777215, 100))
        self.RemoveFromConstrainedBtn.setIconSize(QtCore.QSize(16, 16))
        self.RemoveFromConstrainedBtn.setObjectName("RemoveFromConstrainedBtn")
        self.verticalLayout_4.addWidget(self.RemoveFromConstrainedBtn)
        self.AddToConstrainListPushBtn = QtGui.QPushButton(self.ConstrainedObjectSpaceSwitch)
        self.AddToConstrainListPushBtn.setObjectName("AddToConstrainListPushBtn")
        self.verticalLayout_4.addWidget(self.AddToConstrainListPushBtn)
        self.ConstrainedObjectListView = QtGui.QListWidget(self.ConstrainedObjectSpaceSwitch)
        self.ConstrainedObjectListView.setObjectName("ConstrainedObjectListView")
        self.verticalLayout_4.addWidget(self.ConstrainedObjectListView)
        self.horizontalLayout_2.addWidget(self.ConstrainedObjectSpaceSwitch)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.CreateSpaceSwitchBtn.setText(QtGui.QApplication.translate("Form", "Create SpaceSwitch", None, QtGui.QApplication.UnicodeUTF8))
        self.ControlObjectGroupBox.setTitle(QtGui.QApplication.translate("Form", "Control Object", None, QtGui.QApplication.UnicodeUTF8))
        self.LoadSelectionAsCntrlObjPushBtn.setText(QtGui.QApplication.translate("Form", "LoadSelection as Control Object", None, QtGui.QApplication.UnicodeUTF8))
        self.ObjectSpaceGroup.setTitle(QtGui.QApplication.translate("Form", "Object Space", None, QtGui.QApplication.UnicodeUTF8))
        self.RemoveFromObjectSpaceBtn.setText(QtGui.QApplication.translate("Form", "Remove selected \n"
"from object space list", None, QtGui.QApplication.UnicodeUTF8))
        self.AddToObjectSpacePushBtn.setText(QtGui.QApplication.translate("Form", "Add object selection \n"
"to object space list", None, QtGui.QApplication.UnicodeUTF8))
        self.ConstrainedObjectSpaceSwitch.setTitle(QtGui.QApplication.translate("Form", "Constrained objects", None, QtGui.QApplication.UnicodeUTF8))
        self.RemoveFromConstrainedBtn.setText(QtGui.QApplication.translate("Form", "Remove selected \n"
"from constrained Object list", None, QtGui.QApplication.UnicodeUTF8))
        self.AddToConstrainListPushBtn.setText(QtGui.QApplication.translate("Form", "Add object selection \n"
"to object constrained list", None, QtGui.QApplication.UnicodeUTF8))

