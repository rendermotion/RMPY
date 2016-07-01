import re
import maya.cmds as cmds
NameConvention  = {
	"LastName":0,
	"Side":1,
	"Name":2,
	"Type":3,
	"System":4
}

TypeDictionaray = {
"joint":"jnt",
"undefined":"UDF",
"nurbsCurve":"shp",
"mesh":"msh"
"transform":"grp"

}
def RMGetFromName(ObjName,Token):
	splitString = ObjName.split("_")
	return splitString[NameConvention[Token]]

def RMSetFromName(Name,TextString,Token):
	splitString = ObjName.split("_")
	splitString[Token]=TextString
	return "_".join(splitString)

def RMStringPlus1 (NameString):
	Value = re.split(r"([0-9]+$)",NameString)
	Name = Value[0]
	if len(Value)>=2:
		Number=str(int(Value[1]) + 1)
	else:
		Number = "00"
	return Name + Number

def RMUniqueName(currentName):
	ObjName=RMGetFromName(currentName,'Name')
	Value = re.split(r"([0-9]+$)",ObjName)
	Name = Value[0]
	while(cmds.objExists(currentName)):
		currentName = RMSetFromName(currentName,RMStringPlus1(Name),'Name')
	return currentName

def RMSetNameInFormat(Name,LastName,Side,Type,System):
	NewName = RMUniqueName
	NameDic = {
	"LastName":LastName,
	"Name":Name,
	"Side":Side,
	"Type":Type,
	"System":System
	}
	returnName = []
	for keys in sorted(NameConvention , key = NameConvention.get):
		returnName.append(NameDic[keys])
	return "_".join(returnName)

def RMIsNameInFormat(ObjName):
	splitString = ObjName.split("_")
	if len(splitString)==len(NameConvention.keys()):
		return True
	return False

def RMGuessObjType(Obj):
	Type=TypeDictionary["undefined"]
	ObjType = cmds.objectType(currentName)
	for Types in TypeDictionaray:
		if ObjType ==Types:
			Type = TypeDictionaray[Types]
	if ObjType=="transform":
		children = cmds.listRelatives(currentName,shapes=True)
		if len(children) > 0:
			ShapeType = cmds.objectType(children[0])
			if ShapeType == "nurbsCurve":
				Type="shp"
			elif ShapeType == "mesh":
				Type="msh"
			else:
				Type="SHPUNDEF"
	return Type

def RMGuessTypeInName(currentName):
	NewName = currentName
	if cmds.objExists(NewName):
		if RMIsNameInFormat(NewName):
			Type = RMGuessObjType(currentName)
			NewName = RMSetFromName(NewName,Type,"Type")
	cmds.rename(currentName,RMUniqueName(NewName))

def RMGessName(Obj,NewName,LastName,System,Side="MD"):
	Type=''
	if cmds.objExists(Obj):
		Type = RMGuessObjType(Obj)
		NewName = RMSetNameInFormat(NewName,LastName,Side,Type,System)
		cmds.rename (Obj,NewName)
		return NewName
	else :
		return False


#Value=cmds.ls(sl=True)

#print RMSetNameInFormat("Danie","Object","RH","Undef","Rig")



