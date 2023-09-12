import math
import maya.cmds as cmds
import maya.mel as mel 
import RMRigTools
import RMRigShapeControls


def SpiralOfPoints(initRadius,endRadius,turns,numberOfPoints):
	loc1 = cmds.spaceLocator()
	loc2 = cmds.spaceLocator()
	cmds.parent (loc2[0],loc1[0])
	cmds.setAttr(loc2[0]+".translateX",float(initRadius))
	groupPoints=cmds.group(empty=True)
	degreeTurns = float(turns * 360)
	degreeStep = float(degreeTurns)/ (numberOfPoints-1)
	posStep = (float(initRadius) - float(endRadius)) / (numberOfPoints-1)

	spcLocArray=[]
	startRot=0.0
	startPos = float(initRadius)
	for point in range(0,numberOfPoints):
		NewLoc = cmds.spaceLocator()
		spcLocArray.append(NewLoc[0])
		RMRigTools.RMAlign(loc2[0] , spcLocArray[point] ,3)
		startPos += (-posStep)
		cmds.setAttr (loc2[0] + ".translateX" ,startPos)
		startRot += degreeStep
		cmds.setAttr (loc1[0] + ".rotateZ" ,startRot)
		cmds.parent ( NewLoc,groupPoints)
	jointArray = mel.eval( '''source "RMRigTools.mel";\nsource "RMRigShapeControls.mel";\n
	RMCreateBonesAtPoints( ''' + melstringArray(spcLocArray) + ''');''')
	control = mel.eval('''RMCreaControl("'''+spcLocArray[0] + '''",'''+ str(float(endRadius)) + ''');''')
	cmds.addAttr(control, longName = "unfold", keyable = True, hasMinValue = True, hasMaxValue = True, maxValue = 10, minValue = 0)

	unfoldStep = 10.0 / numberOfPoints
	currentStep = 0.0

	for joints in jointArray:
		currentrot = cmds.joint(joints,q=True,orientation=True)
		RMRigTools.connectWithLimits(control+".unfold",joints + ".rotateZ",[[currentStep,0],[currentStep + unfoldStep,abs(currentrot[2])]])
		currentStep = currentStep + unfoldStep

def SpiralOfPointsStraight(initRadius, endRadius, numberOfPoints, startPoint, endPoint):
	RigTools   = RMRigTools.RMRigTools()
	ShapeCntrl = RMRigShapeControls.RMRigShapeControls()
	distancia  = RMRigTools.RMPointDistance(startPoint,endPoint)
	minLength  = math.sin(math.pi  / (numberOfPoints + 1)) * initRadius #initRadiusdistancia/numberOfPoints/10
	
	print ("minLength:%s" % minLength)

	if minLength * numberOfPoints < distancia:
		#Locators = RigTools.RMCreateNLocatorsBetweenObjects( startPoint, endPoint, numberOfPoints )
		Locators = RigTools.RMCreateBiasedLocatorsBetweenObjects( startPoint, endPoint , numberOfPoints, minLength)
		Locators.insert(0,startPoint)
		Locators.insert(len(Locators),endPoint)
		parentJoint, jointArray = RigTools.RMCreateBonesAtPoints( Locators )
		resetPnt, control = ShapeCntrl.RMCircularControl(startPoint,radius = initRadius)
		cmds.addAttr (control, longName = "unfold", keyable = True, hasMinValue = True, hasMaxValue = True, maxValue = 10,minValue = -10)
		unfoldStep = 10.0 / float(numberOfPoints+1)
		currentStep = 10.0
		index = 0
		deltaRadius = (initRadius - endRadius) / numberOfPoints
		currentRadius = initRadius
		#jointArray.reverse()
		angle=20
		for joints in jointArray[:-1]:
			#angle = 180 - SegmentAngleInCircle(currentRadius, RMRigTools.lenght_of_bone(joints) )
			
			if index > 0:
				angle = getAngle (currentRadius ,joints,jointArray[index-1])
			else: 
				angle = getAngle (currentRadius ,joints,None)

			#angle = SpiralFunction (index, numberOfPoints, initRadius, endRadius, distancia)
			#angle = SpiralFunctionBiasedPoints (index, numberOfPoints, initRadius, endRadius, distancia, minLength)
			RMRigTools.connectWithLimits ( control + ".unfold", joints + ".rotateY", [[-currentStep, angle], [-(currentStep-unfoldStep), 0], [currentStep-unfoldStep, 0], [currentStep, -angle]])
			currentStep = currentStep - unfoldStep

			currentRadius = currentRadius - deltaRadius
			index+=1
