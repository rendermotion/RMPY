from RMPY import RMNameConvention
import maya.api.OpenMaya as om
import math
import pymel.core as pm
import inspect
reload(RMNameConvention)

def average(*args):
    average_result = []
    for vector_index, each_vector in enumerate(args):
        for index, each_value in enumerate(each_vector):
            print index, each_value
            if vector_index == 0:
                average_result = each_vector
            else:
                average_result[index] = average_result[index] + each_value
    return [float(result)/len(args) for result in average_result]


def connectWithLimits(AttrX, AttrY, keys):
    AttrX = validate_pymel_nodes(AttrX)
    AttrY = validate_pymel_nodes(AttrY)
    value = pm.listConnections(AttrY, destination=False, plugs=True, skipConversionNodes=True)
    if value:
        print value[0].node()
        if pm.objectType(value[0].node()) == 'plusMinusAverage':
            plusMinus = value[0].node()
            if AttrX.get(type=True) in ['float', 'doubleLinear', 'doubleAngle']:
                for eachKey in keys:
                    pm.setDrivenKeyframe('%s' % plusMinus.input1D[len(plusMinus.input1D.elements())],
                                           currentDriver='%s' % AttrX, dv=eachKey[0], v=eachKey[1])
            # elif attribute_source.get(type=True) in [vector]:
            #    print 'connecting vector'
            elif AttrX.get(type=True) in ['double3']:
                for eachKey in keys:
                    pm.setDrivenKeyframe('%s' % plusMinus.input3D[len(plusMinus.input3D.elements()) % 3],
                                           currentDriver='%s' % AttrX, dv=eachKey[0], v=eachKey[1])
            else:

                print 'could not add data type: %s' % AttrX.get(type=True)
        else:
            if AttrX.get(type=True) in ['float','doubleLinear', 'doubleAngle']:
                plusMinus = pm.shadingNode("plusMinusAverage", asUtility=True, name="additiveConnection")
                value[0] // AttrY
                value[0] >> plusMinus.input1D[0]
                plusMinus.output1D >> AttrY
                for eachKey in keys:
                    pm.setDrivenKeyframe('%s' % plusMinus.input1D[1],
                                           currentDriver='%s' % AttrX, dv=eachKey[0], v=eachKey[1])
            elif AttrX.get(type=True) in ['double3']:
                plusMinus = pm.shadingNode("plusMinusAverage", asUtility=True, name="additiveConnection")
                value[0] // AttrY
                value[0] >> plusMinus.input3D[0]
                plusMinus.output3D >> AttrY
                for eachKey in keys:
                    pm.setDrivenKeyframe('%s' % plusMinus.input3D[1],
                                           currentDriver='%s' % AttrX, dv=eachKey[0], v=eachKey[1])
            else:
                print 'could not add data type: %s' % AttrX.get(type=True)
    else:
        for eachKey in keys:
            pm.setDrivenKeyframe('%s'%AttrY, currentDriver='%s' % AttrX, dv=eachKey[0], v=eachKey[1])


def connectAttr(attribute_source, attribute_destination, name = 'additiveConnection' ):
    attribute_source = validate_pymel_nodes(attribute_source)
    attribute_destination = validate_pymel_nodes(attribute_destination)
    value = pm.listConnections(attribute_destination, destination = False, plugs=True, skipConversionNodes = True)
    if value:
        print value[0].node()
        if pm.objectType(value[0].node()) == 'plusMinusAverage':
            plusMinus = value[0].node()
            if attribute_source.get(type=True) in ['float','doubleLinear', 'doubleAngle']:
                attribute_source >> plusMinus.input1D[len(plusMinus.input1D.elements())]
            #elif attribute_source.get(type=True) in [vector]:
            #    print 'connecting vector'
            elif attribute_source.get(type=True) in ['double3']:
                attribute_source >> plusMinus.input3D[len(plusMinus.input3D.elements()) % 3]
            else:

                print 'could not add data type: %s' % attribute_source.get(type=True)
        else:
            if attribute_source.get(type=True) in ['float', 'doubleLinear', 'doubleAngle']:
                plusMinus = pm.shadingNode("plusMinusAverage", asUtility=True, name="additiveConnection")
                value[0] // attribute_destination
                value[0] >> plusMinus.input1D[0]
                attribute_source >> plusMinus.input1D[1]
                plusMinus.output1D >> attribute_destination

            elif attribute_source.get(type=True) in ['double3']:
                plusMinus = pm.shadingNode("plusMinusAverage", asUtility=True, name="additiveConnection")
                value[0] // attribute_destination
                value[0] >> plusMinus.input3D[0]
                attribute_source >> plusMinus.input3D[1]
                plusMinus.output3D >> attribute_destination
            else:
                print 'could not add data type: %s' % attribute_source.get(type=True)
    else:
        pm.connectAttr(attribute_source, attribute_destination)

def validate_pymel_nodes(nodes):
    converted_to_list = False
    if type(nodes) not in [list, tuple]:
        nodes = [nodes]
        converted_to_list = True
    return_list = []
    for each in nodes:
        if pm.general.PyNode in inspect.getmro(type(each)):
            return_list.append(each)
        else:
            try:
                return_list += pm.ls(each)
            except:
                raise("Error, can't convert %s to PyNode" % each)

    if converted_to_list == True:
        try:
            return return_list[0]
        except:
            print 'object/s do not exist::%s' % nodes
            raise()
    else:
        return return_list

