from AutoRig import RMLimbIKFK
from AutoRig.Hand import RMGenericHandRig
reload (RMLimbIKFK)
reload (RMGenericHandRig)
import maya.cmds as cmds

class RMBiped(object):
    def __init__(self, NameConv = None):
        if not NameConv:
            self.NameConv = RMNameConvention.RMNameConvention()
        else:
            self.NameConv = NameConv
        self.NameConv.DefaultNames["LastName"] = "Character01"
        self.SPSW = RMSpaceSwitch.RMSpaceSwitch()
    
    def CreateBipedRig(self):
        CharacterName = "MainCharacter"
        MainGroup = cmds.group(empty = True, name = CharacterName)
        mesh = cmds.group( empty = True, name = "msh_grp")
        rig = cmds.group( empty = True, name = "rig_grp")

        deformation = cmds.group( empty = True, name = "deformation")
        kinematics = cmds.group( empty = True, name = "kinematics")
        joints = cmds.group( empty = True, name = "joints")

        controls = cmds.group( empty = True, name = "controls_grp")
        cmds.parent(mesh ,MainGroup)
        cmds.parent(rig ,MainGroup)
        cmds.parent(controls ,MainGroup)
        cmds.parent(deformation , rig)
        cmds.parent(kinematics , rig)
        cmds.parent(joints , rig)
        



        '''arms = cmds.group(empty = True, name = "arm")
        arms = self.NameConv.RMRenameNameInFormat( arms ,Side = "RH", System = "kinematics")


        cmds.parent ( arms, kinematics )
        LimbArmRight = RMLimbIKFK.RMLimbIKFK(self.NameConv)
        LimbArmRight.RMLimbRig("Character01_RH_shoulder_pnt_rfr", FKAxisFree='110')
        
        armsControls = cmds.group(empty = True, name = "arm")
        armsControls = self.NameConv.RMRenameNameInFormat( armsControls ,Side = "RH", System = "controls")


        armsJoints = cmds.group(empty = True, name = "arm")
        armsJoints = self.NameConv.RMRenameNameInFormat( armsJoints ,Side = "RH", System = "joints")

        RMRigTools.RMParentArray(arms,LimbArmRight.kinematics)

        cmds.parent( LimbArmRight.FKparentGroup , armsJoints)
        cmds.parent( LimbArmRight.IKparentGroup , armsJoints)
        cmds.parent( LimbArmRight.SknParentGroup, armsJoints)
        
        cmds.parent( armsJoints, joints)
        
        cmds.parent( LimbArmRight.IKControls, armsControls)
        cmds.parent( LimbArmRight.FKControls, armsControls)

        cmds.parent( armsControls, controls)

        cmds.parent (LimbArmRight.TJArm.TwistControlResetPoint , armsControls)
        
        cmds.parent (LimbArmRight.TJArm.TwistResetJoints , deformation)'''

        
        '''LimbArmLeft = RMLimbIKFK.RMLimbIKFK(self.NameConv)
        LimbArmLeft.RMLimbRig("Character01_LF_shoulder_pnt_rfr",FKAxisFree='110')

        LimbLegRight = RMLimbIKFK.RMLimbIKFK(self.NameConv)
        LimbLegRight.RMLimbRig("Character01_LF_leg_pnt_rfr",FKAxisFree='101')
        LimbLegLeft = RMLimbIKFK.RMLimbIKFK(self.NameConv)
        LimbLegLeft.RMLimbRig("Character01_RH_leg_pnt_rfr",FKAxisFree='101')'''

        GHRightRig = RMGenericHandRig.RMGenericHandRig()
        GHRightRig.CreateHandRig("Character01_RH_palm_pnt_rfr")

        GHLeftRig = RMGenericHandRig.RMGenericHandRig()
        GHLeftRig.CreateHandRig("Character01_LF_palm_pnt_rfr")





BipedRig = RMBiped()
BipedRig.CreateBipedRig()