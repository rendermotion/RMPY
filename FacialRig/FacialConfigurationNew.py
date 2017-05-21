lidShapes = {"lidShapes": {
    'baseMesh': 'Character',
    'Type': 'blendShapeDefinition',
    'isSymetrical': True,
    "baseMesh": "Character",
    'control': 'Character_LF_EyeLidShapes00_ctr_facialRig',
    'blendShapes': {

        # "EyeSpinCCW"       : {"connection": "Spin"            ,"value":  10},
        # "EyeSpinCW"        : {"connection": "Spin"            ,"value": -10},
        "Bulge": {"connection": "Bulge", "value": 10},

    },
    "attributes": {

        # 'Spin'          :{"type": "float", "min": -10, "max":10},
        # 'UpLidInOut'    :{"type": "float", "min": -10, "max":10},
        # 'LowLidInOut'   :{"type": "float", "min": -10, "max":10},
        'Bulge': {"type": "float", "min": 0, "max": 10}

    },

    'order': ['Bulge']
},
    "lidShapesUp": {
        'baseMesh': 'Character',
        'Type': 'blendShapeDefinition',
        'isSymetrical': True,
        'baseMesh': "Character",
        'control': 'Character_LF_EyeLidUpShapes00_ctr_facialRig',

        'blendShapes': {
            "UpLidDn": {"connection": "UpLidUD", "value": 10},
            "UpLidDnHalf": {"connection": "UpLidUD", "value": 5},
            "UpLidUp": {"connection": "UpLidUD", "value": -10},

            "UpperEyeLidSpinCW": {"connection": "UpLidSpin", "value": 10},
            "UpperEyeLidSpinCCW": {"connection": "UpLidSpin", "value": -10},

            "UpperSquint": {"connection": "UpperSquint", "value": 10},

            "UpLidInnerUp": {"connection": "UpLidInnerUD", "value": 10},
            "UpLidInnerDn": {"connection": "UpLidInnerUD", "value": -10},
            "UpLidMidUp": {"connection": "UpLidMidUD", "value": 10},
            "UpLidMidDn": {"connection": "UpLidMidUD", "value": -10},
            "UpLidOuterUp": {"connection": "UpLidOuterUD", "value": 10},
            "UpLidOuterDn": {"connection": "UpLidOuterUD", "value": -10}
        },
        'attributes': {
            'UpLidUD': {"type": "float", "min": -10, "max": 10},
            'UpLidSpin': {"type": "float", "min": -10, "max": 10},

            'UpperSquint': {"type": "float", "min": 0, "max": 10},

            'UpLidInnerUD': {"type": "float", "min": -10, "max": 10},
            'UpLidMidUD': {"type": "float", "min": -10, "max": 10},
            'UpLidOuterUD': {"type": "float", "min": -10, "max": 10},
        },
        'order': ['UpLidUD', 'UpLidSpin', 'UpperSquint', 'UpLidInnerUD', 'UpLidMidUD', 'UpLidOuterUD']
    },

    "lidShapesLow": {
        'baseMesh': 'Character',
        'Type': 'blendShapeDefinition',
        'isSymetrical': True,
        'baseMesh': "Character",
        'control': 'Character_LF_EyeLidLowShapes00_ctr_facialRig',
        'blendShapes': {

            "LowLidUp": {"connection": "LowLidUD", "value": 10},
            "LowLidUpHalf": {"connection": "LowLidUD", "value": 5},
            "LowLidDn": {"connection": "LowLidUD", "value": -10},

            "LowerEyeLidSpinCW": {"connection": "LowLidSpin", "value": 10},
            "LowerEyeLidSpinCCW": {"connection": "LowLidSpin", "value": -10},

            "LowerSquint": {"connection": "LowerSquint", "value": 10},

            "LowLidInnerUp": {"connection": "LowLidInnerUD", "value": 10},
            "LowLidInnerDn": {"connection": "LowLidInnerUD", "value": -10},
            "LowLidMidUp": {"connection": "LowLidMidUD", "value": 10},
            "LowLidMidDn": {"connection": "LowLidMidUD", "value": -10},
            "LowLidOuterUp": {"connection": "LowLidOuterUD", "value": 10},
            "LowLidOuterDn": {"connection": "LowLidOuterUD", "value": -10}
        },
        'attributes': {
            'LowLidUD': {"type": "float", "min": -10, "max": 10},
            'LowLidSpin': {"type": "float", "min": -10, "max": 10},

            'LowerSquint': {"type": "float", "min": 0, "max": 10},

            'LowLidInnerUD': {"type": "float", "min": -10, "max": 10},
            'LowLidMidUD': {"type": "float", "min": -10, "max": 10},
            'LowLidOuterUD': {"type": "float", "min": -10, "max": 10}
        },
        'order': ['LowLidUD', 'LowLidSpin', 'LowerSquint', 'LowLidInnerUD', 'LowLidMidUD', 'LowLidOuterUD']
    },
    "lidShapesOut": {
        'baseMesh': 'Character',
        'Type': 'blendShapeDefinition',
        'isSymetrical': True,
        'baseMesh': "Character",
        'control': 'Character_LF_EyeLidOutShapes00_ctr_facialRig',
        'blendShapes': {"CornerOuterUp": {"connection": "CornerOuterUD", "value": 10}},
        'attributes': {'CornerOuterUD': {"type": "float", "min": 0, "max": 10}},
        'order': ['CornerOuterUD']
    },
    "lidShapesIn": {
        'baseMesh': 'Character',
        'Type': 'blendShapeDefinition',
        'isSymetrical': True,
        'baseMesh': "Character",
        'control': 'Character_LF_EyeLidInShapes00_ctr_facialRig',
        'blendShapes': {"CornerInnerUp": {"connection": "CornerInnerUD", "value": 10}},
        'attributes': {'CornerInnerUD': {"type": "float", "min": 0, "max": 10}},
        'order': ['CornerInnerUD']
    }
}
EyeBallPupil = {"EyeBallL": {'Type': 'blendShapeDefinition',
                             # 'baseMesh'     : 'C_HMn_SNW_Eye_L_MF',
                             'baseMesh': 'C_HMn_SAC_eye_L_MF',
                             'isSymetrical': False,
                             'control': 'Character_LF_EyeLidShapes00_ctr_facialRig',
                             'blendShapes': {'LirisContract': {"connection": "Iris", "value": -10},
                                             'LirisExpand': {"connection": "Iris", "value": 10},
                                             'LPupilContract': {"connection": "Pupil", "value": -10},
                                             'LPupilExpand': {"connection": "Pupil", "value": 10}},
                             'attributes': {'Iris': {"type": "float", "min": -10, "max": 10},
                                            'Pupil': {"type": "float", "min": -10, "max": 10}},
                             'order': ['Iris', 'Pupil']},
                "EyeBallR": {'Type': 'blendShapeDefinition',
                             # 'baseMesh'     : 'C_HMn_SNW_Eye_R_MF',
                             'baseMesh': 'C_HMn_SAC_eye_R_MF',

                             'isSymetrical': False,
                             'control': 'Character_RH_EyeLidShapes00_ctr_facialRig',
                             'blendShapes': {'RirisContract': {"connection": "Iris", "value": -10},
                                             'RirisExpand': {"connection": "Iris", "value": 10},
                                             'RPupilContract': {"connection": "Pupil", "value": -10},
                                             'RPupilExpand': {"connection": "Pupil", "value": 10}},
                             'attributes': {'Iris': {"type": "float", "min": -10, "max": 10},
                                            'Pupil': {"type": "float", "min": -10, "max": 10}},
                             'order': ['Iris', 'Pupil']}
                }