def SpiralFunction (ElementIndex, NumberOfElements, initRadius, endRadius, length):
	resolution = float(length) / (float(NumberOfElements) + 1)
	initDiameter = (float(initRadius)*2)
	print ("resolution:%s"%resolution)

	if initDiameter >= resolution:
		initAngle = 180 - SegmentAngleInCircle(initRadius ,resolution)
		print ("initAngle %s"%initAngle)
	else:
		print ("something went wrong with initDiameter")
		initAngle = 90
	endDiameter = (float(endRadius)*2)
	if endDiameter >= resolution:
		endAngle = 180 - SegmentAngleInCircle(endRadius, resolution)
		print ("endAngle %s"%endAngle)
	else:
		print ("something went wrong with endDiameter")
		endAngle = 90

	return -(initAngle + ((endAngle - initAngle)/NumberOfElements) * (ElementIndex))
def SpiralFunctionBiasedPoints (ElementIndex, NumberOfElements, initRadius, endRadius, Distance, initialSize):
	initDiameter = (float(initRadius)*2)
	endDiameter = (float(endRadius)*2)
	DeltaVector = ((((Distance - initialSize)  - (NumberOfElements * initialSize)) * 2 ) / ( NumberOfElements * (NumberOfElements + 1 )))
	print ("DeltaVector :%s",DeltaVector)
	initResolution = initialSize + (DeltaVector * (NumberOfElements))
	endResolution  = initialSize
	print ("initialSize :%s",initialSize)
	print ("initDiameter:%s",initDiameter)
	
	if initDiameter >= initResolution:
		print ("initResolution %s"%initResolution)
		print ("initDiameter %s"%initDiameter)

		initAngle = 180 - (90 - math.degrees(math.asin(initResolution/initDiameter))) * 2
		print ("initAngle %s"%initAngle)
	
	else:
		print ("some trouble calculating the End Angle")
		initAngle = 90

	if endDiameter >= endResolution:
		endAngle =180 - (90 - math.degrees(math.asin(endResolution /endDiameter)) ) * 2
		print ("endAngle %s"%endAngle)
	else:
		print ("some trouble calculating the End Angle")
		endAngle = 90

	return -(initAngle + ((endAngle - initAngle)/NumberOfElements) * (NumberOfElements - ElementIndex))
def getAngle(radius, joint1,joint2):
	segmentLen01 = RMRigTools.RMLenghtOfBone(joint1)
	
	if joint2:
		segmentLen02 = RMRigTools.RMLenghtOfBone(joint2)
	else:
		segmentLen02 = segmentLen01

	alpha = SegmentAngleInCircle(radius,segmentLen01)
	beta  = SegmentAngleInCircle(radius,segmentLen02)
	return 180 - DeltaBetweenAngles(alpha,beta)
def SegmentAngleInCircle(radius,segmentLen):
	'''calculates the angle between two segments of the same len inside a circle'''
	Diameter = (float(radius)*2)
	return (90 - math.degrees(math.asin(segmentLen/Diameter))) * 2
def DeltaBetweenAngles(alpha, beta):
	'''
	if there are two segments inside a sigle, you provide the angle that each one 
	should have to make a circle(you can get this angles with SegmentAngleInCircle)
	And it will return the angle between this two segmets to form a perfect circle
	'''
	return (beta + (alpha-beta)/2)
def melstringArray(array):
	resultstring='{'
	for elements in array:
		resultstring +='"'+elements+'",'
	resultstring =resultstring[0:-1]
	resultstring += '}'
	return resultstring
#SpiralOfPoints(.3,0,15,100)
#SpiralOfPointsStraight(.2, .05, 30, "locator1","locator2")	


