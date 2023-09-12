import random
import maya.cmds as cmds
import RMRigTools
import nameConvention
import RMRigShapeControls
from AutoRig import RMGenericRigStructure
import pprint


def getMeshObjects(Objects):
    MeshObjects = []
    OtherObjects = []
    NameConv = nameConvention.NameConvention()
    for eachObject in Objects:
        if NameConv.guess_object_type(eachObject) == "msh":
            MeshObjects.append(eachObject)
        else:
            OtherObjects.append(eachObject)
    return {"meshObjects": MeshObjects, "other": OtherObjects}


def SinglePropRig(Object, referencePositionControl):
    # if Object.__class__ == list :
    # elif Object.__class__ in [str,unicode]:
    GRS = RMGenericRigStructure.genericRigStructure()

    NameConv = nameConvention.NameConvention()
    bbMesh = RMRigTools.boundingBoxInfo(Object)
    CtrlPosition = cmds.xform(referencePositionControl, q=True, rp=True, worldSpace=True)
    NameList = Object.split(".")
    cntrlToMeshX = bbMesh.position[0] - CtrlPosition[0]
    cntrlToMeshY = bbMesh.position[1] - CtrlPosition[1]
    cntrlToMeshZ = bbMesh.position[2] - CtrlPosition[2]

    if len(NameList) > 1:
        Ctrl = RMRigShapeControls.RMCreateCubeLine(bbMesh.lenX, bbMesh.lenY, bbMesh.lenZ,
                                                   offsetX=-bbMesh.minDistanceToCenterX + cntrlToMeshX,
                                                   offsetY=-bbMesh.minDistanceToCenterY + bbMesh.lenY / 2 + cntrlToMeshY,
                                                   offsetZ=-bbMesh.minDistanceToCenterZ + bbMesh.lenZ / 2 + cntrlToMeshZ,
                                                   name=NameList[1])
        joint = cmds.joint(name=NameList[1] + "jnt")
    else:
        Ctrl = RMRigShapeControls.RMCreateCubeLine(bbMesh.lenX, bbMesh.lenY, bbMesh.lenZ,
                                                   offsetX=-bbMesh.minDistanceToCenterX + cntrlToMeshX,
                                                   offsetY=-bbMesh.minDistanceToCenterY + bbMesh.lenY / 2 + cntrlToMeshY,
                                                   offsetZ=-bbMesh.minDistanceToCenterZ + bbMesh.lenZ / 2 + cntrlToMeshZ,
                                                   name=NameList[0] + "Ctrl")
        joint = cmds.joint(name=NameList[0] + "jnt")

    Ctrl = NameConv.rename_name_in_format(Ctrl, {'objectType': "control"})
    ResetGroup = RMRigTools.RMCreateGroupOnObj(Ctrl)
    cmds.parent(ResetGroup, GRS.groups["controls"]["group"])
    rigJntGrp = cmds.ls("*SimpleRigJoints*")
    if len(rigJntGrp) == 0:
        jointGroup = cmds.group(empty=True, name="SimpleRigJoints")
        jointGroup = NameConv.rename_name_in_format(jointGroup, {})
        cmds.parent(jointGroup, GRS.groups["rig"]['group'])
    else:
        jointGroup = rigJntGrp
    RMRigTools.RMAlign(referencePositionControl, ResetGroup, 3)

    joint = NameConv.rename_name_in_format(joint, {})

    RMRigTools.RMAlign(referencePositionControl, joint, 3)
    ResetJoint = RMRigTools.RMCreateGroupOnObj(joint)
    cmds.parent(ResetJoint, jointGroup)
    # if cmds.objExists
    # for eachObject in Object:
    cmds.select(clear=True)
    cmds.select(Object)
    cmds.select(joint, add=True)
    cmds.skinCluster()
    cmds.parentConstraint(Ctrl, joint)


# def MultiPropRig ( Objects , referencePoint = None ):
def createControlForObject(objects, controls):
    if len(controls) == 0:
        for eachObject in objects:
            SinglePropRig(eachObject, eachObject)
    elif len(controls) == len(objects):
        for index in range(0, len(controls)):
            SinglePropRig(objects[index], controls[index])
    elif len(controls) == 1 and len(objects) > 1:
        print ("not suported Selection")
    else:
        print ("not suported Selection")


def isNoiseControl(Object):
    Attributes = cmds.listAttr(Object)
    if "movY" in Attributes and "amplitud" in Attributes and "frequency" in Attributes:
        return True
    else:
        return False


