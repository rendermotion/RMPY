import maya.cmds as cmds
import maya.mel as mel
import RMRigTools as RMRigTools

mel.eval('source "RMNameConvention.mel";')
mel.eval('source "RMRigShapeControls.mel";')

def RMCreateClustersOnCurve(curve):
	degree = cmds.getAttr (curve+".degree")
	spans = cmds.getAttr (curve+".spans")
	form = cmds.getAttr (curve+".form")
	#	Form (open = 0, closed = 1, periodic = 2)
	clusterList=[]
	print form
	if form == 0 or form ==1:
		print "Open Line"
		for i in range(0 , (degree + spans)):
			cluster = cmds.cluster(curve + ".cv["+str(i)+"]",name=mel.eval('RMUniqueName "Character_MD_ClusterOnCurve_cls_rig";'))
			clusterList.append(cluster[1])
			cmds.setAttr(cluster[1]+".visibility",0)
			##cmds.cluster(cluster,edit=True,geometry = curve + ".["+str(i)+"]")
	if form == 2:
		print "periodic Line"
		for i in range(0,spans):
			cluster = cmds.cluster(curve+".cv["+str(i)+"]",name=mel.eval('RMUniqueName "Character_MD_ClusterOnCurve_cls_rig";'))
			clusterList.append(cluster[1])
			cmds.setAttr(cluster[1]+".visibility",0)
			#cmds.cluster(cluster,edit=True,geometry = curve + ".["+str(i)+"]")
	return clusterList

def RMJointsOnCurve(curve,JointNumber):
	degree = cmds.getAttr (curve+".degree")
	spans = cmds.getAttr (curve+".spans")
	form = cmds.getAttr (curve+".form")
	#	Form (open = 0, closed = 1, periodic = 2)
	UpVectorObject = cmds.group(empty=True,name=mel.eval('RMUniqueName "Character_MD_UpVector_grp_rig";'))
	jointArray=[]

	for Num in range(0,JointNumber):
		cmds.select(cl=True)
		Newjoint = cmds.joint(name = mel.eval('RMUniqueName "Character_MD_LaceJoint_jnt_rig";'))
		jointArray.append(Newjoint)
	step = 0.0
	if form == 0 or form ==1:
		step =  float(1) / (JointNumber-1)
	else:
		step = float(1) /(JointNumber)

	print "this is the first Step"
	print step
	print spans
	jointCount = 0
	for eachJoint in jointArray:
		motionPath = cmds.pathAnimation(eachJoint, c = curve , follow=True , worldUpObject = UpVectorObject , worldUpType = "objectrotation")
		cmds.setKeyframe (motionPath , v = (step * jointCount) , at = "uValue")
		jointCount+=1
	return {"Joints":jointArray,"UpVector":UpVectorObject}

def RMcreateContolForPnts(points,name):
	cubeLineArray = []
	for obj in points:
		cubeLine = mel.eval('''RMCreateCubeLine(5,5,5,`RMUniqueName "Character_MD_''' + name +'''_Ctrl_rig"`);''')
		#cmds.xform(cubeLine,cp=True)
		RMRigTools.RMAlign(obj,cubeLine,1)
		cmds.makeIdentity (cubeLine,apply=True,t=True,r=True,s=True)
		cmds.parentConstraint(cubeLine,obj)
		cubeLineArray.append(cubeLine)		
	return cubeLineArray

def lacesSystem(curve , jointNumber):
	clusters = RMCreateClustersOnCurve(curve)
	lacesSystem = RMJointsOnCurve(curve,jointNumber)
	rig    = cmds.group(empty=True,name=mel.eval('''RMUniqueName ("Character_MD_LaceRig_grp_LCS");'''))
	cntrls = cmds.group(empty=True,name=mel.eval('''RMUniqueName ("Character_MD_LaceCntrls_grp_LCS");'''))
	print rig
	print cntrls
	for i in lacesSystem["Joints"]:
		cmds.parent(i,rig)
	for i in clusters:
		cmds.parent(i,rig)
	cmds.parent(lacesSystem["UpVector"],rig)
	controls = RMcreateContolForPnts(clusters,"laceControl")
	UpVector = RMcreateContolForPnts([lacesSystem["UpVector"]],"laceUpVector")
	cmds.parent(UpVector[0],cntrls)
	for eachControl in controls:
		cmds.parent(eachControl,cntrls)

#spans = cmds.getAttr (nurbsCircle1+".spans")
#print spans
lacesSystem("LibraryString",5)
#lacesSystem("BridleSecondaryCurve",10)
