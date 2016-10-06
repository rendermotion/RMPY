import maya.cmds as cmds

def RMblendShapeTargetDic (BSNode):
	#AliasNames=cmds.listAttr((BSNode +".weight"),m=True);
	InputTargetGroup=cmds.getAttr ((BSNode+".inputTarget[0].inputTargetGroup"),mi=True);
	BlendShapeDic={}
	for eachTarget in InputTargetGroup:
		AliasName=cmds.listAttr((BSNode +".weight["+str(eachTarget)+"]"),m=True);
		BlendShapeDic[str(AliasName[0])]={}
		BlendShapeDic[str(AliasName[0])]["TargetGroup"]=eachTarget
		Items = cmds.getAttr ((BSNode+".inputTarget[0].inputTargetGroup["+str(eachTarget)+"].inputTargetItem"), mi=True);
		BlendShapeDic[str(AliasName[0])]["Items"]=Items
	return BlendShapeDic

def invertCurrentPaintTargetWeights(ObjectName, index):
	cmds.setAttr("%s.inputTarget[0].paintTargetIndex"%ObjectName, index)
	weights = cmds.getAttr("%s.inputTarget[0].paintTargetWeights"%ObjectName)
	newWeights = []
	index=0
	for i in weights[0]:
	    cmds.setAttr("%s.inputTarget[0].paintTargetWeights[%s]"% (ObjectName,index),float(1.0)- i)
	    index+=1
	weights = cmds.getAttr("%s.inputTarget[0].paintTargetWeights"%ObjectName)

