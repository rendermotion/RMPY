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

def RMCreateGroupOnObj(Obj,Type="inserted", NameConv = None):
    '''
    "world","child","parent","inserted"
    '''
    if not NameConv:
        NameConv = RMNameConvention.RMNameConvention()

    Group = cmds.group( empty = True)

    Group = NameConv.RMRenameBasedOnBaseName(Obj,Group)

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
    if(len(children)>0 and cmds.objectType != "locator"):
        return getAttr(children[0]+".translateX")
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

def RMCreateLineBetwenPoints (Point1, Point2):

    Curve = cmds.curve (degree=1, p=[[0,0,0],[1,0,0]])
    
    NumCVs = cmds.getAttr (Curve+".controlPoints" , size=True)

    Cluster1,Cluster1Handle = cmds.cluster (Curve+".cv[0]", relative=True)

    Cluster2,Cluster2Handle = cmds.cluster (Curve+".cv[1]", relative=True)
    
    print Cluster1
    print Cluster1Handle
    print (str(cmds.objectType(Cluster1)))
    print (str(cmds.objectType(Cluster1Handle)))

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
    Obj1Position = cmds.xform(PointArray[0], rp=True, ws=True, q=True)
    Obj2Position = cmds.xform(PointArray[1], rp=True, ws=True, q=True)

    V1 , V2 = om.MVector(Obj1Position) , om.MVector(Obj2Position)

    initVector = V1 - V2

    firstJntAngle = V1.angle(om.MVector([0,1,0]))

    Angle = firstJntAngle
    
    for index in range(0,len(PointArray)) :

        cmds.makeIdentity (PointArray[index], apply=True, t=1, r=1, s=1)
        cmds.select(cl=True)
        
        if (NameConv.RMIsNameInFormat (PointArray[index])):
            
            newJoint = cmds.joint (p = [0,0,0])
            jointArray.append (NameConv.RMRenameBasedOnBaseName (PointArray[index], newJoint))
        else:
            jointArray.append(cmds.joint (p = [0,0,0], name = NameConv.RMSetNameInFormat("joint", "Character", "MD", "jnt", "rig")))
        
        RMAlign (PointArray[index], jointArray[index],3)
        cmds.makeIdentity (jointArray[index], apply=True, t=1, r=1, s=0)

        if (index > 1) :

            parentOrient = cmds.joint (jointArray[index-1], q=True, orientation=True)

            print parentOrient
            if parentOrient[0] > 90 :

                cmds.joint (jointArray[index-1], e = True, orientatation = [parentOrient[0]-180, parentOrient[1], parentOrient[2]])

            else:

                if parentOrient[0] < -90:

                    cmds.joint (jointArray[index-1], e = True, orientatation = [parentOrient[0]+180, parentOrient[1], parentOrient[2]])
    print jointArray
    RMCreateGroupOnObj (jointArray[0])


#array = cmds.ls(sl=True,type="transform")
RMCreateBonesAtPoints(["locator1","locator2","locator3","locator4"])



