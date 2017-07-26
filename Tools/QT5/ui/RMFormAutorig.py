# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Autorig.ui'
#
# Created: Mon Oct 31 15:31:43 2016
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
        Form.resize(234, 172)
        self.verticalLayout_3 =  QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.AutoRigTab =  QTabWidget(Form)
        self.AutoRigTab.setObjectName("AutoRigTab")
        self.tab =  QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout =  QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout =  QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.heightLabel =  QLabel(self.tab)
        self.heightLabel.setMinimumSize(QSize(20, 0))
        self.heightLabel.setMaximumSize(QSize(50, 16777215))
        self.heightLabel.setTextFormat(Qt.PlainText)
        self.heightLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.heightLabel.setObjectName("heightLabel")
        self.horizontalLayout.addWidget(self.heightLabel)
        self.HeightSpnBox =  QDoubleSpinBox(self.tab)
        self.HeightSpnBox.setMaximum(1000000.0)
        self.HeightSpnBox.setProperty("value", 75.0)
        self.HeightSpnBox.setObjectName("HeightSpnBox")
        self.horizontalLayout.addWidget(self.HeightSpnBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.CreateReferencePointsBtn =  QPushButton(self.tab)
        self.CreateReferencePointsBtn.setObjectName("CreateReferencePointsBtn")
        self.verticalLayout.addWidget(self.CreateReferencePointsBtn)
        self.MirrorSelectionBtn =  QPushButton(self.tab)
        self.MirrorSelectionBtn.setObjectName("MirrorSelectionBtn")
        self.verticalLayout.addWidget(self.MirrorSelectionBtn)
        self.CreateRigBtn =  QPushButton(self.tab)
        self.CreateRigBtn.setObjectName("CreateRigBtn")
        self.verticalLayout.addWidget(self.CreateRigBtn)
        self.AutoRigTab.addTab(self.tab, "")
        self.tab_2 =  QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_2 =  QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.SkeletonHandsBtn =  QPushButton(self.tab_2)
        self.SkeletonHandsBtn.setObjectName("SkeletonHandsBtn")
        self.verticalLayout_2.addWidget(self.SkeletonHandsBtn)
        self.supportScaleRigBtn =  QPushButton(self.tab_2)
        self.supportScaleRigBtn.setObjectName("supportScaleRigBtn")
        self.verticalLayout_2.addWidget(self.supportScaleRigBtn)
        self.feetOrientationBtn =  QPushButton(self.tab_2)
        self.feetOrientationBtn.setObjectName("feetOrientationBtn")
        self.verticalLayout_2.addWidget(self.feetOrientationBtn)
        self.AutoRigTab.addTab(self.tab_2, "")
        self.tab_5 =  QWidget()
        self.tab_5.setObjectName("tab_5")
        self.verticalLayout_4 =  QVBoxLayout(self.tab_5)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.ClavicleSpaceSwitchBtn =  QPushButton(self.tab_5)
        self.ClavicleSpaceSwitchBtn.setObjectName("ClavicleSpaceSwitchBtn")
        self.verticalLayout_4.addWidget(self.ClavicleSpaceSwitchBtn)
        self.PoleVectorBtn =  QPushButton(self.tab_5)
        self.PoleVectorBtn.setObjectName("PoleVectorBtn")
        self.verticalLayout_4.addWidget(self.PoleVectorBtn)
        self.label =  QLabel(self.tab_5)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)
        self.AutoRigTab.addTab(self.tab_5, "")
        self.verticalLayout_3.addWidget(self.AutoRigTab)

        self.retranslateUi(Form)
        self.AutoRigTab.setCurrentIndex(1)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle( QApplication.translate("Form", "Form", None,  -1))
        self.heightLabel.setText( QApplication.translate("Form", "Height", None,   -1))
        self.CreateReferencePointsBtn.setText( QApplication.translate("Form", "Create Reference Points", None,   -1))
        self.MirrorSelectionBtn.setText( QApplication.translate("Form", "Mirror Selection", None,   -1))
        self.CreateRigBtn.setText( QApplication.translate("Form", "CreateRig", None,   -1))
        self.AutoRigTab.setTabText(self.AutoRigTab.indexOf(self.tab),  QApplication.translate("Form", "AutoRig", None,   -1))
        self.SkeletonHandsBtn.setText( QApplication.translate("Form", "Skeleton Hands", None,   -1))
        self.supportScaleRigBtn.setText( QApplication.translate("Form", "Support Scale Rig", None,   -1))
        self.feetOrientationBtn.setText( QApplication.translate("Form", "Correct Feet Orientation", None,   -1))
        self.AutoRigTab.setTabText(self.AutoRigTab.indexOf(self.tab_2),  QApplication.translate("Form", "Snipets", None,   -1))
        self.ClavicleSpaceSwitchBtn.setText( QApplication.translate("Form", "Clavicle Space Switch", None,   -1))
        self.PoleVectorBtn.setText( QApplication.translate("Form", "Correct P Vector Orient", None,   -1))
        self.label.setText( QApplication.translate("Form", "All deprecated snippets are all ready\n"
" included on the autorig default creation", None,   -1))
        self.AutoRigTab.setTabText(self.AutoRigTab.indexOf(self.tab_5),  QApplication.translate("Form", "Deprecated", None,   -1))

