import maya.cmds as cmds
import pprint as pp
from RMPY import nameConvention
from RMPY import RMRigTools
import pymel.core as pm
from RMPY.creators import blendShape

def blend_shape_target_dictionary(BSNode):
    input_target_group = cmds.getAttr(f"{BSNode}.inputTarget[0].inputTargetGroup", mi=True)
    blend_shape_dic = {}
    for eachTarget in input_target_group:
        alias_name = cmds.listAttr((f"{BSNode}.weight["+str(eachTarget)+"]"), m=True)
        blend_shape_dic[str(alias_name[0])] = {}
        blend_shape_dic[str(alias_name[0])]["TargetGroup"] = eachTarget
        items = cmds.getAttr(f"{BSNode}.inputTarget[0].inputTargetGroup[{str(eachTarget)}].inputTargetItem", mi=True)
        blend_shape_dic[str(alias_name[0])]["Items"] = items
    return blend_shape_dic

'''
def invertCurrentPaintTargetWeights(ObjectName,index):
    #cmds.setAttr("%s.inputTarget[0].inputTargetGroup[%s]paintTargetIndex"%ObjectName)
    CompTarget = cmds.getAttr("%s.inputTarget[0].inputTargetGroup[%s].inputTargetItem[6000].inputComponentsTarget"%(ObjectName,index))
    NormID    =cmds.getAttr("%s.inputTarget[0].inputTargetGroup[%s].normalizationId"%(ObjectName,index))
    BaseWeights= cmds.getAttr("%s.inputTarget[0].baseWeights"%(ObjectName))
    NM = cmds.getAttr("%s.inputTarget[0].normalizationGroup[%s].normalizationWeights  "%(ObjectName,index))
    TargetIndex = cmds.getAttr("%s.inputTarget[0].paintTargetIndex"%ObjectName)

    print ('CompTarget:%s'% (CompTarget))
    print ('TargetIndex:%s'% (TargetIndex))
    print ('NormID:%s'% (NormID))
    print ('BaseWeights:%s'% (BaseWeights))
    print ('NM:%s'% (NM))
    weights = cmds.getAttr("%s.inputTarget[0].inputTargetGroup[%s].targetWeights"%(ObjectName,index))
    print ('weights:%s'% (weights))
    newWeights = []
    weightIndex=0
    #for i in weights[0]:
    #    cmds.setAttr("%s.inputTarget[0].inputTargetGroup[%s].targetWeights[%s]"%(ObjectName, index , weightIndex), (float(1.0)- i))
    #    weightIndex+=1
    #weights = cmds.getAttr("%s.inputTarget[0].paintTargetWeights"%ObjectName)
pp.pprint (RMblendShapeTargetDic('blendShape20'))
invertCurrentPaintTargetWeights('blendShape20',3)
'''


def invert_current_paint_target_weights(blendshape_node, index):

    if index != -1:
        weight_map_target = f'inputTarget[{index}].targetWeights'
    else:
        weight_map_target = 'weightList[0].weights'

    weights = cmds.getAttr(f"{blendshape_node}.{weight_map_target}")[0]
    weight_index = cmds.getAttr(f"{blendshape_node}.{weight_map_target}", multiIndices=True)
    destination_geo = cmds.listConnections(f'{blendshape_node}.outputGeometry', source=False)[0]
    vertex_number = cmds.polyEvaluate(destination_geo, vertex=True)
    print(weights)
    print(weight_index)
    for index_vertex in range(vertex_number):
        if index_vertex in weight_index:
            value = weights[weight_index.index(index_vertex)]
        else:
            value = 1
        print(value)
        cmds.setAttr(f"{blendshape_node}.{weight_map_target}[{index_vertex}]", float(1.0) - value)


