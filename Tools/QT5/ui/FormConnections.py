# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_Connections.ui'
#
# Created: Wed Mar 21 21:43:33 2018
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(494, 599)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 170, 411, 302))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 40))
        self.pushButton.setMaximumSize(QtCore.QSize(16777215, 40))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.listWidget = QtWidgets.QListWidget(self.horizontalLayoutWidget)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.verticalLayout_2.addItem(spacerItem)
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.tableWidget = QtWidgets.QTableWidget(self.horizontalLayoutWidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout_2.addWidget(self.tableWidget)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(0, 40))
        self.pushButton_2.setMaximumSize(QtCore.QSize(16777215, 40))
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_3.addWidget(self.pushButton_2)
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.tableWidget_2 = QtWidgets.QTableWidget(self.horizontalLayoutWidget)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.verticalLayout_3.addWidget(self.tableWidget_2)
        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("Form", "Input Connections", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Form", "InputConnections", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Form", "Original Attributes", None, -1))
        self.pushButton_2.setText(QtWidgets.QApplication.translate("Form", "Reload Selection\n"
"Attributtes ", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Form", "Custom Attributes", None, -1))

