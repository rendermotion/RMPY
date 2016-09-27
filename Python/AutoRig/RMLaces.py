import maya.cmds as cmds
import maya.mel as mel
import RMRigTools as RMRigTools
import RMNameConvention
import RMRigShapeControls
reload (RMRigShapeControls)

class RMlaces(object):
	def __init__(self,NameConv = None):
		self.curve = None
		if not NameConv:
			self.NameConv = RMNameConvention.RMNameConvention()
		else:
			self.NameConv = NameConv

		self.shpCtrl = RMRigShapeControls.RMRigShapeControls(NameConv = self.NameConv)

	def RMCreateClustersOnCurve(self , curve = None):
		if curve.__class__ in [str,unicode]:
			masterCurve = curve
			mode = "single"
			#print ("degree:%s",degree)
			#print ("spans:%s",spans)
			#print ("form:%s",form)
		elif  curve.__class__ == list:
			masterCurve = curve[0]
			mode = "multi"
		degree = cmds.getAttr (masterCurve + ".degree")
		spans  = cmds.getAttr (masterCurve + ".spans")
		form   = cmds.getAttr (masterCurve + ".form")
		#	Form (open = 0, closed = 1, periodic = 2)
		clusterList=[]
		if form == 0 or form ==1:
			#print "Open Line"
			for i in range(0 , (degree + spans)):
				cluster = cmds.cluster(masterCurve + ".cv["+str(i)+"]",name=self.NameConv.RMUniqueName ("Character_MD_ClusterOnCurve_cls_rig"))
				if mode == "multi":
					self.RMAddToCluster(i , curve[1:],cluster)
				clusterList.append(cluster[1])
				cmds.setAttr(cluster[1]+".visibility",0)
				##cmds.cluster(cluster,edit=True,geometry = curve + ".["+str(i)+"]")
		if form == 2:
			#print "periodic Line"
			for i in range(0,spans):
				cluster = cmds.cluster(masterCurve+".cv["+str(i)+"]"  ,name = self.NameConv.RMUniqueName ("Character_MD_ClusterOnCurve_cls_rig"))
				if mode == "multi":
					self.RMAddToCluster(i , curve[1:], cluster)
				clusterList.append(cluster[1])
				cmds.setAttr(cluster[1]+".visibility",0)
				#cmds.cluster(cluster,edit=True,geometry = curve + ".["+str(i)+"]")
		return clusterList

	def RMAddToCluster(self , cvIndex , membershipList , cluster):
		clusterSet = cmds.listConnections( cluster, type="objectSet" )
		print clusterSet
		print membershipList
		print cvIndex
		for eachShape in membershipList:
			#cmds.cluster(cluster, edit=True, geometry = eachShape + ".cv["+str(cvIndex)+"]" )
			cmds.sets( eachShape + ".cv["+str(cvIndex)+"]",add = clusterSet[0])

	def RMJointsOnCurve(self, JointNumber,curve = None, JointUpNodeMode = "single", UpVectorArray = None, UpVectorType = "object"):

		'''
		JointUpNodeMode : valid values are "single","multiShape"
		UpVectorType    : valid values are "object","array","world"
		'''

		degree = cmds.getAttr (curve+".degree")
		spans = cmds.getAttr (curve+".spans")
		form = cmds.getAttr (curve+".form")
		#	Form (open = 0, closed = 1, periodic = 2)
		UpVectorObject = None
		if UpVectorType == "object":
			UpVectorObject = cmds.group(empty=True,name = self.NameConv.RMUniqueName ("Character_MD_UpVector_grp_rig"))

		jointArray=[]

		for Num in range(0,JointNumber):
			cmds.select(cl=True)
			Newjoint = cmds.joint(name = self.NameConv.RMUniqueName ("Character_MD_LaceJoint_jnt_rig"))
			jointArray.append(Newjoint)
		step = 0.0
		if form == 0 or form ==1:
			step =  float(spans) / (JointNumber-1)
		else:
			step = float(spans) /(JointNumber)

		jointCount = 0
		for eachJoint in jointArray:
			if UpVectorType=="world":
				motionPath = cmds.pathAnimation(eachJoint, c = curve , follow = True , worldUpType = "scene")
			elif  UpVectorType == "object":
				motionPath = cmds.pathAnimation(eachJoint, c = curve , follow = True , worldUpObject = UpVectorObject , worldUpType = "objectrotation")
			elif  UpVectorType == "array":
				motionPath = cmds.pathAnimation(eachJoint, c = curve , follow = True , worldUpObject = UpVectorArray[jointCount] , worldUpType = "object")
			cmds.setKeyframe (motionPath , v = (step * jointCount) , at = "uValue")

			jointCount+=1
		return {"Joints":jointArray,"UpVector":UpVectorObject}

	def RMcreateContolForPnts(self, points , name):
		cubeLineArray = []
		for obj in points:
			cubeLine = self.shpCtrl.RMCreateCubeLine( 5, 5, 5, centered = True, name = self.NameConv.RMUniqueName ('Character_MD_' + name +'_Ctrl_rig'))
			RMRigTools.RMAlign(obj,cubeLine,1)
			cmds.makeIdentity (cubeLine,apply=True,t=True,r=True,s=True)
			cmds.parentConstraint(cubeLine,obj)
			cubeLineArray.append(cubeLine)		
		return cubeLineArray

	def RMlacesSystem(self, jointNumber,curve = None):
		clusters = self.RMCreateClustersOnCurve(curve = curve)
		lacesSystem = self.RMJointsOnCurve(jointNumber, curve = curve, UpVectorType = "object")
		
		rig    = cmds.group(empty=True,name=self.NameConv.RMUniqueName ("Character_MD_LaceRig_grp_LCS"))
		
		cntrls = cmds.group(empty=True,name=self.NameConv.RMUniqueName ("Character_MD_LaceCntrls_grp_LCS"))
		skinJoints    = cmds.group(empty=True,name=self.NameConv.RMUniqueName ("Character_MD_LaceSkinJoints_grp_LCS"))
		cmds.parent( skinJoints    , rig )
		for i in lacesSystem["Joints"]:
			cmds.parent(i,skinJoints)
		for i in clusters:
			cmds.parent(i,rig)
		cmds.parent(lacesSystem["UpVector"] , rig)
		controls = self.RMcreateContolForPnts(clusters,"laceControl")
		UpVector = self.RMcreateContolForPnts([lacesSystem["UpVector"]],"laceUpVector")
		cmds.parent(UpVector[0],cntrls)
		for eachControl in controls:
			cmds.parent( eachControl , cntrls)

	def RMlacesSystemMultipleRotationControls(self,jointNumber, curve = None):
		OrientationCurve = cmds.duplicate(curve)[0]
		cmds.move (5,OrientationCurve , moveY = True)

		clusterObjects = self.RMCreateClustersOnCurve(curve = [curve,OrientationCurve])

		UpVectorArray = self.RMJointsOnCurve( jointNumber, curve = OrientationCurve , UpVectorType = "world")

		lacesSystem   = self.RMJointsOnCurve( jointNumber, curve = curve , UpVectorArray = UpVectorArray["Joints"] , UpVectorType = "array")

		
		rig    = cmds.group(empty=True,name=self.NameConv.RMUniqueName ("Character_MD_LaceRig_grp_LCS"))

		skinJoints    = cmds.group(empty=True,name=self.NameConv.RMUniqueName ("Character_MD_LaceSkinJoints_grp_LCS"))
		UpVectorJoints    = cmds.group(empty=True,name=self.NameConv.RMUniqueName ("Character_MD_LaceUpVectorJoints_grp_LCS"))
		clusters    = cmds.group(empty=True,name=self.NameConv.RMUniqueName ("Character_MD_clusters_grp_LCS"))

		cmds.parent( skinJoints    , rig )
		cmds.parent( UpVectorJoints, rig )
		cmds.parent( clusters, rig )
		
		cntrls = cmds.group(empty=True,name=self.NameConv.RMUniqueName ("Character_MD_LaceCntrls_grp_LCS"))
		index=0
		for i in lacesSystem["Joints"]:
			cmds.parent (i, skinJoints )
			lacesSystem["Joints"][index] = self.NameConv.RMRenameSetFromName( i , "skinjoint", Token="Type")
			index = index + 1

		for i in UpVectorArray["Joints"]:
			cmds.parent (i, UpVectorJoints )

		for i in clusterObjects:
			cmds.parent(i,clusters)
		#cmds.parent(lacesSystem["UpVector"],rig)
		controls = self.RMcreateContolForPnts(clusterObjects,"laceControl")
		#UpVector = self.RMcreateContolForPnts([lacesSystem["UpVector"]],"laceUpVector")
		#cmds.parent(UpVector[0],cntrls)
		for eachControl in controls:
			cmds.parent( eachControl , cntrls)
	def  RebuildWithNCVs (self,numberOfCvs,curve ):
		if cmds.getAttr (curve+".form")==2:
			if numberOfCvs >= 3:
				curve = cmds.rebuildCurve(curve, spans = numberOfCvs,keepRange = 2)[0]
				return curve
			else:
				return None
		else:
			if numberOfCvs >= 4:
				curve = cmds.rebuildCurve(curve, spans = numberOfCvs - 3,keepRange = 2)[0]
				return curve
			else:
				return None