def copyCurrentPaintTargetWeights(blend_shape_node, index_source, index_destination):

    if index_source != -1:
        weight_map_source = f'inputTarget[{index_source}].targetWeights'
    else:
        weight_map_source = 'weightList[0].weights'

    if index_destination != -1:
        weight_map_destination = 'inputTarget[%s].targetWeights' % index_destination
    else:
        weight_map_destination = 'weightList[0].weights'

    weights = cmds.getAttr(f"{blend_shape_node}.{weight_map_source}[*]")
    weight_index = cmds.getAttr(f"{blend_shape_node}.{weight_map_source}", multiIndices=True)
    try:
        destination_weight_index = cmds.getAttr(f"{blend_shape_node}.{weight_map_destination}", multiIndices=True)
    except:
        destination_weight_index = []
    for vertex_index in set(weight_index + destination_weight_index):
        if vertex_index in weight_index:
            set_value = weights[weight_index.index(vertex_index)]
        else:
            set_value = 1.0
        cmds.setAttr(f"{blend_shape_node}.{weight_map_destination}[{vertex_index}]", set_value)

def copy_paint_to_dictionary(ObjectName, indexSource):
    if indexSource != -1:
        source_weights_token = 'inputTarget[{}].targetWeights'.format(indexSource)
    else:
        source_weights_token = 'weightList[0].weights'

    weights = cmds.getAttr("{}.{}[*]".format(ObjectName, source_weights_token))
    weights_list = cmds.getAttr("{}.{}".format(ObjectName, source_weights_token),
                                multiIndices=True)
    return {'weights': weights, 'weights_list': weights_list}


def paste_paint_from_dictionary(ObjectName, indexDestination, weights_dictionary):
    weights_list = weights_dictionary['weights_list']
    weights = weights_dictionary['weights']
    if indexDestination != -1:
        destination_weights_token = 'inputTarget[%s].targetWeights' % indexDestination
    else:
        destination_weights_token = 'weightList[0].weights'

    current_weight_list = cmds.getAttr("%s.%s" %
                                       (ObjectName, destination_weights_token), multiIndices=True)
    if current_weight_list:
        total_weight_list = set(weights_list + current_weight_list)
    else:
        total_weight_list = weights_list
    for each_index in total_weight_list:
        if each_index in weights_list:
            value = weights[weights_list.index(each_index)]
        else:
            value = 1
        cmds.setAttr(f"{ObjectName}.{destination_weights_token}[{each_index}]", value)


def get_blend_shape(geometry):
    for each in pm.listHistory(geometry, interestLevel=2, pruneDagObjects=True):
        if pm.objectType(each) == 'blendShape':
            return each
    return None
