import maya.cmds as cmds
from RMPY import RMNameConvention
import maya.api.OpenMaya as om
import math


def RMAlign(obj1, obj2, flag):
    if flag == 1 or flag == 3:
        Obj1position = cmds.xform(obj1, q=True, ws=True, rp=True)
        cmds.xform(obj2, ws=True, t=Obj1position)
    if flag == 2 or flag == 3:
        rotateOrderObj1 = cmds.xform(obj1, q=True, rotateOrder=True)
        rotateOrderObj2 = cmds.xform(obj2, q=True, rotateOrder=True)
        if rotateOrderObj1 != rotateOrderObj2:
            Null = cmds.group(em=True)
            cmds.xform(Null, rotateOrder=rotateOrderObj1)
            Obj1rotacion = cmds.xform(obj1, q=True, ws=True, ro=True)
            cmds.xform(Null, ws=True, ro=Obj1rotacion)
            cmds.xform(Null, p=True, rotateOrder=rotateOrderObj2)
            Obj1rotacion = cmds.xform(Null, q=1, ws=1, ro=True)
            cmds.xform(obj2, ws=True, ro=Obj1rotacion)
            #print "Warning : Obj Rotation Order Mismatch on obj "
            #print  (obj2 + " Aligning to " + obj1 + "\n")
            cmds.delete(Null)
        else:
            Obj1rotacion = cmds.xform(obj1, q=True, ws=True, ro=True)
            cmds.xform(obj2, ws=True, ro=Obj1rotacion)


def RMPointDistance(Point01, Point02):
    Position01, Position02 = cmds.xform(Point01, q=True, ws=True, rp=True), cmds.xform(Point02, q=True, ws=True,
                                                                                       rp=True)
    Vector01, Vector02 = om.MVector(Position01), om.MVector(Position02)
    ResultVector = Vector01 - Vector02
    return om.MVector(ResultVector).length()


def RMCreateNLocatorsBetweenObjects(Obj01, Obj02, NumberOfPoints, name="locator", align="FirstObj"):
    '''Valid Values in align are FirstObj, SecondObject, and World'''
    locatorList = []
    Position01, Position02 = cmds.xform(Obj01, q=True, ws=True, rp=True), cmds.xform(Obj02, q=True, ws=True, rp=True)
    Vector01, Vector02 = om.MVector(Position01), om.MVector(Position02)
    ResultVector = Vector02 - Vector01
    Distance = om.MVector(ResultVector).length()
    DeltaVector = (Distance / (NumberOfPoints + 1)) * ResultVector.normal()
    for index in range(0, NumberOfPoints):
        locatorList.append(cmds.spaceLocator(name=name)[0])
        Obj1position = Vector01 + DeltaVector * (index + 1)
        cmds.xform(locatorList[index], ws=True, t=Obj1position)
        if align == "FirstObj":
            RMAlign(Obj01, locatorList[index], 2)
        elif align == "SecondObject":
            RMAlign(Obj02, locatorList[index], 2)
    return locatorList


def connectWithLimits(AttrX, AttrY, keys):
    for eachKey in keys:
        cmds.setDrivenKeyframe(AttrY, currentDriver=AttrX, dv=eachKey[0], v=eachKey[1])


def RMConnectWithLimits(AttrX, AttrY, keys):
    for eachKey in keys:
        cmds.setDrivenKeyframe(AttrY, currentDriver=AttrX, dv=eachKey[0], v=eachKey[1])


def RMCustomPickWalk(Obj, Class, Depth, Direction="down"):
    '''Valid Values of Direction ar up and down'''

    if Direction == "down":
        childs = cmds.listRelatives(Obj, children=True, type=Class)
    else:
        childs = cmds.listRelatives(Obj, parent=True, type=Class)
    returnValue = [Obj]
    if childs:
        if not (Depth == 0 or len(childs) == 0):
            for eachChildren in childs:
                if cmds.nodeType(eachChildren) == Class:
                    returnValue.extend(RMCustomPickWalk(eachChildren, Class, Depth - 1, Direction=Direction))
    return returnValue


def FindInHieararchy(Obj, GrandSon):
    returnArray = [Obj]
    if Obj == GrandSon:
        return returnArray
    allDescendents = cmds.listRelatives(Obj, allDescendents=True)
    if allDescendents:
        if GrandSon in allDescendents:
            Children = cmds.listRelatives(Obj, children=True)
            if Children:
                for eachChildren in Children:
                    Family = FindInHieararchy(eachChildren, GrandSon)
                    returnArray.extend(Family)
                return returnArray
    return []


