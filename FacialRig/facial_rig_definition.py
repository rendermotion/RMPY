definition = dict(
    jaw=dict(
        type='blend_shape_definition',
        isSymetrical=False,
        baseMesh='character',
        control='C_facial00_mouth_ctr',
        blendShapes=dict(midOpen={'connection': 'jawOpen', 'value': 5},
                         fullOpen={'connection': 'jawOpen', 'value': 10},
                         puffFront={'connection': 'jawOpen', 'value': -10},
                         mouthLeft={'connection': 'mouthLR', 'value': 10},
                         mouthRight={'connection': 'mouthLR', 'value': -10},
                         upperLipPucker={'connection': 'upperLipRollInOut', 'value': 10},
                         upperLipLipsIn={'connection': 'upperLipRollInOut', 'value': -10},
                         lowLipPucker={'connection': 'lowLipRollInOut', 'value': 10},
                         lowLipLipsIn={'connection': 'lowLipRollInOut', 'value': -10},
                         kiss={'connection': 'wideNarrow', 'value': -10},
                         bucinator={'connection': 'wideNarrow', 'value': 10},
                         jawForward={'connection': 'jawForwardBackward', 'value': 10},
                         jawBackward={'connection': 'jawForwardBackward', 'value': -10},
                         upperLipUp={'connection': 'upperLipUp', 'value': 10},
                         lowLipDwn={'connection': 'lowLipDown', 'value': 10},
                         ),
        attributes=dict(jawOpen={'type': 'float', 'min': 0, 'max': 10},
                        mouthLR={'type': 'float', 'min': -10, 'max': 10},
                        upperLipRollInOut={'type': 'float', 'min': -10, 'max': 10},
                        lowLipRollInOut={'type': 'float', 'min': -10, 'max': 10},
                        wideNarrow={'type': 'float', 'min': -10, 'max': 10},
                        jawForwardBackward={'type': 'float', 'min': -10, 'max': 10},
                        upperLipUp={'type': 'float', 'min': 0, 'max': 10},
                        lowLipDown={'type': 'float', 'min': 0, 'max': 10},
                        ),
        order=['jawOpen', 'mouthLR', 'upperLipRollInOut', 'lowLipRollInOut', 'wideNarrow', 'jawForwardBackward',
               'upperLipUp', 'lowLipDown']
        ),
    nose=dict(
        type='blend_shape_definition',
        isSymetrical=False,
        baseMesh='character',
        control='C_facial00_nose_ctr',
        blendShapes=dict(LnoseExpand={'connection': 'LNose', 'value': 10},
                         LnoseContract={'connection': 'LNose', 'value': -10},
                         RnoseExpand={'connection': 'RNose', 'value': 10},
                         RnoseContract={'connection': 'RNose', 'value': -10},
                         ),
        attributes=dict(LNose={'type': 'float', 'min': -10, 'max': 10},
                        RNose={'type': 'float', 'min': -10, 'max': 10},
                        ),
        order=['LNose', 'RNose']
        ),
    brow=dict(
        type='blend_shape_definition',
        isSymetrical=True,
        baseMesh='character',
        control='L_facial00_brow_ctr',
        blendShapes=dict(LOutBrowUp={'connection': 'browOut', 'value': 10},
                         LOutBrowDwn={'connection': 'browOut', 'value': -10},
                         LInBrowUp={'connection': 'browIn', 'value': 10},
                         LInBrowDwn={'connection': 'browIn', 'value': -10},
                         LeyesCls={'connection': 'eyeCls', 'value': 10},
                         LeyesOpen={'connection': 'eyeCls', 'value': -10},

                         ),
        attributes=dict(browOut={'type': 'float', 'min': -10, 'max': 10},
                        browIn={'type': 'float', 'min': -10, 'max': 10},
                        eyeCls={'type': 'float', 'min': -10, 'max': 10},
                        ),
        order=['browOut', 'browIn', 'eyeCls']
        ),
    mouthCorner=dict(
        type='blend_shape_definition',
        isSymetrical=True,
        baseMesh='character',
        control='L_facial00_mouthCorner_ctr',
        blendShapes=dict(Lsmile={'connection': 'cornerUpDown', 'value': 10},
                         Lfrown={'connection': 'cornerUpDown', 'value': -10},
                         Lwide={'connection': 'cornerOutIn', 'value': 10},
                         Lkiss={'connection': 'cornerOutIn', 'value': -10},
                         LupLipIn={'connection': 'uplipOutIn', 'value': 10},
                         LupLipOut={'connection': 'uplipOutIn', 'value': -10},
                         LlowLipOut={'connection': 'lowLipOutIn', 'value': 10},
                         LlowLipIn={'connection': 'lowLipOutIn', 'value': -10},
                         ),
        attributes=dict(cornerUpDown={'type': 'float', 'min': -10, 'max': 10},
                        cornerOutIn={'type': 'float', 'min': -10, 'max': 10},
                        uplipOutIn={'type': 'float', 'min': -10, 'max': 10},
                        lowLipOutIn={'type': 'float', 'min': -10, 'max': 10},

                        ),
        order=['cornerUpDown', 'cornerOutIn', 'uplipOutIn', 'lowLipOutIn']
        ),
    cheeks=dict(
        type='blend_shape_definition',
        isSymetrical=True,
        baseMesh='character',
        control='L_facial00_cheek_ctr',
        blendShapes=dict(Lsquint={'connection': 'squint', 'value': 10},
                         LnoseCorrugator={'connection': 'noseCorrugator', 'value': 10},
                         ),
        attributes=dict(squint={'type': 'float', 'min': 0, 'max': 10},
                        noseCorrugator={'type': 'float', 'min': 0, 'max': 10},),
        order=['squint', 'noseCorrugator']
        ),
    browCorrugator=dict(
        type='blend_shape_definition',
        isSymetrical=False,
        baseMesh='character',
        control='C_facial00_foreHead_ctr',
        blendShapes=dict(
                         browCorrugator={'connection': 'corrugator', 'value': 10},
                         ),
        attributes=dict(
                        corrugator={'type': 'float', 'min': 0, 'max': 10},),
        order=['corrugator']


    )
)
eyes_dict = dict(
    eyes=dict(
        type='blend_shape_definition',
        isSymetrical=True,
        baseMesh='character',
        control='L_aim00_eye_grp',
        blendShapes=dict(LlookLeft={'connection': 'rotateY', 'value': 18},
                         LlookRight={'connection': 'rotateY', 'value': -18},
                         LlookUp={'connection': 'rotateZ', 'value': 18},
                         LlookDwn={'connection': 'rotateZ', 'value': -18},
                         ),
        attributes=dict(rotateY={'type': 'float', 'min': -18, 'max': 18},
                        rotateZ={'type': 'float', 'min': -18, 'max': 18},),
        order=['rotateY', 'rotateZ']
    ))

correctives_dict = dict(
        jawCorrectives=dict(
            type='blend_shape_definition',
            isSymetrical=False,
            baseMesh='character',
            control='C_joint00_jaw_ctr',
            blendShapes=dict(jawOpen={'connection': 'rotateZ', 'value': 12}),
            attributes=dict(rotateZ={'type': 'float', 'min': 0, 'max': 10}),
            order=['rotateZ']
            ),
)
if __name__ == '__main__':
    import pymel.core as pm
    selection_list=[]
    for each_dictionary in [definition, eyes_dict]:
        for each_setup in each_dictionary.keys():
            for each_blendshape in each_dictionary[each_setup]['blendShapes'].keys():
                if not pm.objExists(each_blendshape):
                    print '{} not found'.format(each_blendshape)

                if not pm.ls(each_blendshape)[0].getParent().name() == 'blendshapes':
                    selection_list.append(each_blendshape)
    pm.select(selection_list)


