import maya.cmds as cmds

def CreateClustersOnCurve(curve):
	degree = cmds.getAttr (curve+".degree");
	spans = cmds.getAttr (curve+".spans");
	form = cmds.getAttr (curve+".form");
	#	Form (open = 0, closed = 1, periodic = 2)
	print form
	if form == 0 or form ==1:
		print "Open Line"
		for i in range(0 , (degree + spans)-1):
			cluster = cmds.cluster(curve + ".cv["+str(i)+"]",name="ClustOnCurve"+str(i))
			##cmds.cluster(cluster,edit=True,geometry = curve + ".["+str(i)+"]")
	if form == 2:
		print "periodic Line"
		for i in range(0 , spans-1):
			cluster = cmds.cluster(curve + ".cv["+str(i)+"]",name="ClustOnCurve"+str(i))
			##cmds.cluster(cluster,edit=True,geometry = curve + ".["+str(i)+"]")
def JointsOnCurve(curve,JointNumber):
	degree = cmds.getAttr (curve+".degree")
	spans = cmds.getAttr (curve+".spans")
	form = cmds.getAttr (curve+".form")
	#	Form (open = 0, closed = 1, periodic = 2)
	UpVectorObject = cmds.group(empty=True,name="UpVector")
	jointArray=[]

	for Num in range(0,JointNumber):
		cmds.select(cl=True)
		Newjoint = cmds.joint(name = "PathJoint"+ str(Num))
		jointArray.append(Newjoint)
	step = 0 
	if form == 0 or form ==1:
		step = 1 / (JointNumber-1)
	else:
		step = 1 /(JointNumber + 1)
	jointCount=0
	for eachJoint in jointArray:
		motionPath = cmds.pathAnimation(eachJoint,c=curve,worldUpObject=UpVectorObject,worldUpType="objectrotation")
		cmds.pathAnimation(eachJoint,c=curve, stu=0 ,startU=step*jointCount)
		jointCount+=1


JointsOnCurve("curveShape1",5)