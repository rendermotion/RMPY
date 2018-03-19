import maya.cmds as cmds
import maya.mel as mel
import RMRigTools
import RMNameConvention
import RMRigShapeControls


# mel.eval('source "RMAttributes.mel"; \nDeleteAttributes("BookMainControl");')

class RMBookPage(object):
    def __init__(self, NameConv=None):
        if not NameConv:
            self.NameConv = RMNameConvention.RMNameConvention()
        else:
            self.NameConv = NameConv
        self.kinematics = []
        self.origin = 'origin'
        self.height = 'height'
        self.width = 'width'
        self.deepth = 'deepth'
        self.flare2 = None
        self.flareHandle2 = None
        self.flare = None
        self.flareHandle = None
        self.centerBendLocator = None

        self.bendSpread = None
        self.bendHandleSpread = None

        self.bendMidle = None
        self.bendHandleMiddle = None

        self.bendOpen = None
        self.bendHandleOpen = None
        self.widthValue = 0
        self.heightValue = 0

    def CreateBookRefPoints(self):
        self.origin = cmds.spaceLocator(name=self.origin)
        self.height = cmds.spaceLocator(name=self.height)
        self.width = cmds.spaceLocator(name=self.width)
        self.deepth = cmds.spaceLocator(name=self.deepth)
        cmds.xform(self.height, objectSpace=True, t=[0, 5, 0])
        cmds.xform(self.width, objectSpace=True, t=[5, 0, 0])
        cmds.xform(self.deepth, objectSpace=True, t=[0, 0, 10])
        cmds.parent(self.height, self.origin)
        cmds.parent(self.width, self.origin)
        cmds.parent(self.deepth, self.origin)

    def CreateBookRig(self, AffectedObject):

        affected = AffectedObject
        self.widthValue = RMRigTools.RMPointDistance(self.width, self.origin)
        self.heightValue = RMRigTools.RMPointDistance(self.height, self.origin)

        parentGroup = cmds.group(empty=True, name="BookRig")
        self.NameConv.default_names["System"] = parentGroup
        RMRigTools.RMAlign(self.origin, parentGroup, 3)

        cmds.select(affected)
        self.flare2, self.flareHandle2 = cmds.nonLinear(type='flare', lowBound=0, highBound=self.widthValue,
                                                        name="FlareLeafsThick")
        self.flare2 = self.NameConv.rename_name_in_format(self.flare2)
        self.flareHandle2 = self.NameConv.rename_name_in_format(self.flareHandle2)

        RMRigTools.RMAlign(self.origin, self.flareHandle2, 3)
        cmds.xform(self.flareHandle2, objectSpace=True, rotation=[180, 0, 90])
        cmds.setAttr(self.flareHandle2 + ".scale", 1, 1, 1)

        cmds.select(affected)
        self.flare, self.flareHandle = cmds.nonLinear(type='flare', lowBound=0, highBound=self.heightValue,
                                                      name="FlareBorderRefinement")  # endFlareX
        self.flare = self.NameConv.rename_name_in_format(self.flare)
        self.flareHandle = self.NameConv.rename_name_in_format(self.flareHandle)
        RMRigTools.RMAlign(self.origin, self.flareHandle, 3)
        cmds.setAttr(self.flareHandle + ".scale", 1, 1, 1)
        cmds.xform(self.flareHandle, objectSpace=True, translation=[self.widthValue / 2, 0, 0])

        cmds.select(affected)
        self.bendSpread, self.bendHandleSpread = cmds.nonLinear(type='bend', lowBound=-self.widthValue,
                                                                highBound=self.widthValue, curvature=0,
                                                                name="bendSpread")  # curvature
        self.bendSpread = self.NameConv.rename_name_in_format(self.bendSpread)
        self.bendHandleSpread = self.NameConv.rename_name_in_format(self.bendHandleSpread)
        RMRigTools.RMAlign(self.origin, self.bendHandleSpread, 3)
        cmds.xform(self.bendHandleSpread, objectSpace=True, rotation=[0, 0, 90])
        cmds.setAttr(self.bendHandleSpread + ".scale", 1, 1, 1)

        cmds.select(affected)
        # self.bendMidle, self.bendHandleMiddle = cmds.nonLinear(type = 'bend', lowBound = 0 , highBound = self.heightValue / 2 , curvature = 0,name = "bendCenter")#curvature Hight Bound
        self.bendMidle, self.bendHandleMiddle = cmds.nonLinear(type='bend', lowBound=0, highBound=1, curvature=0,
                                                               name="bendCenter")  # curvature Hight Bound
        self.bendMidle = self.NameConv.rename_name_in_format(self.bendMidle)
        self.bendHandleMiddle = self.NameConv.rename_name_in_format(self.bendHandleMiddle)
        RMRigTools.RMAlign(self.origin, self.bendHandleMiddle, 3)
        cmds.setAttr(self.bendHandleMiddle + ".scale", 1, 1, 1)
        cmds.xform(self.bendHandleMiddle, objectSpace=True, translation=[0, self.heightValue / 2, 0])

        cmds.select(affected)
        # self.bendOpen, self.bendHandleOpen = cmds.nonLinear(type = 'bend', lowBound = 0 , highBound = self.heightValue / 2 , curvature = 0,name = "bendOpen")#curvature Hight Bound
        self.bendOpen, self.bendHandleOpen = cmds.nonLinear(type='bend', lowBound=0, highBound=1, curvature=0,
                                                            name="bendOpen")  # curvature Hight Bound
        self.bendOpen = self.NameConv.rename_name_in_format(self.bendOpen)
        self.bendHandleOpen = self.NameConv.rename_name_in_format(self.bendHandleOpen)
        RMRigTools.RMAlign(self.origin, self.bendHandleOpen, 3)
        cmds.setAttr(self.bendHandleOpen + ".scale", 1, 1, 1)

        cmds.select(affected)
        # self.bendOpen, self.bendHandleOpen = cmds.nonLinear(type = 'bend', lowBound = 0 , highBound = self.heightValue / 2 , curvature = 0,name = "bendOpen")#curvature Hight Bound
        # self.bendOpenOposit, self.bendHandleOpenOposit = cmds.nonLinear(type = 'bend', lowBound = 0 , highBound = 1 , curvature = 0,name = "bendOpenOposit")#curvature Hight Bound
        # self.bendOpenOposit = self.NameConv.RMRenameNameInFormat(self.bendOpenOposit)
        # self.bendHandleOpenOposit = self.NameConv.RMRenameNameInFormat(self.bendHandleOpenOposit)

        # RMRigTools.RMAlign(self.origin, self.bendHandleOpenOposit,3)
        # cmds.setAttr(self.bendHandleOpenOposit + ".scale", 1 , 1 , 1)

        self.centerBendLocator = cmds.spaceLocator(name="centerBend")[0]
        self.centerBendLocator = self.NameConv.rename_name_in_format(self.centerBendLocator)

        RMRigTools.RMAlign(self.bendHandleMiddle, self.centerBendLocator, 3)
        cmds.parent(self.bendHandleMiddle, self.centerBendLocator)

        cmds.parent(self.centerBendLocator, parentGroup)

        # cmds.xform( self.bendHandleOpen , objectSpace = True, translation = [self.widthValue,0,0])
        # cmds.xform( self.bendHandleOpenOposit , objectSpace = True, translation = [-self.widthValue,0,0])
        cmds.connectAttr(self.bendHandleOpen + ".scaleX", self.centerBendLocator + ".translateY")
        # cmds.connectAttr(self.bendHandleOpen+".scale",self.bendHandleOpenOposit+".scale")


        cmds.parent(self.bendHandleOpen, parentGroup)
        # cmds.parent( self.bendHandleOpenOposit, parentGroup )
        cmds.parent(self.flareHandle, parentGroup)
        cmds.parent(self.bendHandleSpread, parentGroup)
        cmds.parent(self.flareHandle2, parentGroup)

        ControlResetPoint, Control = RMRigShapeControls.RMCircularControl(self.origin, NameConv=self.NameConv)
        self.AddAttributes(Control)
        self.LinkAttributes(Control)

    def AddAttributes(self, ControlBook):
        cmds.addAttr(ControlBook, longName="BookSpread", keyable=1, hasMinValue=1, hasMaxValue=1, minValue=0,
                     maxValue=10)
        cmds.addAttr(ControlBook, longName="BookLeaf", keyable=1, hasMinValue=1, hasMaxValue=1, minValue=-10,
                     maxValue=10)
        cmds.addAttr(ControlBook, longName="BorderRefinementIn", keyable=1, hasMinValue=1, hasMaxValue=1, minValue=-10,
                     maxValue=10)
        cmds.addAttr(ControlBook, longName="BorderRefinementOut", keyable=1, hasMinValue=1, hasMaxValue=1, minValue=-10,
                     maxValue=10)
        cmds.addAttr(ControlBook, longName="OpenBend", keyable=1, hasMinValue=1, hasMaxValue=1, minValue=-10,
                     maxValue=10)
        cmds.addAttr(ControlBook, longName="OpenLength", keyable=1, hasMinValue=1, hasMaxValue=1, minValue=-10,
                     maxValue=10)
        cmds.addAttr(ControlBook, longName="OpenBendCounter", keyable=1, hasMinValue=1, hasMaxValue=1, minValue=-10,
                     maxValue=10)
        cmds.addAttr(ControlBook, longName="OpenBendCounterOffset", keyable=1, hasMinValue=1, hasMaxValue=1,
                     minValue=-10, maxValue=10)
        cmds.addAttr(ControlBook, longName="OpenBendCounterLenght", keyable=1, hasMinValue=1, hasMaxValue=1,
                     minValue=-10, maxValue=10)

    def LinkAttributes(self, ControlBook):

        RMRigTools.RMConnectWithLimits(ControlBook + ".BookSpread", self.bendSpread + ".curvature", [[0, 0], [10, -60]])
        RMRigTools.RMConnectWithLimits(ControlBook + ".BookLeaf", self.flare + ".endFlareX",
                                       [[-10, -1], [0, 1], [10, 2]])
        RMRigTools.RMConnectWithLimits(ControlBook + ".BorderRefinementOut", self.flare2 + ".startFlareX",
                                       [[-10, -1], [0, 1], [10, 2]])
        RMRigTools.RMConnectWithLimits(ControlBook + ".BorderRefinementIn", self.flare2 + ".endFlareX",
                                       [[-10, -1], [0, 1], [10, 2]])
        RMRigTools.RMConnectWithLimits(ControlBook + ".OpenBend", self.bendOpen + ".curvature",
                                       [[-10, -180], [0, 0], [10, 180]])
        # RMRigTools.RMConnectWithLimits( ControlBook + ".OpenBend",            self.bendOpenOposit   + ".curvature",[[-10,-180],[0,0]] )
        RMRigTools.RMConnectWithLimits(ControlBook + ".OpenLength", self.bendHandleOpen + ".scale",
                                       [[-10, 0], [0, self.heightValue / 2], [10, self.heightValue]])
        RMRigTools.RMConnectWithLimits(ControlBook + ".OpenBendCounter", self.bendMidle + ".curvature",
                                       [[-10, -180], [0, 0], [10, 180]])
        RMRigTools.RMConnectWithLimits(ControlBook + ".OpenBendCounterOffset", self.bendHandleMiddle + ".translateY",
                                       [[-10, -self.heightValue / 2], [0, 0], [10, self.heightValue / 2]])
        RMRigTools.RMConnectWithLimits(ControlBook + ".OpenBendCounterLenght", self.bendHandleMiddle + ".scale",
                                       [[-10, 0], [0, self.heightValue / 2], [10, self.heightValue]])


BookRig = RMBookPage()

# BookRig.CreateBookRefPoints()
selection = cmds.ls(selection=True, type="transform")
BookRig.CreateBookRig(selection)