Cristaline = {"DivergeLf": {
    'Type': "blendShapeDefinition",
    "isSymetrical": False,
    # "baseMesh"    : 'C_HMn_SNW_Crystalline_L_MF',
    "baseMesh": 'C_HMn_SAC_crystalline_L_MF',

    "control": "Character_LF_EyeLidShapes00_ctr_facialRig",

    "attributes": {'PupilDivergeUD': {"type": "float", "min": -10, "max": 10},
                   'PupilDivergeLR': {"type": "float", "min": -10, "max": 10}},

    "blendShapes": {'LPupilDivergeUp': {"connection": "PupilDivergeUD", "value": 10},
                    'LPupilDivergeDn': {"connection": "PupilDivergeUD", "value": -10},
                    'LPupilDivergeLf': {"connection": "PupilDivergeLR", "value": 10},
                    'LPupilDivergeRh': {"connection": "PupilDivergeLR", "value": -10}},
    'order': ['PupilDivergeUD', 'PupilDivergeLR']},
    "DivergeRh": {
        'Type': "blendShapeDefinition",
        "isSymetrical": False,
        # "baseMesh"    : 'C_HMn_SNW_Crystalline_R_MF',

        "baseMesh": 'C_HMn_SAC_crystalline_R_MF',

        "control": "Character_RH_EyeLidShapes00_ctr_facialRig",

        "attributes": {'PupilDivergeUD': {"type": "float", "min": -10, "max": 10},
                       'PupilDivergeLR': {"type": "float", "min": -10, "max": 10}},

        "blendShapes": {'RPupilDivergeUp': {"connection": "PupilDivergeUD", "value": 10},
                        'RPupilDivergeDn': {"connection": "PupilDivergeUD", "value": -10},
                        'RPupilDivergeLf': {"connection": "PupilDivergeLR", "value": 10},
                        'RPupilDivergeRh': {"connection": "PupilDivergeLR", "value": -10}},
        'order': ['PupilDivergeUD', 'PupilDivergeLR']}

}

