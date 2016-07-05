import re
import maya.cmds as cmds

class RMNameConvention ():
	def __init__(self):
		self.NameConvention  = {	"LastName":0,
						"Side":1,
						"Name":2,
						"Type":3,
						"System":4
	 					}
		self.TypeDictionary = {"joint":"jnt",
		"undefined":"UDF",
		"nurbsCurve":"shp",
		"mesh":"msh",
		"transform":"grp"
		}

	def RMGetTypeString(self, Obj):
		if cmds.objectType(Obj) in self.TypeDictionary:
			return self.TypeDictionary[cmds.objectType(Obj)]
		else:
			return self.TypeDictionary["undefined"]

	def RMGetFromName(self, ObjName,Token):
		splitString = ObjName.split("_")
		return splitString[self.NameConvention[Token]]

	def RMSetFromName(self, ObjName, TextString, Token):

		splitString = ObjName.split("_")
		splitString[self.NameConvention[Token]]=TextString
		return "_".join(splitString)

	def RMStringPlus1 (self, NameString):
		Value = re.split(r"([0-9]+$)",NameString)
		Name = Value[0]
		if len(Value)>=2:
			Number=str(int(Value[1]) + 1)
		else:
			Number = "0"
		return Name + Number.zfill(2)

	def RMUniqueName(self, currentName):
		ObjName=self.RMGetFromName(currentName,'Name')
		Value = re.split(r"([0-9]+$)",ObjName)
		Name = Value[0]

		currentName = self.RMSetFromName (currentName, self.RMStringPlus1(Name), 'Name')
		while(cmds.objExists(currentName)):
			Name = self.RMStringPlus1(Name)
			currentName = self.RMSetFromName(currentName,Name,'Name')
		return currentName

	def RMSetNameInFormat(self, Name,LastName,Side,Type,System):
		NameDic = {
		"LastName":LastName,
		"Name":Name,
		"Side":Side,
		"Type":Type,
		"System":System
		}
		returnName = []
		for keys in sorted(self.NameConvention , key = self.NameConvention.get):
			returnName.append(NameDic[keys])
		ReturnNameInFormat = "_".join(returnName)
		return self.RMUniqueName(ReturnNameInFormat)

	def RMIsNameInFormat(self, ObjName):
		splitString = ObjName.split("_")
		if len(splitString)==len(self.NameConvention.keys()):
			return True
		return False

	def RMGuessObjType(self, Obj):
		Type=self.TypeDictionary["undefined"]
		ObjType = cmds.objectType(Obj)
		for Types in self.TypeDictionary:
			if ObjType ==Types:
				Type = self.TypeDictionary[Types]
		if ObjType=="transform":
			children = cmds.listRelatives(Obj, shapes=True)
			if children:
				ShapeType = cmds.objectType(children[0])
				if ShapeType == "nurbsCurve":
					Type="shp"
				elif ShapeType == "mesh":
					Type="msh"
				else:
					Type="SHPUNDEF"
		return Type

	def RMRenameGuessTypeInName(self, currentName):
		NewName = currentName
		if cmds.objExists(NewName):
			if self.RMIsNameInFormat(NewName):
				Type = self.RMGuessObjType(currentName)
				NewName = self.RMSetFromName(NewName,Type,"Type")
		cmds.rename(currentName, self.RMUniqueName(NewName))


	def RMRenameBasedOnBaseName (self, BaseName, ObjToRename, NewName = None, LastName = None,Type = None, System = None, Side = None):

		if not NewName:
			NewName = self.RMGetFromName (BaseName, "Name")
			print NewName
		if not LastName:
			LastName = self.RMGetFromName (BaseName, "LastName")
			print LastName
		if not System:
			System = self.RMGetFromName (BaseName, "System")
			print System
		if not Side:
			Side = self.RMGetFromName (BaseName, "Side")
			print Side
		if not Type:
			Type = self.RMGuessObjType(ObjToRename)
			print Type
		if cmds.objExists(ObjToRename):
			NewName = self.RMSetNameInFormat(NewName, LastName, Side, Type, System)
			cmds.rename (ObjToRename , NewName)
			return NewName
		else :
			return False


