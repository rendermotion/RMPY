import maya.cmds as cmds
import pprint as pp
import RMNameConvention
import RMRigTools
reload (RMNameConvention)


def RMblendShapeTargetDic (BSNode):
    #AliasNames=cmds.listAttr((BSNode +".weight"),m=True);
    InputTargetGroup=cmds.getAttr ((BSNode+".inputTarget[0].inputTargetGroup"),mi=True);
    BlendShapeDic={}
    for eachTarget in InputTargetGroup:
        AliasName=cmds.listAttr((BSNode +".weight["+str(eachTarget)+"]"),m=True);
        BlendShapeDic[str(AliasName[0])]={}
        BlendShapeDic[str(AliasName[0])]["TargetGroup"]=eachTarget
        Items = cmds.getAttr ((BSNode+".inputTarget[0].inputTargetGroup["+str(eachTarget)+"].inputTargetItem"), mi=True);
        BlendShapeDic[str(AliasName[0])]["Items"]=Items
    return BlendShapeDic
'''
def invertCurrentPaintTargetWeights(ObjectName,index):
    #cmds.setAttr("%s.inputTarget[0].inputTargetGroup[%s]paintTargetIndex"%ObjectName)
    CompTarget = cmds.getAttr("%s.inputTarget[0].inputTargetGroup[%s].inputTargetItem[6000].inputComponentsTarget"%(ObjectName,index))
    NormID    =cmds.getAttr("%s.inputTarget[0].inputTargetGroup[%s].normalizationId"%(ObjectName,index))
    BaseWeights= cmds.getAttr("%s.inputTarget[0].baseWeights"%(ObjectName))
    NM = cmds.getAttr("%s.inputTarget[0].normalizationGroup[%s].normalizationWeights  "%(ObjectName,index))
    TargetIndex = cmds.getAttr("%s.inputTarget[0].paintTargetIndex"%ObjectName)

    print 'CompTarget:%s'% (CompTarget)
    print 'TargetIndex:%s'% (TargetIndex)
    print 'NormID:%s'% (NormID)
    print 'BaseWeights:%s'% (BaseWeights)
    print 'NM:%s'% (NM)
    weights = cmds.getAttr("%s.inputTarget[0].inputTargetGroup[%s].targetWeights"%(ObjectName,index))
    print 'weights:%s'% (weights)
    newWeights = []
    weightIndex=0
    #for i in weights[0]:
    #    cmds.setAttr("%s.inputTarget[0].inputTargetGroup[%s].targetWeights[%s]"%(ObjectName, index , weightIndex), (float(1.0)- i))
    #    weightIndex+=1
    #weights = cmds.getAttr("%s.inputTarget[0].paintTargetWeights"%ObjectName)
pp.pprint (RMblendShapeTargetDic('blendShape20'))
invertCurrentPaintTargetWeights('blendShape20',3)
'''
def invertCurrentPaintTargetWeights(ObjectName, index):
    cmds.setAttr("%s.inputTarget[0].paintTargetIndex[%s]"%ObjectName, index)
    weights = cmds.getAttr("%s.inputTarget[0].paintTargetWeights"%ObjectName)
    newWeights = []
    index=0
    for i in weights[0]:
        cmds.setAttr("%s.inputTarget[0].paintTargetWeights[%s]"% (ObjectName,index),float(1.0)- i)
        index+=1
    weights = cmds.getAttr("%s.inputTarget[0].paintTargetWeights"%ObjectName)

def copyCurrentPaintTargetWeights(ObjectName, indexSource, indexDestination):
    weights = cmds.getAttr("%s.inputTarget[0].inputTargetGroup[%s].targetWeights"%(ObjectName, indexSource))
    newWeights = []
    index=0
    for i in weights[0]:
        cmds.setAttr("%s.inputTarget[0].inputTargetGroup[%s].targetWeights[%s]"% (ObjectName,indexDestination,index),float(1.0)- i)
        index+=1

