import maya.cmds as cmds
import maya.api.OpenMaya as om
from RMPY import RMRigTools

def getExtremePoints(listOfPnts):
    MaxDistanceDic = {'points':[],'distance':0}
    for eachPoint in listOfPnts:
        for eachOtherPoint in listOfPnts:
            distanceValue = RMRigTools.RMPointDistance(eachPoint, eachOtherPoint)
            if distanceValue > MaxDistanceDic['distance']:
                MaxDistanceDic['points']= [eachPoint,eachOtherPoint]
                MaxDistanceDic['distance'] = distanceValue
    return MaxDistanceDic

def orderPointsByDistance(straigtPnts, MaxDistanceDic):
    shortArray = straigtPnts
    shortArray.remove(MaxDistanceDic['points'][0])
    shortArray.remove(MaxDistanceDic['points'][1])
    distanceArray = {}
    for eachElement in shortArray:
        distanceArray[eachElement] = RMRigTools.RMPointDistance ( MaxDistanceDic['points'][0],eachElement )
    return sorted(distanceArray, key =  distanceArray.__getitem__)

def equidistant(straigtPnts):
    DistanceDic = getExtremePoints (straigtPnts)
    orderedPoints = orderPointsByDistance( straigtPnts , DistanceDic)
    Position01,Position02 = cmds.xform(DistanceDic['points'][0],q=True,ws=True,rp=True) , cmds.xform(DistanceDic['points'][1],q=True,ws=True,rp=True)
    Vector01 , Vector02 = om.MVector(Position01),om.MVector(Position02)
    
    NumberOfPoints = len(orderedPoints)

    ResultVector = Vector02 - Vector01 
    Distance = om.MVector(ResultVector).length()
    DeltaVector = (Distance/(NumberOfPoints+1))*ResultVector.normal()

    for index in range(0, NumberOfPoints):
        objPosition = Vector01 + DeltaVector * (index + 1)
        cmds.xform(orderedPoints[index],ws=True, t = objPosition)

if __name__=='__main__':
    selection = cmds.ls(selection = True)
    equidistant(selection)
    
