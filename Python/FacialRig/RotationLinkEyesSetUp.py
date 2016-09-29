import maya.cmds as cmds
import RMRigTools
import RMNameConvention
reload (RMRigTools)

def LinkEyes (EyeNode):
	Rigtools = RMRigTools.RMRigTools()
	EyeNodeBB = RMRigTools.boundingBoxInfo(EyeNode)
	eyeRadius = (EyeNodeBB.zmax - EyeNodeBB.zmin)/2

	eyeScale = cmds.getAttr("%s.scale"%EyeNode) [0]

	cmds.setAttr ( EyeNode + ".scale", 1.0, 1.0, 1.0)

	MainUpperLid = cmds.joint(name = "EyeMainUpperLid", rad = eyeRadius / 5)
	UpperLid     = cmds.joint(name = "EyeUpperLidTip" , rad = eyeRadius / 5)
	MainLowerLid = cmds.joint(name = "MainEyeLowerLid", rad = eyeRadius / 5)
	LowerLid     = cmds.joint(name = "EyeLowerLidTip" , rad = eyeRadius / 5)
	RMRigTools.RMAlign(EyeNode, MainUpperLid, 3)
	EyeParent    = Rigtools.RMCreateGroupOnObj(MainUpperLid)
	cmds.parent( MainLowerLid, EyeParent)
	RMRigTools.RMAlign(EyeParent, LowerLid,3)

	MiddleMainUpperLid = cmds.joint( name = "EyeMiddleMainUpperLid", rad = eyeRadius / 5)
	MiddleUpperLid     = cmds.joint( name = "EyeMiddleUpperLidTip" , rad = eyeRadius / 5)
	MiddleMainLowerLid = cmds.joint( name = "MainMiddleEyeLowerLid", rad = eyeRadius / 5)
	MiddleLowerLid     = cmds.joint( name = "EyeMiddleLowerLidTip" , rad = eyeRadius / 5)
	RMRigTools.RMAlign(EyeParent, MiddleMainUpperLid,3)
	cmds.parent( MiddleMainUpperLid, EyeParent )
	cmds.parent( MiddleMainLowerLid, EyeParent )
	
	cmds.setAttr("%s.translateX"%UpperLid, eyeRadius)
	cmds.setAttr("%s.translateX"%LowerLid, eyeRadius)
	cmds.setAttr("%s.translateX"%MiddleUpperLid, eyeRadius)
	cmds.setAttr("%s.translateX"%MiddleLowerLid, eyeRadius)

	mDUpper = cmds.shadingNode("multiplyDivide",asUtility = True)
	cmds.connectAttr("%s.rotate"%MainUpperLid ,"%s.input1"%mDUpper)
	cmds.setAttr("%s.input2"%mDUpper, .5,.5,.5)
	cmds.connectAttr("%s.output"%mDUpper , "%s.rotate"%MiddleMainUpperLid)

	mDLower = cmds.shadingNode("multiplyDivide",asUtility = True)
	cmds.connectAttr          ("%s.rotate"%MainLowerLid ,"%s.input1"%mDLower)
	cmds.setAttr              ("%s.input2"%mDLower, .5,.5,.5)
	cmds.connectAttr          ("%s.output"%mDLower , "%s.rotate"%MiddleMainLowerLid)

	cmds.setAttr(EyeParent +".scale",eyeScale[0],eyeScale[1],eyeScale[2])

	cmds.select(EyeNode, replace=True)
	latticeAttr, lattice, latticeBase = cmds.lattice(name = "EyeLattice", oc= True, dv = [2, 2, 2], ol =  2, ofd = (eyeRadius/3) )
	latticeScale = cmds.getAttr(lattice+".scale")[0]
	cmds.setAttr ( lattice + ".scale", float(latticeScale[0]) + float(eyeScale[0]), float(latticeScale[1]) + float(eyeScale[1]), float(latticeScale[2]) + float(eyeScale[2]))


LinkEyes("pSphere1")





	




