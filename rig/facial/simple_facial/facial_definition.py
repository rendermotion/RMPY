prefix_geometry_list = []

definition = dict(
    jaw=dict(
        type='blend_shape_definition',
        isSymetrical=False,
        baseMesh='character',
        control='C_jaw_facial_ctrl',
        blendShapes=dict(narrow={'connection': 'translateY', 'value': -1},
                         wide={'connection': 'translateY', 'value': 1},
                         smile={'connection': 'translateX', 'value': 1},
                         frown={'connection': 'translateX', 'value': -1},
                         upperLipUp={'connection': 'upperLipUp', 'value': 10},
                         ),
        attributes=dict(
                        translateX={'type': 'float', 'min': -1, 'max': 1},
                        translateY={'type': 'float', 'min': -1, 'max': 1},
                        upperLipUp={'type': 'float', 'min': 0, 'max': 10},
                        ),
        order=['translateX', 'translateY', 'upperLipUp']
        ),
    brow=dict(
        type='blend_shape_definition',
        isSymetrical=True,
        baseMesh='character',
        control='L_brow_facial_ctrl',
        blendShapes=dict(LOutBrowUp={'connection': 'translateX', 'value': 1},
                         LOutBrowDwn={'connection': 'translateX', 'value': -1},
                         LInBrowUp={'connection': 'translateY', 'value': 1},
                         LInBrowDwn={'connection': 'translateY', 'value': -1},
                         LeyesCls={'connection': 'eyeCls', 'value': 10},
                         LeyesCls50={'connection': 'eyeCls', 'value': 5},
                         LeyesOpen={'connection': 'eyeCls', 'value': -10},

                         ),
        attributes=dict(translateX={'type': 'float', 'min': -1, 'max': 1},
                        translateY={'type': 'float', 'min': -1, 'max': 1},
                        eyeCls={'type': 'float', 'min': -10, 'max': 10},
                        ),
        order=['translateX', 'translateY', 'eyeCls']
        ),
    squint=dict(
        type='blend_shape_definition',
        isSymetrical=True,
        baseMesh='character',
        control='L_squint_facial_ctrl',
        blendShapes=dict(Lsquint={'connection': 'translateX', 'value': 1},
                         LnoseCorrugator={'connection': 'translateY', 'value': 1},
                         ),
        attributes=dict(translateX={'type': 'float', 'min': -10, 'max': 10},
                        translateY={'type': 'float', 'min': -10, 'max': 10},

                        ),
        order=['translateX','translateY']
    ),
    mouthCorner=dict(
        type='blend_shape_definition',
        isSymetrical=True,
        baseMesh='character',
        control='L_mouthCorner_facial_ctrl',
        blendShapes=dict(Lsmile={'connection': 'translateX', 'value': 1},
                         Lfrown={'connection': 'translateX', 'value': -1},
                         Lwide={'connection': 'translateY', 'value': 1},
                         Lnarrow={'connection': 'translateY', 'value': -1},
                         # Lkiss={'connection': 'cornerOutIn', 'value': -10},
                         LupLipIn={'connection': 'uplipOutIn', 'value': 10},
                         LupLipOut={'connection': 'uplipOutIn', 'value': -10},
                         LlowLipOut={'connection': 'lowLipOutIn', 'value': 10},
                         LlowLipIn={'connection': 'lowLipOutIn', 'value': -10},
                         ),
        attributes=dict(translateX={'type': 'float', 'min': -1, 'max': 1},
                        translateY={'type': 'float', 'min': -1, 'max': 1},
                        # cornerOutIn={'type': 'float', 'min': -10, 'max': 10},
                        uplipOutIn={'type': 'float', 'min': -10, 'max': 10},
                        lowLipOutIn={'type': 'float', 'min': -10, 'max': 10},

                        ),
        order=['translateX','translateY','uplipOutIn', 'lowLipOutIn']
        ),
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

direct_blendshape = {
    'character': 'head_msh',
    'mustache': 'mustache_grroming',
    'Leyebrow': 'eyebrow_L_msh',
    'Reyebrow': 'eyebrow_R_msh',
    'eyelash': 'eyelashes_grooming'
}

jaw_layer = [u'character']


if __name__ == '__main__':
    import pymel.core as pm
    selection_list=[]
    for each_dictionary in [definition, eyes_dict]:
        for each_setup in each_dictionary.keys():
            for each_blendshape in each_dictionary[each_setup]['blendShapes'].keys():
                if not pm.objExists(each_blendshape):
                    print ('{} not found'.format(each_blendshape))
                if not pm.ls(each_blendshape)[0].getParent().name() == 'blendshapes':
                    selection_list.append(each_blendshape)
    pm.select(selection_list)
