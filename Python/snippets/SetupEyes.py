import maya.cmds as cmds
import RMRigTools

FaceBlendShapesDic={
				"REyeCls":{},
				"LEyeCls":{},
				"Wide":{}, 
				"Narrow":{},
				"UprLipUp":{},
				"UprLipDn":{},
				"LSmile":{},
				"RSmile":{},
				"LFrown" :{},
				"RFrown":{}, 
				"LBrowOutUp":{},
				"RBrowOutUp":{},
				"LBrowOutDn":{}, 
				"RBrowOutDn" :{},
				"LBrowInUp":{},
				"RBrowInUp":{},
				"LBrowInDn":{}, 
				"RBrowInDn":{} ,
				"Browsqueeze":{},
				"LSquint":{},
		        "RSquint":{},
				"REyeRollLf":{},
				"REyeRollRh":{},
				"LEyeRollLf":{},
				"LEyeRollRh":{},
				"LSneer":{},
				"RSneer":{},
				"Incisibus":{}
				}

def connectWithLimits(AttrX,AttrY,keys):
	for eachKey  in keys:
		cmds.setDrivenKeyframe(AttrY, currentDriver = AttrX,dv = eachKey[0],v =eachKey[1])


def LinkM (FaceBlendShapesDic):
	cmds.blendShape("Character",name="FacialBS")
	NumBS=0
	for keys in sorted(FaceBlendShapesDic.iterkeys()):
		if cmds.objExists(keys):
			cmds.blendShape("FacialBS",edit=True, target=["Character",NumBS,keys,1.0])
			FaceBlendShapesDic[keys]["index"] = NumBS
			NumBS+=1
		else:
			print "el objeto" +keys+ " no fue encontrado."
	
	cmds.blendShape("EyeLashes",name="EyeLashesBS")
	cmds.blendShape("EyeLashesBS",edit=True, target=["EyeLashes",0,"RHEyeLashesClosed",1.0])
	cmds.blendShape("EyeLashesBS",edit=True, target=["EyeLashes",1,"LFEyeLashesClosed",1.0])



	connectWithLimits("Character_RH_ReyeCls_ctrl_fc.translateY", "FacialBS.REyeCls",[[0,0],[-2,1]])
	connectWithLimits("Character_LF_LeyeCls_ctrl_fc.translateY", "FacialBS.LEyeCls",[[0,0],[-2,1]])

	connectWithLimits("Character_RH_ReyeCls_ctrl_fc.translateY", "EyeLashesBS.RHEyeLashesClosed",[[0,0],[-2,1]])
	connectWithLimits("Character_LF_LeyeCls_ctrl_fc.translateY", "EyeLashesBS.LFEyeLashesClosed",[[0,0],[-2,1]])


	connectWithLimits("Character_MD_RBrowOutUpDn_ctrl_fc.translateY", "FacialBS.RBrowOutUp",[[0,0],[1,1]])
	connectWithLimits("Character_MD_RBrowOutUpDn_ctrl_fc.translateY", "FacialBS.RBrowOutDn",[[0,0],[-1,1]])	
	connectWithLimits("Character_MD_RBrowOutUpDn_ctrl_fc.translateX", "FacialBS.RBrowInUp",[[0,0],[1,1]])
	connectWithLimits("Character_MD_RBrowOutUpDn_ctrl_fc.translateX", "FacialBS.RBrowInDn",[[0,0],[-1,1]])

	connectWithLimits("Character_MD_LBrowOutUpDn_ctrl_fc.translateY", "FacialBS.LBrowOutUp",[[0,0],[1,1]])
	connectWithLimits("Character_MD_LBrowOutUpDn_ctrl_fc.translateY", "FacialBS.LBrowOutDn",[[0,0],[-1,1]])	
	connectWithLimits("Character_MD_LBrowOutUpDn_ctrl_fc.translateX", "FacialBS.LBrowInUp",[[0,0],[1,1]])
	connectWithLimits("Character_MD_LBrowOutUpDn_ctrl_fc.translateX", "FacialBS.LBrowInDn",[[0,0],[-1,1]])


	connectWithLimits("Character_MD_Browsqueeze_ctrl_fc.translateY", "FacialBS.Browsqueeze",[[0,0],[1,1]])

	connectWithLimits("Character_MD_UprLipUpDn_ctrl_fc.translateY", "FacialBS.UprLipUp",[[0,0],[1,1]])	
	connectWithLimits("Character_MD_UprLipUpDn_ctrl_fc.translateY", "FacialBS.UprLipDn",[[0,0],[-1,1]])	

	connectWithLimits("Character_MD_JawOpen_ctrl_fc.translateX", "FacialBS.Wide",[[0,0],[1,1]])
	connectWithLimits("Character_MD_JawOpen_ctrl_fc.translateX", "FacialBS.Narrow",[[0,0],[-1,1]])

	connectWithLimits("Character_MD_JawOpen_ctrl_fc.translateY", "Jaw.rotateZ",[[0,0],[-1,-20],[1,7]])
	connectWithLimits("Character_MD_JawFwd_ctrl_fc.translateX", "Jaw.rotateY",[[0,0],[1,20],[-1,-20]])
	connectWithLimits("Character_MD_JawFwd_ctrl_fc.translateY", "Jaw.translateX",[[0,0],[1,-1],[-1,1]])

	connectWithLimits("Character_MD_JawOpen_ctrl_fc.translateX", "FacialBS.Wide",[[0,0],[1,1]])




	connectWithLimits("Character_MD_MouthEmotion_ctrl_fc.translateY", "FacialBS.RSmile",[[0,0],[1,1]])
	connectWithLimits("Character_MD_MouthEmotion_ctrl_fc.translateY", "FacialBS.RFrown",[[0,0],[-1,1]])	
	connectWithLimits("Character_MD_MouthEmotion_ctrl_fc.translateX", "FacialBS.LSmile",[[0,0],[1,1]])
	connectWithLimits("Character_MD_MouthEmotion_ctrl_fc.translateX", "FacialBS.LFrown",[[0,0],[-1,1]])

	cmds.expression(name = "RSquintExpresion",unitConversion = "none")
	script ='''\nfloat $Zval=0;
		\nfloat $Xval=0;
		\nif (Character_MD_EyeSquint_ctrl_fc.translateY>=0)
		\n{$Zval=Character_MD_EyeSquint_ctrl_fc.translateY;}
		\nelse{$Zval=0;}
		\nif (Character_MD_EyeSquint_ctrl_fc.translateX<=0) 
		\n{$Xval=-Character_MD_EyeSquint_ctrl_fc.translateX;}
		\nelse {$Xval = 0;}
		\nFacialBS.RSquint = ($Zval-$Xval);'''
	cmds.expression("RSquintExpresion",edit=True,string=script,unitConversion = "none")

	cmds.expression(name = "LSquintExpresion",unitConversion = "none")
	script ='''\nfloat $Zval=0;
		\nfloat $Xval=0;
		\nif (Character_MD_EyeSquint_ctrl_fc.translateY>=0)
		\n{$Zval=Character_MD_EyeSquint_ctrl_fc.translateY;}
		\nelse{$Zval=0;}
		\nif (Character_MD_EyeSquint_ctrl_fc.translateX>=0) 
		\n{$Xval=Character_MD_EyeSquint_ctrl_fc.translateX;}
		\nelse {$Xval = 0;}
		\nFacialBS.LSquint = ($Zval-$Xval);'''
	cmds.expression("LSquintExpresion",edit=True,string=script,unitConversion = "none")


	cmds.expression(name = "RSneerExpresion",unitConversion = "none")
	script ='''\nfloat $Zval=0;
		\nfloat $Xval=0;
		\nif (Character_MD_EyeSneer_ctrl_fc.translateY>=0)
		\n{$Zval=Character_MD_EyeSneer_ctrl_fc.translateY;}
		\nelse{$Zval=0;}
		\nif (Character_MD_EyeSneer_ctrl_fc.translateX<=0) 
		\n{$Xval=-Character_MD_EyeSneer_ctrl_fc.translateX;}
		\nelse {$Xval = 0;}
		\nFacialBS.RSneer = ($Zval-$Xval);'''
	cmds.expression("RSneerExpresion",edit=True,string=script,unitConversion = "none")

	cmds.expression(name = "LSneerExpresion",unitConversion = "none")
	script ='''\nfloat $Zval=0;
		\nfloat $Xval=0;
		\nif (Character_MD_EyeSneer_ctrl_fc.translateY>=0)
		\n{$Zval=Character_MD_EyeSneer_ctrl_fc.translateY;}
		\nelse{$Zval=0;}
		\nif (Character_MD_EyeSneer_ctrl_fc.translateX>=0) 
		\n{$Xval=Character_MD_EyeSquint_ctrl_fc.translateX;}
		\nelse {$Xval = 0;}
		\nFacialBS.LSneer = ($Zval-$Xval);'''
	cmds.expression("LSneerExpresion",edit=True,string=script,unitConversion = "none")



