import pymel.core as pm
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
        self.rig_tools = RMRigTools.RMRigTools()
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
        self.NameConv.RMRenameSetFromName(FeetJoints, "sknjnt", "objectType")
        self.NameConv.RMRenameSetFromName(FeetJoints[2], "jnt", "objectType")
        self.StandardFeetJoints = FeetJoints

    def StardardFeetFK(self, StandarFeetPointsDic, FeetControl=None):
        Side = self.NameConv.RMGetFromName(self.StandardFeetPointsDic["feet"][0], "side")
        self.rootFKJoints, StandardFeetFKJoints = self.StandardReverseFeetJointStructure(StandarFeetPointsDic)

        self.NameConv.RMRenameSetFromName(StandardFeetFKJoints, "FK", "name", mode="add")

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

        pm.parentConstraint(FeetControl, StandardFeetFKJoints[0], mo=True)
        pm.parentConstraint(SecondLimbFeetControl, StandardFeetFKJoints[1], mo=True)
        pm.parentConstraint(StandardFeetFKJoints[0], SecondLimbfeetResetControl, mo=True)

        pm.parent(SecondLimbfeetResetControl, FeetControl)
        RMRigTools.RMLockAndHideAttributes(FeetControl, "000111000h")
        RMRigTools.RMLockAndHideAttributes(SecondLimbFeetControl, "000111000h")

        self.StandardFeetFKJoints = StandardFeetFKJoints
        self.SecondLimbFeetControl = SecondLimbFeetControl
        self.SecondLimbControlResetPoint = SecondLimbfeetResetControl

    def StandardFeetIKRig(self, StandarFeetPointsDic, FeetControl=None):
        self.StandardFeetPointsDic = StandarFeetPointsDic

        Side = self.NameConv.RMGetFromName(self.StandardFeetPointsDic["feet"][0], "side")
        self.rootIKJoints, StandardFeetIKJoints = self.StandardReverseFeetJointStructure(StandarFeetPointsDic)
        self.NameConv.RMRenameSetFromName(StandardFeetIKJoints, "IK", "name", mode="add")

        FootIn = self.StandardFeetPointsDic["limitIn"]
        FootOut = self.StandardFeetPointsDic["limitOut"]
        FootBK = self.StandardFeetPointsDic["limitBack"]

        Length = RMRigTools.RMPointDistance(self.StandardFeetPointsDic["feet"][2], FootBK)
        Width = RMRigTools.RMPointDistance(FootIn, FootOut)

        BallGrp = pm.group(empty=True, name=self.NameConv.RMSetNameInFormat({'name': "Ball", 'side': Side}))
        BallLift = pm.group(empty=True, name=self.NameConv.RMSetNameInFormat({'name': "BallLift", 'side': Side}))
        TapGrp = pm.group(empty=True, name=self.NameConv.RMSetNameInFormat({'name': "TapGrp", 'side': Side}))
        TipGrp = pm.group(empty=True, name=self.NameConv.RMSetNameInFormat({'name': "TipGrp", 'side': Side}))
        SideInGrp = pm.group(empty=True, name=self.NameConv.RMSetNameInFormat({'name': "SideInGrp", 'side': Side}))
        SideOutGrp = pm.group(empty=True, name=self.NameConv.RMSetNameInFormat({'name': "SideOutGrp", 'side': Side}))
        FeetOrient = pm.group(empty=True, name=self.NameConv.RMSetNameInFormat({'name': "FeetOrient", 'side': Side}))
        FeetPalmOrient = pm.group(empty=True, name=self.NameConv.RMSetNameInFormat({'name': "FeetPalmOrient", 'side': Side}))

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

        pm.xform(FeetOrient, objectSpace=True, relative=True, t=[0, 0, Width])
        pm.xform(FeetPalmOrient, objectSpace=True, relative=True, t=[0, 0, Width])

        BallIK, BallIkEffector = pm.ikHandle(sj=StandardFeetIKJoints[0], ee=StandardFeetIKJoints[1],
                                               name="BallIK")  # solver="ikRPsolver",
        TipIK, TipIkEffector = pm.ikHandle(sj=StandardFeetIKJoints[1], ee=StandardFeetIKJoints[2],
                                             name="TipIK")  # solver="ikRPsolver",

        self.NameConv.RMRenameNameInFormat(BallIK, {'side':Side})
        self.NameConv.RMRenameNameInFormat(TipIK, {'side':Side})
        self.NameConv.RMRenameNameInFormat(BallIkEffector, {'side':Side})
        self.NameConv.RMRenameNameInFormat(TipIkEffector, {'side':Side})

        # pm.poleVectorConstraint (FeetOrient, BallIK)
        # pm.poleVectorConstraint (FeetPalmOrient, TipIK)

        pm.parent(BallIK, BallLift)
        pm.parent(TipIK, BallLift)
        pm.parent(BallLift, SideInGrp)
        pm.parent(BallGrp, SideInGrp)
        pm.parent(SideInGrp, SideOutGrp)
        pm.parent(SideOutGrp, TapGrp)
        pm.parent(TapGrp, TipGrp)
        pm.parent(FeetOrient, BallGrp)
        pm.parent(FeetPalmOrient, BallLift)

        TipData = self.rig_tools.RMCreateGroupOnObj(TipGrp)
        MainFeet = self.rig_tools.RMCreateGroupOnObj(TipData)

        self.NameConv.RMRenameSetFromName(MainFeet, "MainFeet", "name")

        if not FeetControl:
            fetControlReset, FeetControl = RMRigShapeControls.RMCreateBoxCtrl(StandarFeetPointsDic["feet"][0],
                                                                              customSize=Length, Yratio=.6, Zratio=.3,
                                                                              name="FeetControl")
            self.fetControlReset = fetControlReset

        # self.feetMainMoveIK = TipData
        pm.parentConstraint(FeetControl, TipData, mo=True)

        self.RMStandardRigAttributes(FeetControl)

        pm.makeIdentity(BallGrp, apply=True, t=1, r=1, s=1, n=0)
        pm.makeIdentity(BallLift, apply=True, t=1, r=1, s=1, n=0)
        pm.makeIdentity(TapGrp, apply=True, t=1, r=1, s=1, n=0)
        pm.makeIdentity(TipGrp, apply=True, t=1, r=1, s=1, n=0)
        pm.makeIdentity(SideInGrp, apply=True, t=1, r=1, s=1, n=0)
        pm.makeIdentity(SideOutGrp, apply=True, t=1, r=1, s=1, n=0)
        pm.makeIdentity(FeetOrient, apply=True, t=1, r=1, s=1, n=0)
        pm.makeIdentity(FeetPalmOrient, apply=True, t=1, r=1, s=1, n=0)

        # pm.parent (self.rootIKJoints, BallGrp)

        RMRigTools.RMConnectWithLimits("%s.ToeLift" % FeetControl, "%s.rotateZ" % BallLift, [[-10, -70], [0, 0], [10, 70]])
        RMRigTools.RMConnectWithLimits("%s.BallPivot" % FeetControl, "%s.rotateZ" % BallGrp, [[-10, 70], [0, 0], [10, -70]])
        RMRigTools.RMConnectWithLimits("%s.HeelPivot" % FeetControl, "%s.rotateZ" % TapGrp, [[-10, -70], [0, 0], [10, 70]])
        RMRigTools.RMConnectWithLimits("%s.ToePivot" % FeetControl, "%s.rotateZ" % TipGrp, [[-10, 70], [0, 0], [10, -70]])
        if (Side == "L"):
            RMRigTools.RMConnectWithLimits("%s.Tilt" % FeetControl, "%s.rotateX" % SideInGrp, [[-10, 70], [0, 0]])
            RMRigTools.RMConnectWithLimits("%s.Tilt" % FeetControl, "%s.rotateX" % SideOutGrp, [[0, 0], [10, -70]])
            RMRigTools.RMConnectWithLimits("%s.ToePivotSide" % FeetControl, "%s.rotateY" % TipGrp,
                                           [[-10, 70], [0, 0], [10, -70]])
        # RMRigTools.RMConnectWithLimits( "%s.ToePivot" , TipGrp + ".rotateZ", [[-10,-70],[0,0],[10,70]])
        else:
            RMRigTools.RMConnectWithLimits("%s.Tilt" % FeetControl, "%s.rotateX" % SideInGrp, [[-10, -70], [0, 0]])
            RMRigTools.RMConnectWithLimits("%s.Tilt" % FeetControl, "%s.rotateX" % SideOutGrp, [[0, 0], [10, 70]])
            RMRigTools.RMConnectWithLimits("%s.ToePivotSide" % FeetControl, "%s.rotateY" % TipGrp,
                                           [[-10, -70], [0, 0], [10, 70]])
        # RMRigTools.RMCreateGroupOnObj( FeetControl)

        pm.scaleConstraint(FeetControl, MainFeet)

        self.MainFeetKinematics = MainFeet
        self.IKAttachPoint = BallGrp
        self.StandardFeetIKJoints = StandardFeetIKJoints

    def StandardReverseFeetJointStructure(self, StandarFeetPointsDic):
        feetResetJoints, feetJoints = self.rig_tools.RMCreateBonesAtPoints(StandarFeetPointsDic["feet"],
                                                                       ZAxisOrientation="Z")

        return feetResetJoints, feetJoints

    def RMStandardRigAttributes(self, Object):
        pm.addAttr(Object, at="float", ln="Twist", hnv=1, hxv=1, h=0, k=1, smn=-10, smx=10)
        pm.addAttr(Object, at="float", ln="ToePivot", hnv=1, hxv=1, h=0, k=1, smn=-10, smx=10)
        pm.addAttr(Object, at="float", ln="ToePivotSide", hnv=1, hxv=1, h=0, k=1, smn=-10, smx=10)
        pm.addAttr(Object, at="float", ln="ToeLift", hnv=1, hxv=1, h=0, k=1, smn=-10, smx=10)
        pm.addAttr(Object, at="float", ln="BallPivot", hnv=1, hxv=1, h=0, k=1, smn=-10, smx=10)
        pm.addAttr(Object, at="float", ln="HeelPivot", hnv=1, hxv=1, h=0, k=1, smn=-10, smx=10)
        pm.addAttr(Object, at="float", ln="Tilt", hnv=1, hxv=1, h=0, k=1, smn=-10, smx=10)
        # pm.addAttr(Object,at="enum" , ln = "Secondary", k = 1, en = "world:COG")
