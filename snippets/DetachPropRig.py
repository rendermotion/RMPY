import maya.cmds as cmds
import RMRigTools

def deleteSimpleRig():
	constraint = cmds.listConnections(type="parentConstraint")
	if constraint and len(constraint) > 0:
		parentConst = constraint[0]
		wAlias = cmds.parentConstraint( parentConst, q=True, wal= True)
		control = cmds.parentConstraint( parentConst, q=True, tl= True)
		joint = cmds.listConnections ( "%s.constraintTranslateX" % (parentConst))
		skinList = cmds.listConnections (joint, type="skinCluster")
		if skinList and len(skinList) > 0:
			skinCluster = skinList[0]
			geolist = cmds.listConnections("%s.outputGeometry"%(skinCluster))
			cmds.delete(skinCluster)
			parentsJoint = cmds.listRelatives(joint,parent = True)
			parentsControl = cmds.listRelatives(control,parent = True)
			cmds.delete(parentsJoint[0])
			cmds.delete(parentsControl[0])
			for eachObject in geolist:
				RMRigTools.RMLockAndHideAttributes(geolist,"1111111111")
		else:
			print "no skin cluster Identified"
	else:
		print "no constraint Node Identified"
deleteSimpleRig()



