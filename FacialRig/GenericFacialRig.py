import maya.cmds as cmds
from RMPY import RMRigTools


class GenericFacial():
    def __init__(self):
        self.FaceBlendShapeDic = {
            "REyeCls": {},
            "LEyeCls": {},
            "Wide": {},
            "Narrow": {},
            "UprLipUp": {},
            "UprLipDn": {},
            "LwrLipUp": {},
            "LwrLipDn": {},
            "LSmile": {},
            "RSmile": {},
            "LFrown": {},
            "RFrown": {},
            "LBrowOutUp": {},
            "RBrowOutUp": {},
            "LBrowOutDn": {},
            "RBrowOutDn": {},
            "LBrowInUp": {},
            "RBrowInUp": {},
            "LBrowInDn": {},
            "RBrowInDn": {},
            "LBrowsqueeze": {},
            "RBrowsqueeze": {},
            "LSquint": {},
            "RSquint": {},
            "LBrowPositionUp": {},
            "LBrowPositionDn": {},
            "RBrowPositionUp": {},
            "RBrowPositionDn": {},
            "REyeRollLf": {},
            "REyeRollRh": {},
            "REyeRollUp": {},
            "REyeRollDn": {},
            "LEyeRollLf": {},
            "LEyeRollRh": {},
            "LEyeRollUp": {},
            "LEyeRollDn": {},
            "LSneer": {},
            "RSneer": {},
            "Incisibus": {}}
        self.IntermediateBlendShapeDic = {
            "LEyeHalfCls": {},
            "REyeHalfCls": {}
        }
        self.JawDic = {
            "Jaw": {}
        }
        self.EyesDic = {
            "LEye": {},
            "REye": {}  # ,
            # "REyeGeo":{},
            # "LEyeGeo":{},
        }

    def checkDicExistance(self, Dictionary):
        for keys in sorted(Dictionary.iterkeys()):
            if cmds.objExists(keys):
                Dictionary[keys]["Exists"] = True
            else:
                Dictionary[keys]["Exists"] = False

    def checkExistance(self):
        self.checkDicExistance(self.FaceBlendShapeDic)
        self.checkDicExistance(self.IntermediateBlendShapeDic)
        self.checkDicExistance(self.JawDic)
        self.checkDicExistance(self.EyesDic)

    def LinkFacial(self, BSname="CharacterFacialBS"):
        self.checkExistance()
        cmds.blendShape("Character", name=BSname)
        NumBS = 0
        for keys in sorted(self.FaceBlendShapeDic.iterkeys()):
            if cmds.objExists(keys):
                if keys == "LEyeCls" and cmds.objExists("LEyeHalfCls"):
                    cmds.blendShape(BSname, edit=True, target=["Character", NumBS, "LEyeHalfCls", .5])
                if keys == "REyeCls" and cmds.objExists("REyeHalfCls"):
                    cmds.blendShape(BSname, edit=True, target=["Character", NumBS, "REyeHalfCls", .5])
                cmds.blendShape(BSname, edit=True, target=["Character", NumBS, keys, 1.0])
                self.FaceBlendShapeDic[keys]["index"] = NumBS
                self.FaceBlendShapeDic[keys]["Exists"] = True

                NumBS += 1
            else:
                print "el objeto" + keys + " no fue encontrado."
                self.FaceBlendShapeDic[keys]["Exists"] = False

        if self.FaceBlendShapeDic["Incisibus"]["Exists"]:
            RMRigTools.connectWithLimits("Character_MD_Incisibus_ctrl_fc.translateY", BSname + ".Incisibus",
                                         [[0, 0], [2, 1]])

        if self.FaceBlendShapeDic["REyeCls"]["Exists"]:
            RMRigTools.connectWithLimits("Character_RH_ReyeCls_ctrl_fc.translateY", BSname + ".REyeCls",
                                         [[0, 0], [-2, 1]])
        if self.FaceBlendShapeDic["LEyeCls"]["Exists"]:
            RMRigTools.connectWithLimits("Character_LF_LeyeCls_ctrl_fc.translateY", BSname + ".LEyeCls",
                                         [[0, 0], [-2, 1]])

        if self.FaceBlendShapeDic["RBrowOutUp"]["Exists"]:
            RMRigTools.connectWithLimits("Character_MD_RBrowOutUpDn_ctrl_fc.translateY", BSname + ".RBrowOutUp",
                                         [[0, 0], [1, 1]])
        if self.FaceBlendShapeDic["RBrowOutDn"]["Exists"]:
            RMRigTools.connectWithLimits("Character_MD_RBrowOutUpDn_ctrl_fc.translateY", BSname + ".RBrowOutDn",
                                         [[0, 0], [-1, 1]])
        if self.FaceBlendShapeDic["RBrowInUp"]["Exists"]:
            RMRigTools.connectWithLimits("Character_MD_RBrowOutUpDn_ctrl_fc.translateX", BSname + ".RBrowInUp",
                                         [[0, 0], [1, 1]])
        if self.FaceBlendShapeDic["RBrowInDn"]["Exists"]:
            RMRigTools.connectWithLimits("Character_MD_RBrowOutUpDn_ctrl_fc.translateX", BSname + ".RBrowInDn",
                                         [[0, 0], [-1, 1]])

        if self.FaceBlendShapeDic["LBrowOutUp"]["Exists"]:
            RMRigTools.connectWithLimits("Character_MD_LBrowOutUpDn_ctrl_fc.translateY", BSname + ".LBrowOutUp",
                                         [[0, 0], [1, 1]])
        if self.FaceBlendShapeDic["LBrowOutDn"]["Exists"]:
            RMRigTools.connectWithLimits("Character_MD_LBrowOutUpDn_ctrl_fc.translateY", BSname + ".LBrowOutDn",
                                         [[0, 0], [-1, 1]])
        if self.FaceBlendShapeDic["LBrowInUp"]["Exists"]:
            RMRigTools.connectWithLimits("Character_MD_LBrowOutUpDn_ctrl_fc.translateX", BSname + ".LBrowInUp",
                                         [[0, 0], [1, 1]])
        if self.FaceBlendShapeDic["LBrowInDn"]["Exists"]:
            RMRigTools.connectWithLimits("Character_MD_LBrowOutUpDn_ctrl_fc.translateX", BSname + ".LBrowInDn",
                                         [[0, 0], [-1, 1]])

        if self.FaceBlendShapeDic["LBrowsqueeze"]["Exists"]:
            RMRigTools.connectWithLimits("Character_MD_Browsqueeze_ctrl_fc.translateY", (BSname + ".LBrowsqueeze"),
                                         [[-1, -1], [0, 0], [1, 1]])
        if self.FaceBlendShapeDic["RBrowsqueeze"]["Exists"]:
            RMRigTools.connectWithLimits("Character_MD_Browsqueeze_ctrl_fc.translateX", (BSname + ".RBrowsqueeze"),
                                         [[-1, -1], [0, 0], [1, 1]])

        if self.FaceBlendShapeDic["UprLipUp"]["Exists"]:
            RMRigTools.connectWithLimits("Character_MD_UprLipUpDn_ctrl_fc.translateY", BSname + ".UprLipUp",
                                         [[0, 0], [1, 1]])
        if self.FaceBlendShapeDic["UprLipDn"]["Exists"]:
            RMRigTools.connectWithLimits("Character_MD_UprLipUpDn_ctrl_fc.translateY", BSname + ".UprLipDn",
                                         [[0, 0], [-1, 1]])

        if self.FaceBlendShapeDic["LwrLipUp"]["Exists"]:
            RMRigTools.connectWithLimits("Character_MD_LowerLipUpDn_ctrl_fc.translateY", BSname + ".LwrLipUp",
                                         [[0, 0], [1, 1]])
        if self.FaceBlendShapeDic["LwrLipDn"]["Exists"]:
            RMRigTools.connectWithLimits("Character_MD_LowerLipUpDn_ctrl_fc.translateY", BSname + ".LwrLipDn",
                                         [[0, 0], [-1, 1]])

        if cmds.objExists("LeyeLookAt") and cmds.objExists("LeyeOrientacion") and self.FaceBlendShapeDic["LEyeRollLf"][
            "Exists"] and self.FaceBlendShapeDic["LEyeRollRh"]["Exists"]:
            if not cmds.objExists("LEyesHzFinalRotationPlus"):
                cmds.shadingNode("plusMinusAverage", asUtility=True, name="LEyesHzFinalRotationPlus")
                cmds.connectAttr("LeyeLookAt.rotateY", "LEyesHzFinalRotationPlus.input1D[0]")
                cmds.connectAttr("LeyeOrientacion.rotateY", "LEyesHzFinalRotationPlus.input1D[1]")

            if self.FaceBlendShapeDic["LEyeRollLf"]["Exists"]:
                RMRigTools.connectWithLimits("LEyesHzFinalRotationPlus.output1D", BSname + ".LEyeRollLf",
                                             [[0, 0], [45, 1]])

            if self.FaceBlendShapeDic["LEyeRollRh"]["Exists"]:
                RMRigTools.connectWithLimits("LEyesHzFinalRotationPlus.output1D", BSname + ".LEyeRollRh",
                                             [[0, 0], [-45, 1]])

        if cmds.objExists("ReyeLookAt") and cmds.objExists("ReyeOrientacion") and self.FaceBlendShapeDic["REyeRollLf"][
            "Exists"] and self.FaceBlendShapeDic["REyeRollRh"]["Exists"]:
            if not cmds.objExists("REyesHorizontalFinalRotationPlus"):
                cmds.shadingNode("plusMinusAverage", asUtility=True, name="REyesHorizontalFinalRotationPlus")
                cmds.connectAttr("ReyeLookAt.rotateY", "REyesHorizontalFinalRotationPlus.input1D[0]")
                cmds.connectAttr("ReyeOrientacion.rotateY", "REyesHorizontalFinalRotationPlus.input1D[1]")

            if self.FaceBlendShapeDic["REyeRollLf"]["Exists"]:
                RMRigTools.connectWithLimits("REyesHorizontalFinalRotationPlus.output1D", BSname + ".REyeRollLf",
                                             [[0, 0], [45, 1]])

            if self.FaceBlendShapeDic["REyeRollRh"]["Exists"]:
                RMRigTools.connectWithLimits("REyesHorizontalFinalRotationPlus.output1D", BSname + ".REyeRollRh",
                                             [[0, 0], [-45, 1]])

        if cmds.objExists("ReyeLookAt") and cmds.objExists("ReyeOrientacion") and self.FaceBlendShapeDic["REyeRollUp"][
            "Exists"] and self.FaceBlendShapeDic["REyeRollDn"]["Exists"]:
            if not cmds.objExists("REyesVerticalFinalRotationPlus"):
                cmds.shadingNode("plusMinusAverage", asUtility=True, name="REyesVerticalFinalRotationPlus")
                cmds.connectAttr("ReyeLookAt.rotateX", "REyesVerticalFinalRotationPlus.input1D[0]")
                cmds.connectAttr("ReyeOrientacion.rotateX", "REyesVerticalFinalRotationPlus.input1D[1]")

            if self.FaceBlendShapeDic["REyeRollUp"]["Exists"]:
                RMRigTools.connectWithLimits("REyesVerticalFinalRotationPlus.output1D", BSname + ".REyeRollUp",
                                             [[0, 0], [-45, 1]])

            if self.FaceBlendShapeDic["REyeRollDn"]["Exists"]:
                RMRigTools.connectWithLimits("REyesVerticalFinalRotationPlus.output1D", BSname + ".REyeRollDn",
                                             [[0, 0], [45, 1]])

        if cmds.objExists("LeyeLookAt") and cmds.objExists("LeyeOrientacion") and self.FaceBlendShapeDic["LEyeRollDn"][
            "Exists"] and self.FaceBlendShapeDic["LEyeRollUp"]["Exists"]:
            if not cmds.objExists("LEyesVerticalFinalRotationPlus"):
                cmds.shadingNode("plusMinusAverage", asUtility=True, name="LEyesVerticalFinalRotationPlus")
                cmds.connectAttr("LeyeLookAt.rotateX", "LEyesVerticalFinalRotationPlus.input1D[0]")
                cmds.connectAttr("LeyeOrientacion.rotateX", "LEyesVerticalFinalRotationPlus.input1D[1]")

            if self.FaceBlendShapeDic["LEyeRollUp"]["Exists"]:
                RMRigTools.connectWithLimits("LEyesVerticalFinalRotationPlus.output1D", BSname + ".LEyeRollUp",
                                             [[0, 0], [-45, 1]])

            if self.FaceBlendShapeDic["LEyeRollDn"]["Exists"]:
                RMRigTools.connectWithLimits("LEyesVerticalFinalRotationPlus.output1D", BSname + ".LEyeRollDn",
                                             [[0, 0], [45, 1]])

        if self.FaceBlendShapeDic["Wide"]["Exists"]:
            RMRigTools.connectWithLimits("Character_MD_JawOpen_ctrl_fc.translateX", BSname + ".Wide", [[0, 0], [1, 1]])
        if self.FaceBlendShapeDic["Narrow"]["Exists"]:
            RMRigTools.connectWithLimits("Character_MD_JawOpen_ctrl_fc.translateX", BSname + ".Narrow",
                                         [[0, 0], [-1, 1]])
        if self.FaceBlendShapeDic["Wide"]["Exists"]:
            RMRigTools.connectWithLimits("Character_MD_JawOpen_ctrl_fc.translateX", BSname + ".Wide", [[0, 0], [1, 1]])

        if self.FaceBlendShapeDic["RSmile"]["Exists"]:
            RMRigTools.connectWithLimits("Character_MD_MouthEmotion_ctrl_fc.translateY", BSname + ".RSmile",
                                         [[0, 0], [1, 1]])
        if self.FaceBlendShapeDic["RFrown"]["Exists"]:
            RMRigTools.connectWithLimits("Character_MD_MouthEmotion_ctrl_fc.translateY", BSname + ".RFrown",
                                         [[0, 0], [-1, 1]])
        if self.FaceBlendShapeDic["LSmile"]["Exists"]:
            RMRigTools.connectWithLimits("Character_MD_MouthEmotion_ctrl_fc.translateX", BSname + ".LSmile",
                                         [[0, 0], [1, 1]])
        if self.FaceBlendShapeDic["LFrown"]["Exists"]:
            RMRigTools.connectWithLimits("Character_MD_MouthEmotion_ctrl_fc.translateX", BSname + ".LFrown",
                                         [[0, 0], [-1, 1]])

        if self.FaceBlendShapeDic["RSquint"]["Exists"]:
            RMRigTools.connectWithLimits("Character_RH_RSquint_ctrl_fc.translateY", BSname + ".RSquint",
                                         [[0, 0], [1, 1]])

        if self.FaceBlendShapeDic["LSquint"]["Exists"]:
            RMRigTools.connectWithLimits("Character_LF_LSquint_ctrl_fc.translateY", BSname + ".LSquint",
                                         [[0, 0], [1, 1]])

        if self.FaceBlendShapeDic["RSneer"]["Exists"]:
            RMRigTools.connectWithLimits("Character_RH_RSneer_ctrl_fc.translateY", BSname + ".RSneer", [[0, 0], [1, 1]])
        if self.FaceBlendShapeDic["LSneer"]["Exists"]:
            RMRigTools.connectWithLimits("Character_LF_LSneer_ctrl_fc.translateY", BSname + ".LSneer", [[0, 0], [1, 1]])

        if self.FaceBlendShapeDic["LBrowPositionUp"]["Exists"]:
            RMRigTools.connectWithLimits("Character_LF_LBrowPosition_ctrl_fc.translateY", BSname + ".LBrowPositionUp",
                                         [[0, 0], [1, 1]])

        if self.FaceBlendShapeDic["RBrowPositionUp"]["Exists"]:
            RMRigTools.connectWithLimits("Character_RH_RBrowPosition_ctrl_fc.translateY", BSname + ".RBrowPositionUp",
                                         [[0, 0], [1, 1]])

        if self.FaceBlendShapeDic["LBrowPositionDn"]["Exists"]:
            RMRigTools.connectWithLimits("Character_LF_LBrowPosition_ctrl_fc.translateY", BSname + ".LBrowPositionDn",
                                         [[0, 0], [-1, 1]])

        if self.FaceBlendShapeDic["RBrowPositionDn"]["Exists"]:
            RMRigTools.connectWithLimits("Character_RH_RBrowPosition_ctrl_fc.translateY", BSname + ".RBrowPositionDn",
                                         [[0, 0], [-1, 1]])

    def JawSetup(self):
        if cmds.objExists("Jaw"):
            RMRigTools.connectWithLimits("Character_MD_JawOpen_ctrl_fc.translateY", "Jaw.rotateZ",
                                         [[0, 0], [-1, -20], [1, 7]])
            RMRigTools.connectWithLimits("Character_MD_JawFwd_ctrl_fc.translateX", "Jaw.rotateY",
                                         [[0, 0], [1, 20], [-1, -20]])
            RMRigTools.connectWithLimits("Character_MD_JawFwd_ctrl_fc.translateY", "Jaw.translateX",
                                         [[0, 0], [1, -1], [-1, 1]])

    def SetupEyes(self):

        if cmds.objExists("LEye") and cmds.objExists("REye"):
            cmds.group(em=True, name="ReyeOrientacion")
            cmds.joint(name="REyeJoint")
            cmds.group(em=True, name="ReyeBase")
            cmds.group(em=True, name="ReyeLookAt")
            cmds.group(em=True, name="ReyePointLookAt")

            cmds.group(em=True, name="LeyeOrientacion")
            cmds.joint(name="LEyeJoint")
            cmds.group(em=True, name="LeyeBase")
            cmds.group(em=True, name="LeyeLookAt")
            cmds.group(em=True, name="LeyePointLookAt")

            cmds.group(em=True, name="eyeOrientation")

            RMRigTools.RMAlign("LEye", "LeyeBase", 3)
            RMRigTools.RMAlign("LEye", "LeyeOrientacion", 3)
            RMRigTools.RMAlign("LEye", "LeyeLookAt", 3)
            RMRigTools.RMAlign("LEye", "LeyePointLookAt", 3)

            cmds.move(10, "LeyePointLookAt", moveZ=True)
            EyeParent = cmds.listRelatives("LEye", parent=True)
            cmds.parent("LeyeBase", EyeParent)
            cmds.parent("LeyeLookAt", "LeyeBase")
            cmds.parent("LeyeOrientacion", "LeyeLookAt")

            cmds.aimConstraint("LeyePointLookAt", "LeyeLookAt", aimVector=[0, 0, 1], worldUpObject="eyeOrientation",
                               worldUpType="objectrotation")

            cmds.expression(name="LEyeExpresionX", unitConversion="none")
            script = "LeyeOrientacion.rotateY = (Character_LF_Ojo_Ctrl_fc.translateX * 4 + Character_MD_OjoRectangle_ctrl_fc.translateX * 4)/10"
            cmds.expression("LEyeExpresionX", edit=True, string=script, unitConversion="none")
            cmds.expression(name="LEyeExpresionY", unitConversion="none")
            script = "LeyeOrientacion.rotateX = -(Character_LF_Ojo_Ctrl_fc.translateY * 4 + Character_MD_OjoRectangle_ctrl_fc.translateY * 4)/10"
            cmds.expression("LEyeExpresionY", edit=True, string=script, unitConversion="none")

            RMRigTools.RMAlign("REye", "ReyeBase", 3)
            RMRigTools.RMAlign("REye", "ReyeOrientacion", 3)
            RMRigTools.RMAlign("REye", "ReyeLookAt", 3)
            RMRigTools.RMAlign("REye", "ReyePointLookAt", 3)

            cmds.move(10, "ReyePointLookAt", moveZ=True)
            EyeParent = cmds.listRelatives("REye", parent=True)
            cmds.parent("ReyeBase", EyeParent)
            cmds.parent("ReyeLookAt", "ReyeBase")
            cmds.parent("ReyeOrientacion", "ReyeLookAt")

            cmds.aimConstraint("ReyePointLookAt", "ReyeLookAt", aimVector=[0, 0, 1], worldUpObject="eyeOrientation",
                               worldUpType="objectrotation")

            cmds.expression(name="REyeExpresionX", unitConversion="none")
            script = "ReyeOrientacion.rotateY = (Character_RH_Ojo_Ctrl_fc.translateX * 4 + Character_MD_OjoRectangle_ctrl_fc.translateX * 4)/10"
            cmds.expression("REyeExpresionX", edit=True, string=script, unitConversion="none")

            cmds.expression(name="REyeExpresionY", unitConversion="none")
            script = "ReyeOrientacion.rotateX = -(Character_RH_Ojo_Ctrl_fc.translateY * 4 + Character_MD_OjoRectangle_ctrl_fc.translateY * 4)/10"
            cmds.expression("REyeExpresionY", edit=True, string=script, unitConversion="none")

            RMRigTools.RMAlign(EyeParent, "eyeOrientation", 1)

            cmds.parent("eyeOrientation", EyeParent)

            # $LeyeBase.parent=$LEye.parent;
            # $ReyeBase.parent=$REye.parent;

            cmds.parent("LEye", "LeyeOrientacion");
            cmds.parent("REye", "ReyeOrientacion");

            '''if cmds.objExists("*REyeGeo*"):
                EyeGeo=cmds.ls("*REyeGeo*",type="transform")
                for geo in EyeGeo:
                    cmds.bindSkin(geo,"REyeJoint")

            if cmds.objExists("*LEyeGeo*"):
                EyeGeo=cmds.ls("*LEyeGeo*",type="transform")
                for geo in EyeGeo:
                    cmds.bindSkin(geo,"LEyeJoint")
            '''

            cmds.parent("OjosLookAt", EyeParent);

            cmds.parent("LeyePointLookAt", "OjosLookAt_L");
            cmds.parent("ReyePointLookAt", "OjosLookAt_R");
        else:
            print "No existen los objetos LEye y REye"

            # SetupEyes()
            # LinkM(self.FaceBlendShapeDic)