def RMAlign(obj1, obj2, flag):
    obj1 = validate_pymel_nodes(obj1)
    obj2 = validate_pymel_nodes(obj2)
    if flag == 1 or flag == 3:
        Obj1position = pm.xform(obj1, q=True, ws=True, rp=True)
        pm.xform(obj2, ws=True, t=Obj1position)
    if flag == 2 or flag == 3:
        rotateOrderObj1 = pm.xform(obj1, q=True, rotateOrder=True)
        rotateOrderObj2 = pm.xform(obj2, q=True, rotateOrder=True)
        if rotateOrderObj1 != rotateOrderObj2:
            Null = pm.group(em=True)
            pm.xform(Null, rotateOrder=rotateOrderObj1)
            Obj1rotacion = pm.xform(obj1, q=True, ws=True, ro=True)
            pm.xform(Null, ws=True, ro=Obj1rotacion)
            pm.xform(Null, p=True, rotateOrder=rotateOrderObj2)
            Obj1rotacion = pm.xform(Null, q=1, ws=1, ro=True)
            pm.xform(obj2, ws=True, ro=Obj1rotacion)
            #print "Warning : Obj Rotation Order Mismatch on obj "
            #print  (obj2 + " Aligning to " + obj1 + "\n")
            pm.delete(Null)
        else:
            Obj1rotacion = pm.xform(obj1, q=True, ws=True, ro=True)
            pm.xform(obj2, ws=True, ro=Obj1rotacion)


def RMPointDistance(Point01, Point02):
    Position01, Position02 = pm.xform(Point01, q=True, ws=True, rp=True), pm.xform(Point02, q=True, ws=True,
                                                                                   rp=True)
    Vector01, Vector02 = om.MVector(Position01), om.MVector(Position02)
    ResultVector = Vector01 - Vector02
    return om.MVector(ResultVector).length()


def RMCreateNLocatorsBetweenObjects(Obj01, Obj02, NumberOfPoints, name="locator", align="FirstObj"):
    '''Valid Values in align are FirstObj, SecondObject, and World'''
    locatorList = []
    Position01, Position02 = pm.xform(Obj01, q=True, ws=True, rp=True), pm.xform(Obj02, q=True, ws=True, rp=True)
    Vector01, Vector02 = om.MVector(Position01), om.MVector(Position02)
    ResultVector = Vector02 - Vector01
    Distance = om.MVector(ResultVector).length()
    DeltaVector = (Distance / (NumberOfPoints + 1)) * ResultVector.normal()
    for index in range(0, NumberOfPoints):
        locatorList.append(pm.spaceLocator(name=name))
        Obj1position = Vector01 + DeltaVector * (index + 1)
        pm.xform(locatorList[index], ws=True, t=Obj1position)
        if align == "FirstObj":
            RMAlign(Obj01, locatorList[index], 2)
        elif align == "SecondObject":
            RMAlign(Obj02, locatorList[index], 2)
    return locatorList

def RMConnectWithLimits(AttrX, AttrY, keys):
    for eachKey in keys:
        pm.setDrivenKeyframe(AttrY, currentDriver=AttrX, dv=eachKey[0], v=eachKey[1])

def RMCustomPickWalk(Obj, Class, Depth, Direction="down"):
    '''Valid Values of Direction ar up and down'''
    Obj = validate_pymel_nodes(Obj)
    if Direction == "down":
        childs = pm.listRelatives(Obj, children=True, type=Class)
    else:
        childs = pm.listRelatives(Obj, parent=True, type=Class)
    returnValue = [Obj]
    if childs:
        if not (Depth == 0 or len(childs) == 0):
            for eachChildren in childs:
                if pm.nodeType(eachChildren) == Class:
                    returnValue.extend(RMCustomPickWalk(eachChildren, Class, Depth - 1, Direction=Direction))
    return returnValue


def FindInHieararchy(Obj, GrandSon):
    returnArray = [Obj]
    if Obj == GrandSon:
        return returnArray
    allDescendents = pm.listRelatives(Obj, allDescendents=True)
    if allDescendents:
        if GrandSon in allDescendents:
            Children = pm.listRelatives(Obj, children=True)
            if Children:
                for eachChildren in Children:
                    Family = FindInHieararchy(eachChildren, GrandSon)
                    returnArray.extend(Family)
                return returnArray
    return []


def RMCreateGroupOnObj(Obj, Type="inserted", NameConv = None):
    Obj = validate_pymel_nodes(Obj)
    '''
    "world","child","parent","inserted"
    '''
    if not NameConv:
        NameConv = RMNameConvention.RMNameConvention()

    Group = pm.group(empty=True)

    if NameConv.is_name_in_format(Obj):
        Group = NameConv.rename_based_on_base_name(Obj, Group, objectType="transform")
    else:
        ValidNameList = Obj.split("_")
        ValidName = ""
        for eachToken in ValidNameList:
            ValidName += eachToken
        NewName = NameConv.set_name_in_format(name = NameConv.add_to_numbered_string(ValidName, "Group"), objectType= "transform")
        Group = pm.rename(Group, NewName)

    RMAlign(Obj, Group, 3)

    Parent = pm.listRelatives(Obj, parent=True)
    if not (Type == "world"):
        if Type == "inserted":
            if Parent:
                RMInsertInHierarchy(Obj, Group)
            else:
                pm.parent(Obj, Group)
        elif Type == "parent":
            pm.parent(Obj, Group)
        elif Type == "child":
            pm.parent(Group, Obj)

    return Group


