import maya.cmds as cmds
import maya.mel as mel
import RMRigTools

# mel.eval('source "RMAttributes.mel"; \nDeleteAttributes("PapirusControl");')

cmds.addAttr("PapirusControl", longName="BendRoll", keyable=1, hasMinValue=1, hasMaxValue=1, minValue=-10, maxValue=10)
cmds.addAttr("PapirusControl", longName="BendRollDirection", keyable=1, hasMinValue=1, hasMaxValue=1, minValue=0,
             maxValue=10)

cmds.addAttr("PapirusControl", longName="SinAmplitude", keyable=1, hasMinValue=1, hasMaxValue=1, minValue=0,
             maxValue=10)
cmds.addAttr("PapirusControl", longName="SinPhase", keyable=1)
cmds.addAttr("PapirusControl", longName="SinDecay", keyable=1, hasMinValue=1, hasMaxValue=1, minValue=-10, maxValue=10)
cmds.addAttr("PapirusControl", longName="SinDecayPos", keyable=1, hasMinValue=1, hasMaxValue=1, minValue=0, maxValue=10)
cmds.addAttr("PapirusControl", longName="SinWaveLen", keyable=1, hasMinValue=1, hasMaxValue=1, minValue=0, maxValue=10)

cmds.addAttr("PapirusControl", longName="BendFloor", keyable=1, hasMinValue=1, hasMaxValue=1, minValue=-10, maxValue=10)
cmds.addAttr("PapirusControl", longName="BendFloorDistance", keyable=1, hasMinValue=1, hasMaxValue=1, minValue=0,
             maxValue=10)

cmds.addAttr("PapirusControl", longName="BendDirection", keyable=1, hasMinValue=1, hasMaxValue=1, minValue=-10,
             maxValue=10)

print "1";
cmds.addAttr("PapirusControl", longName="ExtraControls", attributeType="enum", enumName="Off:On")

print "2";
RMRigTools.connectWithLimits("PapirusControl.BendRoll", "RolledBend.curvature", [[-10, -180], [0, 0], [10, 180]])
cmds.connectAttr("PapirusControl.BendRollDirection", "RollbendHandle.rotateY", force=True)
print "3";
RMRigTools.connectWithLimits("PapirusControl.BendFloor", "FloorBend.curvature", [[-10, -180], [0, 0], [10, 180]])
RMRigTools.connectWithLimits("PapirusControl.BendFloorDistance", "FloorBendHandle.translateZ", [[0, 0], [10, -20]])
print "4";
RMRigTools.connectWithLimits("PapirusControl.SinAmplitude", "Wave.amplitude", [[0, 0], [10, -20]])
cmds.connectAttr("PapirusControl.SinPhase", "Wave.offset", force=True)
print "5";
RMRigTools.connectWithLimits("PapirusControl.SinDecay", "Wave.dropoff", [[-10, -1], [0, 0], [10, 1]])
RMRigTools.connectWithLimits("PapirusControl.SinDecayPos", "sine1Handle.translateZ", [[0, 0], [10, -20]])
RMRigTools.connectWithLimits("PapirusControl.SinWaveLen", "Wave.wavelength", [[0, .1], [10, 6]])
print "6";
RMRigTools.connectWithLimits("PapirusControl.BendDirection", "DirectionBend.curvature", [[-10, -90], [0, 0], [10, 90]])
print "7";
cmds.connectAttr("PapirusControl.ExtraControls", "curve1.visibility", force=True)
