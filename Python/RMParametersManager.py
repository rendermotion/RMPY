import maya.cmds as cmds
import RMRigTools

def deleteAttributes (Object, attribute = None):
	AttrList = cmds.listAttr ( Object, userDefined = True)
	if AttrList:
		for eachAttribute in AttrList:
			cmds.setAttr("%s.%s"%(Object,eachAttribute), l = False )
			cmds.deleteAttr(Object, attribute = eachAttribute)

def addAttributesDic (Object , attributesDic):
	for eachAttribute in attributesDic:
		if attributesDic[eachAttribute]["type"] == "float":
			if "keyable" in attributesDic[eachAttribute]:
				keyable = attributesDic[eachAttribute]["keyable"]
			else :
				keyable = 1
			print "Adding Attribute %s , keyable:%s"%(eachAttribute,keyable)
			cmds.addAttr(Object,at="float", ln = eachAttribute, hnv = 1, hxv = 1, h = 0, k = keyable, smn = float(attributesDic[eachAttribute]["min"]), smx = float(attributesDic[eachAttribute]["max"]))
selection = cmds.ls(selection = True)
for i in selection:
	deleteAttributes (i)

#addAttributesDic( "REyeLidShapes", lidShapes)

Cheeks = {
 "UD"    :{"type": "float", "min":-10, "max":10},
 "LR"    :{"type": "float", "min":-10, "max":10},
 "FB"    :{"type": "float", "min":-10, "max":10},
 "Squint":{"type": "float", "min":  0, "max":10},
 "PUFF"  :{"type": "float", "min":-10, "max":10}
}

EyeBrow = {
	"Angry"    :{"type": "float", "min":-10, "max":10},
	"Sad"      :{"type": "float", "min":-10, "max":10},
	"Surprise" :{"type": "float", "min":-10, "max":10},
	"UD"       :{"type": "float", "min":-10, "max":10},
	"LR"       :{"type": "float", "min":-10, "max":10},
	"FB"       :{"type": "float", "min":-10, "max":10},
	"Tilt"     :{"type": "float", "min":-10, "max":10},
	"Secondary":{"Type": "enum", "enumNames":["Off","On"]}
}

secondaryEyeBrow = {
	"UD"   :{"type": "float", "min":-10, "max":10},
	"LR"   :{"type": "float", "min":-10, "max":10},
	"FB"   :{"type": "float", "min":-10, "max":10},
	"Tilt" :{"type": "float", "min":-10, "max":10}
}

furrow = {
'Furrow'           :{"type": "float", "min":-10, "max":10},
'UD'               :{"type": "float", "min":-10, "max":10},
'FB'               :{"type": "float", "min":-10, "max":10},
'LR'               :{"type": "float", "min":-10, "max":10},
'TILT'             :{"type": "float", "min":-10, "max":10},
'Left_Right_Shapes':{"type": "float", "min":-10, "max":10 , "keyable":False},
'FurrowL'          :{"type": "float", "min":-10, "max":10},
'FurrowR'          :{"type": "float", "min":-10, "max":10}
}

secondaryMouth = {
	"UD"     :{"type": "float", "min":-10, "max":10},
	"LR"     :{"type": "float", "min":-10, "max":10}
}

Nose = {
	"UD"     :{"type": "float", "min":-10, "max":10},
	"LR"     :{"type": "float", "min":-10, "max":10},
	"FB"     :{"type": "float", "min":-10, "max":10},
	"Curl"   :{"type": "float", "min":-10, "max":10},
	"Tilt"   :{"type": "float", "min":-10, "max":10},
	"LSneer" :{"type": "float", "min":-10, "max":10},
	"RSneer" :{"type": "float", "min":-10, "max":10},
	"LFlare" :{"type": "float", "min":-10, "max":10},
	"RFlare" :{"type": "float", "min":-10, "max":10}
}

mouth = {
'SmileFrown'     :{"type": "float", "min":-10, "max":10}, 
'NarrowWide'     :{"type": "float", "min":-10, "max":10},
'Ooo'            :{"type": "float", "min":  0, "max":10},
'Press'          :{"type": "float", "min":  0, "max":10}, 
'Puff'           :{"type": "float", "min":  0, "max":10},
'CornerUD'       :{"type": "float", "min":-10, "max":10},
'Pinch'          :{"type": "float", "min":  0, "max":10},
'LeftRightShapes':{"type": "float", "min":  0, "max":10, "keyable" : False },
'SmileFrownL'    :{"type": "float", "min":-10, "max":10}, 
'SmileFrownR'    :{"type": "float", "min":-10, "max":10}, 
'NarrowWideL'    :{"type": "float", "min":-10, "max":10}, 
'NarrowWideR'    :{"type": "float", "min":-10, "max":10}, 
'CornerL'        :{"type": "float", "min":-10, "max":10}, 
'CornerR'        :{"type": "float", "min":-10, "max":10}, 
'PinchL'         :{"type": "float", "min":  0, "max":10},
'PinchR'         :{"type": "float", "min":  0, "max":10},
'UpperLip'       :{"type": "float", "min":  0, "max":10, "keyable" : False },
'UpperLipSneerL' :{"type": "float", "min":  0, "max":10},
'UpperLipSneerR' :{"type": "float", "min":  0, "max":10},
'UpperLipMidUD'  :{"type": "float", "min":-10, "max":10}, 
'LowerLip'       :{"type": "float", "min":  0, "max":10, "keyable" : False },
'LowerLipSneerL' :{"type": "float", "min":  0, "max":10},
'LowerLipSneerR' :{"type": "float", "min":  0, "max":10},
'LowerLipMidUD'  :{"type": "float", "min":-10, "max":10}, 
'Jaw'            :{"type": "float", "min":  0, "max":10, "keyable" : False },
'StickyLips'     :{"type": "float", "min":  0, "max":10}
}
mouthMover = {
'UD'            :{"type": "float", "min":-10, "max":10}, 
'LR'            :{"type": "float", "min":-10, "max":10}, 
'FB'            :{"type": "float", "min":-10, "max":10}, 
'TILT'          :{"type": "float", "min":-10, "max":10},
'Upper_Lip'     :{"type": "float", "min":-10, "max":10 , "keyable" : False},
'UpperLipUD'    :{"type": "float", "min":-10, "max":10},
'UpperLipLR'    :{"type": "float", "min":-10, "max":10},
'UpperLipFB'    :{"type": "float", "min":-10, "max":10},
'UpperLipTILT'  :{"type": "float", "min":-10, "max":10},
'UpperLipCurl'  :{"type": "float", "min":-10, "max":10},
'Lower_Lip'     :{"type": "float", "min":-10, "max":10 , "keyable" : False},
'LowerLipUD'    :{"type": "float", "min":-10, "max":10},
'LowerLipLR'    :{"type": "float", "min":-10, "max":10},
'LowerLipFB'    :{"type": "float", "min":-10, "max":10},
'LowerLipTILT'  :{"type": "float", "min":-10, "max":10},
'LowerLipCurl'  :{"type": "float", "min":-10, "max":10},
'SecondryShapes':{"Type": "enum", "enumNames":["Off","On"]}
}

