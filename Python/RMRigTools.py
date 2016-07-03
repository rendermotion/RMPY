import maya.cmds as cmds

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



