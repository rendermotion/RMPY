import RMRigTools
reload(RMRigTools)
import RMNameConvention
reload (RMNameConvention)
import maya.cmds as cmds



class GenericHandJointStructure(object):
	def __init__ (self,NameConv = None):
		if not NameConv:
			self.NameConv = RMNameConvention.RMNameConvention()
		else:
			self.NameConv = NameConv
		self.palmJoint = ""
		self.fingerArray = []
	def CreateHandJointStructure (self,Palm):
		fingerRoots = cmds.listRelatives(Palm,children=True, type="transform")
		palmJoint = cmds.joint(name = self.NameConv.RMGetFromName(Palm,"Name"))
		RMRigTools.RMAlign(Palm, palmJoint,3)
		palmJoint = self.NameConv.RMRenameBasedOnBaseName (Palm, palmJoint,System="rig")
		self.fingerArray=[]
		for eachPoint in fingerRoots :
			fingerPoints = RMRigTools.RMCustomPickWalk (eachPoint, "transform", -1)
			FingerRoot , fingerJoints  = RMRigTools.RMCreateBonesAtPoints(fingerPoints,self.NameConv)
			cmds.parent (FingerRoot, palmJoint )
			self.fingerArray.append(fingerJoints)
		self.palmJoint = palmJoint
		return palmJoint

#GHSt = GenericHandJointStructure()











