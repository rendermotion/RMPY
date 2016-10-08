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

def invertCurrentPaintTargetWeights(ObjectName, index):
    cmds.setAttr("%s.inputTarget[0].paintTargetIndex"%ObjectName, index)
    weights = cmds.getAttr("%s.inputTarget[0].paintTargetWeights"%ObjectName)
    newWeights = []
    index=0
    for i in weights[0]:
        cmds.setAttr("%s.inputTarget[0].paintTargetWeights[%s]"% (ObjectName,index),float(1.0)- i)
        index+=1
    weights = cmds.getAttr("%s.inputTarget[0].paintTargetWeights"%ObjectName)

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
            if BSDefinition[eachBSGroup]["isSymetrical"] == True:
                self.CreateMulipleBlendShapes (BSDefinition, "L", blendShapeNode)
                self.CreateMulipleBlendShapes (BSDefinition, "R", blendShapeNode)
            else:
                self.CreateMulipleBlendShapes (BSDefinition, "")

    def ReturnBlendShapesByControl(self,connectionPlug, BSDict):
        orderedList = {'positive':[] , 'negative':[]}
        for eachBlendShape in BSDict:
            if BSDict[eachBlendShape]["connection"] == connectionPlug:
                
                if BSDict[eachBlendShape]["value"] > 0:
                    sign = 'positive'
                else:
                    sign = 'negative'

                if len (orderedList[sign]) == 0:
                    print "Toinsert0:%s"%eachBlendShape
                    orderedList[sign].append(eachBlendShape)
                else:
                    print "Toinsert1:%s"%eachBlendShape
                    index = 0
                    for blendShapes in orderedList[sign]:
                        if (abs(BSDict[eachBlendShape]['value']) > abs(BSDict[blendShapes]['value'])):
                            index += 1
                        else:
                            break
                    orderedList[sign].insert(index,eachBlendShape)
                pass
        return orderedList

    def CreateBlendShapesByControl (self, BlendShapeNode, Plug , BSDefinition, prefix):
        ''' This function adds new blendShapes to a node(BlendShapeNode) based on a plug,
        first it createds a dictionary with  self.ReturnBlendShapesByControl function, 
        This dictionary is then match againts the BS definition and the negative BS are added to a single BS
        and the positive ones are added to a new one.'''
        if cmds.objExists(prefix + eachBS):
            BlendShapesOfSingleControl = self.ReturnBlendShapesByControl(Plug, BSDefinition["blendShapes"])
            blendShapeOriginalGeo = self.findMeshByBlendShapeNode(BlendShapeNode)
            BlendShapeDict = self.RMblendShapeTargetDic(BlendShapeNode)
            NewTargetIndex = len(BlendShapeDict)
            for eachBS in reversed(BlendShapesOfSingleControl['positive']):
                if cmds.objExists(prefix + eachBS):
                    cmds.blendShape(BSName, edit=True, target = [blendShapeOriginalGeo, NewTargetIndex, prefix + eachBS, float (abs(BSDefinition[BSGroups]['blendShapes'][eachBlendShape]["value"])) / 10.0 ])
                else:
                    print " BS  %s not found on scene"%(prefix + eachBS)
            for eachBS in reversed(BlendShapesOfSingleControl['negative ']):
                if cmds.objExists(prefix + eachBS):
                    cmds.blendShape(BSName, edit=True, target = [blendShapeOriginalGeo, NewTargetIndex, prefix + eachBS, float (abs(BSDefinition[BSGroups]['blendShapes'][eachBlendShape]["value"])) / 10.0 ])
                else:
                    print " BS  %s not found on scene"%(prefix + eachBS)

    def findMeshByBlendShapeNode (self,BSNode):
        mesh = cmds.listConnections ("%s.outputGeometry[0]"%BSNode, type='mesh')
        return mesh[0]

    def CreateMulipleBlendShapes (self,BSDefinition, prefix, blendShapeNode = None):
        self.FaceBlendShapeDic = None
        for BSGroups in BSDefinition:
            if BSDefinition[BSGroups]['Type'] == "blendShapeDefinition":
                BSName = BSGroups + "BS"
                if not blendShapeNode:
                    blendShapeOriginalGeo = cmds.duplicate(prefix + BSDefinition[BSGroups]['baseMesh'], name = BSDefinition[BSGroups]['baseMesh'] + BSGroups)
                    if prefix == "":
                        Side = "MD"
                    elif prefix=="R":
                        Side = "RH"
                    elif prefix=="L":
                        Side = "LF"
                    blendShapeOriginalGeo = self.NameConv.RMRenameNameInFormat( blendShapeOriginalGeo, System = "faceRig",Side = Side)
                    cmds.blendShape(blendShapeOriginalGeo, name = BSName)
                    BSName = self.NameConv.RMRenameNameInFormat(BSName, System = "faceRig", Side = Side )
                else :
                    BSName = blendShapeNode
                for eachControl in BSDefinition [BSGroups]['order']:
                    CreateBlendShapesByControl(BSName, eachControl, BSDefinition [BSGroups], prefix)
        return self.FaceBlendShapeDic

    def AddAttributes (self, Object, AttributesDefinition):
        for keys in AttributesDefinition:
            cmds.addAttr(Object, at="float", ln = keys,     hnv = 1, hxv = 1, h = 0, k = 1, smn = 0, smx = 10)

    def linkBlendShapesAttr (self, Object, AttributesDefinition, BSNode):
        blendShapeTargetDic = self.RMblendShapeTargetDic(BSNode)
        #for eachAttr in AttributesDefinition:

    def RMblendShapeTargetDic (self, BSNode):
        #AliasNames=cmds.listAttr((BSNode +".weight"),m=True);
        InputTargetGroup=cmds.getAttr ((BSNode+".inputTarget[0].inputTargetGroup"),mi=True);
        BlendShapeDic={}
        for eachTarget in InputTargetGroup:
            AliasName=cmds.listAttr((BSNode +".weight["+str(eachTarget)+"]"),m=True);
            BlendShapeDic[str(AliasName[0])]={}
            BlendShapeDic[str(AliasName[0])]["TargetGroup"] = eachTarget
            Items = cmds.getAttr ((BSNode+".inputTarget[0].inputTargetGroup["+str(eachTarget)+"].inputTargetItem"), mi=True)
            BlendShapeDic[str(AliasName[0])]["Items"] = Items
        return BlendShapeDic

    def RigBlendShapesByDefinition():
        pass
    def linkJointDefinition (self, object, ):
        