def addAttributes(Object):
    Attributes = cmds.listAttr(Object)
    if not "movY" in Attributes:
        cmds.addAttr(Object, at="float", ln="movY", hnv=1, hxv=1, h=0, k=1, smn=0, smx=10)

    if not "amplitud" in Attributes:
        cmds.addAttr(Object, at="float", ln="amplitud", hnv=1, hxv=1, h=0, k=1, smn=-10, smx=10)

    if not "frequency" in Attributes:
        cmds.addAttr(Object, at="float", ln="frequency", hnv=1, hxv=1, h=0, k=1, smn=-10, smx=10)


def addNoiseOnControl(Object, Control):
    if Object.__class__ == list:
        pass

    elif Object.__class__ in [str]:
        Object = [Object]

    else:
        "Not Valid Arguments on Add Noise"
        return None

    Expresion = '''//{0}
    {0}.rotateX=`noise((time+{2})*{1}.frequency)`*{1}.amplitud;
    {0}.rotateY=`noise((time+{2}+30)*{1}.frequency)`*{1}.amplitud;
    {0}.rotateZ=`noise((time+{2}+60)*{1}.frequency)`*{1}.amplitud;
    {0}.ty=`noise((time+{2}+90)*{1}.frequency)`*{1}.movY + {1}.movY;
    '''
    if not isNoiseControl(Control):
        addAttributes(Control)

    for eachObject in Object:
        constraints = constraintComponents(gessFrom=eachObject)
        ResetGroup = RMRigTools.RMCreateGroupOnObj(eachObject, Type="child")
        for eachkey in constraints.constraintDic:
            cmds.delete(eachkey)
            cmds.parentConstraint(ResetGroup, constraints.constraintDic[eachkey]["affected"], mo=True)
        ExpressionNode = cmds.expression(name="NoiseMainExpresion",
                                         string=Expresion.format(ResetGroup, Control, random.uniform(0, 100)))


def CreateControlOnSelection():
    selection = cmds.ls(sl=True, type="transform")
    ObjectsDic = getMeshObjects(selection)
    createControlForObject(ObjectsDic["meshObjects"], ObjectsDic["other"])


def deleteSimpleRig():
    constraint = cmds.listConnections(type="parentConstraint")
    if constraint and len(constraint) > 0:
        parentConst = constraint[0]
        wAlias = cmds.parentConstraint(parentConst, q=True, wal=True)
        control = cmds.parentConstraint(parentConst, q=True, tl=True)
        joint = cmds.listConnections("%s.constraintTranslateX" % (parentConst))
        skinList = cmds.listConnections(joint, type="skinCluster")
        if skinList and len(skinList) > 0:
            skinCluster = skinList[0]
            geolist = cmds.listConnections("%s.outputGeometry" % (skinCluster))
            cmds.delete(skinCluster)
            parentsJoint = cmds.listRelatives(joint, parent=True)
            parentsControl = cmds.listRelatives(control, parent=True)
            cmds.delete(parentsJoint[0])
            cmds.delete(parentsControl[0])
            for eachObject in geolist:
                RMRigTools.RMLockAndHideAttributes(geolist, "1111111111")
        else:
            print ("no skin cluster Identified")
    else:
        print ("no constraint Node Identified")


class constraintComponents(object):
    def __init__(self, constraint=None, gessFrom=None):
        self.source = None
        self.constrained = []
        self.constrainNodes = []
        self.constraintDic = {}
        if gessFrom:
            if cmds.objExists(gessFrom):
                constraint = cmds.listConnections(gessFrom + ".translate")
                if len(constraint) > 0:
                    for eachConnection in constraint:
                        if cmds.objectType(eachConnection) == "parentConstraint":
                            self.constrainNodes.append(eachConnection)
        else:
            self.constrainNodes = [constraint]
        for eachNode in self.constrainNodes:
            self.constraintDic[eachNode] = {}
            WA = cmds.parentConstraint(self.constrainNodes, q=True, weightAliasList=True)
            TL = cmds.parentConstraint(self.constrainNodes, q=True, targetList=True)
            self.constraintDic[eachNode]["WA"] = WA
            self.constraintDic[eachNode]["TL"] = TL
            self.constraintDic[eachNode]["affected"] = cmds.listConnections(eachNode + ".constraintRotateX")

# constraints = constraintComponents(gessFrom = "Character_MD_pSphere1Ctrl00_ctr_Rig")
# pprint.pprint(constraints.constraintDic)
