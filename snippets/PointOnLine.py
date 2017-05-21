import maya.cmds as cmds
import RMRigTools
def createTwoPointsLineConstraint ( referencePoint01, referencePoint02, OriginObject):
	groupOrigin = cmds.group(empty=True, name="LineOrigin")
	resultPoint = cmds.group(empty=True, name="ResultPoint")
	resultPointConstrained = cmds.group(empty=True, name="ResultPointHeightConstrained")
	group1 = cmds.group(empty=True, name="LineReferencePoint01")
	group2 = cmds.group(empty=True, name="LineReferencePoint02")
	cmds.parentConstraint( referencePoint01, group1     , mo = False )
	cmds.parentConstraint( referencePoint02, group2     , mo = False )
	cmds.parentConstraint( OriginObject    , groupOrigin, mo = False )

	cmds.parent(group1                , groupOrigin)
	cmds.parent(group2                , groupOrigin)
	cmds.parent(resultPoint           , groupOrigin)
	cmds.parent(resultPointConstrained, groupOrigin)
	RMRigTools.RMAlign(resultPointConstrained, groupOrigin, 3)

	Substract01 = cmds.shadingNode('plusMinusAverage', asUtility = True, name = "LineSubstract01")
	Substract02 = cmds.shadingNode('plusMinusAverage', asUtility = True, name = "LineSubstract02")
	Substract03 = cmds.shadingNode('plusMinusAverage', asUtility = True, name = "LineSubstract03")
	Divide      = cmds.shadingNode('multiplyDivide'  , asUtility = True, name = "LineDivide01")
	multiply    = cmds.shadingNode('multiplyDivide'  , asUtility = True, name = "LineMultiply01")
	Adition01   = cmds.shadingNode('plusMinusAverage', asUtility = True, name = "Adition01")

	cmds.setAttr    ("%s.operation" % Substract01, 2)
	cmds.setAttr    ("%s.operation" % Substract02, 2)
	cmds.setAttr    ("%s.operation" % Substract03, 2)

	cmds.connectAttr("%s.translateX"% resultPointConstrained, "%s.translateX" % resultPoint)
	cmds.connectAttr("%s.translateY"% group1, "%s.input1D[0]"%Substract01)
	cmds.connectAttr("%s.translateY"% group2, "%s.input1D[1]"%Substract01)
	cmds.connectAttr("%s.translateX"% group1, "%s.input1D[0]"%Substract02)
	cmds.connectAttr("%s.translateX"% group2, "%s.input1D[1]"%Substract02)
	
	cmds.connectAttr("%s.translateX"% resultPoint, "%s.input1D[0]"%Substract03)
	cmds.connectAttr("%s.translateX"% group2     , "%s.input1D[1]"%Substract03)

	cmds.setAttr    ("%s.operation" % Divide, 2)
	cmds.connectAttr("%s.output1D"  % Substract03, "%s.input1X" % Divide)
	cmds.connectAttr("%s.output1D"  % Substract02, "%s.input2X" % Divide)

	cmds.connectAttr("%s.output1D"  % Substract01, "%s.input1X" % multiply)
	cmds.connectAttr("%s.outputX"   % Divide     , "%s.input2X" % multiply)

	cmds.connectAttr("%s.outputX" % multiply     , "%s.input1D[0]" % Adition01)
	cmds.connectAttr("%s.translateY"% group2     , "%s.input1D[1]" % Adition01)
	cmds.connectAttr("%s.output1D" % Adition01   , "%s.translateY" % resultPoint)

selection = cmds.ls (selection = True)
createTwoPointsLineConstraint(selection[0],selection[1],selection[2])









	




	












