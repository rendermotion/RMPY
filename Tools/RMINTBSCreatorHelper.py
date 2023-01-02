import sys
import maya.cmds as cmds
import maya.OpenMayaUI as mui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance
    from RMPY.Tools.QT5.ui import FormBlendShapeCreatorHelper

except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide import __version__
    from shiboken import wrapInstance
    from RMPY.Tools.QT4.ui import FormBlendShapeCreatorHelper
import maya.mel as mel
import os
from RMPY import RMblendShapesTools


def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QMainWindow)


class Main(MayaQWidgetDockableMixin, QDialog):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent=getMayaWindow())
        self.ui = FormBlendShapeCreatorHelper.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('Blend Shape Creator Helper')
        self.ui.LoadObjectBtn.clicked.connect(self.loadObjectBtnPressed)
        self.ui.FlipWeightsBtn.clicked.connect(self.FlipWeightsBtnPressed)
        self.BSdictionary = None
        self.ui.copy_weights_btn.clicked.connect(self.copy_weghts_btn_pressed)
        self.ui.paste_from_memory_btn.clicked.connect(self.paste_from_memory_btn_pressed)
        self.ui.save_to_memory_btn.clicked.connect(self.save_to_memory_btn_pressed)
        self.ui.paste_from_memory_btn.setEnabled(False)

        self.BSdictionary = None
        self.memory = None
        self.ui.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def loadObjectBtnPressed(self):
        selection = cmds.ls(selection=True)
        BSNodeArray = mel.eval('''source RMDeformers.mel;\nstring $BSNode[]=GetDeformer("'''+selection[0]+'''","blendShape");''')
        if len(BSNodeArray) > 0:
            self.ui.blend_shape_name_lbl.setText(BSNodeArray[0])
            self.BSdictionary = RMblendShapesTools.RMblendShapeTargetDic(BSNodeArray[0])
            self.ui.listWidget.clear()
            self.ui.listWidget.addItem('Base weights')

            for keys in sorted(self.BSdictionary):
                self.ui.listWidget.addItem(keys)

            if len(self.BSdictionary.keys()) >= 1:
                self.ui.listWidget.setCurrentRow(0)
        else:
            print "No Blendshape Node found"

    def FlipWeightsBtnPressed(self):
        blend_shape_node = self.ui.blend_shape_name_lbl.text()
        BsName = self.ui.listWidget.currentItem()

        if blend_shape_node != "":
            index_list = self.get_selected_items_index(blend_shape_node)
            for each_index in index_list:
                RMblendShapesTools.invertCurrentPaintTargetWeights(blend_shape_node, each_index)

    def copy_weghts_btn_pressed(self):
        blend_shape_node = self.ui.blend_shape_name_lbl.text()
        if blend_shape_node != "":
            selected_items_index = self.get_selected_items_index(blend_shape_node)
            source_index = selected_items_index[0]
            for each_index in selected_items_index[1:]:
                print 'source: %s destination: %s' % (source_index, each_index)
                RMblendShapesTools.copyCurrentPaintTargetWeights(blend_shape_node, source_index, each_index)

    def get_selected_items_index(self, blend_shape_node):
        selected_items_index = []
        multi_selection = self.ui.listWidget.selectedItems()
        for each_item in multi_selection:
            if self.ui.listWidget.row(each_item) > 0:
                selected_items_index.append(self.BSdictionary[each_item.text()]["TargetGroup"])
            else:
                selected_items_index.append(-1)
        return selected_items_index

    def paste_from_memory_btn_pressed(self):
        blend_shape_node = self.ui.blend_shape_name_lbl.text()
        if blend_shape_node != "":
            selected_items_index = self.get_selected_items_index(blend_shape_node)
            for each_index in selected_items_index:
                print 'destination: %s' % (each_index)
                RMblendShapesTools.paste_paint_from_dictionary(blend_shape_node, each_index, self.memory)

    def save_to_memory_btn_pressed(self):
        blend_shape_node = self.ui.blend_shape_name_lbl.text()
        if blend_shape_node != "":
            selected_items_index = self.get_selected_items_index(blend_shape_node)
            source_index = selected_items_index[0]
            self.memory = RMblendShapesTools.copy_paint_to_dictionary(blend_shape_node, source_index)

        self.ui.paste_from_memory_btn.setEnabled(True)


if __name__ == '__main__':
    w = Main()
    w.show()
