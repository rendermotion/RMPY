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

	def CreateHandJointStructure (self,Hand):
		fingers = cmds.listRelatives(Hand,children=True, type="transform")
		print fingers
		palmJoint = cmds.joint(name = self.NameConv.RMGetFromName(Hand,"Name"))
		RMRigTools.RMAlign(Hand, palmJoint,3)

		for eachjoint in fingers :
			fingerJoints = RMCustomPickWalk (eachjoint, "transform", -1)
			FingerRoot   = RMRigTools.RMCreateBonesAtPoints(fingerJoints)
			cmds.parent(FingerRoot,palmJoint)

		return palmJoint


GHSt = GenericHandJointStructure()

GHSt.CreateHandJointStructure("Character01_LF_wrist_pnt_rfr")










