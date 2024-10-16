# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aim_to_point.ui'
#
# Created: Sun Nov 10 21:37:08 2019
#      by: PySide6-uic  running on PySide6 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore, QtGui, QtWidgets

class Ui_aim_to_point(object):
    def setupUi(self, aim_to_point):
        aim_to_point.setObjectName("aim_to_point")
        aim_to_point.resize(137, 165)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(aim_to_point)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.aim_point_based_button = QtWidgets.QPushButton(aim_to_point)
        self.aim_point_based_button.setObjectName("aim_point_based_button")
        self.verticalLayout_3.addWidget(self.aim_point_based_button)
        self.widget = QtWidgets.QWidget(aim_to_point)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.aim_axis_label = QtWidgets.QLabel(self.widget)
        self.aim_axis_label.setObjectName("aim_axis_label")
        self.verticalLayout.addWidget(self.aim_axis_label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.X_aim_axis_radio = QtWidgets.QRadioButton(self.widget)
        self.X_aim_axis_radio.setChecked(True)
        self.X_aim_axis_radio.setObjectName("X_aim_axis_radio")
        self.horizontalLayout.addWidget(self.X_aim_axis_radio)
        self.Y_aim_axis_radio = QtWidgets.QRadioButton(self.widget)
        self.Y_aim_axis_radio.setObjectName("Y_aim_axis_radio")
        self.horizontalLayout.addWidget(self.Y_aim_axis_radio)
        self.Z_aim_axis_radio = QtWidgets.QRadioButton(self.widget)
        self.Z_aim_axis_radio.setAutoExclusive(True)
        self.Z_aim_axis_radio.setObjectName("Z_aim_axis_radio")
        self.horizontalLayout.addWidget(self.Z_aim_axis_radio)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_3.addWidget(self.widget)
        self.widget_2 = QtWidgets.QWidget(aim_to_point)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.up_axis_label = QtWidgets.QLabel(self.widget_2)
        self.up_axis_label.setObjectName("up_axis_label")
        self.verticalLayout_2.addWidget(self.up_axis_label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.X_up_axis_radio = QtWidgets.QRadioButton(self.widget_2)
        self.X_up_axis_radio.setChecked(True)
        self.X_up_axis_radio.setObjectName("X_up_axis_radio")
        self.horizontalLayout_2.addWidget(self.X_up_axis_radio)
        self.Y_up_axis_radio = QtWidgets.QRadioButton(self.widget_2)
        self.Y_up_axis_radio.setObjectName("Y_up_axis_radio")
        self.horizontalLayout_2.addWidget(self.Y_up_axis_radio)
        self.Z_up_axis_radio = QtWidgets.QRadioButton(self.widget_2)
        self.Z_up_axis_radio.setObjectName("Z_up_axis_radio")
        self.horizontalLayout_2.addWidget(self.Z_up_axis_radio)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addWidget(self.widget_2)

        self.retranslateUi(aim_to_point)
        QtCore.QMetaObject.connectSlotsByName(aim_to_point)

    def retranslateUi(self, aim_to_point):
        aim_to_point.setWindowTitle(QtWidgets.QApplication.translate("aim_to_point", "Form", None, -1))
        self.aim_point_based_button.setText(QtWidgets.QApplication.translate("aim_to_point", "aim to point", None, -1))
        self.aim_axis_label.setText(QtWidgets.QApplication.translate("aim_to_point", "aim axis", None, -1))
        self.X_aim_axis_radio.setText(QtWidgets.QApplication.translate("aim_to_point", "X", None, -1))
        self.Y_aim_axis_radio.setText(QtWidgets.QApplication.translate("aim_to_point", "Y", None, -1))
        self.Z_aim_axis_radio.setText(QtWidgets.QApplication.translate("aim_to_point", "Z", None, -1))
        self.up_axis_label.setText(QtWidgets.QApplication.translate("aim_to_point", "up axis", None, -1))
        self.X_up_axis_radio.setText(QtWidgets.QApplication.translate("aim_to_point", "X", None, -1))
        self.Y_up_axis_radio.setText(QtWidgets.QApplication.translate("aim_to_point", "Y", None, -1))
        self.Z_up_axis_radio.setText(QtWidgets.QApplication.translate("aim_to_point", "Z", None, -1))

