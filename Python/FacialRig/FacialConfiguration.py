
Connections = {
    "lidShapes":{
                "baseMesh": "Character" ,

                "control" : "Character_LF_EyeLidShapes00_ctr_facialRig" ,

                "blendShapes":{
                            "UpperEyeLidSpinCW" : {"connection":"UpLidSpin"       ,"value":  10},
                            "UpperEyeLidSpinCCW": {"connection":"UpLidSpin"       ,"value": -10},
                            "LowerEyeLidSpinCW" : {"connection":"LowLidSpin"      ,"value":  10},
                            "LowerEyeLidSpinCCW": {"connection":"LowLidSpin"      ,"value": -10},
                            "EyeSpinCCW"        : {"connection":"Spin"            ,"value":  10},
                            "EyeSpinCW"         : {"connection":"Spin"            ,"value": -10},
                
                            "Bulge"             : {"connection":"Bulge"           ,"value":  10},
                            "UpperSquint"       : {"connection":"UpperSquint"     ,"value":  10},
                            "LowerSquint"       : {"connection":"LowerSquint"     ,"value":  10},
                            "UpLidInnerUp"      : {"connection":"UpLidInnerUD"    ,"value":  10},
                            "UpLidInnerDn"      : {"connection":"UpLidInnerUD"    ,"value": -10},
                            "UpLidMidUp"        : {"connection":"UpLidMidUD"      ,"value":  10},
                            "UpLidMidDown"      : {"connection":"UpLidMidUD"      ,"value": -10},
                            "UpLidOuterUp"      : {"connection":"UpLidOuterUD"    ,"value":  10},
                            "UpLidOuterDown"    : {"connection":"UpLidOuterUD"    ,"value": -10},

                            "LowLidInnerUp"     : {"connection":"LowLidInnerUD"   ,"value":  10},
                            "LowLidInnerDown"   : {"connection":"LowLidInnerUD"   ,"value": -10},
                            "LowLidMidUp"       : {"connection":"LowLidMidUD"     ,"value":  10},
                            "LowLidMidDown"     : {"connection":"LowLidMidUD"     ,"value": -10},
                            "LowLidOuterUp"     : {"connection":"LowLidOuterUD"   ,"value":  10},
                            "LowLidOuterDown"   : {"connection":"LowLidOuterUD"   ,"value": -10},
                            
                            "CornerInnerUp"     : {"connection":"CornerOuterUD"   ,"value":  10},
                            "CornerOuterUp"     : {"connection":"CornerOuterUD"   ,"value":  10},
                
                            "UpLidDn"           : {"connection":"UpLidUD"         ,"value":  10},
                            "UpLidDnHalf"       : {"connection":"UpLidUD"         ,"value":   5},
                            "UpLidUp"           : {"connection":"UpLidUD"         ,"value": -10},
                            "LowLidUp"          : {"connection":"LowLidUD"        ,"value":  10},
                            "LowLidUpHalf"      : {"connection":"LowLidUD"        ,"value":   5},
                            "LowLidDn"          : {"connection":"LowLidUD"        ,"value": -10}},
                "skinJoints":{
                            "EyeUpperLid00_jnt_Rig":{"connection":"UpLidUD" , "inputPlug":"rotateY"},
                            "EyeLowerLid00_jnt_Rig":{"connection":"LowLidUD", "inputPlug":"rotateY"},
                            "EyeLidSpin00_grp_Rig" :{"connection":"spin"    , "inputPlug":"rotateX"}},

                "attributes" : {
                                 'UpLidUD'       :{"type": "float", "min":-10, "max":10},
                                 'LowLidUD'      :{"type": "float", "min":-10, "max":10},
                                 'UpLidSpin'     :{"type": "float", "min":-10, "max":10}, 
                                 'LowLidSpin'    :{"type": "float", "min":-10, "max":10},
                                 'Spin'          :{"type": "float", "min":-10, "max":10},
                                 'UpLidInOut'    :{"type": "float", "min":-10, "max":10},
                                 'LowLidInOut'   :{"type": "float", "min":-10, "max":10},
                                 'Bulge'         :{"type": "float", "min":  0, "max":10}, 
                                 'UpperSquint'   :{"type": "float", "min":  0, "max":10}, 
                                 'LowerSquint'   :{"type": "float", "min":  0, "max":10},
                                 'UpLidInnerUD'  :{"type": "float", "min":-10, "max":10}, 
                                 'UpLidMidUD'    :{"type": "float", "min":-10, "max":10}, 
                                 'UpLidOuterUD'  :{"type": "float", "min":-10, "max":10}, 
                                 'LowLidInnerUD' :{"type": "float", "min":-10, "max":10}, 
                                 'LowLidMidUD'   :{"type": "float", "min":-10, "max":10}, 
                                 'LowLidOuterUD' :{"type": "float", "min":-10, "max":10}, 
                                 'CornerInnerUD' :{"type": "float", "min":  0, "max":10}, 
                                 'CornerOuterUD' :{"type": "float", "min":  0, "max":10}},

                'order':    ['UpLidUD','LowLidUD','UpLidSpin','LowLidSpin','Spin','UpLidInOut','LowLidInOut',
                             'Bulge','UpperSquint','LowerSquint','UpLidInnerUD','UpLidMidUD',
                             'UpLidOuterUD','LowLidInnerUD','LowLidMidUD' ,'LowLidOuterUD','CornerInnerUD',
                             'CornerOuterUD']
                },
    "EyeBallPupil":{"baseMesh": "LEyeBall",
                    "control" : "Character_LF_EyeLidShapes00_ctr_facialRig",
                    "blendShapes" : {'irisContract'      : {"connection":"Iris"            ,"value": -10},
                                     'irisExpand'        : {"connection":"Iris"            ,"value":  10},
                                     'PupilContract'     : {"connection":"Pupil"           ,"value": -10},
                                     'PupilExpand'       : {"connection":"Pupil"           ,"value":  10}},

                    "attributes":{'Iris'          :{"type": "float", "min":-10, "max":10},
                                  'Pupil'         :{"type": "float", "min":-10, "max":10}},            

                    'order': ['Iris','Pupil'] },

    "CristallineDiverge":{
                    "baseMesh": "Crystalline",

                    "control" : "Character_LF_EyeLidShapes00_ctr_facialRig",

                    "attributes":{  'PupilDivergeUD':{"type": "float", "min":-10, "max":10},
                                    'PupilDivergeLR':{"type": "float", "min":-10, "max":10}},

                    "blendShapes":{ 'PupilDivergeUp'    : {"connection":"PupilDivergeUD"  ,"value":  10},
                                    'PupilDivergeDn'    : {"connection":"PupilDivergeUD"  ,"value": -10},
                                    'PupilDivergeLf'    : {"connection":"PupilDivergeLR"  ,"value":  10},
                                    'PupilDivergeRh'    : {"connection":"PupilDivergeLR"  ,"value": -10}},
                     'order': ['PupilDivergeUD','PupilDivergeLR']
                }
}








