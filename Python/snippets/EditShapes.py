import maya.cmds as cmds

Select = "Character_MD_circularControl00_ctr_BookRig2"


degree = cmds.getAttr(Select + ".degree")
spans  = cmds.getAttr(Select + ".spans")
print degree 
print spans
CVNum = degree + spans
Values = cmds.getAttr(Select + ".cv[0:%s]" % spans)


selection = cmds.ls(selection = True)
for eachObject in selection:
	index = 0
	for eachValue in Values:
		cmds.setAttr(eachObject + ".cv[%s]" % (index), eachValue[0] , eachValue[1],eachValue[2] )
		index += 1