mouthSecondarys = {"lipUpperMidSecondary": {
    'Type': "blendShapeDefinition",
    "isSymetrical": True,
    "baseMesh": "Character",
    "control": "Character_RH_MidUpLip00_ctr_facialRig",
    "attributes": {"UD": {"type": "float", "min": -10, "max": 10},
                   "FB": {"type": "float", "min": -10, "max": 10}},
    "blendShapes": {'UpperMidUp': {"connection": "UD", "value": 10},
                    'UpperMidDn': {"connection": "UD", "value": -10},
                    'UpperMidFn': {"connection": "FB", "value": 10},
                    'UpperMidBk': {"connection": "FB", "value": -10}},
    'order': ['UD', 'FB']},
    "lipLowMidSecondary": {
        'Type': "blendShapeDefinition",
        "isSymetrical": True,
        "baseMesh": "Character",
        "control": "Character_RH_MidLowLip00_ctr_facialRig",
        "attributes": {"UD": {"type": "float", "min": -10, "max": 10},
                       "FB": {"type": "float", "min": -10, "max": 10}},
        "blendShapes": {'LowMidUp': {"connection": "UD", "value": 10},
                        'LowMidDn': {"connection": "UD", "value": -10},
                        'LowMidFn': {"connection": "FB", "value": 10},
                        'LowMidBk': {"connection": "FB", "value": -10}},
        'order': ['UD', 'FB']},
    "LipCornerSecondary": {
        'Type': "blendShapeDefinition",
        "isSymetrical": True,
        "baseMesh": "Character",
        "control": "Character_RH_CornerLip00_ctr_facialRig",
        "attributes": {"UD": {"type": "float", "min": -10, "max": 10},
                       "FB": {"type": "float", "min": -10, "max": 10}},
        "blendShapes": {'CornerUp': {"connection": "UD", "value": 10},
                        'CornerDn': {"connection": "UD", "value": -10},
                        'CornerFn': {"connection": "FB", "value": 10},
                        'CornerBk': {"connection": "FB", "value": -10}},
        'order': ['UD', 'FB']},
    "LipUpperSecondary": {
        'Type': "blendShapeDefinition",
        "isSymetrical": False,
        "baseMesh": "Character",
        "control": "Character_MD_MidLowLip00_ctr_facialRig",
        "attributes": {"UD": {"type": "float", "min": -10, "max": 10},
                       "FB": {"type": "float", "min": -10, "max": 10}},
        "blendShapes": {'LowUp': {"connection": "UD", "value": 10},
                        'LowDn': {"connection": "UD", "value": -10},
                        'LowFn': {"connection": "FB", "value": 10},
                        'LowBk': {"connection": "FB", "value": -10}},
        'order': ['UD', 'FB']},
    "LipLowSecondary": {
        'Type': "blendShapeDefinition",
        "isSymetrical": False,
        "baseMesh": "Character",
        "control": "Character_MD_MidUpLip00_ctr_facialRig",
        "attributes": {"UD": {"type": "float", "min": -10, "max": 10},
                       "FB": {"type": "float", "min": -10, "max": 10}},
        "blendShapes": {'UpperUp': {"connection": "UD", "value": 10},
                        'UpperDn': {"connection": "UD", "value": -10},
                        'UpperFn': {"connection": "FB", "value": 10},
                        'UpperBk': {"connection": "FB", "value": -10}},
        'order': ['UD', 'FB']}}
