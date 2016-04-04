import maya.cmds as cmds

def RMblendShapeTargetDic (BSNode):
	AliasNames=cmds.listAttr((BSNode +".weight"),m=True);
	InputTargetGroup=cmds.getAttr ((BSNode+".inputTarget[0].inputTargetGroup"),mi=True);
	print InputTargetGroup
	i=0
	BlendShapeDic={}
	for EachAliasName in AliasNames:
		BlendShapeDic[EachAliasName]={"TargetGroup":InputTargetGroup[i]}
		Items = cmds.getAttr ((BSNode+".inputTarget[0].inputTargetGroup["+str(InputTargetGroup[i])+"].inputTargetItem"), mi=True);
		BlendShapeDic[EachAliasName]={"Items":Items}
		i+=1
	return BlendShapeDic
