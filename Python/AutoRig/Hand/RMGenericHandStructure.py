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
		self.fingerRoots = []
		self.fingers = []
	def CreateHandJointStructure (self,Palm):
		self.fingerRoots = cmds.listRelatives(Palm,children=True, type="transform")
		print self.fingerRoots
		palmJoint = cmds.joint(name = self.NameConv.RMGetFromName(Palm,"Name"))

		RMRigTools.RMAlign(Palm, palmJoint,3)
		palmJoint = self.NameConv.RMRenameBasedOnBaseName (Palm, palmJoint,System="rig")
		self.fingers = []

		for eachPoint in self.fingerRoots :
			fingerPoints = RMRigTools.RMCustomPickWalk (eachPoint, "transform", -1)
			FingerRoot , fingerJoints  = RMRigTools.RMCreateBonesAtPoints(fingerPoints,self.NameConv)
			cmds.parent (FingerRoot, palmJoint )
			self.fingers.append(fingerJoints)
		self.palmJoint = palmJoint
		return palmJoint

#GHSt = GenericHandJointStructure()
#GHSt.CreateHandJointStructure("Character01_LF_palm_pnt_rfr")












