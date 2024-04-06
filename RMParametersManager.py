import maya.cmds as cmds


def delete_attributes(Object, attribute=None):
    AttrList = cmds.listAttr(Object, userDefined=True)
    if AttrList:
        for eachAttribute in AttrList:
            cmds.setAttr("%s.%s" % (Object, eachAttribute), l=False)
            cmds.deleteAttr(Object, attribute=eachAttribute)


def add_attributes_dic(Object, attributesDic):
    for eachAttribute in attributesDic:
        if attributesDic[eachAttribute]["type"] == "float":
            if "keyable" in attributesDic[eachAttribute]:
                keyable = attributesDic[eachAttribute]["keyable"]
            else:
                keyable = 1
            print("Adding Attribute %s , keyable:%s" % (eachAttribute, keyable))
            cmds.addAttr(Object, at="float", ln=eachAttribute, hnv=1, hxv=1, h=0, k=keyable,
                         smn=float(attributesDic[eachAttribute]["min"]),
                         smx=float(attributesDic[eachAttribute]["max"]))


selection = cmds.ls(selection=True)
for i in selection:
    delete_attributes(i)

# addAttributesDic( "REyeLidShapes", lidShapes)
