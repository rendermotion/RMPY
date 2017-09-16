FacialRig = {'incisibus':{'Type'        : "blendShapeDefinition",
                        'isSymetrical': False,
                        "baseMesh"    : "Character",
                        'control'     : 'C_Incisibus00_RIG_CTRL',
                        'blendShapes' :{'Incisibus'      :{"connection":"translateY"    ,"value": 10}
                                        },
                        'attributes' : {'translateY':{"type": "float", "min": 0, "max": 10}},
                        'order':['translateY']
                        },
            'jawL':{'Type'        : "blendShapeDefinition",
                   'isSymetrical': False,
                   "baseMesh"    : "Character",
                   'control'     : 'C_JawOpen00_RIG_CTRL',
                   'blendShapes' :{'RWide'      :{"connection":"translateX"    ,"value": 10},
                                   'RNarrow'    :{"connection":"translateX"    ,"value": -10}
                                   },
                   'attributes' : {'translateX':{"type": "float", "min": -10, "max": 10}},
                   'order':['translateX']},
            'jawR':{'Type'        : "blendShapeDefinition",
                   'isSymetrical': False,
                   "baseMesh"    : "Character",
                   'control'     : 'C_JawOpen00_RIG_CTRL',
                   'blendShapes' :{'LWide'      :{"connection":"translateX"    ,"value": 10},
                                   'LNarrow'    :{"connection":"translateX"    ,"value": -10}
                                   },
                   'attributes' : {'translateX':{"type": "float", "min": -10, "max": 10}},
                   'order':['translateX']},
            'UpperLidEyeCls':{'Type'        : "blendShapeDefinition",
                        'isSymetrical': True,
                        "baseMesh"    : "Character",
                        'control'     : 'R_eyeCls00_RIG_CTRL',
                        'blendShapes' :{
                                        'EyeCls'      :{"connection": "translateY"    ,"value": 10},
                                        'Eye3QrtCls'  :{"connection": "translateY"    ,"value": 7.5},
                                        'EyeHalfCls'  :{"connection": "translateY"    ,"value": 5},
                                        'EyeQrtCls'   :{"connection": "translateY"    ,"value": 2.5}
                                       },
                        'attributes' : {'translateY':{"type": "float", "min": 0, "max": 10}},
                        'order':['translateY']},
            'LowLidEyeCls':{'Type'        : "blendShapeDefinition",
                        'isSymetrical': True,
                        "baseMesh"    : 'Character',
                        'control'     : 'R_LowLidEyeCls00_RIG_CTRL',
                        'blendShapes' :{
                                        'LowLidEyeCls'      :{"connection":"translateY"    ,"value": 10},
                                        'LowLidEye3QrtCls'  :{"connection":"translateY"    ,"value": 7.5},
                                        'LowLidEyeHalfCls'  :{"connection":"translateY"    ,"value": 5},
                                        'LowLidEyeQrtCls'   :{"connection":"translateY"    ,"value": 2.5}
                                       },
                        'attributes' :{'translateY': {"type": "float", "min": 0, "max": 10}},
                        'order':['translateY']
                    },
            'BrowInOut': {'Type': "blendShapeDefinition",
                          'isSymetrical': True,
                          "baseMesh": "Character",
                          'control': 'R_BrowInOut00_RIG_CTRL',
                          'blendShapes': {
                              'BrowOutUp': {"connection": "translateX", "value": 10},
                              'BrowOutDn': {"connection": "translateX", "value": -10},
                              'BrowInUp' : {"connection": "translateY", "value": 10},
                              'BrowInDn' : {"connection": "translateY", "value": -10}
                          }
            }
            }
