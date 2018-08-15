import maya.cmds as cmds
from RMPY import RMRigTools


def supportScaleOnRig():
    cmds.scaleConstraint("worldMainCharacter", "L_curveLineBetweenPnts00_Limbik_shp")
    cmds.scaleConstraint("worldMainCharacter", "L_curveLineBetweenPnts01_Limbik_shp")
    cmds.scaleConstraint("worldMainCharacter", "R_curveLineBetweenPnts00_Limbik_shp")
    cmds.scaleConstraint("worldMainCharacter", "R_curveLineBetweenPnts01_Limbik_shp")

    cmds.scaleConstraint("C_mainPlacer00_Rig_ctr", "R_palm00_Rig_grp")
    cmds.scaleConstraint("C_mainPlacer00_Rig_ctr", "L_palm00_Rig_grp")
    cmds.scaleConstraint("C_mainPlacer00_Rig_ctr", "joints")
    cmds.scaleConstraint("C_mainPlacer00_Rig_ctr", "deformation")

    # Avoid Spine Scale
    cmds.parent("C_spineIKCurve00_Rig_shp", "kinematics")

    # ikFixing

    cmds.connectAttr("C_Object00_Rig_pnt.translate",
                     "R_IKBaseDistanceNodewrist00_Limbik_dbtw.point1", force=True)
    cmds.connectAttr("C_Object01_Rig_pnt.translate",
                     "R_IKBaseDistanceNodewrist00_Limbik_dbtw.point2", force=True)

    cmds.connectAttr("C_Object06_Rig_pnt.translate",
                     "L_IKBaseDistanceNodewrist00_Limbik_dbtw.point1", force=True)
    cmds.connectAttr("C_Object07_Rig_pnt.translate",
                     "L_IKBaseDistanceNodewrist00_Limbik_dbtw.point2", force=True)

    cmds.connectAttr("C_Object18_Rig_pnt.translate",
                     "L_IKBaseDistanceNodeankle00_Limbik_dbtw.point1", force=True)
    cmds.connectAttr("C_Object19_Rig_pnt.translate",
                     "L_IKBaseDistanceNodeankle00_Limbik_dbtw.point2", force=True)

    cmds.connectAttr("C_Object12_Rig_pnt.translate",
                     "R_IKBaseDistanceNodeankle00_Limbik_dbtw.point1", force=True)
    cmds.connectAttr("C_Object13_Rig_pnt.translate",
                     "R_IKBaseDistanceNodeankle00_Limbik_dbtw.point2", force=True)

    # TwistJointFixing

    cmds.scaleConstraint("C_mainPlacer00_Rig_ctr", "R_StretchyRefPointsShoulder00_Limbskn_grp")
    cmds.connectAttr("C_Object02_Rig_pnt.translate",
                     "R_DistanceNode00_Limbskn_dbtw.point1", force=True)
    cmds.connectAttr("C_Object03_Rig_pnt.translate",
                     "R_DistanceNode00_Limbskn_dbtw.point2", force=True)

    cmds.scaleConstraint("C_mainPlacer00_Rig_ctr", "R_StretchyRefPointsElbow00_Limbskn_grp")
    cmds.connectAttr("C_Object04_Rig_pnt.translate",
                     "R_DistanceNode01_Limbskn_dbtw.point1", force=True)
    cmds.connectAttr("C_Object05_Rig_pnt.translate",
                     "R_DistanceNode01_Limbskn_dbtw.point2", force=True)

    cmds.scaleConstraint("C_mainPlacer00_Rig_ctr", "L_StretchyRefPointsShoulder00_Limbskn_grp")
    cmds.connectAttr("C_Object08_Rig_pnt.translate",
                     "L_DistanceNode00_Limbskn_dbtw.point1", force=True)
    cmds.connectAttr("C_Object09_Rig_pnt.translate",
                     "L_DistanceNode00_Limbskn_dbtw.point2", force=True)

    cmds.scaleConstraint("C_mainPlacer00_Rig_ctr", "L_StretchyRefPointsElbow00_Limbskn_grp")
    cmds.connectAttr("C_Object10_Rig_pnt.translate",
                     "L_DistanceNode01_Limbskn_dbtw.point1", force=True)
    cmds.connectAttr("C_Object08_Rig_pnt.translate",
                     "L_DistanceNode01_Limbskn_dbtw.point2", force=True)

    cmds.scaleConstraint("C_mainPlacer00_Rig_ctr", "R_StretchyRefPointsLeg00_Limbskn_grp")
    cmds.connectAttr("C_Object14_Rig_pnt.translate",
                     "R_DistanceNode02_Limbskn_dbtw.point1", force=True)
    cmds.connectAttr("C_Object15_Rig_pnt.translate", "R_DistanceNode02_Limbskn_dbtw.point2",
                     force=True)

    cmds.scaleConstraint("C_mainPlacer00_Rig_ctr", "R_StretchyRefPointsKnee00_Limbskn_grp")
    cmds.connectAttr("C_Object16_Rig_pnt.translate",
                     "R_DistanceNode03_Limbskn_dbtw.point1", force=True)
    cmds.connectAttr("C_Object17_Rig_pnt.translate", "R_DistanceNode03_Limbskn_dbtw.point2",
                     force=True)

    cmds.scaleConstraint("C_mainPlacer00_Rig_ctr", "L_StretchyRefPointsLeg00_Limbskn_grp")
    cmds.connectAttr("C_Object20_Rig_pnt.translate",
                     "L_DistanceNode02_Limbskn_dbtw.point1", force=True)
    cmds.connectAttr("C_Object21_Rig_pnt.translate", "L_DistanceNode02_Limbskn_dbtw.point2",
                     force=True)

    cmds.scaleConstraint("C_mainPlacer00_Rig_ctr", "L_StretchyRefPointsKnee00_Limbskn_grp")
    cmds.connectAttr("C_Object22_Rig_pnt.translate",
                     "L_DistanceNode03_Limbskn_dbtw.point1", force=True)
    cmds.connectAttr("C_Object23_Rig_pnt.translate", "L_DistanceNode03_Limbskn_dbtw.point2",
                     force=True)

    cmds.addAttr("C_mainPlacer00_Rig_ctr", at="float", ln="GlobalScale", h=0, k=1)
    cmds.setAttr("C_mainPlacer00_Rig_ctr.GlobalScale", 1)

    RMRigTools.RMLockAndHideAttributes("C_mainPlacer00_Rig_ctr", "xxxxxxhhhx")
    cmds.connectAttr("C_mainPlacer00_Rig_ctr.GlobalScale", "C_mainPlacer00_Rig_ctr.scaleX")
    cmds.connectAttr("C_mainPlacer00_Rig_ctr.GlobalScale", "C_mainPlacer00_Rig_ctr.scaleY")
    cmds.connectAttr("C_mainPlacer00_Rig_ctr.GlobalScale", "C_mainPlacer00_Rig_ctr.scaleZ")

    cmds.shadingNode("multiplyDivide", asUtility=True, name="C_SpineGlobalScale00_Rig_mult")
    cmds.connectAttr("C_SpineCurveOriginalInfo00_Rig_cui.arcLength",
                     "C_SpineGlobalScale00_Rig_mult.input1X")
    cmds.connectAttr("C_mainPlacer00_Rig_ctr.GlobalScale",
                     "C_SpineGlobalScale00_Rig_mult.input2X")
    cmds.connectAttr("C_SpineGlobalScale00_Rig_mult.outputX",
                     "C_SpineScaleRatio00_Rig_mult.input2X", force=True)


supportScaleOnRig()
