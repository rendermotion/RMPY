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
	


