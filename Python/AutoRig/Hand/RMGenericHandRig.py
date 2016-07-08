import RMRigTools
reload(RMRigTools)
import RMNameConvention
reload (RMNameConvention)
import maya.cmds as cmds
from AutoRig.Hand import RMGenericHandStructure
reload (RMGenericHandStructure)


class RMGenericHandRig(object):
	def __init__ (self,RMGenericHandStructure,NameConv = None):
		if not NameConv:
			self.NameConv = RMNameConvention.RMNameConvention()
		else:
			self.NameConv = NameConv
		self.genericHandS = RMGenericHandStructure
	def CreateHandRig():
		pass
	def RMaddFinguerControls(Object):
		cmds.addAttr(Object,at="float", ln = MidUD, hnv = 1, hxv = 1, h = 0, k = 1, smn = 10, smx = 10)


global proc RMaddFinguerControls (string $Object)
{
	addAttr -at "float" -ln MidUD -hnv 1 -hxv 1 -h 0 -k 1 -smn -10 -smx 10 $Object;
	addAttr -at "float" -ln UD1 -hnv 1 -hxv 1 -h 0 -k 1 -smn -10 -smx 10 $Object;
	addAttr -at "float" -ln UD2 -hnv 1 -hxv 1 -h 0 -k 1 -smn -10 -smx 10 $Object;
	addAttr -at "float" -ln UD3 -hnv 1 -hxv 1 -h 0 -k 1 -smn -10 -smx 10 $Object;
	addAttr -at "float" -ln MidLR -hnv 1 -hxv 1 -h 0 -k 1 -smn -10 -smx 10 $Object;
	addAttr -at "float" -ln LR1 -hnv 1 -hxv 1 -h 0 -k 1 -smn -10 -smx 10 $Object;
	addAttr -at "float" -ln LR2 -hnv 1 -hxv 1 -h 0 -k 1 -smn -10 -smx 10 $Object;
	addAttr -at "float" -ln LR3 -hnv 1 -hxv 1 -h 0 -k 1 -smn -10 -smx 10 $Object;
	addAttr -at "float" -ln MidTwist -hnv 1 -hxv 1 -h 0 -k 1 -smn -10 -smx 10 $Object;
	addAttr -at "float" -ln Twist1 -hnv 1 -hxv 1 -h 0 -k 1 -smn -10 -smx 10 $Object;
	addAttr -at "float" -ln Twist2 -hnv 1 -hxv 1 -h 0 -k 1 -smn -10 -smx 10 $Object;
	addAttr -at "float" -ln Twist3 -hnv 1 -hxv 1 -h 0 -k 1 -smn -10 -smx 10 $Object;
	addAttr -at "enum" -k on -ln Secondary -en "Off:On:" $Object;
}

global proc RMaddPalmControls(string $Object)
{
	addAttr -at "float" -ln PalmBend -hnv 1 -hxv 1 -h 0 -k 1 -smn -10 -smx 10 $Object;
	addAttr -at "float" -ln PalmCup -hnv 1 -hxv 1 -h 0 -k 1 -smn -10 -smx 10 $Object;
	addAttr -at "float" -ln Spread -hnv 1 -hxv 1 -h 0 -k 1 -smn -10 -smx 10 $Object;
	addAttr -at "float" -ln Twist -hnv 1 -hxv 1 -h 0 -k 1 -smn -10 -smx 10 $Object;
}


GHS = RMGenericHandStructure.GenericHandJointStructure()
GHS.CreateHandJointStructure("Character01_LF_palm_pnt_rfr")
GHrig = RMGenericHandRig(GHS)


