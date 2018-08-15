import maya.cmds as cmds
from RMPY import nameConvention

reload(nameConvention)
NameConv = nameConvention.NameConvention()


# cmds.addAttr(control,at="float", ln = "Percent", h = 0, k = 1)
# cmds.addAttr(control,at="float", ln = "Stretch", hnv = 1, hxv = 0, h = 0, k = 1, smn = 0)

def pathFollow(curve, control, objectArray, NameConv=None):
    if not NameConv:
        NameConv = nameConvention.NameConvention()
    controlAttr = cmds.listAttr(control)
    if "Percent" not in controlAttr:
        cmds.addAttr(control, at="float", ln="Percent", h=0, k=1)
    if "Stretch" not in controlAttr:
        cmds.addAttr(control, at="float", ln="Stretch", hnv=1, hxv=0, h=0, k=1, smn=0)

    numberOfElements = len(objectArray)
    sumPath = []
    multiplyDivide = []
    index = 0
    for eachObject in objectArray:
        motionPath = cmds.pathAnimation(eachObject, c=curve, follow=True, worldUpType="scene",
                                        name="motionpath%s" % index)
        motionPath = NameConv.rename_name_in_format(motionPath, {'name':motionPath})
        multDivFactor = cmds.shadingNode('multiplyDivide', asUtility=True, name="factor%s" % index)
        multDivFactor = NameConv.rename_name_in_format(multDivFactor, {'name':multDivFactor})
        cmds.connectAttr("%s.Stretch" % control, "%s.input1X" % multDivFactor)
        cmds.setAttr("%s.input2X" % multDivFactor, float(index) / float(len(objectArray)))
        cmds.setAttr("%s.operation" % multDivFactor, 1)
        multiplyDivide.append(multDivFactor)
        addition = cmds.shadingNode('plusMinusAverage', asUtility=True, name="Addition%s" % index)
        addition = NameConv.rename_name_in_format(addition, {'name':addition})
        cmds.connectAttr("%s.outputX" % multDivFactor, "%s.input1D[0]" % addition)
        cmds.connectAttr("%s.Percent" % control, "%s.input1D[1]" % addition)
        cmds.connectAttr("%s.output1D" % addition, "%s.uValue" % motionPath, force=True)
        index += 1


if __name__ == "__main__":
    objectArray = cmds.ls(sl=True)
    pathFollow("curve1", "nurbsCircle1", objectArray)
