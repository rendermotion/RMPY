import maya.cmds as cmds
import RMRigTools


def supportScaleOnRig():
	cmds.scaleConstraint( "worldMainCharacter","Character01_LF_curveLineBetweenPnts00_shp_Rig")
	cmds.scaleConstraint( "worldMainCharacter","Character01_LF_curveLineBetweenPnts01_shp_Rig")
	cmds.scaleConstraint( "worldMainCharacter","Character01_RH_curveLineBetweenPnts00_shp_Rig")
	cmds.scaleConstraint( "worldMainCharacter","Character01_RH_curveLineBetweenPnts01_shp_Rig")

	cmds.scaleConstraint( "Character_MD_mainPlacer00_ctr_Rig","Character01_RH_palm00_grp_Rig")
	cmds.scaleConstraint( "Character_MD_mainPlacer00_ctr_Rig","Character01_LF_palm00_grp_Rig")
	cmds.scaleConstraint( "Character_MD_mainPlacer00_ctr_Rig","joints")
	cmds.scaleConstraint( "Character_MD_mainPlacer00_ctr_Rig","deformation")

	#Avoid Spine Scale 
	cmds.parent         ( "Character01_MD_spineIKCurve00_shp_Rig" , "kinematics")

	#ikFixing

	cmds.connectAttr(  "Character01_MD_StretchyIkHandleStartPoint00_loc_Rig.translate", "Character01_RH_IKBaseDistanceNodewrist00_dbtw_Rig.point1", force = True)
	cmds.connectAttr(  "Character01_MD_StretchyIkHandleEndPoint00_loc_Rig.translate",   "Character01_RH_IKBaseDistanceNodewrist00_dbtw_Rig.point2", force = True)

	cmds.connectAttr(  "Character01_MD_StretchyIkHandleStartPoint01_loc_Rig.translate", "Character01_LF_IKBaseDistanceNodewrist00_dbtw_Rig.point1", force = True)
	cmds.connectAttr(  "Character01_MD_StretchyIkHandleEndPoint01_loc_Rig.translate",   "Character01_LF_IKBaseDistanceNodewrist00_dbtw_Rig.point2", force = True)

	cmds.connectAttr(  "Character01_MD_StretchyIkHandleStartPoint03_loc_Rig.translate", "Character01_LF_IKBaseDistanceNodeankle00_dbtw_Rig.point1", force = True)
	cmds.connectAttr(  "Character01_MD_StretchyIkHandleEndPoint03_loc_Rig.translate",   "Character01_LF_IKBaseDistanceNodeankle00_dbtw_Rig.point2", force = True)
	
	cmds.connectAttr(  "Character01_MD_StretchyIkHandleStartPoint02_loc_Rig.translate", "Character01_RH_IKBaseDistanceNodeankle00_dbtw_Rig.point1", force = True)
	cmds.connectAttr(  "Character01_MD_StretchyIkHandleEndPoint02_loc_Rig.translate",   "Character01_RH_IKBaseDistanceNodeankle00_dbtw_Rig.point2", force = True)

	#TwistJointFixing
	
	cmds.scaleConstraint ( "Character_MD_mainPlacer00_ctr_Rig", "Character01_RH_StretchyRefPointsShoulder00_grp_Rig")
	cmds.connectAttr(  "Character01_MD_startTwistShoulder00_loc_Rig.translate", "Character01_RH_DistanceNode00_dbtw_Rig.point1", force = True)
	cmds.connectAttr(  "Character01_MD_endTwistShoulder00_loc_Rig.translate",   "Character01_RH_DistanceNode00_dbtw_Rig.point2", force = True)

	cmds.scaleConstraint ( "Character_MD_mainPlacer00_ctr_Rig", "Character01_RH_StretchyRefPointsElbow00_grp_Rig")
	cmds.connectAttr(  "Character01_MD_startTwistElbow00_loc_Rig.translate", "Character01_RH_DistanceNode01_dbtw_Rig.point1", force = True)
	cmds.connectAttr(  "Character01_MD_endTwistElbow00_loc_Rig.translate",   "Character01_RH_DistanceNode01_dbtw_Rig.point2", force = True)

	cmds.scaleConstraint ( "Character_MD_mainPlacer00_ctr_Rig", "Character01_LF_StretchyRefPointsShoulder00_grp_Rig")
	cmds.connectAttr(  "Character01_MD_startTwistShoulder01_loc_Rig.translate", "Character01_LF_DistanceNode00_dbtw_Rig.point1", force = True)
	cmds.connectAttr(  "Character01_MD_endTwistShoulder01_loc_Rig.translate",   "Character01_LF_DistanceNode00_dbtw_Rig.point2", force = True)
	
	cmds.scaleConstraint ( "Character_MD_mainPlacer00_ctr_Rig", "Character01_LF_StretchyRefPointsElbow00_grp_Rig")
	cmds.connectAttr(  "Character01_MD_startTwistElbow01_loc_Rig.translate", "Character01_LF_DistanceNode01_dbtw_Rig.point1", force = True)
	cmds.connectAttr(  "Character01_MD_endTwistElbow01_loc_Rig.translate",   "Character01_LF_DistanceNode01_dbtw_Rig.point2", force = True)

	cmds.scaleConstraint ( "Character_MD_mainPlacer00_ctr_Rig", "Character01_RH_StretchyRefPointsLeg00_grp_Rig")	
	cmds.connectAttr(  "Character01_MD_startTwistLeg00_loc_Rig.translate", "Character01_RH_DistanceNode02_dbtw_Rig.point1", force = True)
	cmds.connectAttr(  "Character01_MD_endTwistLeg00_loc_Rig.translate",   "Character01_RH_DistanceNode02_dbtw_Rig.point2", force = True)
	
	cmds.scaleConstraint ( "Character_MD_mainPlacer00_ctr_Rig", "Character01_RH_StretchyRefPointsKnee00_grp_Rig")	
	cmds.connectAttr(  "Character01_MD_startTwistKnee00_loc_Rig.translate", "Character01_RH_DistanceNode03_dbtw_Rig.point1", force = True)
	cmds.connectAttr(  "Character01_MD_endTwistKnee00_loc_Rig.translate",   "Character01_RH_DistanceNode03_dbtw_Rig.point2", force = True)

	cmds.scaleConstraint ( "Character_MD_mainPlacer00_ctr_Rig", "Character01_LF_StretchyRefPointsLeg00_grp_Rig")
	cmds.connectAttr(  "Character01_MD_startTwistLeg01_loc_Rig.translate", "Character01_LF_DistanceNode02_dbtw_Rig.point1", force = True)
	cmds.connectAttr(  "Character01_MD_endTwistLeg01_loc_Rig.translate",   "Character01_LF_DistanceNode02_dbtw_Rig.point2", force = True)

	cmds.scaleConstraint ( "Character_MD_mainPlacer00_ctr_Rig", "Character01_LF_StretchyRefPointsKnee00_grp_Rig")
	cmds.connectAttr(  "Character01_MD_startTwistKnee01_loc_Rig.translate", "Character01_LF_DistanceNode03_dbtw_Rig.point1", force = True)
	cmds.connectAttr(  "Character01_MD_endTwistKnee01_loc_Rig.translate",   "Character01_LF_DistanceNode03_dbtw_Rig.point2", force = True)

	cmds.addAttr("Character_MD_mainPlacer00_ctr_Rig", at="float", ln = "GlobalScale", h = 0, k = 1)
	cmds.setAttr ("Character_MD_mainPlacer00_ctr_Rig.GlobalScale",1)

	RMRigTools.RMLockAndHideAttributes("Character_MD_mainPlacer00_ctr_Rig", "xxxxxxhhhx")
	cmds.connectAttr( "Character_MD_mainPlacer00_ctr_Rig.GlobalScale","Character_MD_mainPlacer00_ctr_Rig.scaleX")
	cmds.connectAttr( "Character_MD_mainPlacer00_ctr_Rig.GlobalScale","Character_MD_mainPlacer00_ctr_Rig.scaleY")
	cmds.connectAttr( "Character_MD_mainPlacer00_ctr_Rig.GlobalScale","Character_MD_mainPlacer00_ctr_Rig.scaleZ")

	cmds.shadingNode("multiplyDivide", asUtility = True, name = "Character_MD_SpineGlobalScale00_mult_Rig")
	cmds.connectAttr ("Character_MD_SpineCurveOriginalInfo00_cui_Rig.arcLength", "Character_MD_SpineGlobalScale00_mult_Rig.input1X")
	cmds.connectAttr ("Character_MD_mainPlacer00_ctr_Rig.GlobalScale",           "Character_MD_SpineGlobalScale00_mult_Rig.input2X")
	cmds.connectAttr ("Character_MD_SpineGlobalScale00_mult_Rig.outputX", "Character_MD_SpineScaleRatio00_mult_Rig.input2X", force = True)


