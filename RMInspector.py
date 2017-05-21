import maya.cmds as cmds
inspectObject = "Character01_MD_COG00_ctr_Rig"
attributes = cmds.listAttr (inspectObject)
for eachAttr in attributes:
	compounds = eachAttr.split(".")
	if len(compounds) <= 1:
	    attrType = cmds.getAttr(inspectObject + "." + eachAttr,type = True)
	    #print attrType
	    #if (attrType != "message"):
	        #Value = cmds.getAttr("nurbsCircle1." + eachAttr)
	    print ("%s = %s" % (eachAttr,attrType))

print ("%s = %s" % ("useObjectColor",cmds.getAttr(inspectObject +".useObjectColor")))
print ("%s = %s" % ("objectColorRGB",cmds.getAttr(inspectObject +".objectColorRGB")))
print ("%s = %s" % ("overrideColor",cmds.getAttr(inspectObject +".overrideColor")))

cmds.setAttr(inspectObject +".useObjectColor",True)