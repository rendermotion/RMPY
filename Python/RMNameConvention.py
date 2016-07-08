import re
import maya.cmds as cmds

class RMNameConvention (object):
	def __init__(self,LastName = "Character", Side = "MD", Name = "Object", Type = "UDF", System = "Rig"):

		self.NameConvention  ={
						"LastName":0,
						"Name":2,
						"Side":1,
						"Type":3,
						"System":4
	 					}

		self.TypeDictionary = { 
							"joint":"jnt",
						    "undefined":"UDF",
							"nurbsCurve":"shp",
							"mesh":"msh",
							"transform":"grp",
							"pointConstraint":"pnc",
							"control":"ctr",
							"locator":"loc"
							}
		self.DefaultNames = {	
				"LastName":LastName,
				"Side":Side,
				"Name":Name,
				"Type":Type,
				"System":System
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
	def RMAddToNumberedString(self, Name, AddName):
		Value = re.split(r"([0-9]+$)",ObjName)
		return Value[0] + AddName + Value[0]

	def RMUniqueName(self, currentName):
		ObjName=self.RMGetFromName(currentName,'Name')
		Value = re.split(r"([0-9]+$)",ObjName)
		Name = Value[0]

		currentName = self.RMSetFromName (currentName, self.RMStringPlus1(Name), 'Name')
		while(cmds.objExists(currentName)):
			Name = self.RMStringPlus1(Name)
			currentName = self.RMSetFromName(currentName,Name,'Name')
		return currentName
	def RMGetTypeFromKey(self,Type):
		if Type in self.TypeDictionary:
			return self.TypeDictionary[Type]
		else:
			return self.TypeDictionary['undefined']

	
	def RMSetNameInFormat(self, Name=None , LastName=None, Side=None, Type=None, System=None):
		if not Name:
			Name = self.DefaultNames["Name"] 
		if not LastName:
			LastName = self.DefaultNames["LastName"] 
		if not Side:
			Side = self.DefaultNames["Side"] 
		if not Type:
			Type = self.DefaultNames["Type"] 
		if not System:
			System = self.DefaultNames["System"] 

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

	def RMRenameNameInFormat (self, Name, LastName=None, Side=None, Type=None, System=None):
			NewNameArray = ()
			NameList = []
			if type(Name) == list:
				NameList = Name
			elif type(Name) in [str,unicode]:
				NameList = [Name]

			else:
				print 'Error no Valid type on RMRenameNameInFromat should be string or list'
			for Names in NameList:
				NewName = self.RMSetNameInFormat(Name=Names, LastName=LastName, Side=Side, Type=Type, System=System)
				Names = cmds.rename(Names,NewName)
				if not Type:
					NewNameArray += tuple([self.RMRenameGuessTypeInName (Names)])
				else :
					NewNameArray += tuple([Names])

			return NewNameArray

	def RMIsNameInFormat (self, ObjName):
		splitString = ObjName.split("_")
		if len(splitString)==len(self.NameConvention.keys()):
			return True
		return False

	def RMGuessObjType(self, Obj):
		Type=""
		
		ObjType = cmds.objectType(Obj)

		if ObjType in self.TypeDictionary: 
			Type = self.TypeDictionary[ObjType]
		else:
			Type = self.TypeDictionary["undefined"]

		if ObjType == "transform":
			children = cmds.listRelatives(Obj, shapes=True)
			if children:
				ShapeType = cmds.objectType(children[0])
				if ShapeType == "nurbsCurve":
					Type = self.TypeDictionary["nurbsCurve"]
				elif ShapeType == "mesh":
					Type = self.TypeDictionary["mesh"]
				elif ShapeType == "locator":
					Type = self.TypeDictionary["locator"]
				else:
					Type=self.TypeDictionary["transform"]
		return Type

	def RMRenameGuessTypeInName(self, currentName):
		NewName = currentName
		if cmds.objExists(NewName):
			if self.RMIsNameInFormat(NewName):
				Type = self.RMGuessObjType(currentName)
				NewName = self.RMSetFromName(NewName,Type,"Type")
		NewName=self.RMUniqueName(NewName)
		cmds.rename (currentName, NewName)
		return NewName

	def RMRenameBasedOnBaseName (self, BaseName, ObjToRename, NewName = None, LastName = None,Type = None, System = None, Side = None):

		if self.RMIsNameInFormat (BaseName):
			if not NewName:
				NewName = self.RMGetFromName (BaseName, "Name")
			if not LastName:
				LastName = self.RMGetFromName (BaseName, "LastName")
			if not System:
				System = self.DefaultNames["System"]
			if not Side:
				Side = self.RMGetFromName (BaseName, "Side")
			if not Type:
				Type = self.RMGuessObjType(ObjToRename)
		else:
			if not NewName:
				NewName = ObjToRename
			if not LastName:
				LastName = self.DefaultNames("LastName")
			if not System:
				System = self.DefaultNames("System")
			if not Side:
				Side = self.DefaultNames("Side")
			if not Type:
				Type = self.RMGuessObjType(ObjToRename)

		if cmds.objExists(ObjToRename):
			NewName = self.RMSetNameInFormat(Name = NewName, LastName = LastName,Side = Side,Type = Type, System = System)
			cmds.rename (ObjToRename , NewName)
			return NewName
		else :
			return False


