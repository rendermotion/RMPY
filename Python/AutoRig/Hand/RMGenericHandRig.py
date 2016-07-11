import RMRigTools
reload(RMRigTools)
import RMNameConvention
reload (RMNameConvention)
import RMRigShapeControls
reload (RMRigShapeControls)

import maya.cmds as cmds
from AutoRig.Hand import RMGenericHandStructure
reload (RMGenericHandStructure)

class RMGenericHandRig(object):
	def __init__ (self,NameConv = None):
		if not NameConv:
			self.NameConv = RMNameConvention.RMNameConvention()
		else:
			self.NameConv = NameConv
		self.GHS = RMGenericHandStructure.GenericHandJointStructure(NameConv = NameConv)

	def CreateHandStructure(self):
		self.GHS.CreateHandJointStructure("Character01_LF_palm_pnt_rfr")

	def CreateHandRig(self):
		self.CreateHandStructure()
		for fingers in self.GHS.fingers:
			self.CreateFingerRig(fingers)


	def CreateFingerRig(self,Finger):
		BoxControl = RMRigShapeControls.RMCreateBoxCtrl(Finger[len(Finger)-1])
		self.RMaddFinguerControls(BoxControl)
		
		cmds.makeIdentity(BoxControl, apply = True , r = True, t = True, s = True, n = 0)
		print "Entering LH"
		print BoxControl
		RMLockAndHideAttributes(BoxControl,"0000000000")

		RMConnectWithLimits (BoxControl + ".MidUD",    Finger[0] + ".rotateY", [[-10,-100],[0,0],[10,100]])
		RMConnectWithLimits (BoxControl + ".MidLR",    Finger[0] + ".rotateZ", [[-10,-120],[0,0],[10,127]])
		RMConnectWithLimits (BoxControl + ".MidTwist", Finger[0] + ".rotateX" ,[[-10, -90],[0,0],[10,90]])
		index = 1
		for eachjoint in range(0,len(Finger)-1):
			RMConnectWithLimits (BoxControl + ".UD" + str(index),    Finger[eachjoint] + ".rotateY", [[-10,-100],[0,0],[10,100]])
			RMConnectWithLimits (BoxControl + ".LR" + str(index),    Finger[eachjoint] + ".rotateZ", [[-10,-120],[0,0],[10,127]])
			RMConnectWithLimits (BoxControl + ".Twist" + str(index), Finger[eachjoint] + ".rotateX" ,[[-10, -90],[0,0],[10, 90]])
			index += 1

	def RMaddFinguerControls(self,Object):
		cmds.addAttr(Object,at="float", ln = "MidUD",   hnv = 1, hxv = 1, h = 0, k = 1, smn = -10, smx = 10)
		cmds.addAttr(Object,at="float", ln = "UD1",     hnv = 1, hxv = 1, h = 0, k = 1, smn = -10, smx = 10)
		cmds.addAttr(Object,at="float", ln = "UD2",     hnv = 1, hxv = 1, h = 0, k = 1, smn = -10, smx = 10)
		cmds.addAttr(Object,at="float", ln = "UD3",     hnv = 1, hxv = 1, h = 0, k = 1, smn = -10, smx = 10)
		cmds.addAttr(Object,at="float", ln = "MidLR",   hnv = 1, hxv = 1, h = 0, k = 1, smn = -10, smx = 10)
		cmds.addAttr(Object,at="float", ln = "LR1",     hnv = 1, hxv = 1, h = 0, k = 1, smn = -10, smx = 10)
		cmds.addAttr(Object,at="float", ln = "LR2",     hnv = 1, hxv = 1, h = 0, k = 1, smn = -10, smx = 10)
		cmds.addAttr(Object,at="float", ln = "LR3",     hnv = 1, hxv = 1, h = 0, k = 1, smn = -10, smx = 10)
		cmds.addAttr(Object,at="float", ln = "MidTwist",hnv = 1, hxv = 1, h = 0, k = 1, smn = -10, smx = 10)
		cmds.addAttr(Object,at="float", ln = "Twist1",  hnv = 1, hxv = 1, h = 0, k = 1, smn = -10, smx = 10)
		cmds.addAttr(Object,at="float", ln = "Twist2",  hnv = 1, hxv = 1, h = 0, k = 1, smn = -10, smx = 10)
		cmds.addAttr(Object,at="float", ln = "Twist3",  hnv = 1, hxv = 1, h = 0, k = 1, smn = -10, smx = 10)
		cmds.addAttr(Object,at="enum" , ln = "Secondary", k = 1, en = "Off:On")

	def RMaddPalmControls(self,Object):
		cmds.addAttr(Object,at="float",ln="PalmBend", hnv = 1,hxv = 1, h = 0, k = 1, smn = 10, smx = 10)
		cmds.addAttr(Object,at="float",ln="PalmCup" , hnv = 1,hxv = 1, h = 0, k = 1, smn = 10, smx = 10)
		cmds.addAttr(Object,at="float",ln="Spread"  , hnv = 1,hxv = 1, h = 0, k = 1, smn = 10, smx = 10)
		cmds.addAttr(Object,at="float",ln="Twist"   , hnv = 1,hxv = 1, h = 0, k = 1, smn = 10, smx = 10)

GHrig = RMGenericHandRig()
GHrig.CreateHandRig()