class BSManager(object):
    def __init__(self, NameConv=None) :
        if NameConv:
            self.NameConv = NameConv
        else:
            self.NameConv = RMNameConvention.RMNameConvention()
        RigTools = RMRigTools.RMRigTools(self.NameConv)
        self.FaceBlendShapeDic = {}

    def AppyBlendShapeDefinition (self, BSDefinition, blendShapeNode = None):
        for eachBSGroup in BSDefinition:
            if BSDefinition[eachBSGroup]['Type'] == 'blendShapeDefinition':
                if BSDefinition[eachBSGroup]["isSymetrical"] == True:
                    self.CreateMulipleBlendShapes (BSDefinition, "L", eachBSGroup, blendShapeNode = blendShapeNode)
                    self.CreateMulipleBlendShapes (BSDefinition, "R", eachBSGroup, blendShapeNode = blendShapeNode)
                else:
                    self.CreateMulipleBlendShapes (BSDefinition, "", eachBSGroup,  blendShapeNode = blendShapeNode)

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

    def connectFromDefinition(self,  BSDefinition, currentBlendShape, blendShapeNode, prefix, extremeValue):
        Side = self.getSideFromPrefix(prefix)
        #print "Connecting:%s.%s To %s.%s"% (self.NameConv.RMSetFromName(BSDefinition["control"],Side,Token = "Side" ), BSDefinition['blendShapes'][currentBlendShape]["connection"], blendShapeNode, prefix +currentBlendShape)
        
        if extremeValue > 0:
            RMRigTools.RMConnectWithLimits("%s.%s"%(self.NameConv.RMSetFromName(BSDefinition["control"],Side,Token = "Side" ), BSDefinition['blendShapes'][currentBlendShape]["connection"]) ,"%s.%s"%(blendShapeNode,prefix + currentBlendShape),[[           0,0], [extremeValue,1]] )
        else:
            RMRigTools.RMConnectWithLimits("%s.%s"%(self.NameConv.RMSetFromName(BSDefinition["control"],Side,Token = "Side" ), BSDefinition['blendShapes'][currentBlendShape]["connection"]) ,"%s.%s"%(blendShapeNode,prefix + currentBlendShape),[[extremeValue,1], [           0,0]] )

    def CreateBlendShapesByControl (self, BlendShapeNode, Plug , BSDefinition, prefix):
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
                SMX = BSDefinition['blendShapes'][BlendShapesOfSingleControl['positive'][len (BlendShapesOfSingleControl['positive']) - 1]]["value"]
            else: 
                SMX = 0
            if  'negative' in BlendShapesOfSingleControl:
                SMN = BSDefinition['blendShapes'][BlendShapesOfSingleControl['negative'][len (BlendShapesOfSingleControl['negative']) - 1]]["value"]
            else: 
                SMN = 0

            connection = BSDefinition['blendShapes'][BlendShapesOfSingleControl['negative'][len (BlendShapesOfSingleControl['negative']) - 1]]["connection"]
            Side = self.getSideFromPrefix(prefix)

            control = self.NameConv.RMSetFromName(BSDefinition["control"] , Side, Token = "Side" )

            self.AddAttributes (control,  connection, SMN, SMX )
            #print BlendShapesOfSingleControl
            #pp.pprint (BlendShapeDict)
            #print "NewTargetIndex:%s"%(NewTargetIndex)
            AtLeastOne = False
            if  'positive' in BlendShapesOfSingleControl:
                for eachBS in reversed(BlendShapesOfSingleControl['positive']):
                    if cmds.objExists(prefix + eachBS):
                        cmds.blendShape(BlendShapeNode, edit=True, target = [blendShapeOriginalGeo, NewTargetIndex + 1, prefix + eachBS, float (abs(BSDefinition['blendShapes'][eachBS]["value"])) / 10.0 ])
                        NewTargetIndex += 1
                        AtLeastOne = True
                    else:
                        print " BS  %s not found on scene"%(prefix + eachBS)
                if AtLeastOne:
                    self.connectFromDefinition( BSDefinition,BlendShapesOfSingleControl['positive'][len(BlendShapesOfSingleControl['positive']) - 1], BlendShapeNode, prefix, 10)
            AtLeastOne = False
            if  'negative' in BlendShapesOfSingleControl:
                for eachBS in reversed(BlendShapesOfSingleControl['negative']):
                    if cmds.objExists(prefix + eachBS):
                        cmds.blendShape(BlendShapeNode, edit=True, target = [blendShapeOriginalGeo, NewTargetIndex + 1, prefix + eachBS, float (abs(BSDefinition['blendShapes'][eachBS]["value"])) / 10.0 ])
                        NewTargetIndex += 1
                        AtLeastOne = True 
                    else:
                        print " BS  %s not found on scene"%(prefix + eachBS)
                if AtLeastOne:
                    self.connectFromDefinition( BSDefinition,BlendShapesOfSingleControl['negative'][len(BlendShapesOfSingleControl['negative']) - 1], BlendShapeNode, prefix, -10)

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
    def CreateMulipleBlendShapes (self,BSDefinition, prefix, BSGroups,  blendShapeNode = None):
        self.FaceBlendShapeDic = None
        if BSDefinition[BSGroups]['Type'] == "blendShapeDefinition":
            #print ("STARTING :%s WITH PREFIX %s"%(BSGroups,prefix))
            if blendShapeNode == None :
                BSName = BSGroups + "BS"
                blendShapeOriginalGeo = cmds.duplicate(prefix + BSDefinition[BSGroups]['baseMesh'], name = self.NameConv.RMGetAShortName(BSDefinition[BSGroups]['baseMesh']) + BSGroups)
                Side = self.getSideFromPrefix(prefix)
                blendShapeOriginalGeo = self.NameConv.RMRenameNameInFormat( blendShapeOriginalGeo, System = "faceRig",Side = Side)
                cmds.blendShape(blendShapeOriginalGeo, name = BSName)
                BSName = self.NameConv.RMRenameNameInFormat(BSName, System = "faceRig", Side = Side )
            else :
                BSName = blendShapeNode
            for eachControl in BSDefinition [BSGroups]['order']:
                self.CreateBlendShapesByControl(BSName, eachControl, BSDefinition [BSGroups], prefix)
        return self.FaceBlendShapeDic

    def AddAttributes (self, Object, Attribute, SMN, SMX ):
        #print ("Adding Attribute:%s  to Object:%s Min:%s MAx %s"%(Attribute,Object,SMN,SMX))
        AttrList = cmds.listAttr(Object)
        if Attribute not in AttrList:
            cmds.addAttr(Object, at="float", ln = Attribute ,hnv = 1, hxv = 1, h = 0, k = 1, smn = SMN, smx = SMX)

    def linkBlendShapesAttr (self, Object, AttributesDefinition, BSNode):
        blendShapeTargetDic = self.RMblendShapeTargetDic(BSNode)
        #for eachAttr in AttributesDefinition:

    def RMblendShapeTargetDic (self, BSNode):
        #AliasNames=cmds.listAttr((BSNode +".weight"),m=True);
        InputTargetGroup=cmds.getAttr ((BSNode+".inputTarget[0].inputTargetGroup"),mi=True);
        BlendShapeDic={}
        for eachTarget in InputTargetGroup:
            AliasName=cmds.listAttr((BSNode + ".weight[" + str(eachTarget) + "]"),m=True);
            BlendShapeDic[str(AliasName[0])] = {}
            BlendShapeDic[str(AliasName[0])]["TargetGroup"] = eachTarget
            Items = cmds.getAttr ((BSNode+".inputTarget[0].inputTargetGroup["+str(eachTarget)+"].inputTargetItem"), mi = True)
            BlendShapeDic[str(AliasName[0])]["Items"] = Items
        return BlendShapeDic

    def linkJointDefinition (self, Side, jointLinkDefinition):
        control = jointLinkDefinition['control']
        if Side in ["LF","RH"]:
            control = self.NameConv.RMSetFromName(jointLinkDefinition['control'], Side, Token = 'Side')

        if cmds.objExists( control):
            for eachAttribute in jointLinkDefinition['order']:
                jointsList = self.returnJointsByControl( eachAttribute, jointLinkDefinition['joints'])
                for eachJoint in jointsList:
                    JointName = eachJoint
                    if Side in [ "LF", "RH"]:
                        JointName = self.NameConv.RMSetFromName(eachJoint, Side, Token = 'Side')
                    if cmds.objExists(JointName):
                        
                        if jointLinkDefinition['joints'][eachJoint]['value'] == None:
                            cmds.connectAttr ('%s.%s'%(control,jointLinkDefinition['joints'][eachJoint]['connection'] ), '%s.%s'%(JointName, jointLinkDefinition['joints'][eachJoint]['inputPlug']),force=True)
                        else:
                            self.AddAttributes ( control, eachAttribute, jointLinkDefinition['attributes'][eachAttribute]['min'], jointLinkDefinition['attributes'][eachAttribute]['max'])
                            RMRigTools.RMConnectWithLimits('%s.%s'%(control,jointLinkDefinition['joints'][eachJoint]['connection'] ), '%s.%s'%(JointName, jointLinkDefinition['joints'][eachJoint]['inputPlug']), jointLinkDefinition['joints'][eachJoint]['value'])
                    else:
                        print "Joint object doesnt exists:%s"%JointName
        else:
            print "Control object doesnt exists:%s"%control
            control = self.NameConv.RMSetFromName(jointLinkDefinition['control'], Side, Token = 'Side')
#if __name__=="__main__":
#    Manager = BSManager()
#    Manager.AppyBlendShapeDefinition( SkinedJoints)