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
    from RMPY.Tools.QT5.ui import FormSpaceSwitch

except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide import __version__
    from shiboken import wrapInstance
    from RMPY.Tools.QT4.ui import FormSpaceSwitch
import maya.mel as mel
import os
import maya.cmds as cmds
from RMPY.AutoRig import RMSpaceSwitch


def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QMainWindow)


class main(MayaQWidgetDockableMixin,QDialog):
    def __init__(self, parent=None):
        super(main, self).__init__(parent=getMayaWindow())

        self.ui = FormSpaceSwitch.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('Space Switch Tool')
        self.SSw = RMSpaceSwitch.RMSpaceSwitch()

        self.ui.LoadSelectionAsCntrlObjPushBtn.clicked.connect(self.LoadSelectionAsControl)

        self.ui.AddToObjectSpacePushBtn.clicked.connect(self.AddToObjectSpace)
        self.ui.RemoveFromObjectSpaceBtn.clicked.connect(self.RemoveFromObjectSpace)

        self.ui.RemoveFromConstrainedBtn.clicked.connect(self.RemoveFromConstrained)
        self.ui.AddToConstrainListPushBtn.clicked.connect(self.AddToConstrainList)
        self.ui.CreateSpaceSwitchBtn.clicked.connect(self.CreateSpaceSwitch)

        self.ui.AddToObjectSpacePushBtn.setDisabled(True)
        self.ui.RemoveFromObjectSpaceBtn.setDisabled(True)
        self.ui.AddToConstrainListPushBtn.setDisabled(True)
        self.ui.RemoveFromConstrainedBtn.setDisabled(True)

    # self.ui.LoadSelectionAsCntrlObjPushBtn.clicked.connect(self.LoadSelectionAsControl)

    def LoadSelectionAsControl(self):
        selectedObject = cmds.ls(sl=True)
        if len(selectedObject) >= 1:
            self.ui.ControllineEdit.setText(selectedObject[0])
            if self.SSw.IsSpaceSwitch(selectedObject[0]):
                self.RedrawLists(selectedObject[0])
                self.ui.CreateSpaceSwitchBtn.setDisabled(True)

                self.ui.AddToObjectSpacePushBtn.setEnabled(True)
                self.ui.RemoveFromObjectSpaceBtn.setEnabled(True)
                self.ui.AddToConstrainListPushBtn.setEnabled(True)
                self.ui.RemoveFromConstrainedBtn.setEnabled(True)

            else:
                self.ui.CreateSpaceSwitchBtn.setEnabled(True)
                self.ui.ObjectSpaceListView.clear()
                self.ui.ConstrainedObjectListView.clear()

                self.ui.AddToObjectSpacePushBtn.setEnabled(True)
                self.ui.RemoveFromObjectSpaceBtn.setEnabled(True)
                self.ui.AddToConstrainListPushBtn.setEnabled(True)
                self.ui.RemoveFromConstrainedBtn.setEnabled(True)

        else:
            self.ui.ObjectSpaceListView.clear()
            self.ui.ConstrainedObjectListView.clear()
            self.ui.ControllineEdit.setText("")

            self.ui.AddToObjectSpacePushBtn.setDisabled(True)
            self.ui.RemoveFromObjectSpaceBtn.setDisabled(True)
            self.ui.AddToConstrainListPushBtn.setDisabled(True)
            self.ui.RemoveFromConstrainedBtn.setDisabled(True)

    def RedrawLists(self, Control):
        if self.SSw.IsSpaceSwitch(Control):
            ObjectAffected = self.SSw.GetAfectedObjectsList(Control)
            self.ui.ConstrainedObjectListView.clear()

            self.addToList(ObjectAffected, self.ui.ConstrainedObjectListView)

            SpaceObject = self.SSw.GetSpaceObjectsList(Control)

            self.ui.ObjectSpaceListView.clear()
            self.addToList(SpaceObject, self.ui.ObjectSpaceListView)
        else:
            self.ui.CreateSpaceSwitchBtn.setEnabled(True)
            self.ui.ObjectSpaceListView.clear()
            self.ui.ConstrainedObjectListView.clear()

    def AddToObjectSpace(self):
        selectedObject = cmds.ls(sl=True)
        CntrlObject = self.ui.ControllineEdit.text()
        if len(selectedObject) >= 1:

            if self.SSw.IsSpaceSwitch(CntrlObject):
                for eachObject in selectedObject:
                    self.SSw.AddSpaceObject(CntrlObject, eachObject)
                self.RedrawLists(CntrlObject)
            else:
                for eachObject in selectedObject:
                    self.addToList([eachObject], self.ui.ObjectSpaceListView)

    def RemoveFromConstrained(self):
        selectedObject = cmds.ls(sl=True)
        CntrlObject = self.ui.ControllineEdit.text()

        if len(selectedObject) >= 1:

            if self.SSw.IsSpaceSwitch(CntrlObject):

                self.SSw.RemoveAffectedObject(CntrlObject, selectedObject[0])

                self.RedrawLists(CntrlObject)

            else:
                for eachSelected in selectedObject:
                    self.removeFromList(eachSelected, self.ui.ConstrainedObjectListView)

    def AddToConstrainList(self):
        selectedObject = cmds.ls(sl=True)
        CntrlObject = self.ui.ControllineEdit.text()
        if len(selectedObject) >= 1:
            if self.SSw.IsSpaceSwitch(CntrlObject):
                self.SSw.AddAffectedObject(CntrlObject, selectedObject[0])
                self.RedrawLists(CntrlObject)
            else:
                for eachObject in selectedObject:
                    self.addToList([eachObject], self.ui.ConstrainedObjectListView)

    def CreateSpaceSwitch(self):
        Control = self.ui.ControllineEdit.text()
        ConstrainedObjects = self.getItemList(self.ui.ConstrainedObjectListView)
        SpaceObjects = self.getItemList(self.ui.ObjectSpaceListView)
        self.SSw.CreateSpaceSwitch(ConstrainedObjects[0], SpaceObjects, Control)

        for eachObject in range(1, len(ConstrainedObjects)):
            self.SSw.AddAffectedObject(Control, ConstrainedObjects[eachObject])
        self.RedrawLists(Control)

    def RemoveFromObjectSpace(self):
        selectedObject = cmds.ls(sl=True)
        CntrlObject = self.ui.ControllineEdit.text()
        if len(selectedObject) >= 1:
            if self.SSw.IsSpaceSwitch(CntrlObject):
                self.SSw.RemoveSpaceObject(CntrlObject, selectedObject[0])
                self.RedrawLists(CntrlObject)
            else:
                for eachObject in selectedObject:
                    self.removeFromList(eachObject, self.ui.ObjectSpaceListView)

    def removeFromList(self, removeString, Qlist):
        ItemCount = Qlist.count()
        for ItemIndex in range(0, ItemCount):
            Item = Qlist.item(ItemIndex)
            if Item.text() == removeString:
                Qlist.takeItem(ItemIndex)
                break

    def getItemList(self, Qlist):
        returnedList = []
        ItemCount = Qlist.count()
        for ItemIndex in range(0, ItemCount):
            Item = Qlist.item(ItemIndex)
            returnedList.append(Item.text())
        return returnedList

    def addToList(self, stringList, Qlist):
        for elements in stringList:
            Qlist.addItem(elements)


if __name__ == '__main__':
    w = main()
    w.show()
