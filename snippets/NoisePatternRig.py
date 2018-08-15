import random
import pymel.core as pm
from RMPY import RMRigTools
from RMPY import nameConvention
from RMPY import RMRigShapeControls
from RMPY.AutoRig import RMGenericRigStructure
import pprint
reload (RMRigTools)
reload (RMRigShapeControls)
reload (RMGenericRigStructure )
reload (nameConvention)

def getMeshObjects(Objects):
    MeshObjects = []
    OtherObjects = []
    NameConv=nameConvention.NameConvention()
    for eachObject in Objects:
        if NameConv.guess_object_type(eachObject) == "msh":
            MeshObjects.append(eachObject)
        else:
            OtherObjects.append(eachObject)
    return {"meshObjects": MeshObjects,"other":OtherObjects}

def SinglePropRig(scene_object, referencePositionControl, centerPivot = False):
    #if Object.__class__ == list :
    #elif Object.__class__ in [str,unicode]:
    GRS = RMGenericRigStructure.genericRigStructure()

    NameConv = nameConvention.NameConvention()
    bbMesh   = RMRigTools.boundingBoxInfo(scene_object)
    CtrlPosition = pm.xform(referencePositionControl,q=True,rp=True, worldSpace = True)

    NameList = scene_object.split(".")
    cntrlToMeshX = bbMesh.position[0] - CtrlPosition[0]
    cntrlToMeshY = bbMesh.position[1] - CtrlPosition[1]
    cntrlToMeshZ = bbMesh.position[2] - CtrlPosition[2]

    if len(NameList) > 1:
        Ctrl = RMRigShapeControls.RMCreateCubeLine(bbMesh.lenX, bbMesh.lenY, bbMesh.lenZ, offsetX = -bbMesh.minDistanceToCenterX + cntrlToMeshX,offsetY = -bbMesh.minDistanceToCenterY + bbMesh.lenY / 2 + cntrlToMeshY,offsetZ = -bbMesh.minDistanceToCenterZ + bbMesh.lenZ / 2 + cntrlToMeshZ,name = NameList[1])
        if centerPivot==True:
            pm.xform(Ctrl, cp=1)
        joint = pm.joint(name=NameList[1]+"jnt")
    else:
        Ctrl = RMRigShapeControls.RMCreateCubeLine(bbMesh.lenX, bbMesh.lenY, bbMesh.lenZ, offsetX = -bbMesh.minDistanceToCenterX + cntrlToMeshX,offsetY = -bbMesh.minDistanceToCenterY + bbMesh.lenY / 2 + cntrlToMeshY,offsetZ = -bbMesh.minDistanceToCenterZ + bbMesh.lenZ / 2 + cntrlToMeshZ,name = NameList[0]+"Ctrl")
        if centerPivot==True:
            pm.xform(Ctrl, cp=1)
        joint = pm.joint(name=NameList[0]+"jnt")

    Ctrl = NameConv.rename_name_in_format(Ctrl, {'objectType': "control"})
    ResetGroup = RMRigTools.RMCreateGroupOnObj(Ctrl)
    pm.parent( ResetGroup , GRS.groups["controls"]["group"] )
    rigJntGrp = pm.ls("*SimpleRigJoints*")
    if len(rigJntGrp) == 0:
        jointGroup = pm.group(empty=True,name = "SimpleRigJoints")
        jointGroup = NameConv.rename_name_in_format (jointGroup, {})
        pm.parent ( jointGroup , GRS.groups["rig"]['group'])
    else:
        jointGroup = rigJntGrp
    if centerPivot!=True:
        RMRigTools.RMAlign ( referencePositionControl, ResetGroup, 3)

    joint = NameConv.rename_name_in_format(joint, {})

    RMRigTools.RMAlign (referencePositionControl, joint, 3)
    ResetJoint = RMRigTools.RMCreateGroupOnObj(joint)
    pm.parent( ResetJoint, jointGroup)
    #if pm.objExists
    #for eachObject in Object:
    pm.parentConstraint(Ctrl, joint)
    pm.skinCluster(joint, scene_object)

#def MultiPropRig ( Objects , referencePoint = None ):
def createControlForObject(objects , controls , centerPivot = False):
    if len(controls) == 0:
        for eachObject in objects:
            SinglePropRig(eachObject,eachObject, centerPivot = centerPivot)
    elif len(controls) == len(objects):
        for index in range(0,len(controls)):
            SinglePropRig(objects[index],controls[index] , centerPivot = centerPivot)
    elif len(controls) == 1 and len(objects)>1:
        print "not suported Selection"
    else:
        print "not suported Selection"

def isNoiseControl(Object):
    Attributes = pm.listAttr(Object)
    if "movY" in Attributes and  "amplitud" in Attributes and "frequency" in Attributes:
        return True
    else:
        return False