###ProvedConfig





BlendShapes = {"lidShapes":{
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
                                'order'       :['PupilDivergeUD' , 'PupilDivergeLR']
                            },
                    
                    "lid":{ 'Type'          : 'jointPlugDefinition',
                            'joints'        : { "EyeUpperLid00_jnt_rig":{'plug'   :[{"connection":"UpLidUD" , "inputPlug":"rotateY", "limmits":[[-10,-16],[0,0],[10,16]]} ],
                                                                         'control':  'Character_LF_EyeLidShapes00_ctr_facialRig'},
                                                "EyeLowerLid00_jnt_rig":{'plug'   :[{"connection":"LowLidUD", "inputPlug":"rotateY", "limmits":[[-10,-16],[0,0],[10,16]]} ],
                                                                         'control':  'Character_LF_EyeLidShapes00_ctr_facialRig'},
                                                "EyeLidSpin00_grp_rig" :{'plug'   :[{"connection":"spin"    , "inputPlug":"rotateX", "limmits":[[-10,-16],[0,0],[10,16]]} ],
                                                                         'control':  'Character_LF_EyeLidShapes00_ctr_facialRig'}
                                              },
                            'defaultControl':'Character_LF_EyeLidShapes00_ctr_facialRig',
                            'attributes'    :{'PupilDivergeUD':{"type": "float", "min":-10, "max":10},
                                              'PupilDivergeLR':{"type": "float", "min":-10, "max":10}}
                           },

                    "mouth":{
                             'Type'   : 'jointPlugDefinition',
                             "joints" :{'LF_MouthMiddleUp_jnt_rig':{'plug'  :[{"connection" :"UD"    , "inputPlug":"translateY", "limmits":[[-10,-16],[0,0],[10,16]]},
                                                                              {"connection" :"LR"    , "inputPlug":"translateX", "limmits":[[-10,-16],[0,0],[10,16]]},
                                                                              {"connection" :"FB"    , "inputPlug":"translateZ", "limmits":[[-10,-16],[0,0],[10,16]]},
                                                                              {"connection" :"Twist" , "inputPlug":"translateZ", "limmits":[[-10,-16],[0,0],[10,16]]}],
                                                                    'control': 'Character_MD_MidUpLip00_ctr_facialRig'
                                                                    }
                                        }
                            },
                                        "lipUpperMidSecondary" :{
                                'Type' : "blendShapeDefinition",
                                "isSymetrical":True,
                                "baseMesh"    : "Character_MD_phoneticsBSphonetics00_msh_rig",
                                "control"     : "Character_RH_MidUpLip00_ctr_facialRig",
                                "attributes"  :{"UD"     :{"type": "float", "min":-10, "max":10},
                                                "FB"     :{"type": "float", "min":-10, "max":10}},
                                "blendShapes" :{'UpperMidUp' : {"connection":"UD"  ,"value":  10},
                                                'UpperMidDn' : {"connection":"UD"  ,"value": -10},
                                                'UpperMidFn' : {"connection":"FB"  ,"value":  10},
                                                'UpperMidBk' : {"connection":"FB"  ,"value": -10}},
                                'order'       :['UD' , 'FB']
                                },
                    "lipLowMidSecondary" :{
                                'Type' : "blendShapeDefinition",
                                "isSymetrical":True,
                                "baseMesh"    : "Character_MD_phoneticsBSphonetics00_msh_rig",
                                "control"     : "Character_RH_MidLowLip00_ctr_facialRig",
                                "attributes"  :{"UD"     :{"type": "float", "min":-10, "max":10},
                                                "FB"     :{"type": "float", "min":-10, "max":10}},
                                "blendShapes" :{'LowMidUp' : {"connection":"UD"  ,"value":  10},
                                                'LowMidDn' : {"connection":"UD"  ,"value": -10},
                                                'LowMidFn' : {"connection":"FB"  ,"value":  10},
                                                'LowMidBk' : {"connection":"FB"  ,"value": -10}},
                                'order'       :['UD' , 'FB']
                                },
                    "LipCornerSecondary" :{
                                'Type' : "blendShapeDefinition",
                                "isSymetrical":True,
                                "baseMesh"    : "Character_MD_phoneticsBSphonetics00_msh_rig",
                                "control"     : "Character_RH_CornerLip00_ctr_facialRig",
                                "attributes"  :{"UD"     :{"type": "float", "min":-10, "max":10},
                                                "FB"     :{"type": "float", "min":-10, "max":10}},
                                "blendShapes" :{'CornerUp' : {"connection":"UD"  ,"value":  10},
                                                'CornerDn' : {"connection":"UD"  ,"value": -10},
                                                'CornerFn' : {"connection":"FB"  ,"value":  10},
                                                'CornerBk' : {"connection":"FB"  ,"value": -10}},
                                'order'       :['UD' , 'FB']
                                },
                    "LipUpperSecondary" :{
                                'Type' : "blendShapeDefinition",
                                "isSymetrical":False,
                                "baseMesh"    : "Character_MD_phoneticsBSphonetics00_msh_rig",
                                "control"     : "Character_MD_MidLowLip00_ctr_facialRig",
                                "attributes"  :{"UD"     :{"type": "float", "min":-10, "max":10},
                                                "FB"     :{"type": "float", "min":-10, "max":10}},
                                "blendShapes" :{'LowUp' : {"connection":"UD"  ,"value":  10},
                                                'LowDn' : {"connection":"UD"  ,"value": -10},
                                                'LowFn' : {"connection":"FB"  ,"value":  10},
                                                'LowBk' : {"connection":"FB"  ,"value": -10}},
                                'order'       :['UD' , 'FB']
                                },
                    "LipLowSecondary" :{
                                'Type' : "blendShapeDefinition",
                                "isSymetrical":False,
                                "baseMesh"    : "Character_MD_phoneticsBSphonetics00_msh_rig",
                                "control"     : "Character_MD_MidUpLip00_ctr_facialRig",
                                "attributes"  :{"UD"     :{"type": "float", "min":-10, "max":10},
                                                "LR"     :{"type": "float", "min":-10, "max":10}},
                                "blendShapes" :{'UpperUp' : {"connection":"UD"  ,"value":  10},
                                                'UpperDn' : {"connection":"UD"  ,"value": -10},
                                                'UpperFn' : {"connection":"FB"  ,"value":  10},
                                                'UpperBk' : {"connection":"FB"  ,"value": -10}},
                                'order'       :['UD' , 'LR']
                                }

                    }
        }