def RMLenghtOfBone(Joint):
    children = pm.listRelatives(Joint, children=True)
    if children:
        if (len(children) > 0 and pm.objectType(children[0]) != "locator"):
            return pm.getAttr(children[0] + ".translateX")
        else:
            return RMJointSize(Joint)
    else:
        return RMJointSize(Joint)


def RMJointSize(Joint):
    if pm.objectType(Joint) == "joint":
        radius = pm.getAttr(Joint + ".radius")
        return (radius * 2)
    else:
        return 1.0


def RMInsertInHierarchy(Obj, InsertObj, InsertType="Parent"):
    Obj = validate_pymel_nodes(Obj)
    InsertObj = validate_pymel_nodes(InsertObj)
    if InsertType == "Parent":
        Parent = Obj.getParent()
        #pm.listRelatives(Obj, parent=True)
        if Parent:
            pm.parent(InsertObj, Parent)
        pm.parent(Obj, InsertObj)
    else:
        children = RMRemoveChildren(Obj)
        Parent = Obj.getParent()
        #Parent = pm.listRelatives(Obj, parent=True)
        pm.parent(InsertObj, Obj)
        pm.parent(children, InsertObj)


def RMRemoveChildren(Node):
    Children = pm.listRelatives(Node, children=True)
    returnArray = []
    for eachChildren in Children:
        if pm.objectType(eachChildren) != "mesh" and pm.objectType(eachChildren) != "nurbsCurve":
            pm.parent(eachChildren, world=True)
            returnArray.append(eachChildren)
    return returnArray


def RMParentArray(Parent, Array):
    for objects in Array:
        pm.parent(objects, Parent)


def RMLockAndHideAttributes(Obj, BitString, LHType="LH"):
    ObjArray = []
    if type(Obj) == list:
        ObjArray = Obj
    else:
        ObjArray = [Obj]
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
                    pm.setAttr('%s%s' % (eachObj, parameter), k=False, l=True)
                elif BitString[InfoDic[parameter]] == "1":
                    pm.setAttr('%s%s' % (eachObj, parameter), k=True, l=False)
                elif BitString[InfoDic[parameter]] == "L":
                    pm.setAttr('%s%s' % (eachObj, parameter), l=False)
                elif BitString[InfoDic[parameter]] == "l":
                    pm.setAttr('%s%s' % (eachObj, parameter), l=True)
                elif BitString[InfoDic[parameter]] == "H":
                    pm.setAttr('%s%s' % (eachObj, parameter), k=True)
                elif BitString[InfoDic[parameter]] == "h":
                    pm.setAttr('%s%s' % (eachObj, parameter), k=False)
                else:
                    pass
    else:
        print "error in LockAndHideAttr Not valid Len on BitString"
        return False
    return True


def RMLinkHerarchyRotation(jntStart, jntEnd, Ctrl, X=True, Y=True, Z=True):
    children = pm.listRelatives(jntStart, children=True)
    if (jntStart == jntEnd):
        if X:
            pm.connectAttr(Ctrl + ".rotateX", jntStart + ".rotateX")
        if Y:
            pm.connectAttr(Ctrl + ".rotateY", jntStart + ".rotateY")
        if Z:
            pm.connectAttr(Ctrl + ".rotateZ", jntStart + ".rotateZ")
        return True
    else:
        for joints in children:
            if RMIsInHierarchy(joints, jntEnd):
                if X:
                    pm.connectAttr(Ctrl + ".rotateX", jntStart + ".rotateX")
                if Y:
                    pm.connectAttr(Ctrl + ".rotateY", jntStart + ".rotateY")
                if Z:
                    pm.connectAttr(Ctrl + ".rotateZ", jntStart + ".rotateZ")
                return RMLinkHerarchyRotation(joints, jntEnd, Ctrl, X, Y, Z)
            else:
                return False


def RMIsInHierarchy(Obj1, Obj2):
    children = pm.listRelatives(Obj1, children=True)
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
    if type(Object) != list:
        ObjList = [Object]
    else:
        ObjList = Object
    for eachObject in ObjList:
        pm.setAttr("%s.rotateOrder" % eachObject, rotateOrderDic[rotationOrder])

