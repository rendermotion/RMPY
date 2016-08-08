import maya.cmds as cmds
import maya.mel as mel
import RMRigTools

#mel.eval('source "RMAttributes.mel"; \nDeleteAttributes("BookMainControl");')


bend = cmds.nonLinear(type = bend, lowBound = -1, highBound =1, curvature = 0)



#cmds.addAttr("BookMainControl",longName="BookOpen",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=0,maxValue=10)
#cmds.addAttr("BookMainControl",longName="BookLeaf",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=-10,maxValue=10)
#cmds.addAttr("BookMainControl",longName="BorderRefinement",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=-10,maxValue=10)
#cmds.addAttr("BookMainControl",longName="OpenBend",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=-10,maxValue=10)
#cmds.addAttr("BookMainControl",longName="OpenLength",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=-10,maxValue=10)
#cmds.addAttr("BookMainControl",longName="OpenBendCounter",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=-10,maxValue=10)
#cmds.addAttr("BookMainControl",longName="OpenBendCounterLenght",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=-10,maxValue=10)

#RMRigTools.connectWithLimits("BookMainControl.BookOpen","bend3.curvature",[[0,0],[10,60]])
#RMRigTools.connectWithLimits("BookMainControl.BookLeaf","flare2.endFlareZ",[[-10,-1],[0,1],[10,2]])
#RMRigTools.connectWithLimits("BookMainControl.BorderRefinement","flare1.startFlareX",[[-10,.8],[0,1],[10,1.2]])
#RMRigTools.connectWithLimits("BookMainControl.OpenBend","bend5.curvature",[[-10,-180],[0,0],[10,180]])
#RMRigTools.connectWithLimits("BookMainControl.OpenLength","bend5Handle.scaleX",[[-10,.2],[0,.5],[10,2]])
#RMRigTools.connectWithLimits("BookMainControl.OpenBendCounter","bend4.curvature",[[-10,-180],[0,0],[10,180]])
RMRigTools.connectWithLimits("BookMainControl.OpenBendCounterLenght","bend4Handle.scaleX",[[-10,.1],[0,1],[10,1.5]])





'''
cmds.addAttr("PapirusControl",longName="SinAmplitude",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=0,maxValue=10)
cmds.addAttr("PapirusControl",longName="SinPhase",keyable=1)
cmds.addAttr("PapirusControl",longName="SinDecay",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=-10,maxValue=10)
cmds.addAttr("PapirusControl",longName="SinDecayPos",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=0,maxValue=10)
cmds.addAttr("PapirusControl",longName="SinWaveLen",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=0,maxValue=10)


cmds.addAttr("PapirusControl",longName="BendFloor",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=-10,maxValue=10)
cmds.addAttr("PapirusControl",longName="BendFloorDistance",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=0,maxValue=10)

cmds.addAttr("PapirusControl",longName="BendDirection",keyable=1,hasMinValue=1,hasMaxValue=1,minValue=-10,maxValue=10)



cmds.addAttr("PapirusControl",longName="ExtraControls",attributeType="enum",enumName = "Off:On")


RMRigTools.connectWithLimits("PapirusControl.BendRoll","RolledBend.curvature",[[-10,-180],[0,0],[10,180]])
cmds.connectAttr("PapirusControl.BendRollDirection","RollbendHandle.rotateY",force=True)

RMRigTools.connectWithLimits("PapirusControl.BendFloor","FloorBend.curvature",[[-10,-180],[0,0],[10,180]])
RMRigTools.connectWithLimits("PapirusControl.BendFloorDistance","FloorBendHandle.translateZ",[[0,0],[10,-20]])

RMRigTools.connectWithLimits("PapirusControl.SinAmplitude","Wave.amplitude",[[0,0],[10,-20]])
cmds.connectAttr("PapirusControl.SinPhase","Wave.offset",force=True)

RMRigTools.connectWithLimits("PapirusControl.SinDecay","Wave.dropoff",[[-10,-1] , [0,0] , [10,1]] )
RMRigTools.connectWithLimits("PapirusControl.SinDecayPos","sine1Handle.translateZ",[[0,0],[10,-20]])
RMRigTools.connectWithLimits("PapirusControl.SinWaveLen","Wave.wavelength",[[0,.1],[10,6]])
RMRigTools.connectWithLimits("PapirusControl.BendDirection","DirectionBend.curvature",[[-10,-90],[0,0],[10,90]])
cmds.connectAttr("PapirusControl.ExtraControls","curve1.visibility",force=True) '''

