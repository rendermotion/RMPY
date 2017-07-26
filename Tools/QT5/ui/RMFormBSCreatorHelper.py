# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BlendShapeCreatorHelper.ui'
#
# Created: Mon Oct 31 15:31:47 2016
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
        Form.resize(193, 252)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.LoadObjectBtn = QPushButton(Form)
        self.LoadObjectBtn.setObjectName("LoadObjectBtn")
        self.verticalLayout.addWidget(self.LoadObjectBtn)
        self.ObjectLbl = QLabel(Form)
        self.ObjectLbl.setText("")
        self.ObjectLbl.setObjectName("ObjectLbl")
        self.verticalLayout.addWidget(self.ObjectLbl)
        self.FlipWeightsBtn = QPushButton(Form)
        self.FlipWeightsBtn.setObjectName("FlipWeightsBtn")
        self.verticalLayout.addWidget(self.FlipWeightsBtn)
        self.listWidget = QListWidget(Form)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.LinkSelected = QPushButton(Form)
        self.LinkSelected.setObjectName("LinkSelected")
        self.verticalLayout.addWidget(self.LinkSelected)

        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QApplication.translate("Form", "Form", None, -1))
        self.LoadObjectBtn.setText(QApplication.translate("Form", "Load Selection", None, -1))
        self.FlipWeightsBtn.setText(QApplication.translate("Form", "Flip Weights", None, -1))
        self.LinkSelected.setText(QApplication.translate("Form", "Extract_Shapes", None, -1))

