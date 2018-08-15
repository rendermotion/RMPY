import maya.cmds as cmds
from RMPY import RMRigTools
from RMPY import nameConvention


class EyeRig(object):
    def __init__(self, NameConv=None):
        if NameConv:
            self.NameConv = NameConv
        else:
            self.NameConv = nameConvention.NameConvention()

    def EyeLidsSetUp(self, EyeNode):

        Rigtools = RMRigTools.RMRigTools()
        EyeNodeBB = RMRigTools.boundingBoxInfo(EyeNode)
        eyeRadius = (EyeNodeBB.zmax - EyeNodeBB.zmin) / 2

        # eyeScale = cmds.getAttr("%s.scale"%EyeNode) [0]
        # cmds.setAttr ( EyeNode + ".scale", 1.0, 1.0, 1.0)


        MainUpperLid = cmds.joint(name="EyeUpperLid", rad=eyeRadius / 5)
        UpperLid = cmds.joint(name="EyeUpperLidTip", rad=eyeRadius / 5)
        MainLowerLid = cmds.joint(name="EyeLowerLid", rad=eyeRadius / 5)
        LowerLid = cmds.joint(name="EyeLowerLidTip", rad=eyeRadius / 5)

        RMRigTools.RMAlign(EyeNode, MainUpperLid, 3)
        EyeParent = Rigtools.RMCreateGroupOnObj(MainUpperLid, Type='parent')
        EyeParent = self.NameConv.rename_set_from_name(EyeParent, "EyeLidSpin", Token='name')
        MainEye = Rigtools.RMCreateGroupOnObj(EyeParent, Type='parent')
        MainEye = self.NameConv.rename_set_from_name(MainEye, "Eye", Token='name')

        upperLidParent = Rigtools.RMCreateGroupOnObj(MainUpperLid)
        upperLidParent = self.NameConv.rename_set_from_name(upperLidParent, "EyeUpperLidReset", Token='name')

        cmds.parent(MainLowerLid, EyeParent)
        LowerLidParent = Rigtools.RMCreateGroupOnObj(MainLowerLid)

        RMRigTools.RMAlign(EyeParent, LowerLid, 3)

        MiddleMainUpperLid = cmds.joint(name="EyeMiddleMainUpperLid", rad=eyeRadius / 5)
        MiddleUpperLid = cmds.joint(name="EyeMiddleUpperLidTip", rad=eyeRadius / 5)
        MiddleMainLowerLid = cmds.joint(name="EyeMiddleLowerLid", rad=eyeRadius / 5)
        MiddleLowerLid = cmds.joint(name="EyeMiddleLowerLidTip", rad=eyeRadius / 5)

        RMRigTools.RMAlign(EyeParent, MiddleMainUpperLid, 3)

        cmds.parent(MiddleMainUpperLid, upperLidParent)
        cmds.parent(MiddleMainLowerLid, LowerLidParent)

        cmds.setAttr("%s.translateX" % UpperLid, eyeRadius)
        cmds.setAttr("%s.translateX" % LowerLid, eyeRadius)
        cmds.setAttr("%s.translateX" % MiddleUpperLid, eyeRadius)
        cmds.setAttr("%s.translateX" % MiddleLowerLid, eyeRadius)

        mDUpper = cmds.shadingNode("multiplyDivide", asUtility=True, name="EyeUpperMultDiv")

        cmds.connectAttr("%s.rotate" % MainUpperLid, "%s.input1" % mDUpper)
        cmds.setAttr("%s.input2" % mDUpper, .5, .5, .5)
        cmds.connectAttr("%s.output" % mDUpper, "%s.rotate" % MiddleMainUpperLid)

        mDLower = cmds.shadingNode("multiplyDivide", asUtility=True, name="EyeLowerMultDiv")
        cmds.connectAttr("%s.rotate" % MainLowerLid, "%s.input1" % mDLower)
        cmds.setAttr("%s.input2" % mDLower, .5, .5, .5)
        cmds.connectAttr("%s.output" % mDLower, "%s.rotate" % MiddleMainLowerLid)

        # cmds.setAttr(EyeParent +".scale",eyeScale[0],eyeScale[1],eyeScale[2])
        cmds.setAttr("%s.rotateY" % MainEye, -90)
        cmds.select(EyeNode, replace=True)
        # latticeAttr, lattice, latticeBase = cmds.lattice(name = "EyeLattice", oc= True, dv = [2, 2, 2], ol =  2, ofd = (eyeRadius/3) )
        # latticeScale = cmds.getAttr(lattice+".scale")[0]


        # cmds.setAttr ( lattice + ".scale", float(latticeScale[0]) + float(eyeScale[0]), float(latticeScale[1]) + float(eyeScale[1]), float(latticeScale[2]) + float(eyeScale[2]))

        # renamingto NameConvention.
        if self.NameConv.is_name_in_format(EyeNode):
            side = self.NameConv.get_from_name(EyeNode, Token="Side")
        else:
            side = "MD"
        # latticeAttr, lattice, latticeBase,
        self.NameConv.rename_name_in_format(
            [mDUpper, mDLower, UpperLid, LowerLid, MiddleMainUpperLid, MiddleMainLowerLid], {'side':side})
        self.NameConv.rename_set_from_name([EyeParent, LowerLidParent, upperLidParent], side, Token="side")
        MainEye = self.NameConv.rename_set_from_name(MainEye, side, Token="side")

        self.NameConv.rename_name_in_format([MiddleUpperLid, MiddleLowerLid], {'objectType': "sknjnt", 'side': side})
        MainLowerLid = self.NameConv.rename_name_in_format(MainLowerLid, {'objectType': "sknjnt", 'side': side})
        MainUpperLid = self.NameConv.rename_name_in_format(MainUpperLid, {'objectType': "sknjnt", 'side': side})

        if not cmds.objExists("Character_MD_EyesRig00_grp_rig"):
            EyesRig = self.NameConv.set_name_in_format("EyesRig", Type="grp", System="rig")
            cmds.group(empty=True, name=EyesRig)
            RMRigTools.RMChangeRotateOrder(EyesRig, "xzy")
            cmds.setAttr("%s.rotateY" % EyesRig, -90)
        else:
            EyesRig = "Character_MD_EyesRig00_grp_rig"

        cmds.parent(MainEye, EyesRig)
        cmds.makeIdentity(MainUpperLid, apply=True, r=1)
        cmds.makeIdentity(MainLowerLid, apply=True, r=1)

        return MainEye


ER = EyeRig()
LEye = ER.EyeLidsSetUp("Character_LF_EyeGeo00_msh_intRig")
REye = ER.EyeLidsSetUp("Character_RH_EyeGeo00_msh_intRig")
