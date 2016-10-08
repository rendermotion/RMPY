import maya.cmds as cmds
import pprint as pp
import RMNameConvention
import RMRigTools
reload (RMNameConvention)


def RMblendShapeTargetDic (BSNode):
	#AliasNames=cmds.listAttr((BSNode +".weight"),m=True);
	InputTargetGroup=cmds.getAttr ((BSNode+".inputTarget[0].inputTargetGroup"),mi=True);
	BlendShapeDic={}
	for eachTarget in InputTargetGroup:
		AliasName=cmds.listAttr((BSNode +".weight["+str(eachTarget)+"]"),m=True);
		BlendShapeDic[str(AliasName[0])]={}
		BlendShapeDic[str(AliasName[0])]["TargetGroup"]=eachTarget
		Items = cmds.getAttr ((BSNode+".inputTarget[0].inputTargetGroup["+str(eachTarget)+"].inputTargetItem"), mi=True);
		BlendShapeDic[str(AliasName[0])]["Items"]=Items
	return BlendShapeDic

def invertCurrentPaintTargetWeights(ObjectName, index):
	cmds.setAttr("%s.inputTarget[0].paintTargetIndex"%ObjectName, index)
	weights = cmds.getAttr("%s.inputTarget[0].paintTargetWeights"%ObjectName)
	newWeights = []
	index=0
	for i in weights[0]:
	    cmds.setAttr("%s.inputTarget[0].paintTargetWeights[%s]"% (ObjectName,index),float(1.0)- i)
	    index+=1
	weights = cmds.getAttr("%s.inputTarget[0].paintTargetWeights"%ObjectName)

class BSManager(object):
	def __init__(self, NameConv=None) :
		if NameConv:
			self.NameConv = NameConv
		else:
			self.NameConv = RMNameConvention.RMNameConvention()
		RigTools = RMRigTools.RMRigTools(self.NameConv)
		self.FaceBlendShapeDic = {}

	def AppyBlendShapeDefinition (self, BSDefinition):
		for eachBSGroup in BSDefinition:
			if BSDefinition[eachBSGroup]["isSymetrical"] == True:
				self.CreateMulipleBlendShapes (BSDefinition, "L")
				self.CreateMulipleBlendShapes (BSDefinition, "R")
			else:
				self.CreateMulipleBlendShapes (BSDefinition, "")

	def CreateMulipleBlendShapes (self,BSDefinition, prefix):
		for BSGroups in BSDefinition:
			BSName = BSGroups + "BS"
			blendShapeOriginalGeo = cmds.duplicate(prefix + BSDefinition[BSGroups]['baseMesh'], name = BSDefinition[BSGroups]['baseMesh'] + BSGroups)

			if prefix == "":
				Side = "MD"
			elif prefix=="R":
				Side = "RH"
			elif prefix=="L":
				Side = "LF"

			blendShapeOriginalGeo = self.NameConv.RMRenameNameInFormat( blendShapeOriginalGeo, System = "faceRig",Side = Side)
			cmds.blendShape(blendShapeOriginalGeo, name = BSName)
			BSName = self.NameConv.RMRenameNameInFormat(BSName, System = "faceRig", Side = Side )
			NumBS = 0	
			self.FaceBlendShapeDic = {}
			for eachBlendShape in BSDefinition [BSGroups]['blendShapes']:
				if cmds.objExists(prefix + eachBlendShape):
					if eachBlendShape not in self.FaceBlendShapeDic:
						self.FaceBlendShapeDic[eachBlendShape] = {}
					cmds.blendShape(BSName,edit=True, target = [blendShapeOriginalGeo, NumBS,prefix + eachBlendShape, float (abs(BSDefinition [BSGroups]['blendShapes'][eachBlendShape]["value"])) / 10.0 ])
					self.FaceBlendShapeDic[eachBlendShape]["index"] = NumBS
					self.FaceBlendShapeDic[eachBlendShape]["Exists"] = True
					NumBS += 1
				else:
					print "The blendShape %s was not Found "% (prefix + eachBlendShape)
		return self.FaceBlendShapeDic


	def AddAttributes (self, Object, AttributesDefinition):
		for keys in AttributesDefinition:
			cmds.addAttr(Object,at="float", ln = keys,     hnv = 1, hxv = 1, h = 0, k = 1, smn = 0, smx = 10)

	def ConnectBlendShapesAttr (self, Object, AttributesDefinition, BSNode):
		blendShapeTargetDic = self.RMblendShapeTargetDic(BSNode)
		#for eachAttr in AttributesDefinition:

	def RMblendShapeTargetDic (self, BSNode):
		#AliasNames=cmds.listAttr((BSNode +".weight"),m=True);
		InputTargetGroup=cmds.getAttr ((BSNode+".inputTarget[0].inputTargetGroup"),mi=True);
		BlendShapeDic={}
		for eachTarget in InputTargetGroup:
			AliasName=cmds.listAttr((BSNode +".weight["+str(eachTarget)+"]"),m=True);
			BlendShapeDic[str(AliasName[0])]={}
			BlendShapeDic[str(AliasName[0])]["TargetGroup"] = eachTarget
			Items = cmds.getAttr ((BSNode+".inputTarget[0].inputTargetGroup["+str(eachTarget)+"].inputTargetItem"), mi=True)
			BlendShapeDic[str(AliasName[0])]["Items"] = Items
		return BlendShapeDic

	def RigByDefinition():
		pass
		
	def ReturnBlendShapesByControl(self,connectionPlug, BSDict):
		orderedList = {'positive':[] , 'negative':[]}
		for eachBlendShape in BSDict:
			if BSDict[eachBlendShape]["connection"] == connectionPlug:
				
				if BSDict[eachBlendShape]["value"] > 0:
					sign = 'positive'
				else:
					sign = 'negative'

				if len (orderedList[sign]) == 0:
					print "Toinsert0:%s"%eachBlendShape
					orderedList[sign].append(eachBlendShape)
				else:
					print "Toinsert1:%s"%eachBlendShape
					index = 0
					for blendShapes in orderedList[sign]:
						if (abs(BSDict[eachBlendShape]['value']) > abs(BSDict[blendShapes]['value'])):
							index += 1
						else:
							break
					orderedList[sign].insert(index,eachBlendShape)
				pass
		return orderedList

