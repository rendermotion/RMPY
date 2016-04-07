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

