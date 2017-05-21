import maya.cmds as cmds
offset = 1.2
referenceObject = "Character_MD_circularControl02_grp_Rig"
startPosition = cmds.xform(referenceObject,query=True,ws = True ,translation = True )

selection = cmds.ls(selection = True)

index=0
for eachObject in selection:
	cmds.xform(eachObject, ws=True, translation = [ startPosition[0], startPosition[1], startPosition[2] + (index * offset)])
	index += 1

