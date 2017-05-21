import maya.cmds as cmds
from RMPY import RMRigTools

reload(RMRigTools)
from RMPY import RMNameConvention

reload(RMNameConvention)
from RMPY import RMRigShapeControls


class RMFeetRig(object):
    def __init__(self, NameConv=None):
        if not NameConv:
            self.NameConv = RMNameConvention.RMNameConvention()
        else:
            self.NameConv = NameConv

        self.StandardFeetPointsDic = None

        self.rootFKJoints = None
        self.rootIKJoints = None

        self.StandardFeetIKJoints = None
        self.StandardFeetFKJoints = None
        self.MainFeetKinematics = None

        self.FeetControl = None
        self.FirstLimbFeetResetControl = None
        self.SecondLimbFeetControl = None
        self.SecondLimbControlResetPoint = None
        # self.StandardFeetDefJoints = None
        # self.rootStandardFeetDefJoints = None
        self.IKAttachPoint = None
        self.rootJoints = None
        self.StandardFeetJoints = None

        self.feetMainMoveIK = None

        self.rootFKJoints

    def RigFeetIKFK(self, StandarFeetPointsDic, IKcontrol=None, FKControl=None):
        self.StandardFeetIKRig(StandarFeetPointsDic, FeetControl=IKcontrol)
        self.StardardFeetFK(StandarFeetPointsDic, FeetControl=FKControl)
        self.rootJoints, FeetJoints = self.StandardReverseFeetJointStructure(StandarFeetPointsDic)
        # StandardFeetFKJoints = self.NameConv.RMRenameSetFromName(StandardFeetIKJoints, "Blend" , "Name" , mode = "add")
        FeetJoints = self.NameConv.RMRenameSetFromName(FeetJoints, "sknjnt", "objectType")
        FeetJoints[2] = self.NameConv.RMRenameSetFromName(FeetJoints[2], "jnt", "objectType")
        self.StandardFeetJoints = FeetJoints

    def StardardFeetFK(self, StandarFeetPointsDic, FeetControl=None):
        Side = self.NameConv.RMGetFromName(self.StandardFeetPointsDic["feet"][0], "Side")
        self.rootFKJoints, StandardFeetFKJoints = self.StandardReverseFeetJointStructure(StandarFeetPointsDic)

        StandardFeetFKJoints = self.NameConv.RMRenameSetFromName(StandardFeetFKJoints, "FK", "name", mode="add")

        FootIn = self.StandardFeetPointsDic["limitIn"]
        FootOut = self.StandardFeetPointsDic["limitOut"]
        FootBK = self.StandardFeetPointsDic["limitBack"]
        Length = RMRigTools.RMPointDistance(self.StandardFeetPointsDic["feet"][2], FootBK)

        if not FeetControl:
            self.FirstLimbFeetResetControl, FeetControl = RMRigShapeControls.RMCircularControl(StandardFeetFKJoints[0],
                                                                                               radius=Length,
                                                                                               name="FKFeetControl")

        self.FeetControl = FeetControl

        SecondLimbfeetResetControl, SecondLimbFeetControl = RMRigShapeControls.RMCircularControl(
            StandardFeetFKJoints[1], radius=Length, name="FKTipFeetControl")

        cmds.parentConstraint(FeetControl, StandardFeetFKJoints[0], mo=True)
        cmds.parentConstraint(SecondLimbFeetControl, StandardFeetFKJoints[1], mo=True)
        cmds.parentConstraint(StandardFeetFKJoints[0], SecondLimbfeetResetControl, mo=True)

        cmds.parent(SecondLimbfeetResetControl, FeetControl)
        RMRigTools.RMLockAndHideAttributes(FeetControl, "000111000h")
        RMRigTools.RMLockAndHideAttributes(SecondLimbFeetControl, "000111000h")

        self.StandardFeetFKJoints = StandardFeetFKJoints
        self.SecondLimbFeetControl = SecondLimbFeetControl
        self.SecondLimbControlResetPoint = SecondLimbfeetResetControl

    def StandardFeetIKRig(self, StandarFeetPointsDic, FeetControl=None):
        self.StandardFeetPointsDic = StandarFeetPointsDic

        Side = self.NameConv.RMGetFromName(self.StandardFeetPointsDic["feet"][0], "Side")
        self.rootIKJoints, StandardFeetIKJoints = self.StandardReverseFeetJointStructure(StandarFeetPointsDic)
        StandardFeetIKJoints = self.NameConv.RMRenameSetFromName(StandardFeetIKJoints, "IK", "name", mode="add")

        FootIn = self.StandardFeetPointsDic["limitIn"]
        FootOut = self.StandardFeetPointsDic["limitOut"]
        FootBK = self.StandardFeetPointsDic["limitBack"]

        Length = RMRigTools.RMPointDistance(self.StandardFeetPointsDic["feet"][2], FootBK)
        Width = RMRigTools.RMPointDistance(FootIn, FootOut)

        BallGrp = cmds.group(empty=True, name=self.NameConv.RMSetNameInFormat({'name': "Ball", 'side': Side}))
        BallLift = cmds.group(empty=True, name=self.NameConv.RMSetNameInFormat({'name': "BallLift", 'side': Side}))
        TapGrp = cmds.group(empty=True, name=self.NameConv.RMSetNameInFormat({'name': "TapGrp", 'side': Side}))
        TipGrp = cmds.group(empty=True, name=self.NameConv.RMSetNameInFormat({'name': "TipGrp", 'side': Side}))
        SideInGrp = cmds.group(empty=True, name=self.NameConv.RMSetNameInFormat({'name': "SideInGrp", 'side': Side}))
        SideOutGrp = cmds.group(empty=True, name=self.NameConv.RMSetNameInFormat({'name': "SideOutGrp", 'side': Side}))
        FeetOrient = cmds.group(empty=True, name=self.NameConv.RMSetNameInFormat({'name': "FeetOrient", 'side': Side}))
        FeetPalmOrient = cmds.group(empty=True, name=self.NameConv.RMSetNameInFormat({'name': "FeetPalmOrient", 'side': Side}))

        RMRigTools.RMAlign(StandardFeetIKJoints[1], BallGrp, 3)
        RMRigTools.RMAlign(StandardFeetIKJoints[1], BallLift, 3)

        RMRigTools.RMAlign(StandardFeetIKJoints[1], TipGrp, 3)
        RMRigTools.RMAlign(StandardFeetIKJoints[2], TipGrp, 1)
        RMRigTools.RMAlign(StandardFeetIKJoints[1], TapGrp, 3)

        RMRigTools.RMAlign(FootIn, SideInGrp, 3)
        RMRigTools.RMAlign(FootOut, SideOutGrp, 3)
        RMRigTools.RMAlign(FootBK, TapGrp, 3)
        RMRigTools.RMAlign(BallGrp, FeetPalmOrient, 3)
        RMRigTools.RMAlign(StandardFeetIKJoints[0], FeetOrient, 3)

        cmds.xform(FeetOrient, objectSpace=True, relative=True, t=[0, 0, Width])
        cmds.xform(FeetPalmOrient, objectSpace=True, relative=True, t=[0, 0, Width])

        BallIK, BallIkEffector = cmds.ikHandle(sj=StandardFeetIKJoints[0], ee=StandardFeetIKJoints[1],
                                               name="BallIK")  # solver="ikRPsolver",
        TipIK, TipIkEffector = cmds.ikHandle(sj=StandardFeetIKJoints[1], ee=StandardFeetIKJoints[2],
                                             name="TipIK")  # solver="ikRPsolver",

        BallIK = self.NameConv.RMRenameNameInFormat(BallIK, {'side':Side})
        TipIK = self.NameConv.RMRenameNameInFormat(TipIK, {'side':Side})
        BallIkEffector = self.NameConv.RMRenameNameInFormat(BallIkEffector, {'side':Side})
        TipIkEffector = self.NameConv.RMRenameNameInFormat(TipIkEffector, {'side':Side})

        # cmds.poleVectorConstraint (FeetOrient, BallIK)
        # cmds.poleVectorConstraint (FeetPalmOrient, TipIK)

        cmds.parent(BallIK, BallLift)
        cmds.parent(TipIK, BallLift)
        cmds.parent(BallLift, SideInGrp)
        cmds.parent(BallGrp, SideInGrp)
        cmds.parent(SideInGrp, SideOutGrp)
        cmds.parent(SideOutGrp, TapGrp)
        cmds.parent(TapGrp, TipGrp)
        cmds.parent(FeetOrient, BallGrp)
        cmds.parent(FeetPalmOrient, BallLift)

        TipData = RMRigTools.RMCreateGroupOnObj(TipGrp)
        MainFeet = RMRigTools.RMCreateGroupOnObj(TipData)

        MainFeet = self.NameConv.RMRenameSetFromName(MainFeet, "MainFeet", "name")

        if not FeetControl:
            fetControlReset, FeetControl = RMRigShapeControls.RMCreateBoxCtrl(StandarFeetPointsDic["feet"][0],
                                                                              customSize=Length, Yratio=.6, Zratio=.3,
                                                                              name="FeetControl")
            self.fetControlReset = fetControlReset

        # self.feetMainMoveIK = TipData
        cmds.parentConstraint(FeetControl, TipData, mo=True)

        self.RMStandardRigAttributes(FeetControl)

        cmds.makeIdentity(BallGrp, apply=True, t=1, r=1, s=1, n=0)
        cmds.makeIdentity(BallLift, apply=True, t=1, r=1, s=1, n=0)
        cmds.makeIdentity(TapGrp, apply=True, t=1, r=1, s=1, n=0)
        cmds.makeIdentity(TipGrp, apply=True, t=1, r=1, s=1, n=0)
        cmds.makeIdentity(SideInGrp, apply=True, t=1, r=1, s=1, n=0)
        cmds.makeIdentity(SideOutGrp, apply=True, t=1, r=1, s=1, n=0)
        cmds.makeIdentity(FeetOrient, apply=True, t=1, r=1, s=1, n=0)
        cmds.makeIdentity(FeetPalmOrient, apply=True, t=1, r=1, s=1, n=0)

        # cmds.parent (self.rootIKJoints, BallGrp)

        RMRigTools.RMConnectWithLimits(FeetControl + ".ToeLift", BallLift + ".rotateZ", [[-10, -70], [0, 0], [10, 70]])
        RMRigTools.RMConnectWithLimits(FeetControl + ".BallPivot", BallGrp + ".rotateZ", [[-10, 70], [0, 0], [10, -70]])
        RMRigTools.RMConnectWithLimits(FeetControl + ".HeelPivot", TapGrp + ".rotateZ", [[-10, -70], [0, 0], [10, 70]])
        RMRigTools.RMConnectWithLimits(FeetControl + ".ToePivot", TipGrp + ".rotateZ", [[-10, 70], [0, 0], [10, -70]])
        if (Side == "LF"):
            RMRigTools.RMConnectWithLimits(FeetControl + ".Tilt", SideInGrp + ".rotateX", [[-10, 70], [0, 0]])
            RMRigTools.RMConnectWithLimits(FeetControl + ".Tilt", SideOutGrp + ".rotateX", [[0, 0], [10, -70]])
            RMRigTools.RMConnectWithLimits(FeetControl + ".ToePivotSide", TipGrp + ".rotateY",
                                           [[-10, 70], [0, 0], [10, -70]])
        # RMRigTools.RMConnectWithLimits( FeetControl + ".ToePivot" , TipGrp + ".rotateZ", [[-10,-70],[0,0],[10,70]])
        else:
            RMRigTools.RMConnectWithLimits(FeetControl + ".Tilt", SideInGrp + ".rotateX", [[-10, -70], [0, 0]])
            RMRigTools.RMConnectWithLimits(FeetControl + ".Tilt", SideOutGrp + ".rotateX", [[0, 0], [10, 70]])
            RMRigTools.RMConnectWithLimits(FeetControl + ".ToePivotSide", TipGrp + ".rotateY",
                                           [[-10, -70], [0, 0], [10, 70]])
        # RMRigTools.RMCreateGroupOnObj( FeetControl)
        cmds.scaleConstraint(FeetControl, MainFeet)

        self.MainFeetKinematics = MainFeet
        self.IKAttachPoint = BallGrp
        self.StandardFeetIKJoints = StandardFeetIKJoints

    def StandardReverseFeetJointStructure(self, StandarFeetPointsDic):
        feetResetJoints, feetJoints = RMRigTools.RMCreateBonesAtPoints(StandarFeetPointsDic["feet"],
                                                                       ZAxisOrientation="Z")

        return feetResetJoints, feetJoints

    def RMStandardRigAttributes(self, Object):
        cmds.addAttr(Object, at="float", ln="Twist", hnv=1, hxv=1, h=0, k=1, smn=-10, smx=10)
        cmds.addAttr(Object, at="float", ln="ToePivot", hnv=1, hxv=1, h=0, k=1, smn=-10, smx=10)
        cmds.addAttr(Object, at="float", ln="ToePivotSide", hnv=1, hxv=1, h=0, k=1, smn=-10, smx=10)
        cmds.addAttr(Object, at="float", ln="ToeLift", hnv=1, hxv=1, h=0, k=1, smn=-10, smx=10)
        cmds.addAttr(Object, at="float", ln="BallPivot", hnv=1, hxv=1, h=0, k=1, smn=-10, smx=10)
        cmds.addAttr(Object, at="float", ln="HeelPivot", hnv=1, hxv=1, h=0, k=1, smn=-10, smx=10)
        cmds.addAttr(Object, at="float", ln="Tilt", hnv=1, hxv=1, h=0, k=1, smn=-10, smx=10)
        # cmds.addAttr(Object,at="enum" , ln = "Secondary", k = 1, en = "world:COG")
