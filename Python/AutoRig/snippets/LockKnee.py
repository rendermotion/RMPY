import maya.cmds
from AutoRig import RMSpaceSwitch
import pprint as pp


group = cmds.group(empty=True, name = "Character01_LF_KneeLockDriver00_ctr_Rig")
SpcSw = RMSpaceSwitch.RMSpaceSwitch()
SpcSw.CreateSpaceSwitchReverse("Character01_LF_KneeLockDriver00_ctr_Rig",["Character01_LF_Knee00_jnt_Limbik", "Character01_LF_KneePoleVectorIK00_ctr_Rig"], "Character01_LF_KneePoleVectorIK00_ctr_Rig" ,Name = "KneeLock", mo = True, sswtype = "float")

pp.pprint (SpcSw.getParentConstraintDic("Character01_LF_SpaceSwitchKnee00_prc_Rig") )
cmds.parentConstraint("Character01_LF_Knee00_jnt_Limbik", "Character01_LF_Knee00_jnt_Limbskn" ,e=True, remove=True)
pp.pprint (SpcSw.getParentConstraintDic("Character01_LF_SpaceSwitchKnee00_prc_Rig") )
cmds.parentConstraint("Character01_LF_KneeLockDriver00_ctr_Rig", "Character01_LF_Knee00_jnt_Limbskn",mo=False)








