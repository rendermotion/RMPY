import maya.cmds as cmds
import RMRigTools
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
	CubeCurve.append(cmds.curve (d = 1, p = [[height, -length/2,  width/2],[height, -length/2, -width/2]]))
	CubeCurve.append(cmds.curve (d = 1, p = [[0     ,  length/2,  width/2],[0     ,  length/2, -width/2]]))
	CubeCurve.append(cmds.curve (d = 1, p = [[height,  length/2,  width/2],[height,  length/2, -width/2]]))
	CubeCurve.append(cmds.curve (d = 1, p = [[0     , -length/2,  width/2],[height, -length/2,  width/2]]))
	CubeCurve.append(cmds.curve (d = 1, p = [[0     ,  length/2, -width/2],[height,  length/2, -width/2]]))
	CubeCurve.append(cmds.curve (d = 1, p = [[0     , -length/2, -width/2],[height, -length/2, -width/2]]))
	CubeCurve.append(cmds.curve (d = 1, p = [[0     ,  length/2,  width/2],[height,  length/2,  width/2]]))
	CubeCurve.append(cmds.curve (d = 1, p = [[0     , -length/2, -width/2],[0     ,  length/2, -width/2]]))
	CubeCurve.append(cmds.curve (d = 1, p = [[0     , -length/2,  width/2],[0     ,  length/2,  width/2]]))
	CubeCurve.append(cmds.curve (d = 1, p = [[height, -length/2, -width/2],[height,  length/2, -width/2]]))
	CubeCurve.append(cmds.curve (d = 1, p = [[height, -length/2,  width/2],[height,  length/2,  width/2]]))
	RMTurnToOne(CubeCurve)
	return CubeCurve[0]

def RMCreateBoxCtrl (Obj, NameConv=None):
	if not NameConv:
		NameConv = RMNameConvention.RMNameConvention()
	JntLength = RMRigTools.RMLenghtOfBone(Obj)
	if (JntLength != 1.0):
		Ctrl = RMCreateCubeLine (JntLength, JntLength/4, JntLength/4)
	else:
		Parents = cmds.listRelatives (Obj, parents = True)
		if len(Parents)!= 0:
			print Parents[0]
			LenghtJoint = RMRigTools.RMLenghtOfBone (Parents[0])
		else :
			LenghtJoint = 1
		Ctrl = RMCreateCubeLine (JntLength/4, JntLength/4, JntLength/4)

	Ctrl = NameConv.RMRenameNameInFormat (Ctrl, Type = "control")

	RMRigTools.RMAlign(Obj, Ctrl, 3)
	return Ctrl

def RMCircularControl (Obj, radius = 1,NameConv = None):
	if not NameConv:
		NameConv = RMNameConvention.RMNameConvention()
	Ctrl, Shape = cmds.circle( normal = [1,0,0],radius=radius, name='circularControl')
	Ctrl = NameConv.RMRenameNameInFormat (Ctrl, Type = "control")
	RMAlign(Obj,Ctrl,3)
	return Ctrl
RMCreateBoxCtrl('joint1')




	