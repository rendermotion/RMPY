import sys
import maya.cmds as cmds
import maya.OpenMayaUI as mui
from PySide import QtGui, QtCore
from shiboken import wrapInstance
import maya.mel as mel
import os
import inspect
#sys.path.append(os.path.dirname(__file__))
from ui import RMFormCopyPosition
import json
reload(RMFormCopyPosition)
import RMUncategorized
reload(RMUncategorized)

'''
sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy.Fixed,QtGui.QSizePolicy.Policy.Fixed)
self.setSizePolicy(sizePolicy)
pol=self.sizePolicy()
'''

def getMayaWindow():
	ptr = mui.MQtUtil.mainWindow()
	return wrapInstance(long(ptr), QtGui.QMainWindow)

class RMCopyPosition(QtGui.QDialog):
	def __init__(self, parent=None):
		super(RMCopyPosition,self).__init__(parent=getMayaWindow())
		self.ui=RMFormCopyPosition.Ui_Form()
		self.ui.setupUi(self)
		self.setWindowTitle('RM Transform Tools ')
		self.Directory=os.path.expanduser("~")
		self.DiskCachePath=((os.path.expanduser("~"))+"/ObjectsTransform.json")
		self.ui.GetTransformBtn.clicked.connect(self.GetTransformBtnPressed)
		self.ui.SaveTransformsBtn.clicked.connect(self.SaveTransformsBtnPressed)
		self.ui.SetTransformBtn.clicked.connect(self.SetTransformBtnPressed)
		self.ui.LoadTransformsBtn.clicked.connect(self.LoadTransformsBtnPressed)
		self.ui.ResetTransformBtn.clicked.connect(self.ResetTransformBtnPressed)
		self.TramsformDic={}
	def GetTransformBtnPressed(self):
		selection = cmds.ls(sl=True)
		self.TramsformDic = RMUncategorized.ObjectTransformDic(selection)
		print "saving file to: %s" %(self.DiskCachePath)
		SaveDic={'type':'ObjectTransforms','data':self.TramsformDic}
		if not os.path.exists(self.Directory):
			os.makedirs(self.Directory)
		with open ( self.DiskCachePath, 'w') as outfile:
		    json.dump (SaveDic,outfile, sort_keys=True,indent=4)
	def SaveTransformsBtnPressed(self):
		selection=cmds.ls(sl=True)
		self.TramsformDic = RMUncategorized.ObjectTransformDic(selection)
		SaveDic={'type':'ObjectTransforms','data':self.TramsformDic}
		if not os.path.exists(self.Directory):
			os.makedirs (self.Directory)
		fname = QtGui.QFileDialog.getSaveFileName(parent=self,caption='Save Filename As',dir=unicode (self.Directory))#self.Directory
		print fname
		with open ( fname[0], 'w') as outfile:
			json.dump (SaveDic,outfile, sort_keys=True,indent=4)

	def SetTransformBtnPressed(self):
		self.TramsformDic={}
		with open (self.DiskCachePath,'r') as outfile:
			OpenDic = json.load(outfile)
		if OpenDic != u'':
			if OpenDic.has_key('data') and OpenDic.has_key('type'):
				if OpenDic['type']==str('ObjectTransforms'):
					self.TramsformDic=OpenDic['data']
					RMUncategorized.SetObjectTransformDic(self.TramsformDic)
					print self.TramsformDic
				else:
					print "File loaded not Valid"
		else:
			print "No File Selected"
		#if self.TramsformDic!={}:
		#	RMUncategorized.SetObjectTransformDic(self.TramsformDic)
		#else:
		#	print"No Data Dic Loaded on memory"

	def LoadTransformsBtnPressed(self):
		self.TramsformDic={}
		fname = QtGui.QFileDialog.getOpenFileName(parent=self,caption='Open file',dir=self.Directory)
		fname[0]
		with open (fname[0],'r') as outfile:
			OpenDic = json.load(outfile)
		if OpenDic != u'':
			if OpenDic.has_key('data') and OpenDic.has_key('type'):
				if OpenDic['type']==str('ObjectTransforms'):
					self.TramsformDic = OpenDic['data']
					RMUncategorized.SetObjectTransformDic(self.TramsformDic)
					print "File Loaded succesfully"
					print self.TramsformDic
				else:
					print "File loaded not Valid"
		else:
			print "No File Selected"
	def ResetTransformBtnPressed(self):
		selection=cmds.ls(sl=True)
		RMUncategorized.ResetPostoZero(selection)

if __name__ == '__main__':
	w = RMCopyPosition()
	w.show()