def create_bones_at_points(PointArray, NameConv=None, ZAxisOrientation="Y"):
    PointArray = validate_pymel_nodes(PointArray)
    if not NameConv:
        NameConv = RMNameConvention.RMNameConvention()

    jointArray = []

    Obj1Position = pm.xform(PointArray[0], q=True, rp=True, ws=True)
    Obj2Position = pm.xform(PointArray[1], q=True, rp=True, ws=True)

    V1, V2 = om.MVector(Obj1Position), om.MVector(Obj2Position)

    initVector = V1 - V2

    firstJntAngle = V1.angle(om.MVector([0, 1, 0]))

    Angle = firstJntAngle

    ParentJoint = RMCreateGroupOnObj(str(PointArray[0]), Type="world")

    for index in range(0, len(PointArray)):

        pm.select(cl=True)

        newJoint = pm.joint(p=[0, 0, 0], name="joint")
        jointArray.append(NameConv.rename_based_on_base_name(str(PointArray[index]), str(newJoint)))

        if index == 0:
            pm.parent(jointArray[0], ParentJoint)

        RMAlign(PointArray[index], jointArray[index], 3)
        pm.makeIdentity(jointArray[index], apply=True, t=1, r=1, s=0)

        if (index > 0):
            if index == 1:
                AxisOrientJoint = pm.joint()
                pm.parent(AxisOrientJoint, ParentJoint)
                RMAlign(PointArray[0], AxisOrientJoint, 3)
                pm.makeIdentity(AxisOrientJoint, apply=True, t=1, r=1, s=0)

                if ZAxisOrientation in "Yy":
                    pm.xform(AxisOrientJoint, translation=[0, -1, 0], objectSpace=True)

                elif ZAxisOrientation in "Zz":
                    pm.xform(AxisOrientJoint, translation=[0, 0, -1], objectSpace=True)

                pm.parent(jointArray[0], AxisOrientJoint)
                pm.parent(jointArray[index], jointArray[index - 1])
                pm.joint(jointArray[index - 1], edit=True, orientJoint="xzy")

                pm.parent(jointArray[index - 1], world=True)
                pm.delete(AxisOrientJoint)
                RMAlign(jointArray[index - 1], ParentJoint, 3)
                pm.parent(jointArray[index - 1], ParentJoint)

            else:
                pm.parent(jointArray[index], jointArray[index - 1])
                pm.joint(jointArray[index - 1], edit=True, orientJoint="xzy")
            # , sao="yup" )

            if index >= 2:
                parentOrient = pm.joint(jointArray[index - 1], q=True, orientation=True)
                pm.joint(jointArray[index - 1], e=True, orientation=[0, parentOrient[1], parentOrient[2]])
                # if parentOrient[0] > 90 :
                # pm.joint (jointArray[index-1], e = True, orientation = [parentOrient[0]-180, parentOrient[1], parentOrient[2]])
                # else:
                # if parentOrient[0] < -90:
                # pm.joint (jointArray[index-1], e = True, orientation = [parentOrient[0]+180, parentOrient[1], parentOrient[2]])

        if index == len(PointArray) - 1:
            RMAlign(jointArray[index - 1], jointArray[index], 2)
            pm.makeIdentity(jointArray[index], apply=True, t=0, r=1, s=0)

    return ParentJoint, jointArray


def RMCreateBonesAtPoints(PointArray, NameConv=None, ZAxisOrientation="Y"):
    if not NameConv:
        NameConv = RMNameConvention.RMNameConvention()

    jointArray = []

    Obj1Position = pm.xform(PointArray[0], q=True, rp=True, ws=True)
    Obj2Position = pm.xform(PointArray[1], q=True, rp=True, ws=True)

    V1, V2 = om.MVector(Obj1Position), om.MVector(Obj2Position)

    initVector = V1 - V2

    firstJntAngle = V1.angle(om.MVector([0, 1, 0]))

    Angle = firstJntAngle

    ParentJoint = RMCreateGroupOnObj(PointArray[0], Type="world")

    for index in range(0, len(PointArray)):

        pm.select(cl=True)

        newJoint = pm.joint(p=[0, 0, 0], name="joint")
        NameConv.rename_based_on_base_name(PointArray[index], newJoint)
        jointArray.append(newJoint)

        if index == 0:
            pm.parent(jointArray[0], ParentJoint)

        RMAlign(PointArray[index], jointArray[index], 3)
        pm.makeIdentity(jointArray[index], apply=True, t=1, r=1, s=0)

        if (index > 0):
            if index == 1:
                AxisOrientJoint = pm.joint()
                pm.parent(AxisOrientJoint, ParentJoint)
                RMAlign(PointArray[0], AxisOrientJoint, 3)
                pm.makeIdentity(AxisOrientJoint, apply=True, t=1, r=1, s=0)

                if ZAxisOrientation in "Yy":
                    pm.xform(AxisOrientJoint, translation=[0, -1, 0], objectSpace=True)

                elif ZAxisOrientation in "Zz":
                    pm.xform(AxisOrientJoint, translation=[0, 0, -1], objectSpace=True)

                pm.parent(jointArray[0], AxisOrientJoint)
                pm.parent(jointArray[index], jointArray[index - 1])
                pm.joint(jointArray[index - 1], edit=True, orientJoint="xzy")

                pm.parent(jointArray[index - 1], world=True)
                pm.delete(AxisOrientJoint)
                RMAlign(jointArray[index - 1], ParentJoint, 3)
                pm.parent(jointArray[index - 1], ParentJoint)

            else:
                pm.parent(jointArray[index], jointArray[index - 1])
                pm.joint(jointArray[index - 1], edit=True, orientJoint="xzy")
            # , sao="yup" )

            if index >= 2:
                parentOrient = pm.joint(jointArray[index - 1], q=True, orientation=True)
                pm.joint(jointArray[index - 1], e=True, orientation=[0, parentOrient[1], parentOrient[2]])
                # if parentOrient[0] > 90 :
                # pm.joint (jointArray[index-1], e = True, orientation = [parentOrient[0]-180, parentOrient[1], parentOrient[2]])
                # else:
                # if parentOrient[0] < -90:
                # pm.joint (jointArray[index-1], e = True, orientation = [parentOrient[0]+180, parentOrient[1], parentOrient[2]])

        if index == len(PointArray) - 1:
            RMAlign(jointArray[index - 1], jointArray[index], 2)
            pm.makeIdentity(jointArray[index], apply=True, t=0, r=1, s=0)

    return ParentJoint, jointArray


