# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RMVisibilityTool.ui'
#
# Created: Fri Aug 26 10:26:44 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(369, 445)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
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
        self.VisibilitySwitchGroupBox = QtGui.QGroupBox(Form)
        self.VisibilitySwitchGroupBox.setObjectName("VisibilitySwitchGroupBox")
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.VisibilitySwitchGroupBox)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label = QtGui.QLabel(self.VisibilitySwitchGroupBox)
        self.label.setObjectName("label")
        self.verticalLayout_6.addWidget(self.label)
        self.VisibilityNameTxt = QtGui.QLineEdit(self.VisibilitySwitchGroupBox)
        self.VisibilityNameTxt.setObjectName("VisibilityNameTxt")
        self.verticalLayout_6.addWidget(self.VisibilityNameTxt)
        self.CreateVisibilitySwitchBtn = QtGui.QPushButton(self.VisibilitySwitchGroupBox)
        self.CreateVisibilitySwitchBtn.setMinimumSize(QtCore.QSize(0, 34))
        self.CreateVisibilitySwitchBtn.setObjectName("CreateVisibilitySwitchBtn")
        self.verticalLayout_6.addWidget(self.CreateVisibilitySwitchBtn)
        self.verticalLayout_3.addWidget(self.VisibilitySwitchGroupBox)
        self.VisibilityGroup = QtGui.QGroupBox(Form)
        self.VisibilityGroup.setObjectName("VisibilityGroup")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.VisibilityGroup)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.RemoveEnumBtn = QtGui.QPushButton(self.VisibilityGroup)
        self.RemoveEnumBtn.setMinimumSize(QtCore.QSize(0, 0))
        self.RemoveEnumBtn.setMaximumSize(QtCore.QSize(16777215, 100))
        self.RemoveEnumBtn.setIconSize(QtCore.QSize(16, 16))
        self.RemoveEnumBtn.setObjectName("RemoveEnumBtn")
        self.verticalLayout_2.addWidget(self.RemoveEnumBtn)
        self.ObjectSpaceListView = QtGui.QListWidget(self.VisibilityGroup)
        self.ObjectSpaceListView.setObjectName("ObjectSpaceListView")
        self.verticalLayout_2.addWidget(self.ObjectSpaceListView)
        self.verticalLayout_3.addWidget(self.VisibilityGroup)
        self.verticalLayout_5.addLayout(self.verticalLayout_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        self.AffectedVisibilityObjects = QtGui.QGroupBox(Form)
        self.AffectedVisibilityObjects.setObjectName("AffectedVisibilityObjects")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.AffectedVisibilityObjects)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.RemoveFromVisibilityBtn = QtGui.QPushButton(self.AffectedVisibilityObjects)
        self.RemoveFromVisibilityBtn.setMinimumSize(QtCore.QSize(0, 0))
        self.RemoveFromVisibilityBtn.setMaximumSize(QtCore.QSize(16777215, 100))
        self.RemoveFromVisibilityBtn.setIconSize(QtCore.QSize(16, 16))
        self.RemoveFromVisibilityBtn.setObjectName("RemoveFromVisibilityBtn")
        self.verticalLayout_4.addWidget(self.RemoveFromVisibilityBtn)
        self.RemoveListSelectedBtn = QtGui.QPushButton(self.AffectedVisibilityObjects)
        self.RemoveListSelectedBtn.setMinimumSize(QtCore.QSize(0, 0))
        self.RemoveListSelectedBtn.setMaximumSize(QtCore.QSize(16777215, 100))
        self.RemoveListSelectedBtn.setIconSize(QtCore.QSize(16, 16))
        self.RemoveListSelectedBtn.setObjectName("RemoveListSelectedBtn")
        self.verticalLayout_4.addWidget(self.RemoveListSelectedBtn)
        self.AddToVisibilitySwitchBtn = QtGui.QPushButton(self.AffectedVisibilityObjects)
        self.AddToVisibilitySwitchBtn.setObjectName("AddToVisibilitySwitchBtn")
        self.verticalLayout_4.addWidget(self.AddToVisibilitySwitchBtn)
        self.ConstrainedObjectListView = QtGui.QListWidget(self.AffectedVisibilityObjects)
        self.ConstrainedObjectListView.setObjectName("ConstrainedObjectListView")
        self.verticalLayout_4.addWidget(self.ConstrainedObjectListView)
        self.horizontalLayout_2.addWidget(self.AffectedVisibilityObjects)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.ControlObjectGroupBox.setTitle(QtGui.QApplication.translate("Form", "Control Object", None, QtGui.QApplication.UnicodeUTF8))
        self.LoadSelectionAsCntrlObjPushBtn.setText(QtGui.QApplication.translate("Form", "LoadSelection as Control Object", None, QtGui.QApplication.UnicodeUTF8))
        self.VisibilitySwitchGroupBox.setTitle(QtGui.QApplication.translate("Form", "Visibility Switch", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Visibility Switch Name", None, QtGui.QApplication.UnicodeUTF8))
        self.CreateVisibilitySwitchBtn.setText(QtGui.QApplication.translate("Form", "Create Visibility Switch", None, QtGui.QApplication.UnicodeUTF8))
        self.VisibilityGroup.setTitle(QtGui.QApplication.translate("Form", "Visibility Switchs", None, QtGui.QApplication.UnicodeUTF8))
        self.RemoveEnumBtn.setText(QtGui.QApplication.translate("Form", "Remove Visibility \n"
"switch from object", None, QtGui.QApplication.UnicodeUTF8))
        self.AffectedVisibilityObjects.setTitle(QtGui.QApplication.translate("Form", "Affected Objects", None, QtGui.QApplication.UnicodeUTF8))
        self.RemoveFromVisibilityBtn.setText(QtGui.QApplication.translate("Form", "Remove selected \n"
"from visibility Object list", None, QtGui.QApplication.UnicodeUTF8))
        self.RemoveListSelectedBtn.setText(QtGui.QApplication.translate("Form", "Remove list selected \n"
"from visibility Object list", None, QtGui.QApplication.UnicodeUTF8))
        self.AddToVisibilitySwitchBtn.setText(QtGui.QApplication.translate("Form", "Add object selection \n"
"to object visibility list", None, QtGui.QApplication.UnicodeUTF8))

