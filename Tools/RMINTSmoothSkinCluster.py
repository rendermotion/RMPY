import importlib
import maya.cmds as cmds
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.OpenMayaUI as mui
import pymel.core as pm
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6 import __version__
from shiboken6 import wrapInstance
from RMPY.rig import rigBase
from RMPY.Tools.QT6.ui import FormSmoothSurfaces

importlib.reload(FormSmoothSurfaces)


def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(int(ptr), QMainWindow)


class Main(MayaQWidgetDockableMixin, QDialog):
    def __init__(self, NameConv=None, parent=None):
        self.rm = rigBase.RigBase()
        super(Main, self).__init__(parent=getMayaWindow())
        self.joint_list = []
        self.nurbs_surface = None
        self.ui = FormSmoothSurfaces.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('Smooth skincluster')
        self.ui.joint_list_btn.clicked.connect(self.set_joint_list)
        self.ui.select_joints_btn.clicked.connect(self.select_joints_pressed)
        self.ui.set_selected_surface_btn.clicked.connect(self.set_selected_surface_btn_pressed)
        self.ui.create_surface_btn.clicked.connect(self.create_surface_btn_pressed)

    @property
    def smooth_surfaces(self):
        smooth_surfaces = pm.ls('smooth_surfaces')
        if smooth_surfaces:
            return smooth_surfaces[0]
        else:
            return pm.group(empty=True, name='smooth_surfaces')

    @property
    def creation_history(self):
        smooth_surfaces = pm.ls('creation_history')
        if smooth_surfaces:
            return smooth_surfaces[0]
        else:
            new_group = pm.group(empty=True, name='creation_history')
            new_group.setParent(self.smooth_surfaces)
            return new_group

    def set_joint_list(self):
        selection = cmds.ls(selection=True)
        if selection:
            self.joint_list = selection
            self.rm.setup_name_convention_node_base(selection[0])

            if len(str(selection)) > 20:
                self.ui.joint_list_btn.setText(str(f'{selection[0:20]}...'))
            else:
                self.ui.joint_list_btn.setText(str(selection))
            self.ui.joint_list_btn.setToolTip(str(selection))

    def select_joints_pressed(self):
        cmds.select(self.joint_list, add=True)

    def set_selected_surface_btn_pressed(self):
        selection = pm.ls(selection=True)
        if selection:
            if pm.objectType(selection[0]) == 'nurbsSurface':
                self.ui.set_selected_surface_btn.setText(str(selection[0].getParent()))
                self.nurbs_surface = selection[0].getParent()
            elif selection[0].getShapes():
                if pm.objectType(selection[0].getShapes()[0]) == 'nurbsSurface':
                    self.ui.set_selected_surface_btn.setText(str(selection[0]))
                    self.nurbs_surface = selection[0]
                else:
                    print('select a nurbs surface before pressing the button')

            else:
                print('select a nurbs surface before pressing the button')

    def create_surface_btn_pressed(self):
        path_curve = self.rm.create.curve.point_base(*self.joint_list,
                                                     periodic=self.ui.periodic_curve_chk.isChecked(),
                                                     ep=True)
        print (self.ui.radius_spnbox)
        path_curve.setParent(self.creation_history)
        loft_circle, make_circle = pm.circle()
        pm.extrude(loft_circle, path_curve,
                   polygon=0,  # output is nurbs surface
                   extrudeType=2,
                   useComponentPivot=0,
                   fixedPath=1,
                   useProfileNormal=1,
                   rotation=0,
                   scale=1,
                   reverseSurfaceIfPathReversed=1)


if __name__ == '__main__':
    Main().show()