def RMCreateGroupOnObj(Obj, Type="inserted", NameConv = None):
    '''
    "world","child","parent","inserted"
    '''
    if not NameConv:
        NameConv = RMNameConvention.RMNameConvention()

    Group = cmds.group(empty=True)

    if NameConv.RMIsNameInFormat(Obj):
        Group = NameConv.RMRenameBasedOnBaseName(Obj, Group, {'objectType': "transform"})

    else:
        ValidNameList = Obj.split("_")
        ValidName = ""
        for eachToken in ValidNameList:
            ValidName += eachToken
        NewName = NameConv.RMSetNameInFormat(
            {'name': NameConv.RMAddToNumberedString(ValidName, "Group"), 'objectType': "transform"})
        Group = cmds.rename(Group, NewName)

    RMAlign(Obj, Group, 3)

    Parent = cmds.listRelatives(Obj, parent=True)
    if not (Type == "world"):
        if Type == "inserted":
            if Parent:
                RMInsertInHierarchy(Obj, Group)
            else:
                cmds.parent(Obj, Group)
        elif Type == "parent":
            cmds.parent(Obj, Group)
        elif Type == "child":
            cmds.parent(Group, Obj)

    return Group


def RMLenghtOfBone(Joint):
    children = cmds.listRelatives(Joint, children=True)
    if children:
        if (len(children) > 0 and cmds.objectType(children[0]) != "locator"):
            return cmds.getAttr(children[0] + ".translateX")
        else:
            return RMJointSize(Joint)
    else:
        return RMJointSize(Joint)


def RMJointSize(Joint):
    if cmds.objectType(Joint) == "joint":
        radius = cmds.getAttr(Joint + ".radius")
        return (radius * 2)
    else:
        return 1.0


def RMInsertInHierarchy(Obj, InsertObj, InsertType="Parent"):
    if InsertType == "Parent":
        Parent = cmds.listRelatives(Obj, parent=True)
        if Parent and len(Parent) > 0:
            cmds.parent(InsertObj, Parent)
        cmds.parent(Obj, InsertObj)
    else:
        children = RMRemoveChildren(Obj)
        Parent = cmds.listRelatives(Obj, parent=True)
        cmds.parent(InsertObj, Obj)
        RMParentArray(InsertObj, children)


def RMRemoveChildren(Node):
    Children = cmds.listRelatives(Node, children=True)
    returnArray = []
    for eachChildren in Children:
        if cmds.objectType(eachChildren) != "mesh" and cmds.objectType(eachChildren) != "nurbsCurve":
            cmds.parent(eachChildren, world=True)
            returnArray.append(eachChildren)
    return returnArray


def RMParentArray(Parent, Array):
    for objects in Array:
        cmds.parent(objects, Parent)


def RMLockAndHideAttributes(Obj, BitString, LHType="LH"):
    ObjArray = []
    if type(Obj) in [str, unicode]:
        ObjArray = [Obj]
    elif type(Obj) == list:
        ObjArray = Obj
    else:
        print "error in LockAndHideAttr not valid Type of Obj"
        return False
    InfoDic = {".translateX": 0,
               ".translateY": 1,
               ".translateZ": 2,
               ".rotateX": 3,
               ".rotateY": 4,
               ".rotateZ": 5,
               ".scaleX": 6,
               ".scaleY": 7,
               ".scaleZ": 8,
               ".visibility": 9}
    if (len(BitString) == 10):
        print ObjArray
        for eachObj in ObjArray:
            for parameter in InfoDic:
                if BitString[InfoDic[parameter]] == "0":
                    cmds.setAttr(eachObj + parameter, k=False, l=True)
                elif BitString[InfoDic[parameter]] == "1":
                    cmds.setAttr(eachObj + parameter, k=True, l=False)
                elif BitString[InfoDic[parameter]] == "L":
                    cmds.setAttr(eachObj + parameter, l=False)
                elif BitString[InfoDic[parameter]] == "l":
                    cmds.setAttr(eachObj + parameter, l=True)
                elif BitString[InfoDic[parameter]] == "H":
                    cmds.setAttr(eachObj + parameter, k=True)
                elif BitString[InfoDic[parameter]] == "h":
                    cmds.setAttr(eachObj + parameter, k=False)
                else:
                    pass
    else:
        print "error in LockAndHideAttr Not valid Len on BitString"
        return False
    return True


