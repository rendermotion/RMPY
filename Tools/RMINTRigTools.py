import maya.cmds as cmds
import maya.OpenMayaUI as mui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import pymel.core as pm
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6 import __version__
from shiboken6 import wrapInstance
from RMPY.Tools.QT5.ui import FormRigTools_old
import maya.mel as mel
import os
from RMPY import RMRigTools
from RMPY.AutoRig import RMGenericJointRig
from RMPY.GenericRig import RMProgressiveConstraint
from RMPY.GenericRig import RMUnfoldRig
# sys.path.append(os.path.dirname(__file__))

from RMPY import RMUncategorized
from RMPY import nameConvention
from RMPY.rig import rigBase
from RMPY.snippets import locator_at_average
from RMPY.AutoRig import RMRigFK
from RMPY.core import transform
from RMPY.core import hierarchy
import importlib
from RMPY.core import mirror_skinning
from RMPY.Tools.QT5.ui import FormRigTools
from RMPY.core import controls
from RMPY.core import rig_core
import importlib
importlib.reload(controls)
importlib.reload(FormRigTools)



def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(int(ptr), QMainWindow)


class Main(MayaQWidgetDockableMixin, QDialog):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent=getMayaWindow())
        self.rigTools = RMRigTools.RMRigTools()
        self.ui = FormRigTools.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('RM Maya Rig Tools')
        self.ui.RenameTool.clicked.connect(self.RenameToolBtnPressed)
        # self.ui.IKOnSelection.clicked.connect(self.IKOnSelectionBtnPressed)
        # self.ui.FKOnSelection.clicked.connect(self.FKOnSelectionBtnPressed)
        self.ui.CreateChildGroup.clicked.connect(self.CreateChildGroupBtnPressed)
        self.ui.CreateParentGroup.clicked.connect(self.CreateParentBtnPressed)
        # self.ui.JointsOnPoints.clicked.connect(self.JointsOnPointsBtnPressed)
        self.ui.AlignRotation.clicked.connect(self.AlignRotationBtnPressed)
        self.ui.AlignPosition.clicked.connect(self.AlignPositionBtnPressed)
        self.ui.AlignAll.clicked.connect(self.AlignAllBtnPressed)
        self.ui.ListConnectedJoints.clicked.connect(self.ListConnectedJointsBtnPressed)
        self.ui.SelectJoints.clicked.connect(self.select_joints_btn_pressed)
        self.ui.SCCombineButton.clicked.connect(self.SCCombineButtonPressed)
        self.ui.AttributeTransferBtn.clicked.connect(self.transfer_attributes)
        self.ui.ExtractGeoBtn.clicked.connect(self.extract_geometry)
        # self.ui.GenericJointChainRigBtn.clicked.connect(self.GenericJointChainRigBtnPressed)
        self.ui.mirror_selection_btn.clicked.connect(self.mirror_selection)
        self.ui.orient_parents_btn.clicked.connect(self.orient_parents)
        self.ui.locator_at_average_btn.clicked.connect(self.locator_at_average)
        self.ui.create_locators_at_nodes_btn.clicked.connect(self.create_locators_at_nodes)
        self.ui.aim_button_btn.clicked.connect(self.aim_align)
        self.ui.hierarchy_switch_btn.clicked.connect(self.hierarchise)
        self.ui.selection_at_average_btn.clicked.connect(self.selection_at_average)
        self.ui.copy_skin_button.clicked.connect(self.copy_skinning)
        self.ui.CopyCvsPosBtn.clicked.connect(self.copy_cv_position)
        self.ui.pushButton_2.clicked.connect(self.mirror_shapes)
        self.ui.points_between_btn.clicked.connect(self.create_locators_between_points)
        self.ui.mirror_skin_button.clicked.connect(self.mirror_skinning_multiple_objects)
        self.ui.curve_point_based_btn.clicked.connect(self.curve_point_base)
        # self.ui.OrientNubButton.clicked.connect(self.OrientNubButtonPressed)
        # self.ui.unfoldRigBtn.clicked.connect(self.unfoldRigBtnPressed)

        # self.ui.ProgressiveConstraintButton.clicked.connect(self.ProgressiveConstraintButtonPressed)

        # self.ui.ConstShapeLblBtn.clicked.connect(self.AttributeTransferBtnPressed)

        # support Multiple selections on qwidgets
        self.ui.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.name_convention = nameConvention.NameConvention()
        self.rig_base = rigBase.RigBase()

    def curve_point_base(self):
        selection = pm.ls(selection=True)
        rig_core.curve.point_base(*selection,
                                  ep=self.ui.create_curve_edit_points_chkbx.isChecked(),
                                  periodic=self.ui.create_curve_periodic_chkbx.isChecked())

    def mirror_skinning_multiple_objects(self):
        selection = pm.ls(selection=True)
        mirror_skinning.mirror_skinBinding(selection)

    def copy_cv_position(self):
        controls.transfer_curve_by_selection()

    def mirror_shapes(self):
        selection = pm.ls(selection=True)
        controls.mirror_controls(*selection)
    def copy_skinning(self):
        selection = pm.ls(selection=True)
        mirror_skinning.copy_skinning(*selection)

    def hierarchise(self):
        selection = pm.ls(selection=True)
        hierarchy.reorder_hierarchy(*selection)

    def aim_align(self):
        selection = pm.ls(selection=True)
        selection.insert(0, selection[0])
        transform.aim_point_based(*selection)

    def orient_parents(self):
        selection = pm.ls(selection=True)
        if selection:
            transform.reorient_to_world(selection[0])
        else:
            print ('select the root node to orient the transforms')

    def locator_at_average(self):
        selection = pm.ls(selection=True)
        self.rig_base.create.space_locator.point_base(*selection)

    def create_locators_at_nodes(self):
        selection = pm.ls(selection=True)
        self.rig_base.create.space_locator.node_base(*selection)

    def create_locators_between_points(self):
        selection = pm.ls(selection=True)
        RMRigTools.RMCreateNLocatorsBetweenObjects(selection[0], selection[1], self.ui.spinBox.value())
    def unfoldRigBtnPressed(self):
        selection = cmds.ls(selection=True)
        RMUnfoldRig.SpiralOfPointsStraight(self.ui.initRadiusSpnBx.value(), self.ui.endRadiusSpnBx.value(),
                                           self.ui.NumberOfPointsSpnBx.value(), selection[0], selection[1])

    def RenameToolBtnPressed(self):
        mel.eval('source RMINTRenameTool.mel;')

    def IKOnSelectionBtnPressed(self):
        mel.eval('source RMRigIK.mel;')
        mel.eval('RMIKCreateonSelected();')

    def FKOnSelectionBtnPressed(self):
        # mel.eval('source RMRigFK.mel;')
        # mel.eval('RMFKCreateonSelected();')
        FKM = RMRigFK.RMRigFK()
        FKM.createOnSelection()

    def CreateChildGroupBtnPressed(self):
        # mel.eval('''source RMRigTools.mel;
        # string $temp[]=`ls -sl`;
        # RMCreateGrouponObj $temp[0] 2;''')
        selection = cmds.ls(selection=True)
        for eachObject in selection:
            RMRigTools.RMCreateGroupOnObj(eachObject, Type='child')

    def GenericJointChainRigBtnPressed(self):
        selection = cmds.ls(selection=True)
        GJR = RMGenericJointRig.RMGenericJointChainRig()
        GJR.CreateJointChainRig(selection[0], UDaxis="Z")

    def OrientNubButtonPressed(self):
        selection = cmds.ls(selection=True)
        RMGenericJointRig.lastTwoJointsInChain(selection)

    def CreateParentBtnPressed(self):
        selection = cmds.ls(selection=True)
        paretnType = ''
        if selection:
            if self.ui.parentRadio.isChecked() == True:
                paretnType = 'parent'
            if self.ui.worldRadio.isChecked() == True:
                paretnType = 'world'
            if self.ui.insertedRadio.isChecked() == True:
                paretnType = 'inserted'

        for eachObject in selection:
            RMRigTools.RMCreateGroupOnObj(eachObject, Type=paretnType)

    def ProgressiveConstraintButtonPressed(self):
        selection = cmds.ls(selection=True)
        ConstraintType = 'parent'
        if selection:
            if self.ui.CnstParentRadio.isChecked() == True:
                ConstraintType = 'parent'
            if self.ui.CnstOrientRadio.isChecked() == True:
                ConstraintType = 'orient'
            if self.ui.CnstPointRadio.isChecked() == True:
                ConstraintType = 'point'
        if self.ui.mantainOffsetChk.isChecked() == True:
            mo = True
        else:
            mo = False
        deepth = self.ui.ProgressiveDepthSpinBox.value()

        RMProgressiveConstraint.deepthProgressiveconstraint(deepth, selection, constraintType=ConstraintType, mo=mo)

    def JointsOnPointsBtnPressed(self):
        selection = cmds.ls(selection=True)
        self.rigTools.RMCreateBonesAtPoints(selection)

    # RMCreateBonesAtPoints $temp;''')
    def AlignPositionBtnPressed(self):
        selection = cmds.ls(selection=True)
        for each in selection[:-1]:
            RMRigTools.RMAlign(selection[-1], each, 1)

    # mel.eval('''source RMRigTools.mel;
    # string $temp[]=`ls -sl`;
    # RMAlign $temp[1] $temp[0] 1;''')

    def AlignRotationBtnPressed(self):
        selection = cmds.ls(selection=True)
        for each in selection[:-1]:
            RMRigTools.RMAlign(selection[-1], each, 2)

    # mel.eval('''source RMRigTools.mel;
    # string $temp[]=`ls -sl`;
    # RMAlign $temp[1] $temp[0] 2;''')
    def AlignAllBtnPressed(self):
        selection = cmds.ls(selection=True)
        for each in selection[:-1]:
            RMRigTools.RMAlign(selection[-1], each, 3)

    # mel.eval('''source RMRigTools.mel;
    # string $temp[]=`ls -sl`;
    # RMAlign $temp[1] $temp[0] 3;''')
    def ListConnectedJointsBtnPressed(self):
        self.ui.listWidget.clear()
        selection = cmds.ls(sl=True)
        for eachObject in selection:
            returned = mel.eval('''source RMRigSkinTools.mel;
			$value =  `getSkinInfluence("''' + eachObject + '''")`;''')
            for i in returned:
                self.ui.listWidget.addItem(i)

    def select_joints_btn_pressed(self):
        Array = self.ui.listWidget.selectedItems()
        cmds.select(clear=True)
        for g in (Array):
            cmds.select(g.text(), add=True)

    @staticmethod
    def SCCombineButtonPressed():
        mel_script = 'source RMRigShapeControls.mel;\n'
        mel_script += 'string $temp[]=`ls -sl`;\n'
        mel_script += 'turn_to_one $temp;\n'
        mel.eval(mel_script)

    @staticmethod
    def transfer_attributes():
        mel_script = 'source RMAttributes.mel;\n'
        mel_script += 'string $temp[] = `ls - sl`;\n'
        mel_script += ' TransferAllAttr $temp[0] $temp[1];\n'
        mel.eval(mel_script)

    def extract_geometry(self):
        RMUncategorized.ExtractGeometry()

    def mirror_selection(self):
        scene_transforms_list = pm.ls(selection=True)
        for eachObject in scene_transforms_list:
            object_transform_dic = RMUncategorized.ObjectTransformDic([eachObject])
            side = self.name_convention.get_from_name(eachObject, "side")
            if side == "R":
                oposit_object = self.name_convention.set_from_name(str(eachObject), "L", "side")
                if cmds.objExists(oposit_object):
                    RMUncategorized.SetObjectTransformDic({oposit_object: object_transform_dic[str(eachObject)]},
                                                          MirrorTranslateX=1, MirrorTranslateY=1, MirrorTranslateZ=-1,
                                                          MirrorRotateX=-1, MirrorRotateY=-1, MirrorRotateZ=1)
                else:
                    print ('object not found %s' % oposit_object)
            else:
                oposit_object = self.name_convention.set_from_name(str(eachObject), "R", "side")
                if cmds.objExists(oposit_object):
                    RMUncategorized.SetObjectTransformDic({oposit_object: object_transform_dic[str(eachObject)]},
                                                          MirrorTranslateX=1, MirrorTranslateY=1, MirrorTranslateZ=-1,
                                                          MirrorRotateX=-1, MirrorRotateY=-1, MirrorRotateZ=1)
                else:
                    print ('object not found %s' % oposit_object)

    @staticmethod
    def selection_at_average():
        selection = pm.ls(selection=True)
        locator_at_average.move_to_average_vertices(selection)



if __name__ == '__main__':
    w = Main()
    w.show()
