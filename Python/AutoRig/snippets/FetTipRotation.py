import maya.cmds as cmds
import RMRigTools

def FetTipRotationCorrect(side="RH"):
	#"Character_LF_TipGrp00_UDF_Rig"
	#"Character01_LF_ankleIK00_ctr_Rig"
	#"Character_LF_TipGrp00_grp_Rig"
	ArrayOfChildren = RMRigTools.RMRemoveChildren ( "Character_%s_TipGrp00_UDF_Rig"%side)
	childGroup = RMRigTools.RMCreateGroupOnObj("Character_%s_TipGrp00_UDF_Rig"%side,Type="world")
	ParentConst = cmds.listConnections("Character_%s_TipGrp00_grp_Rig"%side,type = "parentConstraint")
	cmds.delete(ParentConst[0])
	cmds.makeIdentity("Character_%s_TipGrp00_grp_Rig"%side)
	loc = cmds.spaceLocator(name  = "ReferencePoint")[0]
	cmds.setAttr( "%s.rotateY"%loc, -90)
	RMRigTools.RMAlign( loc , "Character_%s_TipGrp00_grp_Rig"%side, 2 )
	cmds.parentConstraint("Character01_%s_ankleIK00_ctr_Rig"%side, "Character_%s_TipGrp00_grp_Rig"%side, mo = True, name = ParentConst[0])
	cmds.parent(childGroup, "Character_%s_TipGrp00_UDF_Rig"%side)
	RMRigTools.RMParentArray (childGroup , ArrayOfChildren )
	cmds.delete(loc)