def RMLinkHerarchyRotation(jntStart, jntEnd, Ctrl, X=True, Y=True, Z=True):
    children = cmds.listRelatives(jntStart, children=True)
    if (jntStart == jntEnd):
        if X:
            cmds.connectAttr(Ctrl + ".rotateX", jntStart + ".rotateX")
        if Y:
            cmds.connectAttr(Ctrl + ".rotateY", jntStart + ".rotateY")
        if Z:
            cmds.connectAttr(Ctrl + ".rotateZ", jntStart + ".rotateZ")
        return True
    else:
        for joints in children:
            if RMIsInHierarchy(joints, jntEnd):
                if X:
                    cmds.connectAttr(Ctrl + ".rotateX", jntStart + ".rotateX")
                if Y:
                    cmds.connectAttr(Ctrl + ".rotateY", jntStart + ".rotateY")
                if Z:
                    cmds.connectAttr(Ctrl + ".rotateZ", jntStart + ".rotateZ")
                return RMLinkHerarchyRotation(joints, jntEnd, Ctrl, X, Y, Z)
            else:
                return False


def RMIsInHierarchy(Obj1, Obj2):
    children = cmds.listRelatives(Obj1, children=True)
    if Obj1 == Obj2:
        return True
    else:
        for eachChild in children:
            if RMIsInHierarchy(eachChild, Obj2):
                return True
    return False


def RMChangeRotateOrder(Object, rotationOrder):
    rotateOrderDic = {
        'xyz': 0,
        'yzx': 1,
        'zxy': 2,
        'xzy': 3,
        'yxz': 4,
        'zyx': 5
    }
    if type(Object) in [str, unicode]:
        ObjList = [Object]
    else:
        ObjList = Object
    for eachObject in ObjList:
        cmds.setAttr(eachObject + ".rotateOrder", rotateOrderDic[rotationOrder])


def RMCreateBonesAtPoints(PointArray, NameConv=None, ZAxisOrientation="Y"):
    if not NameConv:
        NameConv = RMNameConvention.RMNameConvention()

    jointArray = []

    Obj1Position = cmds.xform(PointArray[0], q=True, rp=True, ws=True)
    Obj2Position = cmds.xform(PointArray[1], q=True, rp=True, ws=True)

    V1, V2 = om.MVector(Obj1Position), om.MVector(Obj2Position)

    initVector = V1 - V2

    firstJntAngle = V1.angle(om.MVector([0, 1, 0]))

    Angle = firstJntAngle

    ParentJoint = RMCreateGroupOnObj(PointArray[0], Type="world")

    for index in range(0, len(PointArray)):

        cmds.select(cl=True)

        newJoint = cmds.joint(p=[0, 0, 0], name="joint")
        jointArray.append(NameConv.RMRenameBasedOnBaseName(PointArray[index], newJoint, {}))

        if index == 0:
            cmds.parent(jointArray[0], ParentJoint)

        RMAlign(PointArray[index], jointArray[index], 3)
        cmds.makeIdentity(jointArray[index], apply=True, t=1, r=1, s=0)

        if (index > 0):
            if index == 1:
                AxisOrientJoint = cmds.joint()
                cmds.parent(AxisOrientJoint, ParentJoint)
                RMAlign(PointArray[0], AxisOrientJoint, 3)
                cmds.makeIdentity(AxisOrientJoint, apply=True, t=1, r=1, s=0)

                if ZAxisOrientation in "Yy":
                    cmds.xform(AxisOrientJoint, translation=[0, -1, 0], objectSpace=True)

                elif ZAxisOrientation in "Zz":
                    cmds.xform(AxisOrientJoint, translation=[0, 0, -1], objectSpace=True)

                cmds.parent(jointArray[0], AxisOrientJoint)
                cmds.parent(jointArray[index], jointArray[index - 1])
                cmds.joint(jointArray[index - 1], edit=True, orientJoint="xzy")

                cmds.parent(jointArray[index - 1], world=True)
                cmds.delete(AxisOrientJoint)
                RMAlign(jointArray[index - 1], ParentJoint, 3)
                cmds.parent(jointArray[index - 1], ParentJoint)

            else:
                cmds.parent(jointArray[index], jointArray[index - 1])
                cmds.joint(jointArray[index - 1], edit=True, orientJoint="xzy")
            # , sao="yup" )

            if index >= 2:
                parentOrient = cmds.joint(jointArray[index - 1], q=True, orientation=True)
                cmds.joint(jointArray[index - 1], e=True, orientation=[0, parentOrient[1], parentOrient[2]])
                # if parentOrient[0] > 90 :
                # cmds.joint (jointArray[index-1], e = True, orientation = [parentOrient[0]-180, parentOrient[1], parentOrient[2]])
                # else:
                # if parentOrient[0] < -90:
                # cmds.joint (jointArray[index-1], e = True, orientation = [parentOrient[0]+180, parentOrient[1], parentOrient[2]])

        if index == len(PointArray) - 1:
            RMAlign(jointArray[index - 1], jointArray[index], 2)
            cmds.makeIdentity(jointArray[index], apply=True, t=0, r=1, s=0)

    return ParentJoint, jointArray


