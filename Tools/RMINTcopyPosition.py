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
    from RMPY.Tools.QT5.ui import FormCopyPosition
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide import __version__
    from shiboken import wrapInstance
    from RMPY.Tools.QT4.ui import FormCopyPosition
import maya.mel as mel
import os
import inspect
# sys.path.append(os.path.dirname(__file__))
import json

from RMPY import RMUncategorized

'''
sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Fixed)
self.setSizePolicy(sizePolicy)
pol=self.sizePolicy()
'''


def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(int(ptr), QMainWindow)


class main(MayaQWidgetDockableMixin, QDialog):
    def __init__(self, parent=None):
        super(main, self).__init__(parent=getMayaWindow())
        self.ui = FormCopyPosition.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('RM Transform Tools ')
        self.Directory = os.path.expanduser("~")
        self.DiskCachePath = ((os.path.expanduser("~")) + "/ObjectsTransform.json")
        self.ui.GetTransformBtn.clicked.connect(self.GetTransformBtnPressed)
        self.ui.SaveTransformsBtn.clicked.connect(self.SaveTransformsBtnPressed)
        self.ui.SetTransformBtn.clicked.connect(self.SetTransformBtnPressed)
        self.ui.LoadTransformsBtn.clicked.connect(self.LoadTransformsBtnPressed)
        self.ui.ResetTransformBtn.clicked.connect(self.ResetTransformBtnPressed)
        self.TramsformDic = {}

    def GetTransformBtnPressed(self):
        selection = cmds.ls(sl=True)
        self.TramsformDic = RMUncategorized.ObjectTransformDic(selection)
        print ("saving file to: %s" % (self.DiskCachePath))
        SaveDic = {'type': 'ObjectTransforms', 'data': self.TramsformDic}
        if not os.path.exists(self.Directory):
            os.makedirs(self.Directory)
        with open(self.DiskCachePath, 'w') as outfile:
            json.dump(SaveDic, outfile, sort_keys=True, indent=4)

    def SaveTransformsBtnPressed(self):
        selection = cmds.ls(sl=True)
        self.TramsformDic = RMUncategorized.ObjectTransformDic(selection)
        SaveDic = {'type': 'ObjectTransforms', 'data': self.TramsformDic}
        if not os.path.exists(self.Directory):
            os.makedirs(self.Directory)
        fname = QFileDialog.getSaveFileName(parent=self, caption='Save Filename As',
                                                  dir=unicode(self.Directory))  # self.Directory
        print fname
        with open(fname[0], 'w') as outfile:
            json.dump(SaveDic, outfile, sort_keys=True, indent=4)

    def SetTransformBtnPressed(self):
        self.TramsformDic = {}
        with open(self.DiskCachePath, 'r') as outfile:
            OpenDic = json.load(outfile)
        if OpenDic != u'':
            if OpenDic.has_key('data') and OpenDic.has_key('type'):
                if OpenDic['type'] == str('ObjectTransforms'):
                    self.TramsformDic = OpenDic['data']
                    RMUncategorized.SetObjectTransformDic(self.TramsformDic)
                    print (self.TramsformDic)
                else:
                    print ("File loaded not Valid")
        else:
            print ("No File Selected")
            # if self.TramsformDic!={}:
            #	RMUncategorized.SetObjectTransformDic(self.TramsformDic)
            # else:
            #	print"No Data Dic Loaded on memory"

    def LoadTransformsBtnPressed(self):
        self.TramsformDic = {}
        fname = QFileDialog.getOpenFileName(parent=self, caption='Open file', dir=self.Directory)
        fname[0]
        with open(fname[0], 'r') as outfile:
            OpenDic = json.load(outfile)
        if OpenDic != u'':
            if OpenDic.has_key('data') and OpenDic.has_key('type'):
                if OpenDic['type'] == str('ObjectTransforms'):
                    self.TramsformDic = OpenDic['data']
                    RMUncategorized.SetObjectTransformDic(self.TramsformDic)
                    print ("File Loaded succesfully")
                    print (self.TramsformDic)
                else:
                    print ("File loaded not Valid")
        else:
            print ("No File Selected")

    def ResetTransformBtnPressed(self):
        selection = cmds.ls(sl=True)
        RMUncategorized.ResetPostoZero(selection)


if __name__ == '__main__':
    w = main()
    w.show()
