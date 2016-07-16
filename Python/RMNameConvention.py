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
	def RMTypeValidation(self, Obj):
		if Obj in self.TypeDictionary.values():
			return Obj
		else:
			if Obj in self.TypeDictionary.keys():
				return self.TypeDictionary[Obj]
			else:
				return self.TypeDictionary["undefined"]

	def RMGetFromName(self, ObjName,Token):
		splitString = ObjName.split("_")
		return splitString[self.NameConvention[Token]]

	def RMSetFromName(self, ObjName, TextString, Token, mode = "regular"):
		'Valid Modes are regular and add'
		returnTuple = ()
		if (type (ObjName) == str) or (type (ObjName) == unicode):
			ObjectList = [ObjName]
		elif (type(ObjName) == list):
			ObjectList = ObjName
		else :
			ObjectList=[]
		for eachObj in ObjectList:
			splitString = eachObj.split("_")
			if mode == 'regular':
				if Token == "Type":
					splitString[self.NameConvention[Token]] = self.TypeDictionary[TextString]
				else:
					splitString[self.NameConvention[Token]] = TextString
			elif mode == 'add':
				splitString[self.NameConvention[Token]] = self.RMAddToNumberedString( splitString[self.NameConvention[Token]], TextString)
			returnTuple += tuple(  ["_".join(splitString)] )
		if len(returnTuple) == 1:
			return str(returnTuple[0])
		else:
			return returnTuple

	def RMRenameSetFromName (self, ObjName, TextString, Token, mode = "regular"):
		newName = self.RMSetFromName( ObjName, TextString, Token, mode = mode)
		newName = self.RMUniqueName( newName)
		cmds.rename (ObjName, newName)
		return newName


	def RMStringPlus1 (self, NameString):
		Value = re.split(r"([0-9]+$)",NameString)
		Name = Value[0]
		if len(Value)>=2:
			Number=str(int(Value[1]) + 1)
		else:
			Number = "0"
		return Name + Number.zfill(2)

	def RMAddToNumberedString(self, Name, AddName):
		Value = re.split(r"([0-9]+$)",Name)
		return Value[0] + (AddName.title()) + Value[1]

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

		Type = self.RMTypeValidation(Type)

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
			if (len(NewNameArray) == 1):
				return NewNameArray[0]
			return NewNameArray

	def RMIsNameInFormat (self, ObjName):
		splitString = ObjName.split("_")
		if len(splitString)==len(self.NameConvention.keys()):
			return True
		return False

	def RMGuessObjType(self, Obj):
		ObjType=""
		
		ObjType = cmds.objectType(Obj)

		ObjType = self.RMTypeValidation(ObjType)

		if ObjType == "transform":
			children = cmds.listRelatives(Obj, shapes=True)
			if children:
				ShapeType = cmds.objectType(children[0])
				if ShapeType == "nurbsCurve":
					ObjType = self.TypeDictionary["nurbsCurve"]
				elif ShapeType == "mesh":
					ObjType = self.TypeDictionary["mesh"]
				elif ShapeType == "locator":
					ObjType = self.TypeDictionary["locator"]
				else:
					ObjType=self.TypeDictionary["transform"]
			else :
				return ObjType
		return ObjType

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
		else:
			return False

#NameConv = RMNameConvention()
#NewName = NameConv.RMGuessObjType("joint1")




#
#print NameConv.RMSetFromName ("Character01_LF_pinky00_jnt_Rig",NameConv.RMStringPlus1("pinky"), 'Name')