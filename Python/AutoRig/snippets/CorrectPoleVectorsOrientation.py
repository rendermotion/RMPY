import maya.cmds as cmds

def correctPoleVectors():
	objectList = ["*LF_elbowPoleVectorIK00_grp_Rig","*RH_elbowPoleVectorIK00_grp_Rig","*RH_KneePoleVectorIK00_grp_Rig","*LF_KneePoleVectorIK00_grp_Rig"]
	for eachObject in objectList:
		SceneObj = cmds.ls( eachObject )
		if len(SceneObj) == 1:
			cmds.setAttr("%s.rotateZ"%SceneObj[0],90)
			cmds.setAttr("%s.rotateX"%SceneObj[0],90)
		else:
			print "problems found trying to parse %s, %s objects found" % (SceneObj,len(SceneObj))


