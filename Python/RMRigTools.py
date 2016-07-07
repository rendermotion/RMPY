import maya.cmds as cmds
import RMNameConvention
reload (RMNameConvention)
import maya.api.OpenMaya as om
import math


def RMAlign(obj1,obj2,flag):
    if (flag==1 or flag == 3):
        Obj1position =cmds.xform(obj1,q=True,ws=True,rp=True)
        cmds.xform(obj2,ws=True,t=Obj1position)
    if (flag==2 or flag==3):
        rotateOrderObj1=cmds.xform(obj1,q=True,rotateOrder=True)
        rotateOrderObj2=cmds.xform(obj2,q=True,rotateOrder=True)
        if rotateOrderObj1 != rotateOrderObj2:
            Null = cmds.group(em=True)
            cmds.xform(Null,rotateOrder=rotateOrderObj1)
            Obj1rotacion=cmds.xform(obj1,q=True,ws=True,ro=True)
            cmds.xform(Null,ws=True,ro=Obj1rotacion)
            cmds.xform(Null,p=True,rotateOrder=rotateOrderObj2)
            Obj1rotacion=cmds.xform(Null,q=1,ws=1,ro=True)
            cmds.xform(obj2,ws=True,ro=Obj1rotacion)
            print "Warning : Obj Rotation Order Mismatch on obj "
            print  (obj2 + " Aligning to "+ obj1+"\n")
            cmds.delete(Null)
        else:
            Obj1rotacion=cmds.xform(obj1,q=True,ws=True,ro=True)
            cmds.xform(obj2,ws=True,ro=Obj1rotacion)


def connectWithLimits(AttrX,AttrY,keys):
    for eachKey  in keys:
        cmds.setDrivenKeyframe(AttrY, currentDriver = AttrX,dv = eachKey[0],v =eachKey[1])


def RMCustomPickWalk(Obj, Class, Depth):
    childs=cmds.listRelatives(Obj,children=True,type = Class)
    returnValue = [Obj]
    if childs:
        if not (Depth == 0 or len(childs) == 0):
            for eachChildren in childs:
                if cmds.nodeType (eachChildren) == Class:
                    returnValue.extend( RMCustomPickWalk (eachChildren, Class, Depth-1))
    return returnValue



def RMCreateGroupOnObj(Obj,Type="inserted", NameConv = None):
    '''
    "world","child","parent","inserted"
    '''
    if not NameConv:
        NameConv = RMNameConvention.RMNameConvention()

    Group = cmds.group( empty = True)

    if NameConv.RMIsNameInFormat(Obj):

        Group = NameConv.RMRenameBasedOnBaseName (Obj, Group)

    else:
        NewName = NameConv.RMSetNameInFormat(Name = NameConv.RMAddToNumberedString(Obj , "Group"))
        Group = cmds.rename (Group, NewName)

    RMAlign(Obj,Group,3)
    Parent = cmds.listRelatives(Obj,parent=True)

    if not (Type == "world"):
        if Type == "inserted":
            RMInsertInHierarchy(Obj,Group)
        elif Type == "parent":
            cmds.parent(Obj,Group)
        elif Type == "child":
            cmds.parent(Group,Obj)

    return Group

def RMLenghtOfBone(Joint):
    children = cmds.listRelatives(Joint,children=True)
    if(len(children) > 0 and cmds.objectType(children[0]) != "locator"):
        return cmds.getAttr(children[0]+".translateX")
    else:
        return 1.0

def RMInsertInHierarchy(Obj,InsertObj,InsertType="Parent"):
    if InsertType == "Parent":
        Parent = cmds.listRelatives(Obj , parent=True)
        if Parent:
            cmds.parent (InsertObj, Parent)
        cmds.parent (Obj, InsertObj)
    else:
        children = RMRemoveChildren(Obj)
        Parent = cmds.listRelatives (Obj, parent=True)
        cmds.parent (InsertObj , Obj)
        RMParentArray (InsertObj, children)

def RMRemoveChildren(Node):
    Children = cmds.listRelatives(Node,children=True)
    returnArray=[]
    for eachChildren in Children:
        if cmds.objectType(eachChildren) != "mesh" and cmds.objectType(eachChildren) != "nurbsCurve":
            cmds.parent(eachChildren , world = True)
            returnArray.append(eachChildren)
    return returnArray

def RMParentArray (Parent, Array):
    for objects in Array:
        cmds.parent(objects,Parent)

def RMLockAndHideAttributes(ObjArray,BitString):
    InfoDic = {".translateX":0,
                ".translateY":1,
                ".translateZ":2,
                ".rotateX":3,
                ".rotateY":4,
                ".rotateZ":5,
                ".scaleX":6,
                ".scaleY":7,
                ".scaleZ":8,
                ".visibility":9}
    if (len(BitString)==10):
        for eachObj in ObjArray:
            for parameter in InfoDic:
                if BitString[InfoDic[parameter]]==0:
                    cmds.setAttr(eachObj+parameter,k=False,l=True)
                else:
                    cmds.setAttr(eachObj+parameter,k=True,l=False)

