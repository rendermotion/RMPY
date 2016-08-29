import math
import maya.cmds as cmds
import maya.mel as mel 
import RMRigTools
reload (RMRigTools)



def SpiralOfPoints(initRadius,endRadius,turns,numberOfPoints):
	print (math.sqrt(2))
	loc1 = cmds.spaceLocator()
	loc2 = cmds.spaceLocator()
	cmds.parent (loc2[0],loc1[0])
	cmds.setAttr(loc2[0]+".translateX",float(initRadius))
	groupPoints=cmds.group(empty=True)
	degreeTurns = float(turns * 360)
	degreeStep = float(degreeTurns)/ (numberOfPoints-1)
	posStep = (float(initRadius) - float(endRadius)) / (numberOfPoints-1)
	print "posStep"
	print posStep
	spcLocArray=[]
	startRot=0.0
	startPos = float(initRadius)
	for point in range(0,numberOfPoints):
		NewLoc = cmds.spaceLocator()
		spcLocArray.append(NewLoc[0])
		RMRigTools.RMAlign(loc2[0] , spcLocArray[point] ,3)
		startPos += (-posStep)
		cmds.setAttr(loc2[0]+".translateX" ,startPos)
		startRot+=degreeStep
		cmds.setAttr(loc1[0]+".rotateZ" ,startRot)
		cmds.parent(NewLoc,groupPoints)
	print melstringArray(spcLocArray)
	jointArray = mel.eval('''source "RMRigTools.mel";\n
	RMCreateBonesAtPoints(''' + melstringArray(spcLocArray)+ ''');''')
	control = mel.eval('''RMCreaControl("'''+spcLocArray[0]+'''",'''+ str(float(endRadius)) + ''');''')
	cmds.addAttr(control,longName="unfold",keyable=True,hasMinValue=True,hasMaxValue=True,maxValue=10,minValue=0)

	unfoldStep = 10.0 / numberOfPoints
	currentStep = 0.0

	for joints in jointArray:
		currentrot = cmds.joint(joints,q=True,orientation=True)
		print currentrot[2]
		RMRigTools.connectWithLimits(control+".unfold",joints + ".rotateZ",[[currentStep,0],[currentStep + unfoldStep,abs(currentrot[2])]])
		currentStep = currentStep + unfoldStep

	
def melstringArray(array):
	resultstring='{'
	for elements in array:
		resultstring +='"'+elements+'",'
	resultstring =resultstring[0:-1]
	resultstring+='}'
	return resultstring

SpiralOfPoints(.3,0,15,100)
	

'''
cmds.addAttr("PapirusControl",longName="SinAmplitude",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=0,maxValue=10)
cmds.addAttr("PapirusControl",longName="SinPhase",keyable=1)
cmds.addAttr("PapirusControl",longName="SinDecay",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=-10,maxValue=10)
cmds.addAttr("PapirusControl",longName="SinDecayPos",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=0,maxValue=10)
cmds.addAttr("PapirusControl",longName="SinWaveLen",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=0,maxValue=10)


cmds.addAttr("PapirusControl",longName="BendFloor",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=-10,maxValue=10)
cmds.addAttr("PapirusControl",longName="BendFloorDistance",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=0,maxValue=10)

cmds.addAttr("PapirusControl",longName="BendDirection",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=-10,maxValue=10)



cmds.addAttr("PapirusControl",longName="ExtraControls",attributeType="enum",enumName = "Off:On")


RMRigTools.connectWithLimits("PapirusControl.BendRoll","RolledBend.curvature",[[-10,-180],[0,0],[10,180]])
cmds.connectAttr("PapirusControl.BendRollDirection","RollbendHandle.rotateY",force=True)

RMRigTools.connectWithLimits("PapirusControl.BendFloor","FloorBend.curvature",[[-10,-180],[0,0],[10,180]])
RMRigTools.connectWithLimits("PapirusControl.BendFloorDistance","FloorBendHandle.translateZ",[[0,0],[10,-20]])

RMRigTools.connectWithLimits("PapirusControl.SinAmplitude","Wave.amplitude",[[0,0],[10,-20]])
cmds.connectAttr("PapirusControl.SinPhase","Wave.offset",force=True)

RMRigTools.connectWithLimits("PapirusControl.SinDecay","Wave.dropoff",[[-10,-1] , [0,0] , [10,1]] )
RMRigTools.connectWithLimits("PapirusControl.SinDecayPos","sine1Handle.translateZ",[[0,0],[10,-20]])
RMRigTools.connectWithLimits("PapirusControl.SinWaveLen","Wave.wavelength",[[0,.1],[10,6]])
RMRigTools.connectWithLimits("PapirusControl.BendDirection","DirectionBend.curvature",[[-10,-90],[0,0],[10,90]])
cmds.connectAttr("PapirusControl.ExtraControls","curve1.visibility",force=True) '''


