import importlib
import maya.cmds as cmds
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.OpenMayaUI as mui
import pymel.core as pm
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2 import __version__
from shiboken2 import wrapInstance
from RMPY.rig import rigBase
from RMPY.Tools.QT6.ui import FormSmoothSurfaces
from RMPY.core import smooth_skin
import json
importlib.reload(smooth_skin)
importlib.reload(FormSmoothSurfaces)


def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(int(ptr), QMainWindow)


class Main(MayaQWidgetDockableMixin, QDialog):
    def __init__(self, NameConv=None, parent=None):
        self.rm = rigBase.RigBase()
        super(Main, self).__init__(parent=getMayaWindow())
        self._joint_list = []
        self.nurbs_surface = None
        self.ui = FormSmoothSurfaces.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('Smooth skincluster')
        self.ui.joint_list_btn.clicked.connect(self.set_joint_list_btn_pressed)
        self.ui.select_joints_btn.clicked.connect(self.select_joints_pressed)
        self.ui.set_selected_surface_btn.clicked.connect(self.set_selected_surface_btn_pressed)
        self.ui.create_surface_btn.clicked.connect(self.create_surface_btn_pressed)
        self.ui.radius_SpinBox.valueChanged.connect(self.radius_value_change)
        self.ui.smooth_btn.clicked.connect(self.smooth_skin_btn_pressed)


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

    def set_joint_list_btn_pressed(self):
        selection = cmds.ls(selection=True)
        if selection:
            self.joint_list = selection

    @property
    def joint_list(self):
        return self._joint_list

    @joint_list.setter
    def joint_list(self, joint_list):
        self._joint_list = joint_list
        self.rm.setup_name_convention_node_base(joint_list[0])
        if len(str(joint_list)) > 20:
            self.ui.joint_list_btn.setText(str('{}...'.format(str(joint_list)[0:20])))
        else:
            self.ui.joint_list_btn.setText(str(joint_list).replace("',", "',\n"))
        self.ui.joint_list_btn.setToolTip(str(joint_list).replace("',", "',\n"))

    def select_joints_pressed(self):
        cmds.select(self.joint_list, add=True)

    def set_selected_surface_btn_pressed(self):
        selection = pm.ls(selection=True)
        if selection:
            if pm.objectType(selection[0]) == 'nurbsSurface':
                self.ui.set_selected_surface_btn.setText(str(selection[0].getParent()))
                self.nurbs_surface = selection[0].getParent()
                self.load_metadata_from_nurbs_surface(selection[0].getParent())
            elif selection[0].getShapes():
                if pm.objectType(selection[0].getShapes()[0]) == 'nurbsSurface':
                    self.ui.set_selected_surface_btn.setText(str(selection[0]))
                    self.nurbs_surface = selection[0]
                    self.load_metadata_from_nurbs_surface(selection[0])
                else:
                    print('select a nurbs surface before pressing the button')

            else:
                print('select a nurbs surface before pressing the button')

    def create_surface_btn_pressed(self):
        path_curve = self.rm.create.curve.point_base(*self.joint_list,
                                                     periodic=self.ui.periodic_curve_chk.isChecked(),
                                                     ep=True)
        path_curve.setParent(self.creation_history)
        loft_circle, make_circle = pm.circle(radius = self.ui.radius_SpinBox.value())
        self.rm.name_convention.rename_name_in_format(loft_circle, make_circle, name='circle')
        loft_circle.setParent(self.creation_history)

        extrude = pm.extrude(loft_circle, path_curve,
                   polygon=0,  # output is nurbs surface
                   extrudeType=2,
                   constructionHistory=True,
                   useComponentPivot=0,
                   fixedPath=1,
                   useProfileNormal=1,
                   rotation=0,
                   scale=1,
                   reverseSurfaceIfPathReversed=1)[0]
        extrude = pm.reverseSurface(extrude,  d = 3 , ch = 1, rpo = 1)[0]
        extrude.setParent(self.smooth_surfaces)
        self.rm.name_convention.rename_name_in_format(extrude, name='smoothSurface')
        self.nurbs_surface = extrude
        self.ui.set_selected_surface_btn.setText(str(extrude))
        self.add_metadata_to_surface()


    def load_metadata_from_nurbs_surface(self, nurbs_surface, update_list=True):
        if 'notes' in pm.listAttr(nurbs_surface):
            if update_list:
                self.joint_list = json.loads(nurbs_surface.notes.get())
            return json.loads(nurbs_surface.notes.get())
        return None


    def smooth_skin_btn_pressed(self):
        selection = pm.ls(selection=True)
        for each in selection:
            skin_cluster = smooth_skin.SmoothSkin().by_geometry(str(each))
            skin_cluster.surface = str(self.nurbs_surface)
            skin_cluster.smooth([str(each) for each in self.joint_list])

    def radius_value_change(self):
        surface_button = pm.ls(self.ui.set_selected_surface_btn.text())
        if surface_button:
            create_curve = pm.listHistory(surface_button[0], type='makeNurbCircle')
            if create_curve:
                create_curve.radius.set(self.ui.radius_SpinBox.value())


    def add_metadata_to_surface(self):
        if 'notes' not in pm.listAttr(self.nurbs_surface):
            pm.addAttr(self.nurbs_surface, ln='notes', type='string')
        self.nurbs_surface.notes.set(json.dumps(self.joint_list))


if __name__=='__main__':
    Main().show()