def RMLinkHerarchyRotation(jntStart, jntEnd, Ctrl,X=True ,Y=True ,Z=True):
    children = cmds.listRelatives(jntStart,children=True)
    if(jntStart == jntEnd):
        return True
    else:
        for joints in children:
            if RMIsInHierarchy(joints,jntEnd):
                if X:
                    cmds.connectAttr( Ctrl+".rotateX", jntStart+".rotateX")
                if Y:
                    cmds.connectAttr( Ctrl+".rotateY", jntStart+".rotateY")
                if Z:
                    cmds.connectAttr( Ctrl+".rotateZ", jntStart+".rotateZ")
                return RMLinkHerarchyRotation(joints,jntEnd,Ctrl,X,Y,Z)
            else:
                return False

def RMIsInHierarchy(Obj1,Obj2):
    children=cmds.listRelatives(Obj1,children=True)
    if Obj1 == Obj02:
        return True
    else:
        for eachChild in children:
            if RMIsInHierarchy(eachChild,Obj2):
                return True
    return False

def RMCreateBonesAtPoints(PointArray,NameConv = None):
    if not NameConv:
        NameConv = RMNameConvention.RMNameConvention()

    jointArray = []
    Obj1Position = cmds.xform(PointArray[0],q=True, rp=True, ws=True)
    Obj2Position = cmds.xform(PointArray[1],q=True, rp=True, ws=True)

    V1 , V2 = om.MVector(Obj1Position) , om.MVector(Obj2Position)

    initVector = V1 - V2

    firstJntAngle = V1.angle(om.MVector([0,1,0]))

    Angle = firstJntAngle

    ParentJoint = RMCreateGroupOnObj (PointArray[0],Type="world")
    
    for index in range(0,len(PointArray)) :

        #cmds.makeIdentity (PointArray[index], apply=True, t=1, r=0, s=1)
        cmds.select(cl=True)
        
        if (NameConv.RMIsNameInFormat (PointArray[index])):
            
            newJoint = cmds.joint (p = [0,0,0])
            jointArray.append (NameConv.RMRenameBasedOnBaseName (PointArray[index], newJoint))
        else:
            jointArray.append(cmds.joint (p = [0,0,0], name = NameConv.RMSetNameInFormat("joint", "Character", "MD", "jnt", "rig")))

            if index==0:
                cmds.parent (jointArray[0], ParentJoint)
        
        RMAlign (PointArray[index], jointArray[index],3)
        cmds.makeIdentity (jointArray[index], apply=True, t=1, r=1, s=0)

        if (index > 0) :
            cmds.parent (jointArray[index], jointArray[index-1])

            cmds.joint(jointArray[index-1], edit=True, orientJoint="xyz")
            #, sao="yup" )

            if index > 1:
                parentOrient = cmds.joint (jointArray[index-1], q=True, orientation=True)
                if parentOrient[0] > 90 :
                    cmds.joint (jointArray[index-1], e = True, orientation = [parentOrient[0]-180, parentOrient[1], parentOrient[2]])

                else:

                    if parentOrient[0] < -90:

                        cmds.joint (jointArray[index-1], e = True, orientation = [parentOrient[0]+180, parentOrient[1], parentOrient[2]])
        
        if index == len(PointArray)-1:
            RMAlign( jointArray[index-1], jointArray[index],2)
            cmds.makeIdentity (jointArray[index], apply=True, t=0, r=1, s=0)
    print jointArray
    
def RMCreateLineBetwenPoints (Point1, Point2,NameConv = None):
    if not NameConv:
        NameConv = RMNameConvention.RMNameConvention()

    Curve = cmds.curve (degree=1, p=[[0,0,0],[1,0,0]], name = "curveLineBetweenPnts")
    print type(Curve)
    Curve = NameConv.RMRenameNameInFormat(Curve)[0]

    NumCVs = cmds.getAttr (Curve + ".controlPoints" , size = True)
    
    Cluster1, Cluster1Handle = cmds.cluster (Curve+".cv[0]", relative=True, name = "clusterLineBetweenPnts")
    Cluster1, Cluster1Handle = NameConv.RMRenameNameInFormat ([Cluster1,Cluster1Handle])
    Cluster2, Cluster2Handle = cmds.cluster (Curve+".cv[1]", relative=True, name = "clusterLineBetweenPnts")
    Cluster2, Cluster2Handle = NameConv.RMRenameNameInFormat ([Cluster2,Cluster2Handle])

    cmds.setAttr(Curve+".overrideEnabled",1)
    cmds.setAttr(Curve+".overrideDisplayType",1)

    RMAlign (Point1, Cluster1Handle, 1)
    RMAlign (Point2, Cluster1Handle, 1)

    PointConstraint1 = cmds.pointConstraint (Point1, Cluster1Handle, name = "PointConstraintLineBetweenPnts")
    PointConstraint1 = NameConv.RMRenameNameInFormat (PointConstraint1)    
    PointConstraint2 = cmds.pointConstraint (Point2, Cluster2Handle, name = "PointConstraintLineBetweenPnts")
    PointConstraint2 = NameConv.RMRenameNameInFormat (PointConstraint2)    

    DataGroup = cmds.group (em = True,name = "DataLineBetweenPnts")
    DataGroup = NameConv.RMRenameNameInFormat (DataGroup)[0]
    cmds.parent (Cluster1Handle, DataGroup)
    cmds.parent (Cluster2Handle, DataGroup)
    cmds.parent (Curve, DataGroup)
    return DataGroup