BlendShapes={
			"lidShapes":{
				     "Diverge":{
				     				"isSymetrical":True,
				                    "baseMesh"    : "Crystalline",

				                    "control"     : "Character_LF_EyeLidShapes00_ctr_facialRig",

				                    "attributes"  :{'PupilDivergeUD':{"type": "float", "min":-10, "max":10},
				                                    'PupilDivergeLR':{"type": "float", "min":-10, "max":10}},

				                    "blendShapes" :{'PupilDivergeUp'      : {"connection":"PupilDivergeUD"  ,"value":  10},
				                                    'PupilDivergeDn'      : {"connection":"PupilDivergeUD"  ,"value": -10},

				                                    'PupilDivergeDn1'      : {"connection":"PupilDivergeUD"  ,"value": -6},
				                                    'PupilDivergeDn2'      : {"connection":"PupilDivergeUD"  ,"value": -5},
				                                    'PupilDivergeDn3'      : {"connection":"PupilDivergeUD"  ,"value": -8},

				                                    'PupilDivergeLf'      : {"connection":"PupilDivergeLR"  ,"value":  10},
				                                    'PupilDivergeRh'      : {"connection":"PupilDivergeLR"  ,"value": -10}},
				                    'order'       :['PupilDivergeUD' , 'PupilDivergeLR']}
				        }
			"secondaryMouth" = {
								"isSymetrical":True,
			                    "baseMesh"    : "Character_MD_phoneticsBSphonetics00_msh_rig",
								"control"     : "Character_MD_MidUpLip00_ctr_facialRig",
								"attributes"  :{"UD"     :{"type": "float", "min":-10, "max":10},
											    "LR"     :{"type": "float", "min":-10, "max":10}},
								"blendShapes" :{'MidUp' : {"connection":"UD"  ,"value":  10},
												'MidDn' : {"connection":"UD"  ,"value": -10},
												'MidUp' : {"connection":"UD"  ,"value":  10},
												'MidDn' : {"connection":"UD"  ,"value": -10},


								}

								'order'       :['UD' , 'LR']}
}
            }

Manager = BSManager()
#Manager.AppyBlendShapeDefinition(BlendShapes["lidShapes"])
print Manager.ReturnBlendShapesByControl('PupilDivergeUD', BlendShapes["lidShapes"]["Diverge"]["blendShapes"])

#pp.pprint(Manager.FaceBlendShapeDic)