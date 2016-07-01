import maya.cmds as cmds
import RMNameConvention

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


def RMCreateGroupOnObj(Obj,Type="world"):
    '''
    "world","child","parent","inserted"
    '''
    Group = cmds.group(RMUniqueName(Obj),empty=True)
    Group = RMGuessTypeInName(Group)
    RMAlign(Obj,Group,3)
    Parent = cmds.listRelatives(Obj,parent=True)
    
    if Type == "parent":
        cmds.parent(Obj,Group)
        if len(Parent)>0:
            cmds.parent(Parent,Group)
    if Type == "child":
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
        print Obj
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
    return Children

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






RMCreateLineBetwenPoints("locator1","locator2")