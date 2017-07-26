# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RMblendShapeEditor.ui'
#
# Created: Mon Oct 31 15:31:40 2016
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
        Form.resize(786, 730)
        self.horizontalLayout_4 = QHBoxLayout(Form)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.BlendShapeRebuilderLabel = QLabel(Form)
        self.BlendShapeRebuilderLabel.setObjectName("BlendShapeRebuilderLabel")
        self.verticalLayout_5.addWidget(self.BlendShapeRebuilderLabel)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.CurrentBSlbl = QLabel(Form)
        self.CurrentBSlbl.setMaximumSize(QSize(108, 16777215))
        self.CurrentBSlbl.setFrameShadow(QFrame.Plain)
        self.CurrentBSlbl.setObjectName("CurrentBSlbl")
        self.horizontalLayout_3.addWidget(self.CurrentBSlbl)
        self.BlendShapeNodeNamelbl = QLabel(Form)
        self.BlendShapeNodeNamelbl.setFrameShape(QFrame.NoFrame)
        self.BlendShapeNodeNamelbl.setObjectName("BlendShapeNodeNamelbl")
        self.horizontalLayout_3.addWidget(self.BlendShapeNodeNamelbl)
        self.GetBlendshapeBtn = QPushButton(Form)
        self.GetBlendshapeBtn.setMinimumSize(QSize(0, 40))
        self.GetBlendshapeBtn.setMaximumSize(QSize(16777215, 40))
        self.GetBlendshapeBtn.setObjectName("GetBlendshapeBtn")
        self.horizontalLayout_3.addWidget(self.GetBlendshapeBtn)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.RebuildTargetsFromSelectionBtn = QPushButton(Form)
        self.RebuildTargetsFromSelectionBtn.setMinimumSize(QSize(0, 40))
        self.RebuildTargetsFromSelectionBtn.setObjectName("RebuildTargetsFromSelectionBtn")
        self.horizontalLayout_2.addWidget(self.RebuildTargetsFromSelectionBtn)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.ReplaceBlendShapeInputBtn = QPushButton(Form)
        self.ReplaceBlendShapeInputBtn.setMinimumSize(QSize(0, 40))
        self.ReplaceBlendShapeInputBtn.setObjectName("ReplaceBlendShapeInputBtn")
        self.verticalLayout.addWidget(self.ReplaceBlendShapeInputBtn)
        self.BlendShapeNodesLbl = QLabel(Form)
        self.BlendShapeNodesLbl.setObjectName("BlendShapeNodesLbl")
        self.verticalLayout.addWidget(self.BlendShapeNodesLbl)
        self.BlendShapeNodeTbl = QListWidget(Form)
        self.BlendShapeNodeTbl.setObjectName("BlendShapeNodeTbl")
        self.verticalLayout.addWidget(self.BlendShapeNodeTbl)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.RebuildSelectedTargets = QPushButton(Form)
        self.RebuildSelectedTargets.setMinimumSize(QSize(0, 40))
        self.RebuildSelectedTargets.setObjectName("RebuildSelectedTargets")
        self.verticalLayout_2.addWidget(self.RebuildSelectedTargets)
        self.TargetGroupsLbl = QLabel(Form)
        self.TargetGroupsLbl.setObjectName("TargetGroupsLbl")
        self.verticalLayout_2.addWidget(self.TargetGroupsLbl)
        self.InputTargetGroupAlias = QListWidget(Form)
        self.InputTargetGroupAlias.setObjectName("InputTargetGroupAlias")
        self.verticalLayout_2.addWidget(self.InputTargetGroupAlias)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.ReplaceTargetWithSelBtn = QPushButton(Form)
        self.ReplaceTargetWithSelBtn.setMinimumSize(QSize(0, 40))
        self.ReplaceTargetWithSelBtn.setMaximumSize(QSize(16777215, 40))
        self.ReplaceTargetWithSelBtn.setObjectName("ReplaceTargetWithSelBtn")
        self.verticalLayout_3.addWidget(self.ReplaceTargetWithSelBtn)
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.TargetList = QListWidget(Form)
        self.TargetList.setObjectName("TargetList")
        self.verticalLayout_3.addWidget(self.TargetList)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.horizontalLayout_4.addLayout(self.verticalLayout_5)
        self.line = QFrame(Form)
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_4.addWidget(self.line)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.CorrectVtxPosBtn = QLabel(Form)
        self.CorrectVtxPosBtn.setFrameShape(QFrame.NoFrame)
        self.CorrectVtxPosBtn.setObjectName("CorrectVtxPosBtn")
        self.verticalLayout_4.addWidget(self.CorrectVtxPosBtn)
        self.LoadSelectionBtn = QPushButton(Form)
        self.LoadSelectionBtn.setObjectName("LoadSelectionBtn")
        self.verticalLayout_4.addWidget(self.LoadSelectionBtn)
        self.listWidget = QListWidget(Form)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_4.addWidget(self.listWidget)
        self.CorrectVtxBtn = QPushButton(Form)
        self.CorrectVtxBtn.setMinimumSize(QSize(100, 30))
        self.CorrectVtxBtn.setObjectName("CorrectVtxBtn")
        self.verticalLayout_4.addWidget(self.CorrectVtxBtn)
        self.horizontalLayout_4.addLayout(self.verticalLayout_4)

        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QApplication.translate("Form", "Form", None, -1))
        self.BlendShapeRebuilderLabel.setText(QApplication.translate("Form", "Blend Shape Rebuilder", None, -1))
        self.CurrentBSlbl.setText(QApplication.translate("Form", "Current Blend Shape:", None, -1))
        self.BlendShapeNodeNamelbl.setText(QApplication.translate("Form", "No Blendshape Node Selected", None, -1))
        self.GetBlendshapeBtn.setText(QApplication.translate("Form", "Get BlendShape Node\n"
"From Selection", None, -1))
        self.RebuildTargetsFromSelectionBtn.setText(QApplication.translate("Form", "Rebuild targets from \n"
"selected node", None, -1))
        self.ReplaceBlendShapeInputBtn.setText(QApplication.translate("Form", "Replace BS Input \n"
" with selection", None, -1))
        self.BlendShapeNodesLbl.setText(QApplication.translate("Form", "BlendShape Nodes", None, -1))
        self.RebuildSelectedTargets.setText(QApplication.translate("Form", "Rebuild selected targets", None, -1))
        self.TargetGroupsLbl.setText(QApplication.translate("Form", "Target Groups Alias", None, -1))
        self.ReplaceTargetWithSelBtn.setText(QApplication.translate("Form", "Replace Selected Target \n"
"With Selection", None, -1))
        self.label_3.setText(QApplication.translate("Form", "BlendShape Targets", None, -1))
        self.CorrectVtxPosBtn.setText(QApplication.translate("Form", "Vertex Position Correction", None, -1))
        self.LoadSelectionBtn.setToolTip(QApplication.translate("Form", "Load Targets you want to correct, then select the vertex on the original shape that you want to transfer to this targets. ", None, -1))
        self.LoadSelectionBtn.setText(QApplication.translate("Form", "Load Selection", None, -1))
        self.CorrectVtxBtn.setText(QApplication.translate("Form", "Correct With \n"
"Selected Verices", None, -1))