EyeJawJoints = {"lidJoints": {
    'Type': "jointLinkDefinition",
    'isSymetrical': True,
    'control': 'Character_LF_EyeLidShapes00_ctr_facialRig',

    'joints': {'Character_LF_EyeLidSpin00_grp_Rig': {"connection": "spin", "inputPlug": "rotateX",
                                                     "value": [[-10, -45], [0, 0], [10, 45]]}},

    "attributes": {"spin": {"type": "float", "min": -10, "max": 10}},
    'order': ['spin']}
}
'''"jawjoint":{
                    'Type'        : "jointLinkDefinition",
                    'isSymetrical': False,
                    'control'     : 'Character_MD_Jaw00_ctr_rig',
                    'joints'      : {"Character_MD_Jaw_sknjnt_RIG":{"connection":"rotateZ" , "inputPlug":"rotateZ", "value" : None}},
                    'attributes'  : {'rotateZ':{}},
                    'order'       : ['rotateZ']}'''

mouth = {"mouthMain": {
    'Type': "blendShapeDefinition",
    'isSymetrical': False,
    "baseMesh": "Character",
    'control': 'Character_MD_Jaw00_ctr_rig',
    'blendShapes': {'Smile': {"connection": "SmileFrown", "value": 10},
                    'Frown': {"connection": "SmileFrown", "value": -10},
                    'Wide': {"connection": "NarrowWide", "value": 10},
                    'Narrow': {"connection": "NarrowWide", "value": -10},
                    'Ooo': {"connection": "Ooo", "value": 10},
                    'CornerUp': {"connection": "CornerUD", "value": 10},
                    'CornerDn': {"connection": "CornerUD", "value": -10},
                    'Pinch': {"connection": "Pinch", "value": 10}
                    },
    'attributes': {'SmileFrown': {"type": "float", "min": -10, "max": 10},
                   'NarrowWide': {"type": "float", "min": -10, "max": 10},
                   'Ooo': {"type": "float", "min": 0, "max": 10},
                   # 'Press'         :{"type": "float", "min":  0, "max":10},
                   # 'Puff'          :{"type": "float", "min":  0, "max":10},
                   'CornerUD': {"type": "float", "min": -10, "max": 10},
                   'Pinch': {"type": "float", "min": 0, "max": 10},

                   'LeftRightShapes': {"type": "float", "min": 0, "max": 10, "keyable": False}},
    'order': [
        'SmileFrown', 'NarrowWide', 'Ooo', 'CornerUD', 'Pinch', 'LeftRightShapes']},

    "mouthSideUpperLip": {
        'Type': "blendShapeDefinition",
        'isSymetrical': True,
        "baseMesh": 'Character',
        'control': 'Character_LF_LipUpShapes00_ctr_facialRig',
        'blendShapes': {
            'LipUpperSneer': {"connection": "UpperSneer", "value": 10},
        },
        'attributes': {
            'UpperSneer': {"type": "float", "min": 0, "max": 10},
        },
        'order': ['UpperSneer']
    },

    "mouthSideLowerLip": {
        'Type': "blendShapeDefinition",
        'isSymetrical': True,
        "baseMesh": "Character",
        'control': 'Character_LF_LipLowShapes00_ctr_facialRig',
        'blendShapes': {
            'LipLowSneer': {"connection": "LowerSneer", "value": 10},
        },
        'attributes': {
            'LowerSneer': {"type": "float", "min": 0, "max": 10}
        },
        'order': ['LowerSneer']
    },

    "mouthUpperLip": {
        'Type': "blendShapeDefinition",
        'isSymetrical': False,
        "baseMesh": "Character",
        'control': 'Character_MD_LipUpShapes00_ctr_facialRig',
        'blendShapes': {

            'UpperLipUp': {"connection": "UpperLipUD", "value": 10},
            'UpperLipDn': {"connection": "UpperLipUD", "value": -10},
            'UpperLipFn': {"connection": "UpperLipFB", "value": 10},
            'UpperLipBk': {"connection": "UpperLipFB", "value": -10},
            'UpperLipCw': {"connection": "UpperLipTILT", "value": 10},
            'UpperLipCcw': {"connection": "UpperLipTILT", "value": -10},
            'UpperLipCurlIn': {"connection": "UpperLipCurl", "value": 10},
            'UpperLipCurlOut': {"connection": "UpperLipCurl", "value": -10},

            'MUpperSneerUp': {"connection": "UpperLipMidUD", "value": 10},
            'MUpperSneerDn': {"connection": "UpperLipMidUD", "value": -10}
        },

        'attributes': {

            'UpperLipUD': {"type": "float", "min": -10, "max": 10},
            'UpperLipFB': {"type": "float", "min": -10, "max": 10},
            'UpperLipTILT': {"type": "float", "min": -10, "max": 10},
            'UpperLipCurl': {"type": "float", "min": -10, "max": 10},

            'SneerMid': {"type": "float", "min": 0, "max": 10, "keyable": False},
            'UpperLipMidUD': {"type": "float", "min": -10, "max": 10}
        },
        'order': ['UpperLipUD', 'UpperLipFB', 'UpperLipTILT', 'UpperLipCurl', 'SneerMid', 'UpperLipMidUD']
    },

    "mouthLowerLip": {
        'Type': "blendShapeDefinition",
        'isSymetrical': False,
        "baseMesh": "Character",
        'control': 'Character_MD_LipLowShapes00_ctr_facialRig',
        'blendShapes': {

            'LowLipUp': {"connection": "LowerLipUD", "value": 10},
            'LowLipDn': {"connection": "LowerLipUD", "value": -10},
            'LowLipFn': {"connection": "LowerLipFB", "value": 10},
            'LowLipBk': {"connection": "LowerLipFB", "value": -10},
            'LowLipCw': {"connection": "LowerLipTILT", "value": 10},
            'LowLipCcw': {"connection": "LowerLipTILT", "value": -10},
            'LowLipCurlIn': {"connection": "LowerLipCurl", "value": 10},
            'LowLipCurlOut': {"connection": "LowerLipCurl", "value": -10},

            'MLowSneerUp': {"connection": "LowerLipMidUD", "value": 10},
            'MLowSneerDn': {"connection": "LowerLipMidUD", "value": -10}
        },
        'attributes': {
            'LowerLipUD': {"type": "float", "min": -10, "max": 10},
            'LowerLipFB': {"type": "float", "min": -10, "max": 10},
            'LowerLipTILT': {"type": "float", "min": -10, "max": 10},
            'LowerLipCurl': {"type": "float", "min": -10, "max": 10},

            'SneerMid': {"type": "float", "min": 0, "max": 10, "keyable": False},
            'LowerLipMidUD': {"type": "float", "min": -10, "max": 10}
        },
        'order': [
            "LowerLipUD", "LowerLipFB", "LowerLipTILT", "LowerLipCurl", 'SneerMid',
            'LowerLipMidUD']
    },

    "mouthSideCornerLip": {
        'Type': "blendShapeDefinition",
        'isSymetrical': True,
        "baseMesh": "Character",
        'control': 'Character_LF_MouthShapes00_ctr_facialRig',
        'blendShapes': {
            'Smile': {"connection": "SmileFrown", "value": 10},
            'Frown': {"connection": "SmileFrown", "value": -10},
            'Wide': {"connection": "NarrowWide", "value": 10},
            'Narrow': {"connection": "NarrowWide", "value": -10},
            'CornerUp': {"connection": "Corner", "value": 10},
            'CornerDn': {"connection": "Corner", "value": -10},
            'pinch': {"connection": "Pinch", "value": 10}
        },
        'attributes': {
            'SmileFrown': {"type": "float", "min": -10, "max": 10},
            'NarrowWide': {"type": "float", "min": -10, "max": 10},
            'Corner': {"type": "float", "min": -10, "max": 10},
            'Pinch': {"type": "float", "min": 0, "max": 10}
        },
        'order': ['SmileFrown', 'NarrowWide', 'Corner', 'Pinch']
    }

}

