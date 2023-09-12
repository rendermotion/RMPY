import maya.cmds as cmds


def ObjectTransformDic(objects):
    ObjectDic = {}
    for eachObject in objects:
        position = (cmds.getAttr(eachObject + ".t"))
        rotation = (cmds.getAttr(eachObject + ".r"))
        scale = (cmds.getAttr(eachObject + ".s"))
        ObjectDic[removeNameSpaceFromName(eachObject)] = {"t": position[0], "r": rotation[0], "s": scale[0]}
    return ObjectDic


def removeNameSpaceFromName(name):
    Address = name.split("|")
    NewAddres = []
    for eachElement in Address:
        objectName = eachElement.split(":")
        NewAddres.append(objectName[len(objectName) - 1])

    return "|".join(NewAddres)


def ResetPostoZero(objects):
    for eachObject in objects:
        try:
            cmds.setAttr(eachObject + ".t", 0, 0, 0)
        except:
            None
        try:
            cmds.setAttr(eachObject + ".r", 0, 0, 0)
        except:
            None
        try:
            cmds.setAttr(eachObject + ".s", 1, 1, 1)
        except:
            None


def SetObjectTransformDic(OTDic, MirrorTranslateX=1, MirrorTranslateY=1, MirrorTranslateZ=1, MirrorRotateX=1,
                          MirrorRotateY=1, MirrorRotateZ=1):
    selection = cmds.ls(selection=True)
    if selection:
        if len(selection) >= 1:
            Namespaces = selection[0].split(":")
            if len(Namespaces) > 1:
                selectionNameSpace = ":".join(Namespaces[0:-1]) + ":"
            else:
                selectionNameSpace = None
        else:
            selectionNameSpace = None
    else:
        selectionNameSpace = None
    for keys in OTDic:
        FocusObject = ignoreNamespace(keys, selectedNamespace=selectionNameSpace)
        if FocusObject:
            try:
                cmds.setAttr(FocusObject + ".translateX", OTDic[keys]["t"][0] * MirrorTranslateX)
            except:
                None
            try:
                cmds.setAttr(FocusObject + ".translateY", OTDic[keys]["t"][1] * MirrorTranslateY)
            except:
                None
            try:
                cmds.setAttr(FocusObject + ".translateZ", OTDic[keys]["t"][2] * MirrorTranslateZ)
            except:
                None
            try:
                cmds.setAttr(FocusObject + ".rotateX", OTDic[keys]["r"][0] * MirrorRotateX)
            except:
                None
            try:
                cmds.setAttr(FocusObject + ".rotateY", OTDic[keys]["r"][1] * MirrorRotateY)
            except:
                None
            try:
                cmds.setAttr(FocusObject + ".rotateZ", OTDic[keys]["r"][2] * MirrorRotateZ)
            except:
                None
            try:
                cmds.setAttr(FocusObject + ".scaleX", OTDic[keys]["s"][0])
            except:
                None
            try:
                cmds.setAttr(FocusObject + ".scaleY", OTDic[keys]["s"][1])
            except:
                None
            try:
                cmds.setAttr(FocusObject + ".scaleZ", OTDic[keys]["s"][2])
            except:
                None
        else:
            print ("No Object Matches name:")
            print (keys)
            break


def ignoreNamespace(Name, selectedNamespace=None):
    if cmds.objExists(str(Name)):
        return str(Name)
    else:
        # filter = cmds.itemFilter(byName="*"+str(Name))
        # FocusObject = cmds.lsThroughFilter(filter)
        FocusObject = cmds.ls("*" + str(Name))
        if FocusObject:
            if len(FocusObject) > 0:
                if len(FocusObject) == 1:
                    return FocusObject[0]
                else:
                    # print ("More than one object matches Name:"+ Name)
                    # print FocusObject
                    if selectedNamespace:
                        usingNamespace = cmds.ls(selectedNamespace + str(Name))
                        if len(usingNamespace) == 1:
                            return usingNamespace
                    else:
                        print ("try to select an object with the namespace "
                               "that you want to paste duplicateObject:{}".format(Name))
                        return None
                    # for i in FocusObject:
                    #	values = i.split(":")
                    #	if values[len(values) - 1] == str(Name):
                    #		return i
            else:
                return None
        else:
            return None


def ExtractGeometry():
    selected = cmds.ls(sl=True)
    sphere = cmds.polySphere(name=selected[0] + "Extracted", constructionHistory=False)
    sphereShape = cmds.listRelatives(sphere, shapes=True)

    if cmds.objectType(selected[0]) == "mesh":
        cmds.connectAttr(selected[0] + ".outMesh", sphereShape[0] + ".inMesh")

    elif cmds.objectType(selected[0]) == "groupParts":
        cmds.connectAttr(selected[0] + ".outputGeometry", sphereShape[0] + ".inMesh")

    elif cmds.objectType(selected[0]) == "blendShape" or cmds.objectType(selected[0]) == "skinCluster":
        cmds.connectAttr(selected[0] + ".outputGeometry[0]", sphereShape[0] + ".inMesh")
    else:
        print ("El tipo de objeto no fue identificado")
