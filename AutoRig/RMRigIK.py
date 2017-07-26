import pymel.core as pm
import maya.OpenMayaUI as mui
import maya.api.OpenMaya as om
import math



def get_polevector_from_reference_nodes(self, JointList):
    VP1 = om.MVector(pm.xform(JointList[0], a=True, ws=True, q=True, rp=True))
    VP2 = om.MVector(pm.xform(JointList[1], a=True, ws=True, q=True, rp=True))
    VP3 = om.MVector(pm.xform(JointList[2], a=True, ws=True, q=True, rp=True))
    V1 = VP2 - VP1
    V2 = VP3 - VP2
    Angle = math.radians((math.degrees(V1.angle(V2)) + 180) / 2 - 90)

    zAxis = (V1 ^ V2).normal()
    yAxis = (V2 ^ zAxis).normal()
    xAxis = V2.normal()

    Y1 = math.cos(Angle)
    X1 = -math.sin(Angle)
    Vy = yAxis * Y1
    Vx = xAxis * X1

    Length = (V1.length() + V2.length()) / 2
    result = ((Vy + Vx) * Length) + VP2
    PoleVector = pm.spaceLocator(name="poleVector")[0]
    PoleVector = self.NameConv.RMRenameBasedOnBaseName(JointList[1], PoleVector, {'name': PoleVector})
    pm.xform(PoleVector, ws=True, t=result)

    return PoleVector
def pole_vector(self, VP1, VP2, VP3):
    V1 = VP2 - VP1
    V2 = VP3 - VP2
    Angle = math.radians((math.degrees(V1.angle(V2)) + 180) / 2 - 90)
    zAxis = (V1 ^ V2).normal()
    yAxis = (V2 ^ zAxis).normal()
    xAxis = V2.normal()

    Y1 = math.cos(Angle)
    X1 = -math.sin(Angle)
    Vy = yAxis * Y1
    Vx = xAxis * X1

    Length = (V1.length() + V2.length()) / 2
    result = ((Vy + Vx) * Length) + VP2
    return {}