def RMCreateLineBetwenPoints(Point1, Point2, NameConv=None):
    if not NameConv:
        NameConv = RMNameConvention.RMNameConvention()

    Curve = pm.curve(degree=1, p=[[0, 0, 0], [1, 0, 0]], name="curveLineBetweenPnts")

    Curve = NameConv.rename_based_on_base_name(Point1, Curve, name=Curve)

    NumCVs = pm.getAttr(Curve + ".controlPoints", size=True)

    Cluster1, Cluster1Handle = pm.cluster(Curve + ".cv[0]", relative=True, name="clusterLineBetweenPnts")
    Cluster1 = NameConv.rename_based_on_base_name(Point1, Cluster1, name= Cluster1)
    Cluster1Handle = NameConv.rename_based_on_base_name(Point1, Cluster1Handle, name= Cluster1Handle)

    Cluster2, Cluster2Handle = pm.cluster(Curve + ".cv[1]", relative=True, name="clusterLineBetweenPnts")
    Cluster2 = NameConv.rename_based_on_base_name(Point2, Cluster2, name= Cluster2)
    Cluster2Handle = NameConv.rename_based_on_base_name(Point2, Cluster2Handle, name= Cluster2Handle)

    pm.setAttr(Curve + ".overrideEnabled", 1)
    pm.setAttr(Curve + ".overrideDisplayType", 1)

    RMAlign(Point1, Cluster1Handle, 1)
    RMAlign(Point2, Cluster1Handle, 1)

    PointConstraint1 = pm.pointConstraint(Point1, Cluster1Handle, name="PointConstraintLineBetweenPnts")
    PointConstraint1 = NameConv.rename_based_on_base_name(Point1, PointConstraint1, name= PointConstraint1)
    PointConstraint2 = pm.pointConstraint(Point2, Cluster2Handle, name="PointConstraintLineBetweenPnts")
    PointConstraint2 = NameConv.rename_based_on_base_name(Point2, PointConstraint2, name= PointConstraint2)

    DataGroup = pm.group(em=True, name="DataLineBetweenPnts")
    DataGroup = NameConv.rename_based_on_base_name(Point1, DataGroup, name= DataGroup)
    pm.parent(Cluster1Handle, DataGroup)
    pm.parent(Cluster2Handle, DataGroup)
    pm.parent(Curve, DataGroup)
    return DataGroup, Curve


def RMCreateClustersOnCurve(curve, NameConv=None):
    if not NameConv:
        NameConv = RMNameConvention.RMNameConvention()

    degree = pm.getAttr(curve + ".degree")
    spans = pm.getAttr(curve + ".spans")
    form = pm.getAttr(curve + ".form")
    print ("degree:%s", degree)
    print ("spans:%s", spans)
    print ("form:%s", form)
    #   Form (open = 0, closed = 1, periodic = 2)
    clusterList = []
    print form
    if form == 0 or form == 1:
        print "Open Line"
        for i in range(0, (degree + spans)):
            Cluster2Handle, cluster = pm.cluster(curve + ".cv[" + str(i) + "]", name="ClusterOnCurve")
            if NameConv.is_name_in_format(curve):
                cluster = NameConv.rename_based_on_base_name(curve, cluster, name=cluster)
                # Cluster2Handle = NameConv.RMRenameBasedOnBaseName(curve, Cluster2Handle, NewName = Cluster2Handle)
            else:
                cluster = NameConv.rename_name_in_format(cluster)
                # Cluster2Handle = NameConv.RMRenameNameInFormat(Cluster2Handle)
            clusterList.append(cluster)
            pm.setAttr(cluster + ".visibility", 0)
            ##pm.cluster(cluster,edit=True,geometry = curve + ".["+str(i)+"]")
    if form == 2:
        print "periodic Line"
        for i in range(0, spans):
            Cluster2Handle, cluster = pm.cluster(curve + ".cv[" + str(i) + "]", name="ClusterOnCurve")
            print cluster
            if NameConv.is_name_in_format(curve):
                cluster = NameConv.rename_based_on_base_name(curve, cluster, name= cluster)
                # Cluster2Handle = NameConv.RMRenameBasedOnBaseName(curve, Cluster2Handle, NewName = Cluster2Handle)
            else:
                cluster = NameConv.rename_name_in_format(cluster)
                # Cluster2Handle = NameConv.RMRenameNameInFormat(Cluster2Handle)
            clusterList.append(cluster)
            pm.setAttr(cluster + ".visibility", 0)
            # pm.cluster(cluster,edit=True,geometry = curve + ".["+str(i)+"]")
    return clusterList

def objectsInListExists(objectsLists,verbose = True ):
    listString = ''
    exists = True
    for eachObject in objectsLists:
        existEachObjec = pm.objExists(eachObject)
        if not existEachObjec:
            listString = '%s %s'%(listString, eachObject)
        exists = exists and existEachObjec
    if verbose and not exists:
        print 'the folowing objects were not found: %s'%listString
    return exists

