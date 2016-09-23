
import RMRigTools
reload(RMRigTools)

import RMNameConvention
reload (RMNameConvention)

import RMRigShapeControls
reload (RMRigShapeControls)
import re

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
		
		self.fingerRoot={
		"middle":None,
		"ring":None,
		"pinky":None,
		"index":None,
		"thumb":None
		}
		self.PalmReferencePoints ={
		"middle":None,
		"ring":None,
		"pinky":None,
		"index":None,
		"thumb":None
		}
		self.PalmFingerControlGrp={
		"middle":None,
		"ring": None,
		"pinky":None,
		"index":None,
		"thumb":None
		}
		self.PalmResetPoint =None
		self.PalmControl = None
		self.fingerControlsReset = []
		self.fingerContols=[]
		self.MainKinematics = None
		self.MainControl = None

	def CreateHandRig(self,PalmReferencePoint,PalmControl = None):
		self.CreateHandStructure(PalmReferencePoint)
		for fingers in self.GHS.fingers:
			self.CreateFingerSquareRig(fingers)
			
		self.CreatePalmRig ( PalmControl = PalmControl )
		RMRigTools.RMParentArray(self.PalmControl,self.fingerControlsReset)
		palmLen = RMRigTools.RMPointDistance( self.PalmControl, self.GHS.fingerRoots[0])
		cmds.parentConstraint(self.MainKinematics,self.GHS.palmJoint)
		cmds.parentConstraint(self.MainKinematics,self.MainControl)
		
		self.GHS.palmJoint = self.NameConv.RMRenameSetFromName(self.GHS.palmJoint, "sknjnt", "Type")
		for eachFinger in self.GHS.fingers:
			eachFinger = self.NameConv.RMRenameSetFromName(eachFinger[:-1], "sknjnt", "Type")

		#self.PalmControl
		#RMRigShapeControls.RMCreateBoxCtrl(self.GHS.palmJoint, Yratio = .5, size = palmLen, NameConv =  NameConv)

	def CreateHandStructure(self,PalmReferencePoint):
		self.GHS.CreateHandJointStructure(PalmReferencePoint)
		self.IdentifyJoints(self.GHS.fingerRoots)

	def CreatePalmRig(self,PalmControl = None):
		
		if self.NameConv.RMGetFromName(self.GHS.palmJoint,"Side") == "LF":
			sideVariation = -1
		else:
			sideVariation = 1

		self.CreatePalmReferencePoints()


		if PalmControl== None:
			palmResetPoint , PalmControl = RMRigShapeControls.RMCircularControl(self.GHS.palmJoint)
		else :
			palmResetPoint = cmds.group(empty = True, name = "palmControl")
			palmResetPoint = self.NameConv.RMRenameBasedOnBaseName (self.GHS.palmJoint, palmResetPoint, NewName = palmResetPoint)
			RMRigTools.RMAlign( self.GHS.palmJoint, palmResetPoint,3)

		self.PalmControl = PalmControl
		self.PalmResetPoint = palmResetPoint
		self.MainControl = palmResetPoint

		#palmResetPoint = self.NameConv.RMRenameSetFromName(palmResetPoint,"palmControls","Name")
		
		self.RMaddPalmControls (self.PalmControl)
		RMRigTools.RMLockAndHideAttributes(self.PalmControl,"0000000000")
		
		pinky = self.GHS.fingerJointsByName("pinky")
		if pinky:
			self.PalmFingerControlGrp["pinky"] = RMRigTools.RMCreateGroupOnObj(pinky[0])
			RMRigTools.RMChangeRotateOrder(pinky,"yxz")
			RMRigTools.RMConnectWithLimits(self.PalmControl + ".Spread",self.PalmFingerControlGrp["pinky"] + '.rotateZ', [[-10,sideVariation * 10] ,[0,0],[10,sideVariation * -60]])
		ring = self.GHS.fingerJointsByName("ring")
		if ring:
			self.PalmFingerControlGrp["ring"] = RMRigTools.RMCreateGroupOnObj(ring[0])
			RMRigTools.RMChangeRotateOrder(ring,"yxz")
			RMRigTools.RMConnectWithLimits(self.PalmControl + ".Spread",self.PalmFingerControlGrp["ring"] + '.rotateZ',  [[-10,sideVariation * 5] ,[0,0],[10,sideVariation * -30]])
		middle = self.GHS.fingerJointsByName("middle")
		if middle:
			self.PalmFingerControlGrp["middle"] = RMRigTools.RMCreateGroupOnObj(middle[0])
			RMRigTools.RMChangeRotateOrder(middle,"yxz")
			RMRigTools.RMConnectWithLimits(self.PalmControl + ".Spread", self.PalmFingerControlGrp["middle"] + '.rotateZ',[[-10,0]  ,[0,0],[10,sideVariation * -5]])
		index = self.GHS.fingerJointsByName("index")
		if index:
			self.PalmFingerControlGrp["index"] = RMRigTools.RMCreateGroupOnObj(index[0])
			RMRigTools.RMChangeRotateOrder(index,"yxz")
			RMRigTools.RMConnectWithLimits(self.PalmControl + ".Spread",self.PalmFingerControlGrp["index"] + '.rotateZ', [[-10,sideVariation * -5],[0,0],[10,sideVariation * 30]])
		thumb = self.GHS.fingerJointsByName("thumb")
		if thumb:
			self.PalmFingerControlGrp["thumb"] = RMRigTools.RMCreateGroupOnObj(thumb[0])
			RMRigTools.RMChangeRotateOrder(thumb,"yxz")
			RMRigTools.RMConnectWithLimits(self.PalmControl + ".Spread",self.PalmFingerControlGrp["thumb"] + '.rotateZ', [[-10,sideVariation * -10],[0,0],[10,sideVariation * 60]])

		for eachFingerName in self.fingerRoot:
			if eachFingerName != 'thumb':
				RMRigTools.RMConnectWithLimits(self.PalmControl+".PalmBend",self.PalmFingerControlGrp[eachFingerName]+'.rotateY',[[-10,90],[0,0],[10,-90]])
				RMRigTools.RMConnectWithLimits(self.PalmControl+".Twist",self.PalmReferencePoints[eachFingerName]+'.rotateX',[[-10,sideVariation * 45],[0,0],[10,sideVariation * -45]])

		RMRigTools.RMConnectWithLimits(self.PalmControl+".PalmCup",self.PalmReferencePoints ["pinky"]+'.rotateX', [[0,0],[10,sideVariation * 50]])
		RMRigTools.RMConnectWithLimits(self.PalmControl+".PalmCup",self.PalmReferencePoints ["ring"]+'.rotateX',  [[0,0],[10,sideVariation * 25]])
		RMRigTools.RMConnectWithLimits(self.PalmControl+".PalmCup",self.PalmReferencePoints ["middle"]+'.rotateX',[[0,0],[10,sideVariation * 5]])
		RMRigTools.RMConnectWithLimits(self.PalmControl+".PalmCup",self.PalmReferencePoints ["index"]+'.rotateX', [[0,0],[10,sideVariation * -30]])
		RMRigTools.RMConnectWithLimits(self.PalmControl+".PalmCup",self.PalmReferencePoints ["thumb"]+'.rotateX', [[0,0],[10,sideVariation * -60]])

		


	def CreatePalmReferencePoints(self):
		HandPalm = RMRigTools.RMCreateGroupOnObj(self.GHS.palmJoint,Type = "world", NameConv = self.NameConv)
		for keys in self.fingerRoot:
			childGroup = RMRigTools.RMCreateGroupOnObj(HandPalm,Type = "child", NameConv = self.NameConv)
			childGroup = self.NameConv.RMRenameSetFromName (childGroup, keys, 'Name','add')
			cmds.parentConstraint(childGroup, self.fingerRoot[keys], maintainOffset = True)
			self.PalmReferencePoints[keys] = childGroup

		self.MainKinematics = HandPalm


	def CreateFingerSquareRig(self,Finger):

		if self.NameConv.RMGetFromName(Finger[0],"Side")=="LF":
			sideVariation = 1
		else:
			sideVariation = -1

		BoxResetPoint , BoxControl = RMRigShapeControls.RMCreateBoxCtrl(Finger[len(Finger)-1], ParentBaseSize = True, Xratio = .5 ,Yratio = .5 ,Zratio = .5)
		self.RMaddFinguerControls(BoxControl)
		
		cmds.makeIdentity(BoxControl, apply = True , r = False, t = True, s = True, n = 0)
		cmds.parentConstraint(Finger[len(Finger)-1],BoxResetPoint)

		RMRigTools.RMLockAndHideAttributes(BoxControl,"0000000000")

		RMRigTools.RMConnectWithLimits (BoxControl + ".MidUD",    Finger[0] + ".rotateY", [[-10,100],[0,0],[10,-100]])
		RMRigTools.RMConnectWithLimits (BoxControl + ".MidLR",    Finger[0] + ".rotateZ", [[-10,sideVariation * 120],[0,0],[10,sideVariation * -127]])
		RMRigTools.RMConnectWithLimits (BoxControl + ".MidTwist", Finger[0] + ".rotateX" ,[[-10,sideVariation * 90],[0,0],[10,sideVariation * -90]])
		index = 1
		for eachjoint in range(0,len(Finger)-1):
			RMRigTools.RMConnectWithLimits (BoxControl + ".UD" + str(index),    Finger[eachjoint] + ".rotateY", [[-10,100],[0,0],[10,-100]])
			RMRigTools.RMConnectWithLimits (BoxControl + ".LR" + str(index),    Finger[eachjoint] + ".rotateZ", [[-10,sideVariation * 120],[0,0],[10,sideVariation * -127]])
			RMRigTools.RMConnectWithLimits (BoxControl + ".Twist" + str(index), Finger[eachjoint] + ".rotateX" ,[[-10, sideVariation * 90],[0,0],[10, sideVariation * -90]])
			index += 1
		self.fingerControlsReset.append(BoxResetPoint)
		self.fingerContols.append(BoxControl)

	def IdentifyJoints(self, fingerRootArray):
		for fingers in self.fingerRoot:
			for Roots in fingerRootArray:
				if re.search(fingers,Roots):
					self.fingerRoot[fingers] = Roots

	def IdentifyByString(self,IDstring,fingerList):
		for eachFinger in fingerList:
			if re.search(IDstring,eachFinger):
				return eachFinger

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
		cmds.addAttr(Object,at="float",ln="PalmBend", hnv = 1,hxv = 1, h = 0, k = 1, smn = -10, smx = 10)
		cmds.addAttr(Object,at="float",ln="PalmCup" , hnv = 1,hxv = 1, h = 0, k = 1, smn = -10, smx = 10)
		cmds.addAttr(Object,at="float",ln="Spread"  , hnv = 1,hxv = 1, h = 0, k = 1, smn = -10, smx = 10)
		cmds.addAttr(Object,at="float",ln="Twist"   , hnv = 1,hxv = 1, h = 0, k = 1, smn = -10, smx = 10)

