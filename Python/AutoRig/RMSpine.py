import maya.cmds
import maya.api.OpenMaya as om
import RMNameConvention
reload(RMNameConvention)
import RMRigTools
reload(RMRigTools)
import RMRigShapeControls
import pprint


class RMSpine(object):
    def __init__(self,NameConv = None):
        if not NameConv:
            self.NameConv = RMNameConvention.RMNameConvention()
        else:
            self.NameConv = NameConv
        self.spineIK = None
        self.spineJoints = None
        self.rootSpine = None
        self.spineCurve = None

    def RMCreateSpineRig(self,SpineRef):

        self.RMCreateJointStructure(SpineRef)
        self.RMCreateSpineIKSystem()

    def RMCreateJointStructure(self,SpineRef):
        self.rootSpine , joints = RMRigTools.RMCreateBonesAtPoints(SpineRef,ZAxisOrientation = "z")
        self.spineJoints = joints
        return joints     

    
    
    def RMCreateSpineIKSystem(self):
        self.spineIK, effector, self.spineCurve = cmds.ikHandle(startJoint = self.spineJoints[0],endEffector = self.spineJoints[len(self.spineJoints)-1],createCurve = True,numSpans = len(self.spineJoints) ,solver = "ikSplineSolver",name = "spineIK")
        self.spineIK = self.NameConv.RMRenameBasedOnBaseName(self.spineJoints[len(self.spineJoints)-1],self.spineIK)
        effector = self.NameConv.RMRenameBasedOnBaseName(self.spineJoints[len(self.spineJoints)-1],effector,NewName = "spineIKEffector")
        self.spineCurve = self.NameConv.RMRenameBasedOnBaseName(self.spineJoints[len(self.spineJoints)-1],self.spineCurve,NewName = "spineIKCurve")
        Clusters = RMRigTools.RMCreateClustersOnCurve(self.spineCurve)
        ClustersGroup = RMRigTools.RMCreateGroupOnObj(Clusters[0])
        RMRigTools.RMParentArray(ClustersGroup,Clusters[1:])
        COG = RMRigShapeControls.RMCreateBoxCtrl(self.spineJoints[0],Yratio=3,Zratio=3)
        COG = self.NameConv.RMRenameSetFromName(COG,"COG","Name")
        ResetCOG = RMRigTools.RMCreateGroupOnObj(COG)
        Chest = RMRigShapeControls.RMCreateBoxCtrl(self.spineJoints[len(self.spineJoints) - 1],Yratio=3,Zratio=3)
        Chest = self.NameConv.RMRenameSetFromName(Chest,"Chest","Name")
        ResetChest = RMRigTools.RMCreateGroupOnObj(Chest)
        cmds.parent(ResetChest,COG)

        cmds.setAttr(self.spineIK + ".dTwistControlEnable",1)
        cmds.setAttr(self.spineIK + ".dWorldUpType",4)
        cmds.setAttr(self.spineIK + ".dForwardAxis",0)
        cmds.setAttr(self.spineIK + ".dWorldUpAxis",0)
        cmds.connectAttr(COG + ".worldMatrix[0]", self.spineIK + ".dWorldUpMatrix")
        cmds.connectAttr(Chest + ".worldMatrix[0]", self.spineIK + ".dWorldUpMatrixEnd")


        
        



RSP = RMSpine()
spineJoints = ["Character01_MD_Spine_pnt_rfr","Character01_MD_Spine1_pnt_rfr","Character01_MD_Spine2_pnt_rfr","Character01_MD_Spine3_pnt_rfr","Character01_MD_Spine4_pnt_rfr"]
RSP.RMCreateSpineRig(spineJoints)


