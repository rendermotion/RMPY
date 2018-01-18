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
    from RMPY.Tools.QT5.ui import FormBlendShapeEditor

except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide import __version__
    from shiboken import wrapInstance
    from RMPY.Tools.QT4.ui import FormBlendShapeEditor
import maya.mel as mel
import os
from RMPY import RMblendShapesTools as RMbst

reload(RMbst)
# sys.path.append(os.path.dirname(__file__))


reload(FormBlendShapeEditor)


def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QMainWindow)


class main(MayaQWidgetDockableMixin, QDialog):
    def __init__(self, parent=None):
        super(main, self).__init__(parent=getMayaWindow())
        self.ui = FormBlendShapeEditor.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('Blend Shape Editor')
        self.ui.GetBlendshapeBtn.clicked.connect(self.GetBlendshapeBtnPressed)
        self.ui.ReplaceBlendShapeInputBtn.clicked.connect(self.ReplaceBlendShapeInputBtnPressed)
        self.ui.RebuildTargetsFromSelectionBtn.clicked.connect(self.RebuildTargetsFromSelectionBtnPressed)
        self.ui.ReplaceTargetWithSelBtn.clicked.connect(self.ReplaceTargetWithSelBtnPressed)
        self.ui.InputTargetGroupAlias.currentItemChanged.connect(self.UpdateBlendShapeTargets)

        self.ui.LoadSelectionBtn.clicked.connect(self.LoadSelectionBtnPressed)
        self.ui.CorrectVtxBtn.clicked.connect(self.CorrectVtxBtnPressed)
        self.ui.RebuildSelectedTargets.clicked.connect(self.RebuildSelectedTargets)

        self.ui.InputTargetGroupAlias.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.ui.listWidget.setSelectionMode(QAbstractItemView.NoSelection)

        self.BlendShapeDic = {}
        self.currentBS = {}

    def UpdateBlendShapeTargets(self):
        CurrentItem = self.ui.InputTargetGroupAlias.currentItem()
        if (CurrentItem):
            CurrentItemKey = CurrentItem.text().split()
            for keys in self.BlendShapeDic:
                self.currentBS = self.BlendShapeDic[keys][CurrentItemKey[1]]
                self.ui.TargetList.clear()
                for i in self.currentBS["Items"]:
                    self.ui.TargetList.addItem("BS At:" + unicode(float(i - 5000) / 1000))

    def RebuildSelectedTargets(self):
        Array = self.ui.InputTargetGroupAlias.selectedItems()
        BSNode = self.ui.BlendShapeNodeNamelbl.text()
        if BSNode == "":
            BSNodeArray = mel.eval(
                '''source RMDeformers.mel;\nstring $BSNode[]=GetDeformer("''' + selection[0] + '''","blendShape");''')
            self.ui.BlendShapeNodeNamelbl.setText(BSNodeArray[0])
            for g in (Array):
                SelectedItemText = g.text().split()
                print SelectedItemText[1]
                if len(BSNodeArray) >= 0:
                    mel.eval('''source "RMBlendShapeTools.mel";\nRMrebuildBSTarget("''' + BSNode + '''","''' +
                             SelectedItemText[1] + '''");''')
        else:
            for g in (Array):
                SelectedItemText = g.text().split()
                mel.eval(
                    '''source RMBlendShapeTools.mel;\nRMrebuildBSTarget("''' + BSNode + '''","''' + SelectedItemText[
                        1] + '''");''')

    def GetBlendshapeBtnPressed(self):
        selection = cmds.ls(sl=True)
        BSNode = mel.eval(
            '''source RMDeformers.mel;\nstring $BSNode[]=GetDeformer("''' + selection[0] + '''","blendShape");''')
        self.currentBS = {}
        self.ui.BlendShapeNodeNamelbl.setText(BSNode[0])
        self.BlendShapeDic[BSNode[0]] = RMbst.RMblendShapeTargetDic(BSNode[0])
        self.ui.BlendShapeNodeTbl.clear()
        self.ui.BlendShapeNodeTbl.addItem(BSNode[0])

        BlendShapeItem = self.ui.BlendShapeNodeTbl.item(0)
        self.ui.BlendShapeNodeTbl.setCurrentItem(BlendShapeItem)
        flag = 0
        index = 0
        self.ui.InputTargetGroupAlias.clear()
        orderdic = {}
        for keys in self.BlendShapeDic[BSNode[0]]:
            orderdic[keys] = self.BlendShapeDic[BSNode[0]][keys]["TargetGroup"]

        for i in sorted(self.BlendShapeDic[BSNode[0]], key=orderdic.__getitem__):  # self.BlendShapeDic[BSNode[0]]:
            self.ui.InputTargetGroupAlias.addItem(str(self.BlendShapeDic[BSNode[0]][i]["TargetGroup"]) + " " + i)
            if flag == index:
                self.currentBS = self.BlendShapeDic[BSNode[0]][i]
                CurrentItem = self.ui.InputTargetGroupAlias.item(index)
                self.ui.InputTargetGroupAlias.setCurrentItem(CurrentItem)
            index += 1

    def ReplaceBlendShapeInputBtnPressed(self):
        BSNode = self.ui.BlendShapeNodeNamelbl.text()
        selection = cmds.ls(sl=True)
        if len(selection) > 0:
            if cmds.objectType(selection[0]) == 'mesh':
                GroupParts = mel.eval(
                    '''source RMBlendShapeTools.mel;\nstring $GroupParts=RMGetGPInputShape("''' + BSNode + '''");''')
                cmds.connectAttr((selection[0] + '.outMesh'), (GroupParts + '.inputGeometry'), f=True)

            elif cmds.objectType(selection[0]) == 'transform':
                Shapes = cmds.listRelatives(selection[0], s=True)
                if len(Shapes) > 0:
                    GroupParts = mel.eval(
                        '''source RMBlendShapeTools.mel;\nstring $GroupParts=RMGetGPInputShape("''' + BSNode + '''");''')
                    cmds.connectAttr((Shapes[0] + ".outMesh"), (GroupParts + ".inputGeometry"), f=True)

    def RebuildTargetsFromSelectionBtnPressed(self):
        BSNode = self.ui.BlendShapeNodeNamelbl.text()
        if BSNode == "":
            BSNodeArray = mel.eval(
                '''source RMDeformers.mel;\nstring $BSNode[]=GetDeformer("''' + selection[0] + '''","blendShape");''')
            if len(BSNodeArray) >= 0:
                mel.eval('''source "RMBlendShapeTools.mel";\nRMblendShapeRebuilder("''' + BSNode + '''");''')
        else:
            mel.eval('''source RMBlendShapeTools.mel;\nRMblendShapeRebuilder("''' + BSNode + '''");''')

    def ReplaceTargetWithSelBtnPressed(self):
        BSNode = self.ui.BlendShapeNodeNamelbl.text()
        CurrentGroup = self.ui.InputTargetGroupAlias.currentItem()
        CurrentTarget = self.ui.TargetList.currentItem()
        if (CurrentGroup):
            CurrentItemKey = CurrentGroup.text().split()
            print CurrentGroup.text()
            if (CurrentTarget):
                TargetStr = CurrentTarget.text()
                BSTarget = TargetStr.split(":")
                BSTargetNum = float(BSTarget[1])
                selection = cmds.ls(sl=True)
                if (len(selection) > 0):
                    if cmds.objectType(selection[0]) == 'mesh':
                        cmds.connectAttr(selection[0] + ".outMesh", (BSNode + ".inputTarget[0].inputTargetGroup[" + str(
                            self.BlendShapeDic[BSNode][CurrentItemKey[1]]["TargetGroup"]) + "].inputTargetItem[" + str(
                            int(BSTargetNum * 1000 + 5000)) + "].inputGeomTarget"), f=True)
                    elif cmds.objectType(selection[0]) == 'transform':
                        Shapes = cmds.listRelatives(selection[0], s=True)
                        if len(Shapes) > 0:
                            cmds.connectAttr(Shapes[0] + ".outMesh", (
                            BSNode + ".inputTarget[0].inputTargetGroup[" + str(
                                self.BlendShapeDic[BSNode][CurrentItemKey[1]][
                                    "TargetGroup"]) + "].inputTargetItem[" + str(
                                int(BSTargetNum * 1000 + 5000)) + "].inputGeomTarget"), f=True)

    def LoadSelectionBtnPressed(self):
        self.ui.listWidget.clear()
        selection = cmds.ls(sl=True)
        for i in selection:
            self.ui.listWidget.addItem(i)

    def CorrectVtxBtnPressed(self):
        # Array=self.ui.listWidget.selectedItems()
        ItemNum = self.ui.listWidget.count()
        Objects = []
        Txt = "{"
        for g in range(0, ItemNum):
            Item = self.ui.listWidget.item(g)
            Txt += "\""
            Txt += Item.text()
            Txt += "\""
            Txt += ","
        Txt = Txt[:-1]
        Txt += "}"
        mel.eval('''
		source RMcomponents.mel;
		string $selection[] = `ls -sl`;
		vertexPositionTransfer($selection,''' + Txt + ''',"worldSpace");
		''')


if __name__ == '__main__':
    w = main()
    w.show(dockable=True)
