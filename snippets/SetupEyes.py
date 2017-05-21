import maya.cmds as cmds
import RMRigTools


class GenericFacial():
	self.FaceBlendShapesDic={
				"REyeCls":{},
				"LEyeCls":{},
				"Wide":{}, 
				"Narrow":{},
				"UprLipUp":{},
				"UprLipDn":{},
				"LwrLipUp":{},
				"LwrLipDn":{},
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
	def LinkM (self):
		cmds.blendShape("Character",name="FacialBS")
		NumBS=0
		for keys in sorted(self.FaceBlendShapeDic.iterkeys()):
			if cmds.objExists(keys):
				cmds.blendShape("FacialBS",edit=True, target=["Character",NumBS,keys,1.0])
				self.FaceBlendShapeDic[keys]["index"] = NumBS
				self.FaceBlendShapeDic[keys]["Exists"] = True
				NumBS+=1
			else:
				print "el objeto" + keys + " no fue encontrado."
				self.FaceBlendShapeDic[keys]["Exists"] = False
		
		if cmds.objExists("RHEyeLashesClosed") and cmds.objExists("LFEyeLashesClosed") :
			cmds.blendShape("EyeLashes",name="EyeLashesBS")
			cmds.blendShape("EyeLashesBS",edit=True, target=["EyeLashes",0,"RHEyeLashesClosed",1.0])
			cmds.blendShape("EyeLashesBS",edit=True, target=["EyeLashes",1,"LFEyeLashesClosed",1.0])

			("Character_RH_ReyeCls_ctrl_fc.translateY", "EyeLashesBS.RHEyeLashesClosed",[[0,0],[-2,1]])

			RMRigTools.connectWithLimits("Character_LF_LeyeCls_ctrl_fc.translateY", "EyeLashesBS.LFEyeLashesClosed",[[0,0],[-2,1]])

		
		if self.FaceBlendShapeDic["REyeCls"]["Exists"]:
			RMRigTools.connectWithLimits("Character_RH_ReyeCls_ctrl_fc.translateY", "FacialBS.REyeCls",[[0,0],[-2,1]])
		if self.FaceBlendShapeDic["LEyeCls"]["Exists"]:
			RMRigTools.connectWithLimits("Character_LF_LeyeCls_ctrl_fc.translateY", "FacialBS.LEyeCls",[[0,0],[-2,1]])


		if self.FaceBlendShapeDic["RBrowOutUp"]["Exists"]:
			RMRigTools.connectWithLimits("Character_MD_RBrowOutUpDn_ctrl_fc.translateY", "FacialBS.RBrowOutUp",[[0,0],[1,1]])
		if self.FaceBlendShapeDic["RBrowOutDn"]["Exists"]:
			RMRigTools.connectWithLimits("Character_MD_RBrowOutUpDn_ctrl_fc.translateY", "FacialBS.RBrowOutDn",[[0,0],[-1,1]])	
		if self.FaceBlendShapeDic["RBrowInUp"]["Exists"]:
			RMRigTools.connectWithLimits("Character_MD_RBrowOutUpDn_ctrl_fc.translateX", "FacialBS.RBrowInUp",[[0,0],[1,1]])
		if self.FaceBlendShapeDic["RBrowInDn"]["Exists"]:
			RMRigTools.connectWithLimits("Character_MD_RBrowOutUpDn_ctrl_fc.translateX", "FacialBS.RBrowInDn",[[0,0],[-1,1]])

		if self.FaceBlendShapeDic["LBrowOutUp"]["Exists"]:
			RMRigTools.connectWithLimits("Character_MD_LBrowOutUpDn_ctrl_fc.translateY", "FacialBS.LBrowOutUp",[[0,0],[1,1]])
		if self.FaceBlendShapeDic["LBrowOutDn"]["Exists"]:
			RMRigTools.connectWithLimits("Character_MD_LBrowOutUpDn_ctrl_fc.translateY", "FacialBS.LBrowOutDn",[[0,0],[-1,1]])	
		if self.FaceBlendShapeDic["LBrowInUp"]["Exists"]:
			RMRigTools.connectWithLimits("Character_MD_LBrowOutUpDn_ctrl_fc.translateX", "FacialBS.LBrowInUp",[[0,0],[1,1]])
		if self.FaceBlendShapeDic["LBrowInDn"]["Exists"]:
			RMRigTools.connectWithLimits("Character_MD_LBrowOutUpDn_ctrl_fc.translateX", "FacialBS.LBrowInDn",[[0,0],[-1,1]])

		if self.FaceBlendShapeDic["Browsqueeze"]["Exists"]:
			RMRigTools.connectWithLimits("Character_MD_Browsqueeze_ctrl_fc.translateY", "FacialBS.Browsqueeze",[[0,0],[1,1]])

		if self.FaceBlendShapeDic["UprLipUp"]["Exists"]:
			RMRigTools.connectWithLimits("Character_MD_UprLipUpDn_ctrl_fc.translateY", "FacialBS.UprLipUp",[[0,0],[1,1]])	
		if self.FaceBlendShapeDic["UprLipDn"]["Exists"]:
			RMRigTools.connectWithLimits("Character_MD_UprLipUpDn_ctrl_fc.translateY", "FacialBS.UprLipDn",[[0,0],[-1,1]])	

		if self.FaceBlendShapeDic["LwrLipUp"]["Exists"]:
			RMRigTools.connectWithLimits("Character_MD_LowerLipUpDn_ctrl_fc.translateY", "FacialBS.LwrLipUp",[[0,0],[1,1]])	
		if self.FaceBlendShapeDic["LwrLipDn"]["Exists"]:
			RMRigTools.connectWithLimits("Character_MD_LowerLipUpDn_ctrl_fc.translateY", "FacialBS.LwrLipDn",[[0,0],[-1,1]])	


		if self.FaceBlendShapeDic["Wide"]["Exists"]:
			RMRigTools.connectWithLimits("Character_MD_JawOpen_ctrl_fc.translateX", "FacialBS.Wide",[[0,0],[1,1]])
		if self.FaceBlendShapeDic["Narrow"]["Exists"]:
			RMRigTools.connectWithLimits("Character_MD_JawOpen_ctrl_fc.translateX", "FacialBS.Narrow",[[0,0],[-1,1]])
		if self.FaceBlendShapeDic["Wide"]["Exists"]:
			RMRigTools.connectWithLimits("Character_MD_JawOpen_ctrl_fc.translateX", "FacialBS.Wide",[[0,0],[1,1]])

		if cmds.objExists("Jaw"):
			RMRigTools.connectWithLimits("Character_MD_JawOpen_ctrl_fc.translateY", "Jaw.rotateZ",[[0,0],[-1,-20],[1,7]])
			RMRigTools.connectWithLimits("Character_MD_JawFwd_ctrl_fc.translateX", "Jaw.rotateY",[[0,0],[1,20],[-1,-20]])
			RMRigTools.connectWithLimits("Character_MD_JawFwd_ctrl_fc.translateY", "Jaw.translateX",[[0,0],[1,-1],[-1,1]])


		if self.FaceBlendShapeDic["RSmile"]["Exists"]:
			RMRigTools.connectWithLimits("Character_MD_MouthEmotion_ctrl_fc.translateY", "FacialBS.RSmile",[[0,0],[1,1]])
		if self.FaceBlendShapeDic["RFrown"]["Exists"]:
			RMRigTools.connectWithLimits("Character_MD_MouthEmotion_ctrl_fc.translateY", "FacialBS.RFrown",[[0,0],[-1,1]])	
		if self.FaceBlendShapeDic["LSmile"]["Exists"]:
			RMRigTools.connectWithLimits("Character_MD_MouthEmotion_ctrl_fc.translateX", "FacialBS.LSmile",[[0,0],[1,1]])
		if self.FaceBlendShapeDic["LFrown"]["Exists"]:
			RMRigTools.connectWithLimits("Character_MD_MouthEmotion_ctrl_fc.translateX", "FacialBS.LFrown",[[0,0],[-1,1]])

		if self.FaceBlendShapeDic["RSquint"]["Exists"]:
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

		if self.FaceBlendShapeDic["LSquint"]["Exists"]:
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

		if self.FaceBlendShapeDic["RSneer"]["Exists"]:
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
		if self.FaceBlendShapeDic["LSneer"]["Exists"]:
			cmds.expression(name = "LSneerExpresion",unitConversion = "none")
			script ='''\nfloat $Zval=0;
				\nfloat $Xval=0;
				\nif (Character_MD_EyeSneer_ctrl_fc.translateY>=0)
				\n{$Zval=Character_MD_EyeSneer_ctrl_fc.translateY;}
				\nelse{$Zval=0;}
				\nif (Character_MD_EyeSneer_ctrl_fc.translateX>=0) 
				\n{$Xval=Character_MD_EyeSneer_ctrl_fc.translateX;}
				\nelse {$Xval = 0;}
				\nFacialBS.LSneer = ($Zval-$Xval);'''
			cmds.expression("LSneerExpresion",edit=True,string=script,unitConversion = "none")
	def SetupEyes(self):
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

#RMRigTools.connectWithLimits("REyeFollow.rotateY","FacialBS.REyeRollLf",[[0,0],[16,1]])
#RMRigTools.connectWithLimits("REyeFollow.rotateY","FacialBS.REyeRollRh",[[0,0],[-16,1]])
#RMRigTools.connectWithLimits("LEyeFollow.rotateY","FacialBS.LEyeRollLf",[[0,0],[16,1]])
#RMRigTools.connectWithLimits("LEyeFollow.rotateY","FacialBS.LEyeRollRh",[[0,0],[-16,1]])

#RMRigTools.connectWithLimits("Character_RH_ReyeCls_ctrl_fc.translateY", "FacialBS.REyeCls",[[0,0],[-2,1]])
#RMRigTools.connectWithLimits("Character_LF_LeyeCls_ctrl_fc.translateY", "FacialBS.LEyeCls",[[0,0],[-2,1]])
#RMRigTools.connectWithLimits("Character_MD_AutoEyeLids_ctrl_fc.translateY","FacialBS.Incisibus",[[0,0],[-2,1]])


RMRigTools.connectWithLimits("Character_MD_UprLipUpDn_ctrl_fc.translateY", "FacialBS.UpperLipUp",[[0,0],[1,1]])	
RMRigTools.connectWithLimits("Character_MD_UprLipUpDn_ctrl_fc.translateY", "FacialBS.UpperLipDn",[[0,0],[-1,1]])	
RMRigTools.connectWithLimits("Character_MD_LowerLipUpDn_ctrl_fc.translateY", "FacialBS.LowerLipUp",[[0,0],[1,1]])	
RMRigTools.connectWithLimits("Character_MD_LowerLipUpDn_ctrl_fc.translateY", "FacialBS.LowerLipDn",[[0,0],[-1,1]])	

#SetupEyes()
#LinkM(self.FaceBlendShapeDic)