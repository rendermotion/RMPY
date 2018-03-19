import maya.cmds as cmds
import RMRigTools
import RMNameConvention
import RMblendShapesTools
BSlist = {'phonetics': {
					'attributes' :{'O':{},'CH':{},'E':{},'I':{},'A':{},'P':{},'WQ':{},'FV':{},'close':{},'Sv01':{},'Sv02':{},'MBP':{},'L':{},'superO':{}},
					'control':"nurbsCircle1",
					'original':"CabezaRockaleta"
					}

	      }
class BSManager(object):
	def __init__(self, NameConv=None) :
		if NameConv:
			self.NameConv = NameConv
		else:
			self.NameConv = RMNameConvention.RMNameConvention()
		RigTools = RMRigTools.RMRigTools(self.NameConv)

	def ApplyBlendShapes(self,BSDefinition):
		for BSGroups in BSDefinition:
			BSName = BSGroups + "BS"
			cmds.duplicate(BSDefinition[BSGroups]['original'], name = BSName + BSGroups)
			blendShapeOriginalGeo = BSName + BSGroups
			blendShapeOriginalGeo = self.NameConv.rename_name_in_format(blendShapeOriginalGeo, System ="rig")
			cmds.blendShape(blendShapeOriginalGeo, name = BSName)
			BSName = self.NameConv.rename_name_in_format(BSName, System ="rig")
			NumBS = 0
			for keys in BSDefinition[BSGroups]['attributes']:
				if cmds.objExists(keys):
					cmds.blendShape(BSName,edit=True, target=[blendShapeOriginalGeo,NumBS,keys,1.0])
					self.FaceBlendShapeDic[keys]["index"] = NumBS
					self.FaceBlendShapeDic[keys]["Exists"] = True
					NumBS += 1 


	def AddAttributes (self, Object, AttributesDefinition):
		for keys in AttributesDefinition:
			cmds.addAttr(Object,at="float", ln = keys,     hnv = 1, hxv = 1, h = 0, k = 1, smn = 0, smx = 10)

	def ConnectBlendShapesAttr (Object, AttributesDefinition, BSNode):
		blendShapeTargetDic = RMblendShapesTools.RMblendShapeTargetDic(BSNode)
		print blendShapeTargetDic
		#for eachAttr in AttributesDefinition:
Manager = BSManager()
Manager.ApplyBlendShapes(BSlist)




		