BlendShapes={
            "lidShapes":{
                    "Diverge":{
                                'Type':"blendShapeDefinition",
                                "isSymetrical":True,
                                "baseMesh"    : "Crystalline",

                                "control"     : "Character_LF_EyeLidShapes00_ctr_facialRig",

                                "attributes"  :{'PupilDivergeUD':{"type": "float", "min":-10, "max":10},
                                                'PupilDivergeLR':{"type": "float", "min":-10, "max":10}},

                                "blendShapes" :{'PupilDivergeUp'      : {"connection":"PupilDivergeUD"  ,"value":  10},
                                                'PupilDivergeDn'      : {"connection":"PupilDivergeUD"  ,"value": -10},
                                                'PupilDivergeLf'      : {"connection":"PupilDivergeLR"  ,"value":  10},
                                                'PupilDivergeRh'      : {"connection":"PupilDivergeLR"  ,"value": -10}},
                                'order'       :['PupilDivergeUD' , 'PupilDivergeLR']},
                    
                    "lid":{ 'Type'          : 'jointPlugDefinition',
                            'joints'        : { "EyeUpperLid00_jnt_rig":{'plug'   :[{"connection":"UpLidUD" , "inputPlug":"rotateY", "limmits":[[-10,-16],[0,0],[10,16]]} ],
                                                                         'control':  'Character_LF_EyeLidShapes00_ctr_facialRig'},
                                                "EyeLowerLid00_jnt_rig":{'plug'   :[{"connection":"LowLidUD", "inputPlug":"rotateY", "limmits":[[-10,-16],[0,0],[10,16]]} ],
                                                                         'control':  'Character_LF_EyeLidShapes00_ctr_facialRig'},
                                                "EyeLidSpin00_grp_rig" :{'plug'   :[{"connection":"spin"    , "inputPlug":"rotateX", "limmits":[[-10,-16],[0,0],[10,16]]} ],
                                                                         'control':  'Character_LF_EyeLidShapes00_ctr_facialRig'}},
                            'defaultControl':'Character_LF_EyeLidShapes00_ctr_facialRig'},
                            'attributes'    :{'PupilDivergeUD':{"type": "float", "min":-10, "max":10},
                                              'PupilDivergeLR':{"type": "float", "min":-10, "max":10}}
                           },

                    "mouth":{
                             'Type'   : 'jointPlugDefinition',
                             "joints" :{'LF_MouthMiddleUp_jnt_rig':{'plug'  :[{"connection" :"UD"    , "inputPlug":"translateY", "limmits":[[-10,-16],[0,0],[10,16]]},
                                                                              {"connection" :"LR"    , "inputPlug":"translateX", "limmits":[[-10,-16],[0,0],[10,16]]},
                                                                              {"connection" :"FB"    , "inputPlug":"translateZ", "limmits":[[-10,-16],[0,0],[10,16]]},
                                                                              {"connection" :"Twist" , "inputPlug":"translateZ", "limmits":[[-10,-16],[0,0],[10,16]]}],
                                                                    'control': 'Character_MD_MidUpLip00_ctr_facialRig'}
                            }
                    }
            }
#                                       'LF_MouthMiddleDn_jnt_rig':
#                                       'LF_MouthCorner_jnt_rig'  :
#                                       'LF_MouthUp_jnt_rig'      :
#                                       'LF_MouthDn_jnt_rig'      :


Manager = BSManager()
#Manager.AppyBlendShapeDefinition(BlendShapes["lidShapes"])
#print Manager.ReturnBlendShapesByControl('PupilDivergeUD', BlendShapes["lidShapes"]["Diverge"]["blendShapes"])
print Manager.findMeshByBlendShapeNode("Character_RH_DivergeBS00_bs_faceRig")
#pp.pprint(Manager.FaceBlendShapeDic)