def  addAttributes(Object):
    Attributes = pm.listAttr(Object)
    if not "movY" in Attributes:
        pm.addAttr( Object , at="float", ln = "movY",   hnv = 1, hxv = 1, h = 0, k = 1, smn = 0, smx = 10)
    
    if not "amplitud" in Attributes:
        pm.addAttr( Object , at="float", ln = "amplitud",   hnv = 1, hxv = 1, h = 0, k = 1, smn = -10, smx = 10)
    
    if not "frequency" in Attributes:
        pm.addAttr( Object , at="float", ln = "frequency",   hnv = 1, hxv = 1, h = 0, k = 1, smn = -10, smx = 10)

def addNoiseOnControl(Object,Control):
    if Object.__class__ == list :
        pass

    elif Object.__class__ in [str,unicode]:
        Object=[Object]
    
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
        constraints = constraintComponents(gessFrom = eachObject)
        ResetGroup = RMRigTools.RMCreateGroupOnObj( eachObject ,Type="child")
        for eachkey in constraints.constraintDic:
            pm.delete(eachkey)
            pm.parentConstraint(ResetGroup,constraints.constraintDic[eachkey]["affected"],mo=True)
        ExpressionNode = pm.expression (name = "NoiseMainExpresion", string = Expresion.format( ResetGroup , Control, random.uniform (0,100)))


def CreateControlOnSelection(centerPivot = False):
    selection = pm.ls(sl=True, type="transform")
    ObjectsDic = getMeshObjects(selection)
    createControlForObject(ObjectsDic["meshObjects"],ObjectsDic["other"],centerPivot = centerPivot)

def deleteSimpleRig():
    constraint = pm.listConnections(type="parentConstraint")
    if constraint and len(constraint) > 0:
        parentConst = constraint[0]
        wAlias = pm.parentConstraint( parentConst, q=True, wal= True)
        control = pm.parentConstraint( parentConst, q=True, tl= True)
        joint = pm.listConnections ( "%s.constraintTranslateX" % (parentConst))
        skinList = pm.listConnections (joint, type="skinCluster")
        if skinList and len(skinList) > 0:
            skinCluster = skinList[0]
            geolist = pm.listConnections("%s.outputGeometry"%(skinCluster))
            pm.delete(skinCluster)
            parentsJoint = pm.listRelatives(joint,parent = True)
            parentsControl = pm.listRelatives(control,parent = True)
            pm.delete(parentsJoint[0])
            pm.delete(parentsControl[0])
            for eachObject in geolist:
                RMRigTools.RMLockAndHideAttributes(geolist,"1111111111")
        else:
            print "no skin cluster Identified"
    else:
        print "no constraint Node Identified"        
def openTransform():
    controlObj = pm.ls(selection = True)
    parentObject = pm.listRelatives(controlObj[0], parent=True)[0]
    print ("parentObject= %s"% parentObject)
    constraint =  pm.listConnections(controlObj[0],type = "parentConstraint")[0]
    print ("constraint= %s"% constraint)
    joints   =  pm.listConnections(constraint ,type = "joint")[0]
    print ("joints= %s"% joints)
    skinCluster =  pm.listConnections(joints ,type = "skinCluster")[0]
    print ("skinCluster= %s"% skinCluster)
    geometry =  pm.listConnections(skinCluster ,type = "mesh")[0]
    print ("geometry= %s"% geometry)
    pm.select(geometry, replace = True) 
    pm.select(parentObject, add = True) 
    pm.isolateSelect( "modelPanel4", state = 1)
    pm.isolateSelect( "modelPanel4", loadSelected = 1)
    print ("isolating = \n%s, \n%s"%(geometry,parentObject))
    pm.select(parentObject, replace = True)
    pm.delete(constraint)
    return joints , controlObj
    
def closeTransform(controlObj,joints):
    pm.makeIdentity(eachObject, apply=True, t=1)
    pm.parentConstraint(controlObj, joints, mo = True)
    pm.isolateSelect("modelPanel4",state = 0)

#if value:
#    joints = None
#    controlObject = None
#    joints, controlObject = openTransform()
#    value = False
#else:
#    closeTransform(controlObject,joints)
#    value = True


class constraintComponents(object):
    def __init__(self,constraint=None,gessFrom=None):
        self.source         = None
        self.constrained    = []
        self.constrainNodes = []
        self.constraintDic = {}
        if gessFrom:
            if pm.objExists(gessFrom):
                constraint = pm.listConnections(gessFrom+".translate")
                if len(constraint) > 0:
                    for eachConnection in constraint:
                        if pm.objectType(eachConnection) == "parentConstraint":
                            self.constrainNodes.append(eachConnection)
        else :
            self.constrainNodes = [constraint]
        for eachNode in self.constrainNodes:
            self.constraintDic[eachNode]={}
            WA = pm.parentConstraint (self.constrainNodes, q = True, weightAliasList = True)
            TL = pm.parentConstraint (self.constrainNodes, q = True, targetList = True)
            self.constraintDic[eachNode]["WA"] = WA
            self.constraintDic[eachNode]["TL"] = TL
            self.constraintDic[eachNode]["affected"] = pm.listConnections(eachNode + ".constraintRotateX")

#constraints = constraintComponents(gessFrom = "Character_MD_pSphere1Ctrl00_ctr_Rig")
#pprint.pprint(constraints.constraintDic)
if __name__=="__main__":
    pass
    #print value
    #openTransform()