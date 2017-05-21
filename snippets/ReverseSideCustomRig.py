import maya.cmds as cmds
import RMUncategorized

    


def MirrorChildren(Objects):
    for eachObject in Objects: 
        children = cmds.listRelatives(eachObject, children = True,type='transform')
        if (children):
            MirrorChildren(children)

    for eachObject in Objects:
        ObjectTransformDic = RMUncategorized.ObjectTransformDic( [eachObject] )
        SplitArray = eachObject.split("_")
        Side = SplitArray[1]
        if Side == "R":
            SplitArray[1]="L"
            OpositObject = "_".join(SplitArray)
            if cmds.objExists(OpositObject):
                RMUncategorized.SetObjectTransformDic({OpositObject : ObjectTransformDic[eachObject]}, MirrorTranslateX = -1 , MirrorTranslateY = 1 , MirrorTranslateZ = 1 , MirrorRotateX = 1 , MirrorRotateY = -1 , MirrorRotateZ = -1)
                if cmds.objectType(eachObject) == 'joint':
                    X = cmds.getAttr("%s.jointOrientX"%(eachObject))
                    Y = cmds.getAttr("%s.jointOrientY"%(eachObject))
                    Z = cmds.getAttr("%s.jointOrientZ"%(eachObject))
                    cmds.setAttr ("%s.jointOrientX"%(OpositObject),-X)
                    cmds.setAttr ("%s.jointOrientY"%(OpositObject),Y)
                    cmds.setAttr ("%s.jointOrientZ"%(OpositObject),Z)
        else:
            SplitArray[1]="R"
            OpositObject = "_".join(SplitArray)
            if cmds.objExists(OpositObject):
                RMUncategorized.SetObjectTransformDic({OpositObject : ObjectTransformDic[eachObject]}, MirrorTranslateX = -1 , MirrorTranslateY = 1 , MirrorTranslateZ = 1 , MirrorRotateX = 1 , MirrorRotateY = -1 , MirrorRotateZ = -1)
                if cmds.objectType(eachObject) == 'joint': 
                    X = cmds.getAttr("%s.jointOrientX"%(eachObject))
                    Y = cmds.getAttr("%s.jointOrientY"%(eachObject))
                    Z = cmds.getAttr("%s.jointOrientZ"%(eachObject))
                    cmds.setAttr ("%s.jointOrientX"%(OpositObject), -X)
                    cmds.setAttr ("%s.jointOrientY"%(OpositObject), Y)
                    cmds.setAttr ("%s.jointOrientZ"%(OpositObject), Z)

selection = cmds.ls(selection = True)

MirrorChildren(selection)
