import maya.cmds as cmds

def ObjectTransformDic(objects):
	ObjectDic={}
	for eachObject in objects:
		Address=eachObject.split("|")
		if len(Address)== 1:
			position =(cmds.getAttr(eachObject+".t"))
			rotation = (cmds.getAttr(eachObject+".r"))
			scale = (cmds.getAttr(eachObject+".s"))
			objectName=eachObject.split(":",1)
			if (len(objectName)>1):
				ObjectDic[objectName[1]]={"t":position[0], "r":rotation[0],"s":scale[0]}
			else:
				ObjectDic[eachObject]={"t":position[0], "r":rotation[0],"s":scale[0]}
	return ObjectDic
def ResetPostoZero(objects):
	for eachObject in objects:
		try:
			cmds.setAttr(eachObject+".t",0,0,0)
		except:
			None
		try:
			cmds.setAttr(eachObject+".r",0,0,0)
		except:
			None
		try:
			cmds.setAttr(eachObject+".s",1,1,1)
		except:
			None
def SetObjectTransformDic(OTDic):
	for keys in OTDic:
		FocusObject = ignoreNamespace(keys)
		if FocusObject:
			try:
				cmds.setAttr(FocusObject+".t",OTDic[keys]["t"][0],OTDic[keys]["t"][1],OTDic[keys]["t"][2])
			except:
				None
			try:
				cmds.setAttr(FocusObject+".r",OTDic[keys]["r"][0],OTDic[keys]["r"][1],OTDic[keys]["r"][2])
			except:
				None
			try:
				cmds.setAttr(FocusObject+".s",OTDic[keys]["s"][0],OTDic[keys]["s"][1],OTDic[keys]["s"][2])
			except:
				None
		else:
			print "No Object Matches name:"
			print keys
def ignoreNamespace(Name):
	if cmds.objExists(str(Name)):
		return str(Name)
	else:
		filter = cmds.itemFilter(byName="*"+str(Name))
		FocusObject = cmds.lsThroughFilter(filter)
		if FocusObject:
			if len(FocusObject)>0:
				if len(FocusObject)==1:
					return FocusObject[0]
				else:
					print ("More than one object matches Name:"+ Name)
					print FocusObject
					for i in FocusObject:
						values = i.split(":")
						if values[len(values) - 1] == str(Name):
							return i
					return None
			else:
				return None
		else:
			return None
