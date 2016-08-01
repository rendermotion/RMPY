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

def RMCreateCubeLine (height, length, width,centered = False,offsetX = 0 ,offsetY = 0, offsetZ = 0,name=""):
	if centered == True:
		offsetX = -height/2
	if name=="":
		defaultName = "CubeLine"
	else :
		defaultName = name

	CubeCurve = []
	CubeCurve.append(cmds.curve (d = 1, p = [[0     + offsetX, -length/2+ offsetY,  width/2+ offsetZ],[0     + offsetX, -length/2+ offsetY, -width/2+ offsetZ]], name = defaultName))
	CubeCurve.append(cmds.curve (d = 1, p = [[height+ offsetX, -length/2+ offsetY,  width/2+ offsetZ],[height+ offsetX, -length/2+ offsetY, -width/2+ offsetZ]], name = defaultName))
	CubeCurve.append(cmds.curve (d = 1, p = [[0     + offsetX,  length/2+ offsetY,  width/2+ offsetZ],[0     + offsetX,  length/2+ offsetY, -width/2+ offsetZ]], name = defaultName))
	CubeCurve.append(cmds.curve (d = 1, p = [[height+ offsetX,  length/2+ offsetY,  width/2+ offsetZ],[height+ offsetX,  length/2+ offsetY, -width/2+ offsetZ]], name = defaultName))
	CubeCurve.append(cmds.curve (d = 1, p = [[0     + offsetX, -length/2+ offsetY,  width/2+ offsetZ],[height+ offsetX, -length/2+ offsetY,  width/2+ offsetZ]], name = defaultName))
	CubeCurve.append(cmds.curve (d = 1, p = [[0     + offsetX,  length/2+ offsetY, -width/2+ offsetZ],[height+ offsetX,  length/2+ offsetY, -width/2+ offsetZ]], name = defaultName))
	CubeCurve.append(cmds.curve (d = 1, p = [[0     + offsetX, -length/2+ offsetY, -width/2+ offsetZ],[height+ offsetX, -length/2+ offsetY, -width/2+ offsetZ]], name = defaultName))
	CubeCurve.append(cmds.curve (d = 1, p = [[0     + offsetX,  length/2+ offsetY,  width/2+ offsetZ],[height+ offsetX,  length/2+ offsetY,  width/2+ offsetZ]], name = defaultName))
	CubeCurve.append(cmds.curve (d = 1, p = [[0     + offsetX, -length/2+ offsetY, -width/2+ offsetZ],[0     + offsetX,  length/2+ offsetY, -width/2+ offsetZ]], name = defaultName))
	CubeCurve.append(cmds.curve (d = 1, p = [[0     + offsetX, -length/2+ offsetY,  width/2+ offsetZ],[0     + offsetX,  length/2+ offsetY,  width/2+ offsetZ]], name = defaultName))
	CubeCurve.append(cmds.curve (d = 1, p = [[height+ offsetX, -length/2+ offsetY, -width/2+ offsetZ],[height+ offsetX,  length/2+ offsetY, -width/2+ offsetZ]], name = defaultName))
	CubeCurve.append(cmds.curve (d = 1, p = [[height+ offsetX, -length/2+ offsetY,  width/2+ offsetZ],[height+ offsetX,  length/2+ offsetY,  width/2+ offsetZ]], name = defaultName))
	RMTurnToOne(CubeCurve)
	return CubeCurve[0]

def RMCreateBoxCtrl (Obj, NameConv = None, Xratio = 1 ,Yratio = 1 ,Zratio = 1, ParentBaseSize = False, customSize = 0,  name = ""):
	if not NameConv:
		NameConv = RMNameConvention.RMNameConvention()
	if name=="":
		defaultName = "BoxControl"
	else:
		defaultName = name

	Parents = cmds.listRelatives (Obj, parent = True)

	if Parents and len(Parents) != 0 and ParentBaseSize == True:
		JntLength = RMRigTools.RMLenghtOfBone (Parents[0])
		Ctrl = RMCreateCubeLine (JntLength * Xratio, JntLength * Yratio, JntLength * Zratio, name = defaultName)
	else:
		if customSize!=0:
			JntLength = customSize

		elif cmds.objectType(Obj) == "joint":
			JntLength = RMRigTools.RMLenghtOfBone(Obj)

		else:
			JntLength = 1
		Ctrl = RMCreateCubeLine (JntLength * Xratio, JntLength * Yratio, JntLength * Zratio, name = defaultName)

	if name == '' and NameConv.RMIsNameInFormat(Obj):
		Ctrl = NameConv.RMRenameBasedOnBaseName(Obj,Ctrl)
	else:
		Ctrl = NameConv.RMRenameNameInFormat(Ctrl)
	Ctrl = NameConv.RMRenameSetFromName (Ctrl,"control","Type")

	RMRigTools.RMAlign(Obj, Ctrl, 3)
	ResetGroup = RMRigTools.RMCreateGroupOnObj(Ctrl)
	return ResetGroup , Ctrl

def RMCircularControl (Obj, radius = 1,NameConv = None, axis = "X", name = ""):
	if not NameConv:
		NameConv = RMNameConvention.RMNameConvention()
	if name == '':
		defaultName = "circularControl"
	else :
		defaultName = name
	if axis in "yY":
		Ctrl, Shape = cmds.circle( normal = [0,1,0],radius=radius, name = defaultName)
	elif axis in "zZ":
		Ctrl, Shape = cmds.circle( normal = [0,0,1],radius=radius, name = defaultName)
	elif axis in "xX":
		Ctrl, Shape = cmds.circle( normal = [1,0,0],radius=radius, name = defaultName)
	
	if name == '' and NameConv.RMIsNameInFormat(Obj):

		Ctrl = NameConv.RMRenameBasedOnBaseName(Obj,Ctrl)
	else:

		Ctrl = NameConv.RMRenameNameInFormat(Ctrl)

	Ctrl = NameConv.RMRenameSetFromName (Ctrl,"control","Type")

	RMRigTools.RMAlign(Obj,Ctrl,3)
	ResetGroup = RMRigTools.RMCreateGroupOnObj(Ctrl)
	return ResetGroup , Ctrl
	

def RMImportMoveControl(Obj, scale = 1,NameConv = None, name = ''):
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
	if name != '':
		Ctrl = cmds.rename( Ctrl, name)

	cmds.setAttr( Ctrl + ".scale", scale, scale, scale)

	cmds.makeIdentity( Ctrl, apply = True, t = 1, r = 1, s = 1)

	if name != '' and NameConv.RMIsNameInFormat(Obj):

		Ctrl = NameConv.RMRenameBasedOnBaseName(Obj,Ctrl)

	else :

		Ctrl = NameConv.RMRenameNameInFormat(Ctrl)

	Ctrl = NameConv.RMRenameSetFromName (Ctrl, "control", "Type")

	RMRigTools.RMAlign(Obj,Ctrl,3)
	fosterParent = cmds.listRelatives(Ctrl,parent = True)
	ParentGroup = RMRigTools.RMCreateGroupOnObj(Ctrl)
	cmds.delete(fosterParent)
	return ParentGroup , Ctrl



#RMImportMoveControl ("locator",scale = 3)

	