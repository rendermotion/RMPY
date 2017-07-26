# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RMSpaceSwitchTool.ui'
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
        Form.resize(505, 553)
        self.horizontalLayout_2 = QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.CreateSpaceSwitchBtn = QPushButton(Form)
        self.CreateSpaceSwitchBtn.setMinimumSize(QSize(0, 34))
        self.CreateSpaceSwitchBtn.setObjectName("CreateSpaceSwitchBtn")
        self.horizontalLayout.addWidget(self.CreateSpaceSwitchBtn)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
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
        self.ObjectSpaceGroup = QGroupBox(Form)
        self.ObjectSpaceGroup.setObjectName("ObjectSpaceGroup")
        self.verticalLayout_2 = QVBoxLayout(self.ObjectSpaceGroup)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.RemoveFromObjectSpaceBtn = QPushButton(self.ObjectSpaceGroup)
        self.RemoveFromObjectSpaceBtn.setMinimumSize(QSize(0, 0))
        self.RemoveFromObjectSpaceBtn.setMaximumSize(QSize(16777215, 100))
        self.RemoveFromObjectSpaceBtn.setIconSize(QSize(16, 16))
        self.RemoveFromObjectSpaceBtn.setObjectName("RemoveFromObjectSpaceBtn")
        self.verticalLayout_2.addWidget(self.RemoveFromObjectSpaceBtn)
        self.AddToObjectSpacePushBtn = QPushButton(self.ObjectSpaceGroup)
        self.AddToObjectSpacePushBtn.setObjectName("AddToObjectSpacePushBtn")
        self.verticalLayout_2.addWidget(self.AddToObjectSpacePushBtn)
        self.ObjectSpaceListView = QListWidget(self.ObjectSpaceGroup)
        self.ObjectSpaceListView.setObjectName("ObjectSpaceListView")
        self.verticalLayout_2.addWidget(self.ObjectSpaceListView)
        self.verticalLayout_3.addWidget(self.ObjectSpaceGroup)
        self.verticalLayout_5.addLayout(self.verticalLayout_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        self.ConstrainedObjectSpaceSwitch = QGroupBox(Form)
        self.ConstrainedObjectSpaceSwitch.setObjectName("ConstrainedObjectSpaceSwitch")
        self.verticalLayout_4 = QVBoxLayout(self.ConstrainedObjectSpaceSwitch)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.RemoveFromConstrainedBtn = QPushButton(self.ConstrainedObjectSpaceSwitch)
        self.RemoveFromConstrainedBtn.setMinimumSize(QSize(0, 0))
        self.RemoveFromConstrainedBtn.setMaximumSize(QSize(16777215, 100))
        self.RemoveFromConstrainedBtn.setIconSize(QSize(16, 16))
        self.RemoveFromConstrainedBtn.setObjectName("RemoveFromConstrainedBtn")
        self.verticalLayout_4.addWidget(self.RemoveFromConstrainedBtn)
        self.AddToConstrainListPushBtn = QPushButton(self.ConstrainedObjectSpaceSwitch)
        self.AddToConstrainListPushBtn.setObjectName("AddToConstrainListPushBtn")
        self.verticalLayout_4.addWidget(self.AddToConstrainListPushBtn)
        self.ConstrainedObjectListView = QListWidget(self.ConstrainedObjectSpaceSwitch)
        self.ConstrainedObjectListView.setObjectName("ConstrainedObjectListView")
        self.verticalLayout_4.addWidget(self.ConstrainedObjectListView)
        self.horizontalLayout_2.addWidget(self.ConstrainedObjectSpaceSwitch)

        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QApplication.translate("Form", "Form", None, -1))
        self.CreateSpaceSwitchBtn.setText(QApplication.translate("Form", "Create SpaceSwitch", None, -1))
        self.ControlObjectGroupBox.setTitle(QApplication.translate("Form", "Control Object", None, -1))
        self.LoadSelectionAsCntrlObjPushBtn.setText(QApplication.translate("Form", "LoadSelection as Control Object", None, -1))
        self.ObjectSpaceGroup.setTitle(QApplication.translate("Form", "Object Space", None, -1))
        self.RemoveFromObjectSpaceBtn.setText(QApplication.translate("Form", "Remove selected \n"
"from object space list", None, -1))
        self.AddToObjectSpacePushBtn.setText(QApplication.translate("Form", "Add object selection \n"
"to object space list", None, -1))
        self.ConstrainedObjectSpaceSwitch.setTitle(QApplication.translate("Form", "Constrained objects", None, -1))
        self.RemoveFromConstrainedBtn.setText(QApplication.translate("Form", "Remove selected \n"
"from constrained Object list", None, -1))
        self.AddToConstrainListPushBtn.setText(QApplication.translate("Form", "Add object selection \n"
"to object constrained list", None, -1))