def SetupEyes():
	if cmds.objExists("LEye") and cmds.objExists("REye"):
		cmds.group(em=True,name="ReyeOrientacion")
		cmds.group(em=True,name="ReyeBase")
		cmds.group(em=True,name="ReyeLookAt")
		cmds.group(em=True,name="ReyePointLookAt")
		
		cmds.group(em=True,name="LeyeOrientacion")
		cmds.group(em=True,name="LeyeBase")
		cmds.group(em=True,name="LeyeLookAt")
		cmds.group(em=True,name="LeyePointLookAt")
		
		cmds.group(em=True,name="eyeOrientation")

		RMRigTools.RMAlign("LEye","LeyeBase",3)
		RMRigTools.RMAlign("LEye","LeyeOrientacion",3)
		RMRigTools.RMAlign("LEye","LeyeLookAt",3)
		RMRigTools.RMAlign("LEye","LeyePointLookAt",3)

		cmds.move(10,"LeyePointLookAt",moveZ=True)
		EyeParent = cmds.listRelatives("LEye",parent=True)
		cmds.parent("LeyeBase",EyeParent)
		cmds.parent("LeyeLookAt","LeyeBase")
		cmds.parent("LeyeOrientacion","LeyeLookAt")

		cmds.aimConstraint("LeyePointLookAt","LeyeLookAt",worldUpObject="eyeOrientation",worldUpType="objectrotation")

		cmds.expression(name = "LEyeExpresionX",unitConversion = "none")
		script = "LeyeOrientacion.rotateY = (Character_LF_Ojo_Ctrl_fc.translateX * 4 + Character_MD_OjoRectangle_ctrl_fc.translateX * 4)/10"
		cmds.expression("LEyeExpresionX",edit=True, string=script,unitConversion = "none")
		cmds.expression(name = "LEyeExpresionY",unitConversion = "none")
		script = "LeyeOrientacion.rotateZ = (Character_LF_Ojo_Ctrl_fc.translateY * 4 + Character_MD_OjoRectangle_ctrl_fc.translateY * 4)/10"
		cmds.expression("LEyeExpresionY",edit=True, string=script,unitConversion = "none")


		RMRigTools.RMAlign("REye","ReyeBase",3)
		RMRigTools.RMAlign("REye","ReyeOrientacion",3)
		RMRigTools.RMAlign("REye","ReyeLookAt",3)
		RMRigTools.RMAlign("REye","ReyePointLookAt",3)

		cmds.move(10,"ReyePointLookAt",moveZ=True)
		EyeParent = cmds.listRelatives("REye",parent=True)
		cmds.parent("ReyeBase",EyeParent)
		cmds.parent("ReyeLookAt","ReyeBase")
		cmds.parent("ReyeOrientacion","ReyeLookAt")

		cmds.aimConstraint("ReyePointLookAt","ReyeLookAt",worldUpObject="eyeOrientation",worldUpType="objectrotation")

		cmds.expression(name = "REyeExpresionX",unitConversion = "none")
		script = "ReyeOrientacion.rotateY = (Character_RH_Ojo_Ctrl_fc.translateX * 4 + Character_MD_OjoRectangle_ctrl_fc.translateX * 4)/10"
		cmds.expression("REyeExpresionX",edit=True, string=script,unitConversion = "none")

		cmds.expression(name = "REyeExpresionY",unitConversion = "none")
		script = "ReyeOrientacion.rotateZ = (Character_RH_Ojo_Ctrl_fc.translateY * 4 + Character_MD_OjoRectangle_ctrl_fc.translateY * 4)/10"
		cmds.expression("REyeExpresionY",edit=True, string=script,unitConversion = "none")
		
		RMRigTools.RMAlign(EyeParent,"eyeOrientation",1)
		cmds.parent("eyeOrientation",EyeParent)

		#$LeyeBase.parent=$LEye.parent;
		#$ReyeBase.parent=$REye.parent;

		cmds.parent("LEye","LeyeOrientacion");
		cmds.parent("REye","ReyeOrientacion");
		
		
		cmds.parent("OjosLookAt",EyeParent);

		cmds.parent("LeyePointLookAt","OjosLookAt_L");
		cmds.parent("ReyePointLookAt","OjosLookAt_R");

	else:
		print "No existen los objetos LEye y REye"



#connectWithLimits("REyeFollow.rotateY","FacialBS.REyeRollLf",[[0,0],[16,1]])
#connectWithLimits("REyeFollow.rotateY","FacialBS.REyeRollRh",[[0,0],[-16,1]])
#connectWithLimits("LEyeFollow.rotateY","FacialBS.LEyeRollLf",[[0,0],[16,1]])
#connectWithLimits("LEyeFollow.rotateY","FacialBS.LEyeRollRh",[[0,0],[-16,1]])


connectWithLimits("Character_MD_AutoEyeLids_ctrl_fc.translateY","FacialBS.Incisibus",[[0,0],[-2,1]])