Cheeks = {'cheeks': {'Type': "blendShapeDefinition",
                     'isSymetrical': True,
                     "baseMesh": "Character",
                     'control': 'Character_LF_Cheeks00_ctr_facialRig',
                     'blendShapes': {'cheekUp': {"connection": "UD", "value": 10},
                                     'cheekDn': {"connection": "UD", "value": -10},
                                     'cheekIn': {"connection": "LR", "value": 10},
                                     'cheekOut': {"connection": "LR", "value": -10},
                                     'cheekFn': {"connection": "FB", "value": 10},
                                     'cheekBk': {"connection": "FB", "value": -10},
                                     'Squint': {"connection": "Squint", "value": 10},
                                     'PuffOut': {"connection": "PUFF", "value": 10},
                                     'PuffIn': {"connection": "PUFF", "value": -10}},

                     'attributes': {"UD": {"type": "float", "min": -10, "max": 10},
                                    "LR": {"type": "float", "min": -10, "max": 10},
                                    "FB": {"type": "float", "min": -10, "max": 10},
                                    "Squint": {"type": "float", "min": 0, "max": 10},
                                    "PUFF": {"type": "float", "min": -10, "max": 10}},
                     'order': ["UD", "LR", "FB", "Squint", "PUFF"]}}
mouthMover = {'mouthMover': {'Type': "blendShapeDefinition",
                             'isSymetrical': False,
                             "baseMesh": "Character",
                             'control': 'Character_MD_MouthMover00_ctr_facialRig',
                             'blendShapes': {'mouthUp': {"connection": "UD", "value": 10},
                                             'mouthDn': {"connection": "UD", "value": -10},
                                             'mouthLf': {"connection": "LR", "value": 10},
                                             'mouthRh': {"connection": "LR", "value": -10},
                                             'mouthFn': {"connection": "FB", "value": 10},
                                             'mouthBk': {"connection": "FB", "value": -10},
                                             'TiltCw': {"connection": "Tilt", "value": 10},
                                             'TiltCcw': {"connection": "Tilt", "value": -10}
                                             },

                             'attributes': {
                                 'UD': {"type": "float", "min": -10, "max": 10},
                                 'LR': {"type": "float", "min": -10, "max": 10},
                                 'FB': {"type": "float", "min": -10, "max": 10},
                                 'Tilt': {"type": "float", "min": -10, "max": 10}
                             },

                             'order': ["UD", "LR", "FB", "Tilt"]}}