class BSManager(object):
    def __init__(self, NameConv=None) :
        if NameConv:
            self.NameConv = NameConv
        else:
            self.NameConv = nameConvention.NameConvention()
        RigTools = RMRigTools.RMRigTools(self.NameConv)
        self.FaceBlendShapeDic = {}

    def AppyBlendShapeDefinition (self, BSDefinition, blendShapeNode = None, objectPrefix = ""):
        for eachBSGroup in BSDefinition:
            if BSDefinition[eachBSGroup]['Type'] == 'blendShapeDefinition':
                if BSDefinition[eachBSGroup]["isSymetrical"] == True:
                    self.CreateMulipleBlendShapes (BSDefinition, "L", eachBSGroup, blendShapeNode = blendShapeNode,objectPrefix = objectPrefix)
                    self.CreateMulipleBlendShapes (BSDefinition, "R", eachBSGroup, blendShapeNode = blendShapeNode,objectPrefix = objectPrefix)
                else:
                    self.CreateMulipleBlendShapes (BSDefinition, "", eachBSGroup,  blendShapeNode = blendShapeNode,objectPrefix = objectPrefix)

            elif BSDefinition[eachBSGroup]['Type'] == 'jointLinkDefinition':
                if BSDefinition[eachBSGroup]["isSymetrical"] == True:
                    self.linkJointDefinition("LF",BSDefinition[eachBSGroup] )
                    self.linkJointDefinition("RH",BSDefinition[eachBSGroup] )
                else:
                    self.linkJointDefinition("MD",BSDefinition[eachBSGroup] )

    def returnBlendShapesByControl(self,connectionPlug, BSDict):
        orderedList = {'positive':[] , 'negative':[]}
        for eachBlendShape in BSDict:
            if BSDict[eachBlendShape]["connection"] == connectionPlug:
                if BSDict[eachBlendShape]["value"] > 0:
                    sign = 'positive'
                else:
                    sign = 'negative'

                if len (orderedList[sign]) == 0:
                    #print "Toinsert0:%s"%eachBlendShape
                    orderedList[sign].append(eachBlendShape)
                else:
                    #print "Toinsert1:%s"%eachBlendShape
                    index = 0
                    for blendShapes in orderedList[sign]:
                        if (abs(BSDict[eachBlendShape]['value']) > abs(BSDict[blendShapes]['value'])):
                            index += 1
                        else:
                            break
                    orderedList[sign].insert(index,eachBlendShape)
                pass
        return orderedList

    def returnJointsByControl(self, connectionPlug, JointDic):
        orderedList = []
        for eachJoint in JointDic:
            if JointDic[eachJoint]['connection'] == connectionPlug:
                orderedList.append(eachJoint)
        return orderedList

    def connectFromDefinition(self,  BSDefinition, currentBlendShape, blendShapeNode, prefix, extremeValue, objectPrefix = ''):
        if prefix!="":
            Side = self.getSideFromPrefix(prefix)
            #print "Connecting:%s.%s To %s.%s"% (self.NameConv.RMSetFromName(BSDefinition["control"],Side,Token = "Side" ), BSDefinition['blendShapes'][currentBlendShape]["connection"], blendShapeNode, prefix +currentBlendShape)
            control = self.NameConv.set_from_name(BSDefinition["control"], Side, Token ="Side")
        else:
            control = BSDefinition["control"]

        if extremeValue > 0:
            RMRigTools.RMConnectWithLimits("%s.%s"%(control, BSDefinition['blendShapes'][currentBlendShape]["connection"]) ,"%s.%s"%(blendShapeNode,prefix + objectPrefix + currentBlendShape),[[           0,0], [extremeValue,1]] )
        else:
            RMRigTools.RMConnectWithLimits("%s.%s"%(control, BSDefinition['blendShapes'][currentBlendShape]["connection"]) ,"%s.%s"%(blendShapeNode,prefix + objectPrefix +currentBlendShape) ,[[extremeValue,1], [           0,0]] ) 

    def CreateBlendShapesByControl (self, BlendShapeNode, Plug , BSDefinition, prefix, objectPrefix = ''):
        ''' This function adds new blendShapes to a node(BlendShapeNode) based on a plug,
        first it createds a dictionary with  self.returnBlendShapesByControl function, 
        This dictionary is then match againts the BS definition and the negative BS are added to a single BS
        and the positive ones are added to a new one.'''
        if cmds.objExists(BlendShapeNode):
            BlendShapesOfSingleControl = self.returnBlendShapesByControl(Plug, BSDefinition["blendShapes"])
            blendShapeOriginalGeo = self.findMeshByBlendShapeNode(BlendShapeNode)
            BlendShapeDict = self.RMblendShapeTargetDic(BlendShapeNode)

            NewTargetIndex = len(BlendShapeDict)

            if  'positive' in BlendShapesOfSingleControl:
                if len (BlendShapesOfSingleControl['positive']) >= 1:
                    SMX = BSDefinition['blendShapes'][BlendShapesOfSingleControl['positive'][len (BlendShapesOfSingleControl['positive']) - 1]]["value"]
                else: SMX = 10
            else: 
                SMX = 0
            if  'negative' in BlendShapesOfSingleControl:
                if len (BlendShapesOfSingleControl['negative']) >= 1:
                    SMN = BSDefinition['blendShapes'][BlendShapesOfSingleControl['negative'][len (BlendShapesOfSingleControl['negative']) - 1]]["value"]
                else:
                    SMN = 0
            else: 
                SMN = 0

            #connection = BSDefinition['blendShapes'][BlendShapesOfSingleControl['negative'][len (BlendShapesOfSingleControl['negative']) - 1]]["connection"]
            if prefix != '':
                Side = self.getSideFromPrefix(prefix)
                control = self.NameConv.set_from_name(BSDefinition["control"], Side, Token ="Side")
            else:
                control =BSDefinition["control"]

            if "keyable" in BSDefinition['attributes'][Plug]:
                if BSDefinition['attributes'][Plug]["keyable"]:
                    keyable = 1
                else:
                    keyable = 0
            else:
                keyable = 1

            self.AddAttributes (control,  Plug , SMN, SMX, keyable )
            #print BlendShapesOfSingleControl
            #pp.pprint (BlendShapeDict)
            #print "NewTargetIndex:%s"%(NewTargetIndex)
            AtLeastOne = False
            if  'positive' in BlendShapesOfSingleControl and len(BlendShapesOfSingleControl['positive']) >= 1:
                if (prefix + BlendShapesOfSingleControl['positive'][len(BlendShapesOfSingleControl['positive']) - 1]) not in BlendShapeDict:
                    for eachBS in BlendShapesOfSingleControl['positive']:
                        if cmds.objExists(prefix + eachBS):
                            print("adding pblendShape:%s"% (prefix + eachBS))
                            cmds.blendShape(BlendShapeNode, edit=True, target = [blendShapeOriginalGeo, NewTargetIndex + 1, prefix + objectPrefix + eachBS, float (abs(BSDefinition['blendShapes'][eachBS]["value"])) / 10.0 ])
                            #NewTargetIndex += 1
                            AtLeastOne = True
                        else:
                            print (" BS  %s not found on scene"%(prefix+ objectPrefix + eachBS))
                    if AtLeastOne:
                        NewTargetIndex += 1
                        self.connectFromDefinition( BSDefinition,BlendShapesOfSingleControl['positive'][len(BlendShapesOfSingleControl['positive']) - 1], BlendShapeNode, prefix, 10, objectPrefix = objectPrefix)
                else:
                    self.connectFromDefinition( BSDefinition,BlendShapesOfSingleControl['positive'][len(BlendShapesOfSingleControl['positive']) - 1], BlendShapeNode, prefix, 10,  objectPrefix = objectPrefix)

            AtLeastOne = False
            if  'negative' in BlendShapesOfSingleControl and len(BlendShapesOfSingleControl['negative']) >= 1:
                if (prefix + BlendShapesOfSingleControl['negative'][len(BlendShapesOfSingleControl['negative']) - 1]) not in BlendShapeDict:
                    for eachBS in BlendShapesOfSingleControl['negative']:
                        if cmds.objExists(prefix + eachBS):
                            print ("adding blendShape:%s"% (prefix+objectPrefix + eachBS))
                            cmds.blendShape(BlendShapeNode, edit=True, target = [blendShapeOriginalGeo, NewTargetIndex + 1, prefix+ objectPrefix + eachBS, float (abs(BSDefinition['blendShapes'][eachBS]["value"])) / 10.0 ])
                            #NewTargetIndex += 1
                            AtLeastOne = True 
                        else:
                            print (" BS  %s not found on scene"%(prefix + objectPrefix + eachBS))
                    if AtLeastOne:
                        NewTargetIndex += 1
                        self.connectFromDefinition( BSDefinition,BlendShapesOfSingleControl['negative'][len(BlendShapesOfSingleControl['negative']) - 1], BlendShapeNode, prefix, -10,  objectPrefix = objectPrefix)
                else :
                    self.connectFromDefinition( BSDefinition,BlendShapesOfSingleControl['negative'][len(BlendShapesOfSingleControl['negative']) - 1], BlendShapeNode, prefix, -10,  objectPrefix = objectPrefix)

    def findMeshByBlendShapeNode (self,BSNode):
        mesh = cmds.listConnections ("%s.outputGeometry[0]"%BSNode, type='mesh')
        return mesh[0]
    def getSideFromPrefix(self, prefix):
        if prefix == "":
            Side = "MD"
        elif prefix=="R":
            Side = "RH"
        elif prefix=="L":
            Side = "LF"
        return Side
    def CreateMulipleBlendShapes (self,BSDefinition, prefix, BSGroups,  blendShapeNode = None, objectPrefix = ''):
        self.FaceBlendShapeDic = None
        if BSDefinition[BSGroups]['Type'] == "blendShapeDefinition":
            print ("blendShapeNode%s"%blendShapeNode)
            if blendShapeNode == None :

                bs_node_list = blendShape.BlendShape().get_blend_shape_list(selection[0])
                if len(bs_node_list) == 0:
                    print ("No blendshape Found on %s" % BSDefinition[BSGroups]['baseMesh'])
                    BSName = BSGroups + objectPrefix + "BS"
                    #blendShapeOriginalGeo = cmds.duplicate(prefix + BSDefinition[BSGroups]['baseMesh'], name = self.NameConv.RMGetAShortName(BSDefinition[BSGroups]['baseMesh']) + BSGroups)
                    Side = self.getSideFromPrefix(prefix)
                    #blendShapeOriginalGeo = self.NameConv.RMRenameNameInFormat( blendShapeOriginalGeo, System = "faceRig",Side = Side)
                    #cmds.blendShape(blendShapeOriginalGeo, name = BSName)
                    cmds.blendShape(BSDefinition[BSGroups]['baseMesh'], name = BSName)
                    BSName = self.NameConv.rename_name_in_format(BSName, {'system': "faceRig", 'side': Side})
                else:
                    BSName = bs_node_list[0]
            else :
                BSName = blendShapeNode
            for eachControl in BSDefinition [BSGroups]['order']:
                self.CreateBlendShapesByControl(BSName, eachControl, BSDefinition [BSGroups], prefix, objectPrefix = objectPrefix)
        return self.FaceBlendShapeDic

    def AddAttributes (self, Object, Attribute, SMN, SMX,keyable = 1 ):
        #print ("Adding Attribute:%s  to Object:%s Min:%s MAx %s"%(Attribute,Object,SMN,SMX))
        AttrList = cmds.listAttr(Object)
        if Attribute not in AttrList:
            cmds.addAttr(Object, at="float", ln = Attribute ,hnv = 1, hxv = 1, h = 0, k = keyable, smn = SMN, smx = SMX)

    def linkBlendShapesAttr (self, Object, AttributesDefinition, BSNode):
        blendShapeTargetDic = self.RMblendShapeTargetDic(BSNode)
        #for eachAttr in AttributesDefinition:

    def RMblendShapeTargetDic (self, BSNode):
        #AliasNames=cmds.listAttr((BSNode +".weight"),m=True);
        InputTargetGroup = cmds.getAttr ((BSNode+".inputTargetGroup"), mi=True);
        BlendShapeDic={}
        if InputTargetGroup:
            for eachTarget in InputTargetGroup:
                AliasName=cmds.listAttr((BSNode + ".weight[" + str(eachTarget) + "]"), m=True)
                BlendShapeDic[str(AliasName[0])] = {}
                BlendShapeDic[str(AliasName[0])]["TargetGroup"] = eachTarget
                Items = cmds.getAttr ((BSNode+".inputTargetGroup["+str(eachTarget)+"].inputTargetItem"), mi = True)
                BlendShapeDic[str(AliasName[0])]["Items"] = Items
        return BlendShapeDic

    def linkJointDefinition (self, Side, jointLinkDefinition):
        control = jointLinkDefinition['control']
        if Side in ["LF","RH"]:
            control = self.NameConv.set_from_name(jointLinkDefinition['control'], Side, Token ='Side')

        if cmds.objExists( control):
            for eachAttribute in jointLinkDefinition['order']:
                jointsList = self.returnJointsByControl( eachAttribute, jointLinkDefinition['joints'])
                for eachJoint in jointsList:
                    JointName = eachJoint
                    if Side in [ "LF", "RH"]:
                        JointName = self.NameConv.set_from_name(eachJoint, Side, Token ='Side')
                    if cmds.objExists(JointName):
                        
                        if jointLinkDefinition['joints'][eachJoint]['value'] == None:
                            cmds.connectAttr ('%s.%s'%(control,jointLinkDefinition['joints'][eachJoint]['connection'] ), '%s.%s'%(JointName, jointLinkDefinition['joints'][eachJoint]['inputPlug']),force=True)
                        else:
                            self.AddAttributes ( control, eachAttribute, jointLinkDefinition['attributes'][eachAttribute]['min'], jointLinkDefinition['attributes'][eachAttribute]['max'])
                            RMRigTools.RMConnectWithLimits('%s.%s'%(control,jointLinkDefinition['joints'][eachJoint]['connection'] ), '%s.%s'%(JointName, jointLinkDefinition['joints'][eachJoint]['inputPlug']), jointLinkDefinition['joints'][eachJoint]['value'])
                    else:
                        print ("Joint object doesnt exists:%s"%JointName)
        else:
            print ("Control object doesnt exists:%s"%control)
            control = self.NameConv.set_from_name(jointLinkDefinition['control'], Side, Token='Side')

#if __name__=="__main__":
#    Manager = BSManager()
#    Manager.AppyBlendShapeDefinition( SkinedJoints)