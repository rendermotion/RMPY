# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_BlendShapeCreatorHelper.ui'
#
# Created: Tue Jul 26 20:23:11 2022
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(320, 326)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.blend_shape_name_lbl = QtWidgets.QLabel(Form)
        self.blend_shape_name_lbl.setText("")
        self.blend_shape_name_lbl.setObjectName("blend_shape_name_lbl")
        self.verticalLayout.addWidget(self.blend_shape_name_lbl)
        self.LoadObjectBtn = QtWidgets.QPushButton(Form)
        self.LoadObjectBtn.setObjectName("LoadObjectBtn")
        self.verticalLayout.addWidget(self.LoadObjectBtn)
        self.copy_weights_btn = QtWidgets.QPushButton(Form)
        self.copy_weights_btn.setObjectName("copy_weights_btn")
        self.verticalLayout.addWidget(self.copy_weights_btn)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.save_to_memory_btn = QtWidgets.QPushButton(Form)
        self.save_to_memory_btn.setObjectName("save_to_memory_btn")
        self.horizontalLayout.addWidget(self.save_to_memory_btn)
        self.paste_from_memory_btn = QtWidgets.QPushButton(Form)
        self.paste_from_memory_btn.setObjectName("paste_from_memory_btn")
        self.horizontalLayout.addWidget(self.paste_from_memory_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.FlipWeightsBtn = QtWidgets.QPushButton(Form)
        self.FlipWeightsBtn.setObjectName("FlipWeightsBtn")
        self.verticalLayout.addWidget(self.FlipWeightsBtn)
        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.LinkSelected = QtWidgets.QPushButton(Form)
        self.LinkSelected.setObjectName("LinkSelected")
        self.verticalLayout.addWidget(self.LinkSelected)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.LoadObjectBtn.setText(QtWidgets.QApplication.translate("Form", "Load Selection", None, -1))
        self.copy_weights_btn.setText(QtWidgets.QApplication.translate("Form", "Copy weights from selection", None, -1))
        self.save_to_memory_btn.setText(QtWidgets.QApplication.translate("Form", "Save to memory", None, -1))
        self.paste_from_memory_btn.setText(QtWidgets.QApplication.translate("Form", "Paste from memory", None, -1))
        self.FlipWeightsBtn.setText(QtWidgets.QApplication.translate("Form", "Flip Weights", None, -1))
        self.LinkSelected.setText(QtWidgets.QApplication.translate("Form", "Extract_Shapes", None, -1))

