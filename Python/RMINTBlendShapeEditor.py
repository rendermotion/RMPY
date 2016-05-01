import sys
import maya.cmds as cmds
import maya.OpenMayaUI as mui
from PySide import QtGui, QtCore
from shiboken import wrapInstance
import maya.mel as mel
import os
import RMblendShapesTools as RMbst
reload(RMbst)
#sys.path.append(os.path.dirname(__file__))
from ui import RMFormBlendShapeEditor
reload(RMFormBlendShapeEditor)

def getMayaWindow():
	ptr = mui.MQtUtil.mainWindow()
	return wrapInstance(long(ptr), QtGui.QMainWindow)

class RMBlendShapeEditor(QtGui.QDialog):
	def __init__(self, parent=None):
		super(RMBlendShapeEditor,self).__init__(parent=getMayaWindow())
		self.ui=RMFormBlendShapeEditor.Ui_Form()
		self.ui.setupUi(self)
		self.setWindowTitle('Blend Shape Editor')
		self.ui.GetBlendshapeBtn.clicked.connect(self.GetBlendshapeBtnPressed)
		self.ui.ReplaceBlendShapeInputBtn.clicked.connect(self.ReplaceBlendShapeInputBtnPressed)
		self.ui.RebuildTargetsFromSelectionBtn.clicked.connect(self.RebuildTargetsFromSelectionBtnPressed)
		self.ui.ReplaceTargetWithSelBtn.clicked.connect(self.ReplaceTargetWithSelBtnPressed)
		self.ui.InputTargetGroupAlias.currentItemChanged.connect(self.UpdateBlendShapeTargets)
		
		self.ui.LoadSelectionBtn.clicked.connect(self.LoadSelectionBtnPressed)
		self.ui.CorrectVtxBtn.clicked.connect(self.CorrectVtxBtnPressed)

		self.ui.listWidget.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
		self.BlendShapeDic={}
		self.currentBS ={}
	def UpdateBlendShapeTargets(self):
		CurrentItem = self.ui.InputTargetGroupAlias.currentItem()
		if (CurrentItem):
			for keys in self.BlendShapeDic:
				self.currentBS = self.BlendShapeDic[keys][CurrentItem.text()]
				self.ui.TargetList.clear()
				for i in self.currentBS["Items"]:
					self.ui.TargetList.addItem("BS At:"+ unicode(float(i-5000)/1000))

	def GetBlendshapeBtnPressed(self):
		selection = cmds.ls(sl=True)
		BSNode = mel.eval('''source RMDeformers.mel;\nstring $BSNode[]=GetDeformer("'''+selection[0]+'''","blendShape");''')
		self.currentBS={}
		self.ui.BlendShapeNodeNamelbl.setText(BSNode[0])
		self.BlendShapeDic[BSNode[0]] = RMbst.RMblendShapeTargetDic(BSNode[0])
		self.ui.BlendShapeNodeTbl.clear()
		self.ui.BlendShapeNodeTbl.addItem(BSNode[0])

		BlendShapeItem = self.ui.BlendShapeNodeTbl.item(0)
		self.ui.BlendShapeNodeTbl.setCurrentItem(BlendShapeItem)
		flag=0
		index=0
		self.ui.InputTargetGroupAlias.clear()
		for i in self.BlendShapeDic[BSNode[0]]:
			self.ui.InputTargetGroupAlias.addItem(i)
			if flag == index:
				self.currentBS = self.BlendShapeDic[BSNode[0]][i]
				CurrentItem = self.ui.InputTargetGroupAlias.item(index)
				self.ui.InputTargetGroupAlias.setCurrentItem(CurrentItem)
			index+=1

	def ReplaceBlendShapeInputBtnPressed(self):
		BSNode = self.ui.BlendShapeNodeNamelbl.text()
		selection = cmds.ls(sl=True)
		if (len(selection)>0):
			if cmds.objectType(selection[0])=='mesh':
				GroupParts = mel.eval('''source RMBlendShapeTools.mel;\nstring $GroupParts=RMGetGPInputShape("''' + BSNode + '''");''')
				cmds.connectAttr((selection[0]+'.outMesh'),(GroupParts + '.inputGeometry'),f=True)

			elif cmds.objectType(selection[0])=='transform':
				Shapes = cmds.listRelatives(selection[0],s=True )
				if len(Shapes) > 0:
					GroupParts = mel.eval('''source RMBlendShapeTools.mel;\nstring $GroupParts=RMGetGPInputShape("''' + BSNode + '''");''')
					cmds.connectAttr((Shapes[0]+".outMesh"),(GroupParts+".inputGeometry"),f = True)

	def RebuildTargetsFromSelectionBtnPressed(self):
		BSNode = self.ui.BlendShapeNodeNamelbl.text()
		if BSNode == "":
			BSNodeArray = mel.eval('''source RMDeformers.mel;\nstring $BSNode[]=GetDeformer("'''+selection[0]+'''","blendShape");''')
			if len(BSNodeArray)>=0:
				mel.eval('''source "RMBlendShapeTools.mel";\nRMblendShapeRebuilder("'''+BSNode+'''");''')		
		else:
			mel.eval('''source RMBlendShapeTools.mel;\nRMblendShapeRebuilder("'''+BSNode+'''");''')

	def ReplaceTargetWithSelBtnPressed(self):
		BSNode = self.ui.BlendShapeNodeNamelbl.text()
		CurrentGroup = self.ui.InputTargetGroupAlias.currentItem()
		CurrentTarget = self.ui.TargetList.currentItem()
		if (CurrentGroup):
			print CurrentGroup.text()
			if (CurrentTarget):
				TargetStr = CurrentTarget.text()
				BSTarget =TargetStr.split(":")
				BSTargetNum = float(BSTarget[1])
				selection = cmds.ls(sl=True)
				if (len(selection)>0):
					if cmds.objectType(selection[0])=='mesh':
						cmds.connectAttr(selection[0]+".outMesh",(BSNode +".inputTarget[0].inputTargetGroup[" + str(self.BlendShapeDic[BSNode][CurrentGroup.text()]["TargetGroup"]) + "].inputTargetItem["+ str(int(BSTargetNum*1000+5000))+"].inputGeomTarget"),f=True)
					elif cmds.objectType(selection[0])=='transform':
						Shapes = cmds.listRelatives(selection[0],s=True)
						if len(Shapes) > 0:
							cmds.connectAttr(Shapes[0]+".outMesh",(BSNode +".inputTarget[0].inputTargetGroup[" +str(self.BlendShapeDic[BSNode][CurrentGroup.text()]["TargetGroup"])+ "].inputTargetItem["+ str(int(BSTargetNum*1000+5000))+"].inputGeomTarget") , f=True)
	def LoadSelectionBtnPressed(self):
		self.ui.listWidget.clear()
		selection = cmds.ls(sl=True)
		for i in selection:
			self.ui.listWidget.addItem(i)
	def CorrectVtxBtnPressed(self):
		#Array=self.ui.listWidget.selectedItems()
		ItemNum = self.ui.listWidget.count()
		Objects=[]
		Txt="{"
		for g in range(0,ItemNum):
			Item = self.ui.listWidget.item(g)
			Txt+="\""
			Txt+=Item.text()
			Txt+="\""
			Txt+=","
		Txt=Txt[:-1]
		Txt+="}"
		mel.eval('''
		source RMcomponents.mel;
		string $selection[] = `ls -sl`;
		vertexPositionTransfer($selection,'''+ Txt +''');
		''')

if __name__ == '__main__':
	w = RMBlendShapeEditor()
	w.show()
