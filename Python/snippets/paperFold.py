import maya.cmds as cmds
import RMRigTools
from AutoRig import RMSpaceSwitch
import RMUserParameters
reload (RMUserParameters)
'''
def paperFold(control, objectList):
	CtrlParameters = RMUserParameters.RMUserParameters(control)
	CtrlParameters.addNumeric('paperFold')
	yincrement = 10.0/ (len (objectList))
	sign = -1
	loop = 0.0
	for i in reversed (objectList[:-1]):
		if  i == objectList[0]:
			RMRigTools.RMConnectWithLimits("%s.paperFold"%control,"%s.rotateZ"%i,[[yincrement * loop , 178*sign ] , [yincrement * (loop + 2.0), 90*sign]])
		else:
			RMRigTools.RMConnectWithLimits("%s.paperFold"%control,"%s.rotateZ"%i,[[yincrement * loop , 178*sign ] , [(yincrement * (loop + 3.0)), 0    ]])
			print "yincrement = %s , %s to %s "%(yincrement, yincrement * loop , (yincrement * (loop + 2)))
		loop = loop + 1
		sign = sign * -1

pointArray = RMRigTools.RMCreateNLocatorsBetweenObjects("locator1", "locator2", 11)
jointArray = RMRigTools.RMCreateBonesAtPoints(["locator1"] + pointArray +["locator2"])
paperFold("nurbsCircle1", jointArray[1])
'''
'''
#MotionPaths = cmds.ls(type="motionPath")
MotionPaths = cmds.ls(selection=True)
for eachMotionPath in MotionPaths[1:]:
    cmds.setAttr("%s.frontAxis"%eachMotionPath,0)
    cmds.setAttr("%s.worldUpType"%eachMotionPath,2)
    cmds.connectAttr("Character_MD_laceUpVector00_Ctrl_rig.worldMatrix[0]","%s.worldUpMatrix"%eachMotionPath)
'''
'''
selection = cmds.ls(selection=True )
print selection
#value = (len(selection))/2 - 1
#listaJoints = selection[1:value]
#listaPuntos = selection[((len(selection))/2):]
'''

joints   = [u'Character_MD_HatNub07_jnt_Dynamic', u'Character_MD_HatNub06_jnt_Dynamic', u'Character_MD_HatNub05_jnt_Dynamic', u'Character_MD_HatNub04_jnt_Dynamic', u'Character_MD_HatNub03_jnt_Dynamic', u'Character_MD_HatNub02_jnt_Dynamic', u'Character_MD_HatNub01_jnt_Dynamic', u'Character_MD_HatNub00_jnt_Dynamic']
locators = [u'Character_MD_HatNub07_jnt_Rig', u'Character_MD_HatNub06_jnt_Rig', u'Character_MD_HatNub05_jnt_Rig', u'Character_MD_HatNub04_jnt_Rig', u'Character_MD_HatNub03_jnt_Rig', u'Character_MD_HatNub02_jnt_Rig', u'Character_MD_HatNub01_jnt_Rig', u'Character_MD_HatNub00_jnt_Rig']
drivers  = [u'Hat00joint', u'Hat01joint', u'Hat02joint', u'Hat03joint', u'Hat04joint', u'Hat05joint', u'Hat06joint', u'Hat07joint']

#CtrlParameters = RMUserParameters.RMUserParameters("HatBase")
#CtrlParameters.addNumeric('DynamicHat')

#yincrement = 10.0/ (len (locators))

#loop = 0
#for eachDriver in drivers:
#	constraint        = cmds.parentConstraint(loop] , eachDriver, mo = False)[0]
#	cmds.parentConstraint ( locators[loop] , eachDriver, mo = False)
#	WA = cmds.parentConstraint (constraint, q = True, weightAliasList = True)
#	RMRigTools.RMConnectWithLimits("HatBaseShape.DynamicHat", "%s.%s"%(constraint , WA[0]), [[yincrement * loop , 1], [yincrement * (loop + 3), 0]])
#	RMRigTools.RMConnectWithLimits("HatBaseShape.DynamicHat", "%s.%s"%(constraint , WA[1]), [[yincrement * loop , 0], [yincrement * (loop + 3), 1]])
#	loop = loop + 1

constraintManager = RMSpaceSwitch.RMSpaceSwitch()
constraintManager.RMCreateListConstraintSwitch (drivers, locators,'HatBase',SpaceSwitchName = "DynamicHat", reverse = True)
constraintManager.RMCreateListConstraintSwitch (drivers, joints ,'HatBase',SpaceSwitchName = "DynamicHat", reverse = False)