Nose = {'Nose': {'Type': "blendShapeDefinition",
                 'isSymetrical': False,
                 "baseMesh": "Character",
                 'control': 'Character_MD_Nose00_ctr_facialRig',
                 'blendShapes': {'noseUp': {"connection": "UD", "value": 10},
                                 'noseDn': {"connection": "UD", "value": -10},
                                 'noseLf': {"connection": "LR", "value": 10},
                                 'noseRh': {"connection": "LR", "value": -10},
                                 'noseFn': {"connection": "FB", "value": 10},
                                 'noseBk': {"connection": "FB", "value": -10},
                                 'noseCurlUp': {"connection": "Curl", "value": 10},
                                 'noseCurlDn': {"connection": "Curl", "value": -10},
                                 'noseTiltCw': {"connection": "Tilt", "value": 10},
                                 'noseTiltCcw': {"connection": "Tilt", "value": -10}
                                 },
                 'attributes': {
                     "UD": {"type": "float", "min": -10, "max": 10},
                     "LR": {"type": "float", "min": -10, "max": 10},
                     "FB": {"type": "float", "min": -10, "max": 10},
                     "Curl": {"type": "float", "min": -10, "max": 10},
                     "Tilt": {"type": "float", "min": -10, "max": 10},
                 },
                 'order': ["UD", "LR", "FB", "Curl", "Tilt"]},
        'NoseLf': {'Type': "blendShapeDefinition",
                   'isSymetrical': True,
                   "baseMesh": "Character",
                   'control': 'Character_LF_Nose00_ctr_facialRig',
                   'blendShapes': {
                       'noseSneer': {"connection": "Sneer", "value": 10},
                       'noseFlareIn': {"connection": "Flare", "value": -10},
                       'noseFlareOut': {"connection": "Flare", "value": 10}
                   },
                   'attributes': {
                       "Sneer": {"type": "float", "min": 0, "max": 10},
                       "Flare": {"type": "float", "min": -10, "max": 10}
                   },
                   'order': ["Sneer", "Flare"]
                   },
        }

