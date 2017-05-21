from AutoRig import RMSpaceSwitch


SPSW = RMSpaceSwitch.RMSpaceSwitch()

SkeletonSkn = ["DogSkeleton_LF_Leg00_sknjnt_DetachLeg",
				"DogSkeleton_LF_Leg01_sknjnt_DetachLeg",
				"DogSkeleton_LF_Leg02_sknjnt_DetachLeg",
				"DogSkeleton_LF_Leg03_sknjnt_DetachLeg"]

SkeletonFK = ["DogSkeleton_LF_LegFK00_jnt_DetachLeg",
				"DogSkeleton_LF_LegFK01_jnt_DetachLeg",
				"DogSkeleton_LF_LegFK02_jnt_DetachLeg",
				"DogSkeleton_LF_LegFK03_jnt_DetachLeg"]

SkeletonIK = ["bn_l_dogSkeleton_MD_scapula_jnt_ful",
			  "bn_l_dogSkeleton_MD_armA_jnt_ful",
			  "bn_l_dogSkeleton_MD_elbow_jnt_ful",
			  "bn_l_dogSkeleton_MD_wrist_jnt_ful"]


SPSW.RMCreateListConstraintSwitch (["cc_l_frontPaw01_grp"], ["cc_l_frontPawFKRefPoint_grp"], "cc_l_Scapula01", SpaceSwitchName = "IKFKSwitch")
SPSW.RMCreateListConstraintSwitch (["cc_l_frontPaw01_grp"], ["cc_l_frontPawIKRefPoint_grp"], "cc_l_Scapula01", SpaceSwitchName = "IKFKSwitch", reverse = True)


