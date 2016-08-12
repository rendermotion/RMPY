import maya.cmds as cmds
import maya.mel as mel
import RMRigTools
import RMNameConvention
import RMRigShapeControls

#mel.eval('source "RMAttributes.mel"; \nDeleteAttributes("BookMainControl");')

class RMBookPage(object):
    def __init__(self,NameConv = None):
        if not NameConv:
            self.NameConv = RMNameConvention.RMNameConvention()
        else:
            self.NameConv = NameConv
        self.kinematics = []
        self.origin   = 'origin'
        self.height   = 'height'
        self.width    = 'width'
        self.deepth   = 'deepth'
        self.flare2 = None
        self.flareHandle2 = None
        self.flare = None
        self.flareHandle = None
        self.centerBendLocator = None

    def CreateBookRefPoints(self):
        self.origin = cmds.spaceLocator(name = self.origin)
        self.height = cmds.spaceLocator(name = self.height)
        self.width = cmds.spaceLocator(name = self.width)
        self.deepth = cmds.spaceLocator(name = self.deepth)
        cmds.xform(self.height,objectSpace=True,t=[0,5,0])
        cmds.xform(self.width,objectSpace=True,t=[5,0,0])
        cmds.xform(self.deepth,objectSpace=True,t=[0,0,10])
        cmds.parent(self.height,self.origin)
        cmds.parent(self.width,self.origin)
        cmds.parent(self.deepth,self.origin)

    def CreateBookRig(self):

        affected ='pCube1'
        widthValue = RMRigTools.RMPointDistance( self.width, self.origin )
        heightValue = RMRigTools.RMPointDistance( self.height, self.origin )

        parentGroup = cmds.group( empty = True, name = "BookRig")
        RMRigTools.RMAlign(self.origin, parentGroup,3)


        cmds.select ( affected )
        self.flare2, self.flareHandle2= cmds.nonLinear(type = 'flare', lowBound = 0, highBound = widthValue, name = "FlareLeafsThick")
        RMRigTools.RMAlign(self.origin, self.flareHandle2 , 3)
        cmds.xform( self.flareHandle2 , objectSpace = True, rotation = [180,0,90])
        cmds.setAttr( self.flareHandle2 + ".scale", 1 , 1 , 1)

        cmds.select ( affected )
        self.flare, self.flareHandle = cmds.nonLinear(type = 'flare', lowBound = 0, highBound = heightValue, name = "FlareBorderRefinement")#endFlareX
        RMRigTools.RMAlign(self.origin, self.flareHandle,3)
        cmds.setAttr(self.flareHandle + ".scale", 1 , 1 , 1)

        cmds.select ( affected )
        self.bendSpread, self.bendHandleSpread= cmds.nonLinear(type = 'bend', lowBound = -widthValue , highBound =widthValue, curvature = 0, name = "bendSpread")#curvature
        RMRigTools.RMAlign(self.origin, self.bendHandleSpread,3)
        cmds.xform( self.bendHandleSpread , objectSpace = True, rotation = [0,0,90])
        cmds.setAttr(self.bendHandleSpread + ".scale", 1 , 1 , 1)

        cmds.select ( affected )
        self.bendMidle, self.bendHandleMiddle= cmds.nonLinear(type = 'bend', lowBound = 0 , highBound = heightValue / 2 , curvature = 0,name = "bendCenter")#curvature Hight Bound 
        RMRigTools.RMAlign(self.origin, self.bendHandleMiddle,3)
        cmds.setAttr(self.bendHandleMiddle + ".scale", 1 , 1 , 1)
        cmds.xform( self.bendHandleMiddle , objectSpace = True, translation = [0,heightValue / 2,0])

        cmds.select ( affected )
        self.bendOpen, self.bendHandleOpen = cmds.nonLinear(type = 'bend', lowBound = 0 , highBound = heightValue / 2 , curvature = 0,name = "bendOpen")#curvature Hight Bound 
        RMRigTools.RMAlign(self.origin, self.bendHandleOpen,3)
        cmds.setAttr(self.bendHandleOpen + ".scale", 1 , 1 , 1)

        self.centerBendLocator = cmds.spaceLocator(name = "centerBend")[0]
        RMRigTools.RMAlign(self.bendHandleMiddle,self.centerBendLocator,3)
        cmds.parent(self.bendHandleMiddle, self.centerBendLocator)
        cmds.parent(self.centerBendLocator, self.bendHandleOpen)

        cmds.xform( self.bendHandleOpen , objectSpace = True, translation = [widthValue,0,0])
        cmds.connectAttr(self.bendOpen+".highBound",self.centerBendLocator+".translateY")

        cmds.parent( )



    def AddAttributes(self,ControlBook):
        cmds.addAttr(ControlBook,longName="BookOpen",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=0,maxValue=10)
        cmds.addAttr(ControlBook,longName="BookLeaf",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=-10,maxValue=10)
        cmds.addAttr(ControlBook,longName="BorderRefinement",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=-10,maxValue=10)
        cmds.addAttr(ControlBook,longName="OpenBend",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=-10,maxValue=10)
        cmds.addAttr(ControlBook,longName="OpenLength",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=-10,maxValue=10)
        cmds.addAttr(ControlBook,longName="OpenBendCounter",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=-10,maxValue=10)
        cmds.addAttr(ControlBook,longName="OpenBendCounterLenght",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=-10,maxValue=10)

    def LinkAttributes(self,ControlBook ):

        RMRigTools.connectWithLimits( ControlBook + ".BookOpen","bend3.curvature",[[0,0],[10,60]] )
        RMRigTools.connectWithLimits( ControlBook + ".BookLeaf","self.flare2.endFlareZ",[[-10,-1],[0,1],[10,2]] )
        RMRigTools.connectWithLimits( ControlBook + ".BorderRefinement","flare1.startFlareX",[[-10,.8],[0,1],[10,1.2]] )
        RMRigTools.connectWithLimits( ControlBook + ".OpenBend","bend5.curvature",[[-10,-180],[0,0],[10,180]] )
        RMRigTools.connectWithLimits( ControlBook + ".OpenLength","bend5Handle.scaleX",[[-10,.2],[0,.5],[10,2]] )
        RMRigTools.connectWithLimits( ControlBook + ".OpenBendCounter","bend4.curvature",[[-10,-180],[0,0],[10,180]] )
        RMRigTools.connectWithLimits( ControlBook + ".OpenBendCounterLenght","bend4Handle.scaleX",[[-10,.1],[0,1],[10,1.5]] )

        



BookRig = RMBookPage()
#BookRig.CreateBookRefPoints()
BookRig.CreateBookRig()