'''
	loc1 = cmds.spaceLocator()
	loc2 = cmds.spaceLocator()
	cmds.parent (loc2[0],loc1[0])
	cmds.setAttr(loc2[0]+".translateX",float(initRadius))
	groupPoints=cmds.group(empty=True)
	degreeTurns = float(turns * 360)
	degreeStep = float(degreeTurns)/ (numberOfPoints-1)
	posStep = ( float (initRadius) - float (endRadius) ) / (numberOfPoints-1)
	spcLocArray=[]
	startRot=0.0
	startPos = float(initRadius)
	for point in range(0,numberOfPoints):
		NewLoc = cmds.spaceLocator()
		spcLocArray.append(NewLoc[0])
		RMRigTools.RMAlign(loc2[0] , spcLocArray[point] ,3)
		startPos += (-posStep)
		cmds.setAttr (loc2[0] + ".translateX" ,startPos)
		startRot += degreeStep
		cmds.setAttr (loc1[0] + ".rotateZ" ,startRot)
		cmds.parent ( NewLoc,groupPoints)
	print melstringArray ( spcLocArray)
	jointArray = mel.eval( 'source "RMRigTools.mel";\nsource "RMRigShapeControls.mel";\n
	RMCreateBonesAtPoints( ' + melstringArray(spcLocArray) + ');')
	control = mel.eval('RMCreaControl("'+spcLocArray[0] + '",'+ str(float(endRadius)) + ');')
	cmds.addAttr(control,longName="unfold",keyable=True,hasMinValue=True,hasMaxValue=True,maxValue=10,minValue=0)

	unfoldStep = 10.0 / numberOfPoints
	currentStep = 0.0

	for joints in jointArray:
		currentrot = cmds.joint(joints,q=True,orientation=True)
		print currentrot[2]
		RMRigTools.connectWithLimits(control+".unfold",joints + ".rotateZ",[[currentStep,0],[currentStep + unfoldStep,abs(currentrot[2])]])
		currentStep = currentStep + unfoldStep
	'''



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
'''

'''
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


'''
cmds.addAttr("MainControl",longName="SinAmplitude",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=0,maxValue=10)
cmds.addAttr("MainControl",longName="SinPhase",keyable=1)
cmds.addAttr("MainControl",longName="SinDecay",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=-10,maxValue=10)
cmds.addAttr("MainControl",longName="SinDecayPos",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=0,maxValue=10)
cmds.addAttr("MainControl",longName="SinWaveLen",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=0,maxValue=10)
cmds.addAttr("MainControl",longName="UpperBend",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=-10,maxValue=10)
cmds.addAttr("MainControl",longName="UpperBendLength",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=0,maxValue=10)
cmds.addAttr("MainControl",longName="UpperBendDirection",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=-10,maxValue=10)

cmds.addAttr("MainControl",longName="LowerBend",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=-10,maxValue=10)
cmds.addAttr("MainControl",longName="LowerBendLength",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=0,maxValue=10)
cmds.addAttr("MainControl",longName="LowerBendDirection",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=-10,maxValue=10)

cmds.addAttr("MainControl",longName="BendDirection",keyable=1,hasMinValue=1,hasMaxValue=1, minValue=-10,maxValue=10)
cmds.addAttr("MainControl",longName="ExtraControls",attributeType="enum",enumName = "Off:On")
'''
#cmds.addAttr("MainControl",longName="TransversalBend",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=-10,maxValue=10)
#cmds.addAttr("MainControl",longName="TransversalBendLength",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=0,maxValue=10)
#cmds.addAttr("MainControl",longName="TransversalBendDirection",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=-10,maxValue=10)

'''RMRigTools.connectWithLimits("MainControl.SinDecay","sine.dropoff",[[-10,-1] , [0,0] , [10,1]])
RMRigTools.connectWithLimits("MainControl.SinDecayPos","sineHandle.translateZ",[[0,0],[10,-20]])
RMRigTools.connectWithLimits("MainControl.SinWaveLen","sine.wavelength",[[0,.1],[10,6]])
RMRigTools.connectWithLimits("MainControl.SinAmplitude","sine.amplitude",[[0,0],[10,20]])

RMRigTools.connectWithLimits("MainControl.LowerBend","lowerBend.curvature",[[-10,-180],[0,0],[10,180]])
RMRigTools.connectWithLimits("MainControl.LowerBendLength","lowerBend.highBound",[[-10,-1],[0,0],[10,1]])
RMRigTools.connectWithLimits("MainControl.LowerBendDirection","lowerBendHandle.rotateX",[[-10,-60],[0,0],[10,60]])

RMRigTools.connectWithLimits("MainControl.UpperBend","upperBend.curvature",[[-10,-180],[0,0],[10,180]])
RMRigTools.connectWithLimits("MainControl.UpperBendLength","upperBend.highBound",[[-10,-1],[0,0],[10,1]])
RMRigTools.connectWithLimits("MainControl.UpperBendDirection","upperBendHandle.rotateX",[[-10,-60],[0,0],[10,60]])

RMRigTools.connectWithLimits("MainControl.TransversalBend","transversalBend.curvature",[[-10,-180],[0,0],[10,180]])

RMRigTools.connectWithLimits("MainControl.TransversalBendDirection","transversalBend.rotateX",[[-10,-180],[0,0],[10,180]])
'''

