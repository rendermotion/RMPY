import pymel.core as pm
import pymel.core.datatypes as dt


def calculate_offset_matrix():
    ik_feet, fk_feet = pm.ls('L_ikIK00_leg_ctr', 'L_fk00_ankleFeet_ctr')
    offset_matrix = ik_feet.worldMatrix[0].get() * fk_feet.worldMatrix[0].get().inverse()
    print(offset_matrix)



def feet_ik_fk_switch():
    offset = dt.Matrix([[0.8311992826048229, 0.4487139680912628, 0.32827355579915385, 0.0],
                        [-0.4750393684343335, 0.8799645438524838, 0.0, 0.0],
                        [-0.28886908978763454, -0.15594286262052404, 0.9445826975776015, 0.0], [0.0, 0.0, 0.0, 1.0]])
    toes_main = pm.ls('L_fk01_ankleFeet_ctr')[0]
    ik_ankle_joint = pm.ls('L_IKOutput00_ankleFeet_jnt')[0]
    limit_foots = pm.ls('L_tap00_footLimitBack_ctr')[0]

def feet_fk_to_ik_switch():
    ik_ankle_joint, ik_toe_joint = pm.ls('L_IKOutput00_ankleFeet_jnt', 'L_joint00_ankleFeet_jnt')
    fk_feet_control, fk_toe_control = pm.ls('L_fk00_ankleFeet_ctr', 'L_fk01_ankleFeet_ctr')
    pm.matchTransform(fk_feet_control, ik_ankle_joint)
    pm.matchTransform(fk_toe_control, ik_toe_joint)







if __name__ == '__main__':
    feet_fk_to_ik_switch()