def RMCreateLineBetwenPoints(Point1, Point2, NameConv=None):
    if not NameConv:
        NameConv = RMNameConvention.RMNameConvention()

    Curve = cmds.curve(degree=1, p=[[0, 0, 0], [1, 0, 0]], name="curveLineBetweenPnts")

    Curve = NameConv.RMRenameBasedOnBaseName(Point1, Curve, {'name': Curve})

    NumCVs = cmds.getAttr(Curve + ".controlPoints", size=True)

    Cluster1, Cluster1Handle = cmds.cluster(Curve + ".cv[0]", relative=True, name="clusterLineBetweenPnts")
    Cluster1 = NameConv.RMRenameBasedOnBaseName(Point1, Cluster1, {'name': Cluster1})
    Cluster1Handle = NameConv.RMRenameBasedOnBaseName(Point1, Cluster1Handle, {'name': Cluster1Handle})

    Cluster2, Cluster2Handle = cmds.cluster(Curve + ".cv[1]", relative=True, name="clusterLineBetweenPnts")
    Cluster2 = NameConv.RMRenameBasedOnBaseName(Point2, Cluster2, {'name': Cluster2})
    Cluster2Handle = NameConv.RMRenameBasedOnBaseName(Point2, Cluster2Handle, {'name': Cluster2Handle})

    cmds.setAttr(Curve + ".overrideEnabled", 1)
    cmds.setAttr(Curve + ".overrideDisplayType", 1)

    RMAlign(Point1, Cluster1Handle, 1)
    RMAlign(Point2, Cluster1Handle, 1)

    PointConstraint1 = cmds.pointConstraint(Point1, Cluster1Handle, name="PointConstraintLineBetweenPnts")[0]
    PointConstraint1 = NameConv.RMRenameBasedOnBaseName(Point1, PointConstraint1, {'name': PointConstraint1})
    PointConstraint2 = cmds.pointConstraint(Point2, Cluster2Handle, name="PointConstraintLineBetweenPnts")[0]
    PointConstraint2 = NameConv.RMRenameBasedOnBaseName(Point2, PointConstraint2, {'name': PointConstraint2})

    DataGroup = cmds.group(em=True, name="DataLineBetweenPnts")
    DataGroup = NameConv.RMRenameBasedOnBaseName(Point1, DataGroup, {'name': DataGroup})
    cmds.parent(Cluster1Handle, DataGroup)
    cmds.parent(Cluster2Handle, DataGroup)
    cmds.parent(Curve, DataGroup)
    return DataGroup, Curve


def RMCreateClustersOnCurve(curve, NameConv=None):
    if not NameConv:
        NameConv = RMNameConvention.RMNameConvention()

    degree = cmds.getAttr(curve + ".degree")
    spans = cmds.getAttr(curve + ".spans")
    form = cmds.getAttr(curve + ".form")
    print ("degree:%s", degree)
    print ("spans:%s", spans)
    print ("form:%s", form)
    #   Form (open = 0, closed = 1, periodic = 2)
    clusterList = []
    print form
    if form == 0 or form == 1:
        print "Open Line"
        for i in range(0, (degree + spans)):
            Cluster2Handle, cluster = cmds.cluster(curve + ".cv[" + str(i) + "]", name="ClusterOnCurve")
            if NameConv.RMIsNameInFormat(curve):
                cluster = NameConv.RMRenameBasedOnBaseName(curve, cluster, {'name': cluster})
                # Cluster2Handle = NameConv.RMRenameBasedOnBaseName(curve, Cluster2Handle, NewName = Cluster2Handle)
            else:
                cluster = NameConv.RMRenameNameInFormat(cluster, {})
                # Cluster2Handle = NameConv.RMRenameNameInFormat(Cluster2Handle)
            clusterList.append(cluster)
            cmds.setAttr(cluster + ".visibility", 0)
            ##cmds.cluster(cluster,edit=True,geometry = curve + ".["+str(i)+"]")
    if form == 2:
        print "periodic Line"
        for i in range(0, spans):
            Cluster2Handle, cluster = cmds.cluster(curve + ".cv[" + str(i) + "]", name="ClusterOnCurve")
            print cluster
            if NameConv.RMIsNameInFormat(curve):
                cluster = NameConv.RMRenameBasedOnBaseName(curve, cluster, {'name': cluster})
                # Cluster2Handle = NameConv.RMRenameBasedOnBaseName(curve, Cluster2Handle, NewName = Cluster2Handle)
            else:
                cluster = NameConv.RMRenameNameInFormat(cluster, {})
                # Cluster2Handle = NameConv.RMRenameNameInFormat(Cluster2Handle)
            clusterList.append(cluster)
            cmds.setAttr(cluster + ".visibility", 0)
            # cmds.cluster(cluster,edit=True,geometry = curve + ".["+str(i)+"]")
    return clusterList

