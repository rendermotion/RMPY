# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RMRigDisplay.ui'
#
# Created: Mon Oct 31 15:31:39 2016
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
        Form.resize(236, 179)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ChangeJointdrawStyle = QPushButton(Form)
        self.ChangeJointdrawStyle.setMaximumSize(QSize(100, 30))
        self.ChangeJointdrawStyle.setObjectName("ChangeJointdrawStyle")
        self.horizontalLayout.addWidget(self.ChangeJointdrawStyle)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QApplication.translate("Form", "Form", None, -1))
        self.ChangeJointdrawStyle.setText(QApplication.translate("Form", "Joint DrawStyle", None, -1))

