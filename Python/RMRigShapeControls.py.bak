import maya.cmds as cmds
import RMRigTools
import os 
reload (RMRigTools)
import RMNameConvention
reload (RMNameConvention)

def RMTurnToOne (curveArray):
	for eachCurve in curveArray[1:]:
		shapesInCurve = cmds.listRelatives(eachCurve, s=True, children=True)
		for eachShape in shapesInCurve:
			cmds.parent (eachShape, curveArray[0], shape=True, add=True)
			cmds.delete(eachCurve)

def RMCreateCubeLine (height, length, width):
	CubeCurve = []
	CubeCurve.append(cmds.curve (d = 1, p = [[0     , -length/2,  width/2],[0     , -length/2, -width/2]], name = "cubeControl"))
	CubeCurve.append(cmds.curve (d = 1, p = [[height, -length/2,  width/2],[height, -length/2, -width/2]], name = "cubeControl"))
	CubeCurve.append(cmds.curve (d = 1, p = [[0     ,  length/2,  width/2],[0     ,  length/2, -width/2]], name = "cubeControl"))
	CubeCurve.append(cmds.curve (d = 1, p = [[height,  length/2,  width/2],[height,  length/2, -width/2]], name = "cubeControl"))
	CubeCurve.append(cmds.curve (d = 1, p = [[0     , -length/2,  width/2],[height, -length/2,  width/2]], name = "cubeControl"))
	CubeCurve.append(cmds.curve (d = 1, p = [[0     ,  length/2, -width/2],[height,  length/2, -width/2]], name = "cubeControl"))
	CubeCurve.append(cmds.curve (d = 1, p = [[0     , -length/2, -width/2],[height, -length/2, -width/2]], name = "cubeControl"))
	CubeCurve.append(cmds.curve (d = 1, p = [[0     ,  length/2,  width/2],[height,  length/2,  width/2]], name = "cubeControl"))
	CubeCurve.append(cmds.curve (d = 1, p = [[0     , -length/2, -width/2],[0     ,  length/2, -width/2]], name = "cubeControl"))
	CubeCurve.append(cmds.curve (d = 1, p = [[0     , -length/2,  width/2],[0     ,  length/2,  width/2]], name = "cubeControl"))
	CubeCurve.append(cmds.curve (d = 1, p = [[height, -length/2, -width/2],[height,  length/2, -width/2]], name = "cubeControl"))
	CubeCurve.append(cmds.curve (d = 1, p = [[height, -length/2,  width/2],[height,  length/2,  width/2]], name = "cubeControl"))
	RMTurnToOne(CubeCurve)
	return CubeCurve[0]

def RMCreateBoxCtrl (Obj, NameConv = None, Xratio = 1 ,Yratio = 1 ,Zratio = 1, ParentBaseSize = False ):
	if not NameConv:
		NameConv = RMNameConvention.RMNameConvention()

	Parents = cmds.listRelatives (Obj, parent = True)

	if len(Parents) != 0 and ParentBaseSize == True:
		JntLength = RMRigTools.RMLenghtOfBone (Parents[0])
		Ctrl = RMCreateCubeLine (JntLength * Xratio, JntLength * Yratio, JntLength * Zratio)
	else:
		JntLength = RMRigTools.RMLenghtOfBone(Obj)
		Ctrl = RMCreateCubeLine (JntLength * Xratio, JntLength * Yratio, JntLength * Zratio)

	Ctrl = NameConv.RMRenameBasedOnBaseName(Obj,Ctrl)
	Ctrl = NameConv.RMRenameSetFromName (Ctrl,"control","Type")

	RMRigTools.RMAlign(Obj, Ctrl, 3)
	return Ctrl

def RMCircularControl (Obj, radius = 1,NameConv = None):
	if not NameConv:
		NameConv = RMNameConvention.RMNameConvention()
	Ctrl, Shape = cmds.circle( normal = [1,0,0],radius=radius, name='circularControl')

	Ctrl = NameConv.RMRenameBasedOnBaseName(Obj,Ctrl)
	Ctrl = NameConv.RMRenameSetFromName (Ctrl,"control","Type")

	RMRigTools.RMAlign(Obj,Ctrl,3)
	return Ctrl

def RMImportMoveControl(Obj, scale = 1,NameConv = None):
	if not NameConv:
		NameConv = RMNameConvention.RMNameConvention()
	path = os.path.dirname(RMRigTools.__file__)
	print path
	RMMel=os.path.split(path)
	FinalPath = os.path.join(RMMel[0],"Python\AutoRig\RigShapes","ControlMover.mb")
	if os.path.isfile(FinalPath):
		cmds.file(FinalPath,i=True,type="mayaBinary",ignoreVersion=True,mergeNamespacesOnClash=False,rpr="Control",pr=False)
	else:
		print "archivo no encontrado"
		return None
	Ctrl =  "ControlCross"
	cmds.setAttr(Ctrl + ".scale",scale,scale,scale)

	cmds.makeIdentity(Ctrl, apply = True, t = 1, r = 1, s = 1)

	Ctrl = NameConv.RMRenameBasedOnBaseName(Obj,Ctrl)

	Ctrl = NameConv.RMRenameSetFromName (Ctrl,"control","Type")

	RMRigTools.RMAlign(Obj,Ctrl,3)
	ParentGroup = RMRigTools.RMCreateGroupOnObj(Ctrl)

	return ParentGroup , Ctrl





	