class boundingBoxInfo(object):
    def __init__(self, scene_object):
        self.xmin = None
        self.ymin = None
        self.zmin = None
        self.xmax = None
        self.ymax = None
        self.zmax = None

        if scene_object.__class__ == list:
            for eachObject in scene_object:
                Values = pm.xform(eachObject, q=True, bb=True)
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

        else:
            if scene_object.__class__ in [str, unicode]:
                scene_object = validate_pymel_nodes(scene_object)
            elif pm.general.PyNode in inspect.getmro(type(scene_object)):
                pass
            else:
                raise AttributeError

            self.BaseObject = scene_object
            Values = pm.xform(scene_object, q=True, bb=True)
            self.position = pm.xform(scene_object, q=True, rp=True, worldSpace=True)
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

        self.position = pm.xform(self.BaseObject, q=True, rp=True, worldSpace=True)
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

    def create_bones_at_points(self, PointArray, ZAxisOrientation = "Y"):
        PointArray = validate_pymel_nodes(PointArray)
        jointArray = []
        Obj1Position = pm.xform(PointArray[0], q=True, rp=True, ws=True)
        Obj2Position = pm.xform(PointArray[1], q=True, rp=True, ws=True)

        V1, V2 = om.MVector(Obj1Position), om.MVector(Obj2Position)

        initVector = V1 - V2

        firstJntAngle = V1.angle(om.MVector([0, 1, 0]))

        Angle = firstJntAngle

        ParentJoint = self.RMCreateGroupOnObj(PointArray[0], Type="world")

        for index in range(0, len(PointArray)):

            pm.select(cl=True)

            newJoint = pm.joint(p=[0, 0, 0], name="joint")
            self.NameConv.rename_based_on_base_name(PointArray[index], newJoint, objectType='joint')
            jointArray.append(newJoint)

            if index == 0:
                pm.parent(jointArray[0], ParentJoint)

            RMAlign(PointArray[index], jointArray[index], 3)
            pm.makeIdentity(jointArray[index], apply=True, t=1, r=1, s=0)

            if (index > 0):
                if index == 1:
                    AxisOrientJoint = pm.joint()
                    pm.parent(AxisOrientJoint, ParentJoint)
                    RMAlign(PointArray[0], AxisOrientJoint, 3)
                    pm.makeIdentity(AxisOrientJoint, apply=True, t=1, r=1, s=0)

                    if ZAxisOrientation in "Yy":
                        pm.xform(AxisOrientJoint, translation=[0, -1, 0], objectSpace=True)

                    elif ZAxisOrientation in "Zz":
                        pm.xform(AxisOrientJoint, translation=[0, 0, -1], objectSpace=True)

                    pm.parent(jointArray[0], AxisOrientJoint)
                    pm.parent(jointArray[index], jointArray[index - 1])
                    pm.joint(jointArray[index - 1], edit=True, orientJoint="xzy")

                    pm.parent(jointArray[index - 1], world=True)
                    pm.delete(AxisOrientJoint)
                    RMAlign(jointArray[index - 1], ParentJoint, 3)
                    pm.parent(jointArray[index - 1], ParentJoint)

                else:
                    pm.parent(jointArray[index], jointArray[index - 1])
                    pm.joint(jointArray[index - 1], edit=True, orientJoint="xzy")
                # , sao="yup" )

                if index >= 2:
                    parentOrient = pm.joint(jointArray[index - 1], q=True, orientation=True)
                    pm.joint(jointArray[index - 1], e=True, orientation=[0, parentOrient[1], parentOrient[2]])
                    # if parentOrient[0] > 90 :
                    # pm.joint (jointArray[index-1], e = True, orientation = [parentOrient[0]-180, parentOrient[1], parentOrient[2]])
                    # else:
                    # if parentOrient[0] < -90:
                    # pm.joint (jointArray[index-1], e = True, orientation = [parentOrient[0]+180, parentOrient[1], parentOrient[2]])

            if index == len(PointArray) - 1:
                RMAlign(jointArray[index - 1], jointArray[index], 2)
                pm.makeIdentity(jointArray[index], apply=True, t=0, r=1, s=0)

        return ParentJoint, jointArray


    def RMCreateBonesAtPoints(self, PointArray, ZAxisOrientation = "Y"):
        PointArray = validate_pymel_nodes(PointArray)
        jointArray = []

        Obj1Position = pm.xform(PointArray[0], q=True, rp=True, ws=True)
        Obj2Position = pm.xform(PointArray[1], q=True, rp=True, ws=True)

        V1, V2 = om.MVector(Obj1Position), om.MVector(Obj2Position)

        initVector = V1 - V2

        firstJntAngle = V1.angle(om.MVector([0, 1, 0]))

        Angle = firstJntAngle

        ParentJoint = self.RMCreateGroupOnObj(PointArray[0], Type="world")

        for index in range(0, len(PointArray)):

            pm.select(cl=True)

            newJoint = pm.joint(p=[0, 0, 0], name="joint")
            self.NameConv.rename_based_on_base_name(PointArray[index], newJoint, objectType='joint')
            jointArray.append(newJoint)

            if index == 0:
                pm.parent(jointArray[0], ParentJoint)

            RMAlign(PointArray[index], jointArray[index], 3)
            pm.makeIdentity(jointArray[index], apply=True, t=1, r=1, s=0)

            if (index > 0):
                if index == 1:
                    AxisOrientJoint = pm.joint()
                    pm.parent(AxisOrientJoint, ParentJoint)
                    RMAlign(PointArray[0], AxisOrientJoint, 3)
                    pm.makeIdentity(AxisOrientJoint, apply=True, t=1, r=1, s=0)

                    if ZAxisOrientation in "Yy":
                        pm.xform(AxisOrientJoint, translation=[0, -1, 0], objectSpace=True)

                    elif ZAxisOrientation in "Zz":
                        pm.xform(AxisOrientJoint, translation=[0, 0, -1], objectSpace=True)

                    pm.parent(jointArray[0], AxisOrientJoint)
                    pm.parent(jointArray[index], jointArray[index - 1])
                    pm.joint(jointArray[index - 1], edit=True, orientJoint="xzy")

                    pm.parent(jointArray[index - 1], world=True)
                    pm.delete(AxisOrientJoint)
                    RMAlign(jointArray[index - 1], ParentJoint, 3)
                    pm.parent(jointArray[index - 1], ParentJoint)

                else:
                    pm.parent(jointArray[index], jointArray[index - 1])
                    pm.joint(jointArray[index - 1], edit=True, orientJoint="xzy")
                # , sao="yup" )

                if index >= 2:
                    parentOrient = pm.joint(jointArray[index - 1], q=True, orientation=True)
                    pm.joint(jointArray[index - 1], e=True, orientation=[0, parentOrient[1], parentOrient[2]])
                    # if parentOrient[0] > 90 :
                    # pm.joint (jointArray[index-1], e = True, orientation = [parentOrient[0]-180, parentOrient[1], parentOrient[2]])
                    # else:
                    # if parentOrient[0] < -90:
                    # pm.joint (jointArray[index-1], e = True, orientation = [parentOrient[0]+180, parentOrient[1], parentOrient[2]])

            if index == len(PointArray) - 1:
                RMAlign(jointArray[index - 1], jointArray[index], 2)
                pm.makeIdentity(jointArray[index], apply=True, t=0, r=1, s=0)

        return ParentJoint, jointArray

    def RMCreateGroupOnObj(self, Obj, Type = "inserted", name=None):
        Obj = validate_pymel_nodes(Obj)
        '''
        "world","child","parent","inserted","sibling"
        '''
        Group = pm.group(empty=True)

        if self.NameConv.is_name_in_format(Obj):
            self.NameConv.rename_based_on_base_name(Obj, Group)
            if name is not None:
                self.NameConv.rename_set_from_name(Group, name, 'name')
        else:
            if name is None:
                ValidNameList = Obj.split("_")
                ValidName = ""
                for eachToken in ValidNameList:
                    ValidName += eachToken
            else:
                ValidName = name
            NewName = self.NameConv.set_name_in_format(name= ValidName , objectType= "transform")
            pm.rename(Group, NewName)

        RMAlign(Obj, Group, 3)

        Parent = pm.listRelatives(Obj, parent=True)
        if not (Type == "world"):
            if Type == "inserted":
                if Parent:
                    RMInsertInHierarchy(Obj, Group)
                else:
                    pm.parent(Obj, Group)
            elif Type == "parent":
                pm.parent(Obj, Group)
            elif Type == "child":
                pm.parent(Group, Obj)
            elif Type == "sibling":
                pm.parent(Group, Parent)

        return Group

    def createLineAtPoints(self, pointList, periodic=False, degree=3):

        listofPoints = [pm.xform('%s' % eachPointList, q=True, ws=True, rp=True) for eachPointList in pointList]
        if not periodic:
            Curve = pm.curve(degree=degree, p=listofPoints, name='line')
        else:
            fullListPoint = listofPoints + listofPoints[:3]
            numElements = len(fullListPoint)
            knotVector = range(-degree + 1, 0) + range(numElements)
            Curve = pm.curve(degree=degree, p=fullListPoint, periodic=periodic, name='line', k=knotVector)
        self.NameConv.rename_based_on_base_name(pointList[0], Curve, name=Curve)
        return Curve

    def RMCreateLineBetwenPoints(self, Point1, Point2):
        Curve = pm.curve(degree=1, p=[[0, 0, 0], [1, 0, 0]], name="curveLineBetweenPnts")

        self.NameConv.rename_based_on_base_name(Point1, Curve, name=Curve)

        NumCVs = pm.getAttr(Curve + ".controlPoints", size=True)

        Cluster1, Cluster1Handle = pm.cluster(Curve + ".cv[0]", relative=True, name="clusterLineBetweenPnts")
        self.NameConv.rename_based_on_base_name(Point1, Cluster1, name=Cluster1)
        self.NameConv.rename_based_on_base_name(Point1, Cluster1Handle, name= Cluster1Handle)

        Cluster2, Cluster2Handle = pm.cluster(Curve + ".cv[1]", relative=True, name="clusterLineBetweenPnts")
        self.NameConv.rename_based_on_base_name(Point2, Cluster2, name=Cluster2)
        self.NameConv.rename_based_on_base_name(Point2, Cluster2Handle, name=Cluster2Handle)

        pm.setAttr(Curve + ".overrideEnabled", 1)
        pm.setAttr(Curve + ".overrideDisplayType", 1)

        RMAlign(Point1, Cluster1Handle, 1)
        RMAlign(Point2, Cluster1Handle, 1)

        PointConstraint1 = pm.pointConstraint(Point1, Cluster1Handle, name="PointConstraintLineBetweenPnts")
        self.NameConv.rename_based_on_base_name(Point1, PointConstraint1, name=PointConstraint1)
        PointConstraint2 = pm.pointConstraint(Point2, Cluster2Handle, name="PointConstraintLineBetweenPnts")
        self.NameConv.rename_based_on_base_name(Point2, PointConstraint2, name=PointConstraint2)

        DataGroup = pm.group(em=True, name="DataLineBetweenPnts")
        self.NameConv.rename_based_on_base_name(Point1, DataGroup, name= DataGroup)
        pm.parent(Cluster1Handle, DataGroup)
        pm.parent(Cluster2Handle, DataGroup)
        pm.parent(Curve, DataGroup)
        return DataGroup, Curve

    def RMCreateClustersOnCurve(self, curve):
        degree = pm.getAttr("%s.degree" % curve)
        spans = pm.getAttr("%s.spans" % curve)
        form = pm.getAttr("%s.form" % curve)
        #   Form (open = 0, closed = 1, periodic = 2)
        clusterList = []
        if form == 0 or form == 1:
            for i in range(0, (degree + spans)):
                Cluster2Handle, cluster = pm.cluster(curve + ".cv[" + str(i) + "]", name="ClusterOnCurve")
                if self.NameConv.is_name_in_format(curve):
                    self.NameConv.rename_based_on_base_name(curve, cluster, name=cluster)
                    # Cluster2Handle = self.NameConv.RMRenameBasedOnBaseName(curve, Cluster2Handle, NewName = Cluster2Handle)
                else:
                    self.NameConv.rename_name_in_format(cluster)
                    # Cluster2Handle = self.NameConv.RMRenameNameInFormat(Cluster2Handle)
                clusterList.append(cluster)
                pm.setAttr(cluster + ".visibility", 0)
                ##pm.cluster(cluster,edit=True,geometry = curve + ".["+str(i)+"]")
        if form == 2:
            #print "periodic Line"
            for i in range(0, spans):
                Cluster2Handle, cluster = pm.cluster(curve + ".cv[" + str(i) + "]", name="ClusterOnCurve")
                print cluster
                if self.NameConv.is_name_in_format(curve):
                    self.NameConv.rename_based_on_base_name(curve, cluster, name=cluster)
                    # Cluster2Handle = self.NameConv.RMRenameBasedOnBaseName(curve, Cluster2Handle, NewName = Cluster2Handle)
                else:
                    self.NameConv.rename_name_in_format(cluster)
                    # Cluster2Handle = self.NameConv.RMRenameNameInFormat(Cluster2Handle)
                clusterList.append(cluster)
                pm.setAttr(cluster + ".visibility", 0)
                # pm.cluster(cluster,edit=True,geometry = curve + ".["+str(i)+"]")
        return clusterList

    def RMCreateNLocatorsBetweenObjects(self, Obj01, Obj02, numberOfPoints, name="locator", align="FirstObj"):
        '''Valid Values in align are FirstObj, SecondObject, and World'''
        locatorList = []
        Position01, Position02 = pm.xform(Obj01, q=True, ws=True, rp=True), pm.xform(Obj02, q=True, ws=True,
                                                                                         rp=True)
        Vector01, Vector02 = om.MVector(Position01), om.MVector(Position02)
        ResultVector = Vector02 - Vector01
        Distance = om.MVector(ResultVector).length()
        DeltaVector = (Distance / (numberOfPoints + 1)) * ResultVector.normal()
        for index in range(0, numberOfPoints):
            newLocator = pm.spaceLocator(name=name)
            self.NameConv.rename_based_on_base_name(Obj01, newLocator)
            locatorList.append(newLocator)
            # locatorList.append(self.NameConv.RMRenameNameInFormat(newLocator, {}))
            Obj1position = Vector01 + DeltaVector * (index + 1)
            pm.xform(locatorList[index], ws=True, t=Obj1position)
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
        Position01, Position02 = pm.xform(Obj01, q=True, ws=True, rp=True), pm.xform(Obj02, q=True, ws=True,
                                                                                         rp=True)
        Vector01, Vector02 = om.MVector(Position01), om.MVector(Position02)
        ResultVector = Vector02 - Vector01
        Distance = om.MVector(ResultVector).length()
        DeltaVector = (
        (((Distance - initialSize) - (numberOfPoints * initialSize)) * 2) / (numberOfPoints * (numberOfPoints + 1)))
        TempValue = 0
        # DeltaVector = (Distance/(numberOfPoints+1))*ResultVector.normal()
        for index in range(0, numberOfPoints):
            newLocator = pm.spaceLocator(name=name)
            locatorList.append(self.NameConv.rename_name_in_format(newLocator))
            TempValue = TempValue + initialSize + (DeltaVector) * (numberOfPoints - index)
            Obj1position = Vector01 + TempValue * ResultVector.normal()
            print ("vectorValue=%s" % Obj1position.length())
            pm.xform(locatorList[index], ws=True, t=Obj1position)
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
