import maya.cmds as cmds
import RMRigTools
from AutoRig import RMSpaceSwitch
import RMUserParameters

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

joints   = [u'Character_MD_joint00_jnt_Rig',u'Character_MD_joint01_jnt_Rig', u'Character_MD_joint02_jnt_Rig', u'Character_MD_joint03_jnt_Rig', u'Character_MD_joint04_jnt_Rig', u'Character_MD_joint05_jnt_Rig', u'Character_MD_joint06_jnt_Rig', u'Character_MD_joint07_jnt_Rig', u'Character_MD_joint08_jnt_Rig', u'Character_MD_joint09_jnt_Rig', u'Character_MD_joint10_jnt_Rig', u'Character_MD_joint11_jnt_Rig',u'Character_MD_joint12_jnt_Rig']
locators = [u'locator12', u'locator11', u'locator10', u'locator9', u'locator8', u'locator7', u'locator6', u'locator5', u'locator4', u'locator3', u'locator2', u'locator1', u'locator']
drivers  = [u'Character_MD_TirasdePapel00_sknjnt_Rig', u'Character_MD_TirasdePapel01_sknjnt_Rig', u'Character_MD_TirasdePapel02_sknjnt_Rig', u'Character_MD_TirasdePapel03_sknjnt_Rig', u'Character_MD_TirasdePapel04_sknjnt_Rig', u'Character_MD_TirasdePapel05_sknjnt_Rig', u'Character_MD_TirasdePapel06_sknjnt_Rig', u'Character_MD_TirasdePapel07_sknjnt_Rig', u'Character_MD_TirasdePapel08_sknjnt_Rig', u'Character_MD_TirasdePapel09_sknjnt_Rig', u'Character_MD_TirasdePapel10_sknjnt_Rig', u'Character_MD_TirasdePapel11_sknjnt_Rig', u'Character_MD_TirasdePapel12_sknjnt_Rig']



yincrement = 10.0/ (len (locators))

loop = 0
for eachDriver in reversed(drivers):
	constraint        = cmds.parentConstraint(joints[len(joints) - loop - 1] , eachDriver, mo = False)[0]
	cmds.parentConstraint ( locators[len(locators) - loop - 1] , eachDriver, mo = False)
	constraintManager = RMSpaceSwitch.RMSpaceSwitch()
	
	WA = cmds.parentConstraint (constraint, q = True, weightAliasList = True)
	RMRigTools.RMConnectWithLimits("nurbsCircle1.paperFold", "%s.%s"%(constraint , WA[0]), [[yincrement * loop , 1], [yincrement * (loop + 3), 0]])
	RMRigTools.RMConnectWithLimits("nurbsCircle1.paperFold", "%s.%s"%(constraint , WA[1]), [[yincrement * loop , 0], [yincrement * (loop + 3), 1]])
	loop = loop + 1