def objectsInListExists(objectsLists,verbose = True ):
    listString = ''
    exists = True
    for eachObject in objectsLists:
        existEachObjec = cmds.objExists(eachObject)
        if not existEachObjec:
            listString = '%s %s'%(listString, eachObject)
        exists = exists and existEachObjec
    if verbose and not exists:
        print 'the folowing objects were not found: %s'%listString
    return exists

class boundingBoxInfo(object):
    def __init__(self, Object):
        self.xmin = None
        self.ymin = None
        self.zmin = None
        self.xmax = None
        self.ymax = None
        self.zmax = None

        if Object.__class__ == list:
            for eachObject in Objects:
                Values = cmds.xform(eachObject, q=True, bb=True)
                if self.xmin == None or self.xmin > Values[0]:
                    self.xmin = Values[0]
                if self.ymin == None or self.ymin > Values[1]:
                    self.ymin = Values[1]
                if self.zmin == None or self.zmin > Values[2]:
                    self.zmin = Values[2]
                if self.xmax == None or self.xmax < Values[3]:
                    self.xmax = Values[3]
                if self.ymax == None or self.ymax < Values[4]:
                    self.ymax = Values[4]
                if self.zmax == None or self.zmax < Values[5]:
                    self.zmax = Values[5]
        elif Object.__class__ in [str, unicode]:
            self.BaseObject = Object
            Values = cmds.xform(Object, q=True, bb=True)
            self.position = cmds.xform(Object, q=True, rp=True, worldSpace=True)
            self.xmin = Values[0]
            self.ymin = Values[1]
            self.zmin = Values[2]
            self.xmax = Values[3]
            self.ymax = Values[4]
            self.zmax = Values[5]

        self.lenX = self.xmax - self.xmin
        self.lenY = self.ymax - self.ymin
        self.lenZ = self.zmax - self.zmin
        self.minDistanceToCenterX = self.position[0] - self.xmin
        self.minDistanceToCenterY = self.position[1] - self.ymin
        self.minDistanceToCenterZ = self.position[2] - self.zmin
        self.maxDistanceToCenterX = self.position[0] - self.xmax
        self.maxDistanceToCenterY = self.position[1] - self.ymax
        self.maxDistanceToCenterZ = self.position[2] - self.zmax
        self.offsetX = (self.minDistanceToCenterX - self.maxDistanceToCenterX) / 2
        self.offsetY = (self.minDistanceToCenterY - self.maxDistanceToCenterY) / 2
        self.offsetZ = (self.minDistanceToCenterZ - self.maxDistanceToCenterZ) / 2

    def recalculate(self):
        self.position = cmds.xform(Object, q=True, rp=True, worldSpace=True)
        self.lenX = Values[3] - Values[0]
        self.lenY = Values[4] - Values[1]
        self.lenZ = Values[5] - Values[2]
        self.xmin = Values[0]
        self.ymin = Values[1]
        self.zmin = Values[2]
        self.xmax = Values[3]
        self.ymax = Values[4]
        self.zmax = Values[5]
        self.minDistanceToCenterX = self.position[0] - self.xmin
        self.minDistanceToCenterY = self.position[1] - self.ymin
        self.minDistanceToCenterZ = self.position[2] - self.zmin
        self.maxDistanceToCenterX = self.position[0] - self.xmax
        self.maxDistanceToCenterY = self.position[1] - self.ymax
        self.maxDistanceToCenterZ = self.position[2] - self.zmax
        self.offsetX = (self.minDistanceToCenterX - self.maxDistanceToCenterX) / 2
        self.offsetY = (self.minDistanceToCenterY - self.maxDistanceToCenterY) / 2
        self.offsetZ = (self.minDistanceToCenterZ - self.maxDistanceToCenterZ) / 2