Furrow = {'Furrow': {'Type': "blendShapeDefinition",
                     'isSymetrical': False,
                     "baseMesh": "Character",
                     'control': 'Character_MD_Furrow00_ctr_facialRig',
                     'blendShapes': {'Furrow': {"connection": "Furrow", "value": 10},
                                     'FurrowUp': {"connection": "UD", "value": 10},
                                     'FurrowDn': {"connection": "UD", "value": -10},
                                     'FurrowFn': {"connection": "FB", "value": 10},
                                     'FurrowBk': {"connection": "FB", "value": -10},
                                     'FurrowLf': {"connection": "LR", "value": 10},
                                     'FurrowRh': {"connection": "LR", "value": -10},
                                     'FurrowTiltCw': {"connection": "TILT", "value": 10},
                                     'FurrowTiltCcw': {"connection": "TILT", "value": -10},
                                     'FurrowL': {"connection": "FurrowL", "value": 10},
                                     'FurrowR': {"connection": "FurrowR", "value": 10}
                                     },
                     'attributes': {
                         'Furrow': {"type": "float", "min": 0, "max": 10},
                         'UD': {"type": "float", "min": -10, "max": 10},
                         'FB': {"type": "float", "min": -10, "max": 10},
                         'LR': {"type": "float", "min": -10, "max": 10},
                         'TILT': {"type": "float", "min": -10, "max": 10},
                         'Left_Right_Shapes': {"type": "float", "min": -10, "max": 10, "keyable": False},
                         'FurrowL': {"type": "float", "min": 0, "max": 10},
                         'FurrowR': {"type": "float", "min": 0, "max": 10}
                     },
                     'order': ['Furrow', "UD", "LR", "FB", "TILT", "Left_Right_Shapes", "FurrowL", "FurrowR"]}}

