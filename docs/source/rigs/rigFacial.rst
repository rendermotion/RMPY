==========
Rig Facial
==========

Class that reads a definition and creates a blendshape connection between the controls and the objects.
The rig comes with an example of a dictionary to connect FACS shapes to face controls.
This controls are suposed to connect with a rig created using rigBlendshapeControls.

The dictionary connects controls with blendshapes, it should have the following keys.

.. code-block:: python
    :caption: Example of a dictionary used to connect a facial rig.

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
        )

