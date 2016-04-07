# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RMblendShapeEditor.ui'
#
# Created: Thu Apr 07 14:20:20 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(390, 275)
        self.verticalLayout_4 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.CurrentBSlbl = QtGui.QLabel(Form)
        self.CurrentBSlbl.setMaximumSize(QtCore.QSize(108, 16777215))
        self.CurrentBSlbl.setFrameShadow(QtGui.QFrame.Plain)
        self.CurrentBSlbl.setObjectName("CurrentBSlbl")
        self.horizontalLayout_3.addWidget(self.CurrentBSlbl)
        self.BlendShapeNodeNamelbl = QtGui.QLabel(Form)
        self.BlendShapeNodeNamelbl.setFrameShape(QtGui.QFrame.NoFrame)
        self.BlendShapeNodeNamelbl.setObjectName("BlendShapeNodeNamelbl")
        self.horizontalLayout_3.addWidget(self.BlendShapeNodeNamelbl)
        self.GetBlendshapeBtn = QtGui.QPushButton(Form)
        self.GetBlendshapeBtn.setMinimumSize(QtCore.QSize(0, 40))
        self.GetBlendshapeBtn.setMaximumSize(QtCore.QSize(16777215, 40))
        self.GetBlendshapeBtn.setObjectName("GetBlendshapeBtn")
        self.horizontalLayout_3.addWidget(self.GetBlendshapeBtn)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.RebuildTargetsFromSelectionBtn = QtGui.QPushButton(Form)
        self.RebuildTargetsFromSelectionBtn.setMinimumSize(QtCore.QSize(0, 40))
        self.RebuildTargetsFromSelectionBtn.setObjectName("RebuildTargetsFromSelectionBtn")
        self.horizontalLayout_2.addWidget(self.RebuildTargetsFromSelectionBtn)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.ReplaceBlendShapeInputBtn = QtGui.QPushButton(Form)
        self.ReplaceBlendShapeInputBtn.setMinimumSize(QtCore.QSize(0, 40))
        self.ReplaceBlendShapeInputBtn.setObjectName("ReplaceBlendShapeInputBtn")
        self.verticalLayout.addWidget(self.ReplaceBlendShapeInputBtn)
        self.BlendShapeNodesLbl = QtGui.QLabel(Form)
        self.BlendShapeNodesLbl.setObjectName("BlendShapeNodesLbl")
        self.verticalLayout.addWidget(self.BlendShapeNodesLbl)
        self.BlendShapeNodeTbl = QtGui.QListWidget(Form)
        self.BlendShapeNodeTbl.setObjectName("BlendShapeNodeTbl")
        self.verticalLayout.addWidget(self.BlendShapeNodeTbl)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem)
        self.TargetGroupsLbl = QtGui.QLabel(Form)
        self.TargetGroupsLbl.setObjectName("TargetGroupsLbl")
        self.verticalLayout_2.addWidget(self.TargetGroupsLbl)
        self.InputTargetGroupAlias = QtGui.QListWidget(Form)
        self.InputTargetGroupAlias.setObjectName("InputTargetGroupAlias")
        self.verticalLayout_2.addWidget(self.InputTargetGroupAlias)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.ReplaceTargetWithSelBtn = QtGui.QPushButton(Form)
        self.ReplaceTargetWithSelBtn.setMinimumSize(QtCore.QSize(0, 40))
        self.ReplaceTargetWithSelBtn.setMaximumSize(QtCore.QSize(16777215, 40))
        self.ReplaceTargetWithSelBtn.setObjectName("ReplaceTargetWithSelBtn")
        self.verticalLayout_3.addWidget(self.ReplaceTargetWithSelBtn)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.TargetList = QtGui.QListWidget(Form)
        self.TargetList.setObjectName("TargetList")
        self.verticalLayout_3.addWidget(self.TargetList)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.CurrentBSlbl.setText(QtGui.QApplication.translate("Form", "Current Blend Shape:", None, QtGui.QApplication.UnicodeUTF8))
        self.BlendShapeNodeNamelbl.setText(QtGui.QApplication.translate("Form", "No Blendshape Node Selected", None, QtGui.QApplication.UnicodeUTF8))
        self.GetBlendshapeBtn.setText(QtGui.QApplication.translate("Form", "Get BlendShape Node\n"
"From Selection", None, QtGui.QApplication.UnicodeUTF8))
        self.RebuildTargetsFromSelectionBtn.setText(QtGui.QApplication.translate("Form", "Rebuild targets from \n"
"selected node", None, QtGui.QApplication.UnicodeUTF8))
        self.ReplaceBlendShapeInputBtn.setText(QtGui.QApplication.translate("Form", "Replace BS Input \n"
" with selection", None, QtGui.QApplication.UnicodeUTF8))
        self.BlendShapeNodesLbl.setText(QtGui.QApplication.translate("Form", "BlendShape Nodes", None, QtGui.QApplication.UnicodeUTF8))
        self.TargetGroupsLbl.setText(QtGui.QApplication.translate("Form", "Target Groups Alias", None, QtGui.QApplication.UnicodeUTF8))
        self.ReplaceTargetWithSelBtn.setText(QtGui.QApplication.translate("Form", "Replace Selected Target \n"
"With Selection", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "BlendShape Targets", None, QtGui.QApplication.UnicodeUTF8))

