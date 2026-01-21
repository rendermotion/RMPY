import pymel.core as pm

corrective_order = ['arm', 'elbow', 'knee', 'leg', 'legn', 'legSide', 'ankle',  'anklen']

config_correctives = {'arm': {'targets': [60],
                              'drivers': ['L_clavicle01_clavicle_jnt', 'L_intermediate00_shoulder_jnt'],
                              'rotationOrder': 'zyx', 'RFlip': False},
                      'elbow': {'targets': [-90],
                                'drivers': ['L_intermediate00_shoulder_jnt', 'L_intermediate01_shoulder_jnt'],
                                'rotationOrder': 'yzx', 'RFlip': True},

                      'knee': {'targets': [-90],
                                'drivers': ['L_intermediate00_leg_jnt', 'L_intermediate01_leg_jnt'],
                                'rotationOrder': 'zyx', 'RFlip': True},

                      'leg': {'targets': [90],
                              'drivers': ['C_hip00_Hip_sknjnt', 'L_twist00_leg_jnt'],
                              'rotationOrder': 'zyx', 'RFlip': False},

                      'legn': {'targets': [-60],
                               'drivers': ['C_hip00_Hip_sknjnt', 'L_twist00_leg_jnt'],
                               'rotationOrder': 'zyx', 'RFlip': False},

                      'legSide': {'targets': [60],
                                  'drivers': ['C_hip00_Hip_sknjnt', 'L_twist00_leg_jnt'],
                                  'rotationOrder': 'yzx', 'RFlip': True},
                      'ankle':  {'targets': [25],
                                 'drivers': ['L_ribbonJoints09_leg_sknjnt', 'L_intermediate00_ankleFeet_sknjnt'],
                                 'rotationOrder': 'zyx', 'RFlip': False},

                      'anklen':  {'targets': [-45],
                                 'drivers': ['L_ribbonJoints09_leg_sknjnt', 'L_intermediate00_ankleFeet_sknjnt'],
                                 'rotationOrder': 'zyx', 'RFlip': False}
                      }

base_mesh = {'BabyK_body_lvl2': {'arm': ['L_armZ60_corrective_msh'],
                                 'elbow': ['L_elbowYn90_corrective_msh'],
                                 'knee': ['L_kneeZn100_corrective_msh'],
                                 'leg': ['L_legZ90_corrective_msh'],
                                 'legn': ['L_legZn90_corrective_msh'],
                                 'legSide': ['L_legY90_corrective_msh'],
                                 'ankle': ['L_ankleFeet40_corrective_msh'],
                                 'anklen': ['L_ankleFeetn40_corrective_msh'],
                          }
             }

def rename_blend_shapes():
    selection = pm.ls(selection=True)
    for each in selection:
        current_name = each.name()
        each.rename('{}_{}'.format(current_name[0], current_name[1:]))


if __name__ == '__main__':
    rename_blend_shapes()

