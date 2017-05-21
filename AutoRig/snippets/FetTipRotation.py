import maya.cmds as cmds
from RMPY import RMRigTools


def FetTipRotationCorrect(side="RH"):
    # "Character_LF_TipGrp00_UDF_Rig"
    # "Character01_LF_ankleIK00_ctr_Rig"
    # "Character_LF_TipGrp00_grp_Rig"
    ArrayOfChildren = RMRigTools.RMRemoveChildren("Character_%s_TipGrp00_UDF_Rig" % side)
    childGroup = RMRigTools.RMCreateGroupOnObj("Character_%s_TipGrp00_UDF_Rig" % side, Type="world")
    ParentConst = cmds.listConnections("Character_%s_TipGrp00_grp_Rig" % side, type="parentConstraint")
    cmds.delete(ParentConst[0])
    cmds.makeIdentity("Character_%s_TipGrp00_grp_Rig" % side)
    loc = cmds.spaceLocator(name="ReferencePoint")[0]
    RMRigTools.RMAlign("Character_%s_TipGrp00_grp_Rig" % side, loc, 2)
    cmds.setAttr("%s.rotateX" % loc, 0)
    # cmds.setAttr( "%s.rotateX"%loc, -90)f
    cmds.setAttr("%s.rotateZ" % loc, 0)
    RMRigTools.RMAlign(loc, "Character_%s_TipGrp00_grp_Rig" % side, 2)
    cmds.parentConstraint("Character01_%s_ankleIK00_ctr_Rig" % side, "Character_%s_TipGrp00_grp_Rig" % side, mo=True,
                          name=ParentConst[0])
    cmds.parent(childGroup, "Character_%s_TipGrp00_UDF_Rig" % side)
    RMRigTools.RMParentArray(childGroup, ArrayOfChildren)
    cmds.delete(loc)


def fetAnkleRotationCorrect(side="RH"):
    # IKCorrection
    control = "Character01_%s_ankleIK00_ctr_Rig" % side
    Ball = "Character01_%s_BallIk00_jnt_Rig" % side
    # ArrayOfChildren = RMRigTools.RMRemoveChildren (control)
    ParentConst = cmds.listConnections(control, type="parentConstraint")
    IKGroup = cmds.listConnections("%s.constraintRotateX" % ParentConst[0])[0]
    cmds.delete(ParentConst)
    controlParent = cmds.listRelatives(control, parent=True)
    loc = cmds.spaceLocator(name="ReferencePoint")[0]
    loc2 = cmds.spaceLocator(name="ReferencePoint")[0]

    Balltranslation = cmds.xform(Ball, q=True, ws=True, translation=True)
    controlTranslation = cmds.xform(control, q=True, ws=True, translation=True)
    cmds.xform(loc, translation=(Balltranslation[0], controlTranslation[1], Balltranslation[2]))
    RMRigTools.RMAlign(control, loc2, 3)
    cmds.aimConstraint(loc, loc2, aimVector=[0, 1, 0], upVector=[-1, 0, 0], worldUpType='scene')
    RMRigTools.RMAlign(loc2, controlParent, 3)
    cmds.parentConstraint(control, IKGroup, mo=True)

    # FK Correction
    FKcontrol = "Character01_%s_ankleFK00_ctr_Rig" % side
    ParentConst = cmds.listConnections(FKcontrol, type="parentConstraint")
    resultingSet = set(ParentConst)
    FKparentConstrained = []
    for eachConstraint in resultingSet:
        FKparentConstrained.append(cmds.listConnections("%s.constraintRotateX" % eachConstraint)[0])
        cmds.delete(eachConstraint)

    FKcontrolParent = cmds.listRelatives(FKcontrol, parent=True)
    RMRigTools.RMAlign(control, FKcontrolParent[0], 3)

    for eachobject in FKparentConstrained:
        cmds.parentConstraint(FKcontrol, eachobject, mo=True)
    cmds.delete(loc)
    cmds.delete(loc2)