class RMRigTools(object):
    def __init__(self, NameConv=None):
        if NameConv == None:
            self.NameConv = RMNameConvention.RMNameConvention()
        else:
            self.NameConv = NameConv

    def RMCreateBonesAtPoints(self, PointArray, ZAxisOrientation = "Y"):

        jointArray = []

        Obj1Position = cmds.xform(PointArray[0], q=True, rp=True, ws=True)
        Obj2Position = cmds.xform(PointArray[1], q=True, rp=True, ws=True)

        V1, V2 = om.MVector(Obj1Position), om.MVector(Obj2Position)

        initVector = V1 - V2

        firstJntAngle = V1.angle(om.MVector([0, 1, 0]))

        Angle = firstJntAngle

        ParentJoint = self.RMCreateGroupOnObj(PointArray[0], Type="world")

        for index in range(0, len(PointArray)):

            cmds.select(cl=True)

            newJoint = cmds.joint(p=[0, 0, 0], name="joint")
            print 'pointArrayIndex::::%s' % PointArray[index]
            jointArray.append(self.NameConv.RMRenameBasedOnBaseName(PointArray[index], newJoint, {'objectType':'joint'}))

            if index == 0:
                cmds.parent(jointArray[0], ParentJoint)

            RMAlign(PointArray[index], jointArray[index], 3)
            cmds.makeIdentity(jointArray[index], apply=True, t=1, r=1, s=0)

            if (index > 0):
                if index == 1:
                    AxisOrientJoint = cmds.joint()
                    cmds.parent(AxisOrientJoint, ParentJoint)
                    RMAlign(PointArray[0], AxisOrientJoint, 3)
                    cmds.makeIdentity(AxisOrientJoint, apply=True, t=1, r=1, s=0)

                    if ZAxisOrientation in "Yy":
                        cmds.xform(AxisOrientJoint, translation=[0, -1, 0], objectSpace=True)

                    elif ZAxisOrientation in "Zz":
                        cmds.xform(AxisOrientJoint, translation=[0, 0, -1], objectSpace=True)

                    cmds.parent(jointArray[0], AxisOrientJoint)
                    cmds.parent(jointArray[index], jointArray[index - 1])
                    cmds.joint(jointArray[index - 1], edit=True, orientJoint="xzy")

                    cmds.parent(jointArray[index - 1], world=True)
                    cmds.delete(AxisOrientJoint)
                    RMAlign(jointArray[index - 1], ParentJoint, 3)
                    cmds.parent(jointArray[index - 1], ParentJoint)

                else:
                    cmds.parent(jointArray[index], jointArray[index - 1])
                    cmds.joint(jointArray[index - 1], edit=True, orientJoint="xzy")
                # , sao="yup" )

                if index >= 2:
                    parentOrient = cmds.joint(jointArray[index - 1], q=True, orientation=True)
                    cmds.joint(jointArray[index - 1], e=True, orientation=[0, parentOrient[1], parentOrient[2]])
                    # if parentOrient[0] > 90 :
                    # cmds.joint (jointArray[index-1], e = True, orientation = [parentOrient[0]-180, parentOrient[1], parentOrient[2]])
                    # else:
                    # if parentOrient[0] < -90:
                    # cmds.joint (jointArray[index-1], e = True, orientation = [parentOrient[0]+180, parentOrient[1], parentOrient[2]])

            if index == len(PointArray) - 1:
                RMAlign(jointArray[index - 1], jointArray[index], 2)
                cmds.makeIdentity(jointArray[index], apply=True, t=0, r=1, s=0)

        return ParentJoint, jointArray

    def RMCreateGroupOnObj(self, Obj, Type = "inserted", name = None):
        '''
        "world","child","parent","inserted","sibling"
        '''
        Group = cmds.group(empty=True)

        if self.NameConv.RMIsNameInFormat(Obj):
            Group = self.NameConv.RMRenameBasedOnBaseName(Obj, Group, {})
            if name is not None:
                Group = self.NameConv.RMRenameSetFromName(Group, name, 'name')
        else:
            if name is None:
                ValidNameList = Obj.split("_")
                ValidName = ""
                for eachToken in ValidNameList:
                    ValidName += eachToken
            else:
                ValidName = name
            NewName = self.NameConv.RMSetNameInFormat({'name': ValidName , 'objectType': "transform"})
            Group = cmds.rename(Group, NewName)

        RMAlign(Obj, Group, 3)

        Parent = cmds.listRelatives(Obj, parent=True)
        if not (Type == "world"):
            if Type == "inserted":
                if Parent:
                    RMInsertInHierarchy(Obj, Group)
                else:
                    cmds.parent(Obj, Group)
            elif Type == "parent":
                cmds.parent(Obj, Group)
            elif Type == "child":
                cmds.parent(Group, Obj)
            elif Type == "sibling":
                cmds.parent(Group, Parent)

        return Group

    def createLineAtPoints(self, pointList, periodic=False, degree=3):

        listofPoints = [cmds.xform('%s' % eachPointList, q=True, ws=True, rp=True) for eachPointList in pointList]
        if not periodic:
            Curve = cmds.curve(degree=degree, p=listofPoints, name='line')
        else:
            fullListPoint = listofPoints + listofPoints[:3]
            numElements = len(fullListPoint)
            knotVector = range(-degree + 1, 0) + range(numElements)
            Curve = cmds.curve(degree=degree, p=fullListPoint, periodic=periodic, name='line', k=knotVector)
        Curve = self.NameConv.RMRenameBasedOnBaseName(pointList[0], Curve, {'name': Curve})
        return Curve

    def RMCreateLineBetwenPoints(self, Point1, Point2):
        Curve = cmds.curve(degree=1, p=[[0, 0, 0], [1, 0, 0]], name="curveLineBetweenPnts")

        Curve = self.NameConv.RMRenameBasedOnBaseName(Point1, Curve, {'name': Curve})

        NumCVs = cmds.getAttr(Curve + ".controlPoints", size=True)

        Cluster1, Cluster1Handle = cmds.cluster(Curve + ".cv[0]", relative=True, name="clusterLineBetweenPnts")
        Cluster1 = self.NameConv.RMRenameBasedOnBaseName(Point1, Cluster1, {'name': Cluster1})
        Cluster1Handle = self.NameConv.RMRenameBasedOnBaseName(Point1, Cluster1Handle, {'name': Cluster1Handle})

        Cluster2, Cluster2Handle = cmds.cluster(Curve + ".cv[1]", relative=True, name="clusterLineBetweenPnts")
        Cluster2 = self.NameConv.RMRenameBasedOnBaseName(Point2, Cluster2, {'name': Cluster2})
        Cluster2Handle = self.NameConv.RMRenameBasedOnBaseName(Point2, Cluster2Handle, {'name': Cluster2Handle})

        cmds.setAttr(Curve + ".overrideEnabled", 1)
        cmds.setAttr(Curve + ".overrideDisplayType", 1)

        RMAlign(Point1, Cluster1Handle, 1)
        RMAlign(Point2, Cluster1Handle, 1)

        PointConstraint1 = cmds.pointConstraint(Point1, Cluster1Handle, name="PointConstraintLineBetweenPnts")[0]
        PointConstraint1 = self.NameConv.RMRenameBasedOnBaseName(Point1, PointConstraint1, {'name': PointConstraint1})
        PointConstraint2 = cmds.pointConstraint(Point2, Cluster2Handle, name="PointConstraintLineBetweenPnts")[0]
        PointConstraint2 = self.NameConv.RMRenameBasedOnBaseName(Point2, PointConstraint2, {'name': PointConstraint2})

        DataGroup = cmds.group(em=True, name="DataLineBetweenPnts")
        DataGroup = self.NameConv.RMRenameBasedOnBaseName(Point1, DataGroup, {'name': DataGroup})
        cmds.parent(Cluster1Handle, DataGroup)
        cmds.parent(Cluster2Handle, DataGroup)
        cmds.parent(Curve, DataGroup)
        return DataGroup, Curve

    def RMCreateClustersOnCurve(self, curve):
        degree = cmds.getAttr(curve + ".degree")
        spans = cmds.getAttr(curve + ".spans")
        form = cmds.getAttr(curve + ".form")
        print ("degree:%s", degree)
        print ("spans:%s", spans)
        print ("form:%s", form)
        #   Form (open = 0, closed = 1, periodic = 2)
        clusterList = []
        print form
        if form == 0 or form == 1:
            print "Open Line"
            for i in range(0, (degree + spans)):
                Cluster2Handle, cluster = cmds.cluster(curve + ".cv[" + str(i) + "]", name="ClusterOnCurve")
                if self.NameConv.RMIsNameInFormat(curve):
                    cluster = self.NameConv.RMRenameBasedOnBaseName(curve, cluster, {'name': cluster})
                    # Cluster2Handle = self.NameConv.RMRenameBasedOnBaseName(curve, Cluster2Handle, NewName = Cluster2Handle)
                else:
                    cluster = self.NameConv.RMRenameNameInFormat(cluster, {})
                    # Cluster2Handle = self.NameConv.RMRenameNameInFormat(Cluster2Handle)
                clusterList.append(cluster)
                cmds.setAttr(cluster + ".visibility", 0)
                ##cmds.cluster(cluster,edit=True,geometry = curve + ".["+str(i)+"]")
        if form == 2:
            print "periodic Line"
            for i in range(0, spans):
                Cluster2Handle, cluster = cmds.cluster(curve + ".cv[" + str(i) + "]", name="ClusterOnCurve")
                print cluster
                if self.NameConv.RMIsNameInFormat(curve):
                    cluster = self.NameConv.RMRenameBasedOnBaseName(curve, cluster, {'name': cluster})
                    # Cluster2Handle = self.NameConv.RMRenameBasedOnBaseName(curve, Cluster2Handle, NewName = Cluster2Handle)
                else:
                    cluster = self.NameConv.RMRenameNameInFormat(cluster, {})
                    # Cluster2Handle = self.NameConv.RMRenameNameInFormat(Cluster2Handle)
                clusterList.append(cluster)
                cmds.setAttr(cluster + ".visibility", 0)
                # cmds.cluster(cluster,edit=True,geometry = curve + ".["+str(i)+"]")
        return clusterList

    def RMCreateNLocatorsBetweenObjects(self, Obj01, Obj02, numberOfPoints, name="locator", align="FirstObj"):
        '''Valid Values in align are FirstObj, SecondObject, and World'''
        locatorList = []
        Position01, Position02 = cmds.xform(Obj01, q=True, ws=True, rp=True), cmds.xform(Obj02, q=True, ws=True,
                                                                                         rp=True)
        Vector01, Vector02 = om.MVector(Position01), om.MVector(Position02)
        ResultVector = Vector02 - Vector01
        Distance = om.MVector(ResultVector).length()
        DeltaVector = (Distance / (numberOfPoints + 1)) * ResultVector.normal()
        for index in range(0, numberOfPoints):
            newLocator = cmds.spaceLocator(name=name)[0]
            locatorList.append(self.NameConv.RMRenameBasedOnBaseName(Obj01, newLocator, {}))
            # locatorList.append(self.NameConv.RMRenameNameInFormat(newLocator, {}))
            Obj1position = Vector01 + DeltaVector * (index + 1)
            cmds.xform(locatorList[index], ws=True, t=Obj1position)
            if align == "FirstObj":
                RMAlign(Obj01, locatorList[index], 2)
            elif align == "SecondObject":
                RMAlign(Obj02, locatorList[index], 2)
        return locatorList

    def RMCreateBiasedLocatorsBetweenObjects(self, Obj01, Obj02, numberOfPoints, initialSize, name="locator",
                                             align="FirstObj"):
        '''Valid Values in align are FirstObj, SecondObject, and World'''
        numberOfPoints = numberOfPoints
        locatorList = []
        Position01, Position02 = cmds.xform(Obj01, q=True, ws=True, rp=True), cmds.xform(Obj02, q=True, ws=True,
                                                                                         rp=True)
        Vector01, Vector02 = om.MVector(Position01), om.MVector(Position02)
        ResultVector = Vector02 - Vector01
        Distance = om.MVector(ResultVector).length()
        DeltaVector = (
        (((Distance - initialSize) - (numberOfPoints * initialSize)) * 2) / (numberOfPoints * (numberOfPoints + 1)))
        TempValue = 0
        # DeltaVector = (Distance/(numberOfPoints+1))*ResultVector.normal()
        for index in range(0, numberOfPoints):
            newLocator = cmds.spaceLocator(name=name)[0]
            locatorList.append(self.NameConv.RMRenameNameInFormat(newLocator, {}))
            TempValue = TempValue + initialSize + (DeltaVector) * (numberOfPoints - index)
            Obj1position = Vector01 + TempValue * ResultVector.normal()
            print ("vectorValue=%s" % Obj1position.length())
            cmds.xform(locatorList[index], ws=True, t=Obj1position)
            if align == "FirstObj":
                RMAlign(Obj01, locatorList[index], 2)
            elif align == "SecondObject":
                RMAlign(Obj02, locatorList[index], 2)
        return locatorList

        # rigTools = RMRigTools()
        # locators = rigTools.RMCreateBiasedLocatorsBetweenObjects("locator1","locator2",6,.5)
        # locators.insert(0,"locator1")
        # locators.insert(len(locators),"locator2")
        # RMCreateBonesAtPoints( locators )