secondaryEyeBrow = {
    "EyeBrowMidSecondary": {
        'Type': "blendShapeDefinition",
        "isSymetrical": True,
        "baseMesh": "Character",
        "control": "Character_LF_InnerEyeBrow00_ctr_facialRig",
        "attributes": {"UD": {"type": "float", "min": -10, "max": 10},
                       "LR": {"type": "float", "min": -10, "max": 10},
                       "FB": {"type": "float", "min": -10, "max": 10},
                       "Tilt": {"type": "float", "min": -10, "max": 10}},
        "blendShapes": {
            'BrowMidUp': {"connection": "UD", "value": 10},
            'BrowMidDn': {"connection": "UD", "value": -10},
            'BrowMidLf': {"connection": "LR", "value": 10},
            'BrowMidRh': {"connection": "LR", "value": -10},
            'BrowMidFn': {"connection": "FB", "value": 10},
            'BrowMidBk': {"connection": "FB", "value": -10},
            'BrowMidTiltCw': {"connection": "Tilt", "value": 10},
            'BrowMidTiltCcw': {"connection": "Tilt", "value": -10},
        },
        'order': ['UD', 'LR', 'FB', 'Tilt']},
    "EyeBrowInnerSecondary": {
        'Type': "blendShapeDefinition",
        "isSymetrical": True,
        "baseMesh": "Character",
        "control": "Character_LF_InnerEyeBrow00_ctr_facialRig",
        "attributes": {"UD": {"type": "float", "min": -10, "max": 10},
                       "LR": {"type": "float", "min": -10, "max": 10},
                       "FB": {"type": "float", "min": -10, "max": 10},
                       "Tilt": {"type": "float", "min": -10, "max": 10}},
        "blendShapes": {
            'BrowInUp': {"connection": "UD", "value": 10},
            'BrowInDn': {"connection": "UD", "value": -10},
            'BrowInLf': {"connection": "LR", "value": 10},
            'BrowInRh': {"connection": "LR", "value": -10},
            'BrowInFn': {"connection": "FB", "value": 10},
            'BrowInBk': {"connection": "FB", "value": -10},
            'BrowInTiltCw': {"connection": "Tilt", "value": 10},
            'BrowInTiltCcw': {"connection": "Tilt", "value": -10},
        },
        'order': ['UD', 'LR', 'FB', 'Tilt']},
    "EyeBrowOutSecondary": {
        'Type': "blendShapeDefinition",
        "isSymetrical": True,
        "baseMesh": "Character",
        "control": "Character_LF_InnerEyeBrow00_ctr_facialRig",
        "attributes": {"UD": {"type": "float", "min": -10, "max": 10},
                       "LR": {"type": "float", "min": -10, "max": 10},
                       "FB": {"type": "float", "min": -10, "max": 10},
                       "Tilt": {"type": "float", "min": -10, "max": 10}},
        "blendShapes": {
            'BrowOutUp': {"connection": "UD", "value": 10},
            'BrowOutDn': {"connection": "UD", "value": -10},
            'BrowOutLf': {"connection": "LR", "value": 10},
            'BrowOutRh': {"connection": "LR", "value": -10},
            'BrowOutFn': {"connection": "FB", "value": 10},
            'BrowOutBk': {"connection": "FB", "value": -10},
            'BrowOutTiltCw': {"connection": "Tilt", "value": 10},
            'BrowOutTiltCcw': {"connection": "Tilt", "value": -10},
        },
        'order': ['UD', 'LR', 'FB', 'Tilt']}
}

EyeBrow = {"EyeBrow": {
    'Type': "blendShapeDefinition",
    "isSymetrical": True,
    "baseMesh": "Character",
    "control": "Character_LF_EyeBrow00_ctr_facialRig",
    "attributes": {"Angry": {"type": "float", "min": 0, "max": 10},
                   "Sad": {"type": "float", "min": 0, "max": 10},
                   "Surprise": {"type": "float", "min": 0, "max": 10},
                   "UD": {"type": "float", "min": -10, "max": 10},
                   "LR": {"type": "float", "min": -10, "max": 10},
                   "FB": {"type": "float", "min": -10, "max": 10},
                   "Tilt": {"type": "float", "min": -10, "max": 10}},
    "blendShapes": {
        'Angry': {"connection": "Angry", "value": 10},
        'Sad': {"connection": "Sad", "value": 10},
        'Surprise': {"connection": "Surprise", "value": 10},

        'BrowUp': {"connection": "UD", "value": 10},
        'BrowDn': {"connection": "UD", "value": -10},
        'BrowIn': {"connection": "LR", "value": 10},
        'BrowOut': {"connection": "LR", "value": -10},
        'BrowFn': {"connection": "FB", "value": 10},
        'BrowTiltCw': {"connection": "Tilt", "value": 10},
        'BrowTiltCcw': {"connection": "Tilt", "value": -10},
    },
    'order': ["Angry", "Sad", "Surprise", 'UD', 'LR', 'FB', 'Tilt']}
}
