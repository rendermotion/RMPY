from RMPY.rig.switches import rigBoolSwitch
import pymel.core as pm

def build():
    bendis = [u'L_bendy00_leg_grp', u'L_bendy00_shoulder_grp', u'L_bendy01_leg_grp', u'L_bendy01_shoulder_grp',
              u'L_bendy02_leg_grp', u'L_bendy02_shoulder_grp', u'L_bendy03_leg_grp', u'L_bendy03_shoulder_grp',
              u'L_bendy04_leg_grp', u'L_bendy04_shoulder_grp', u'L_bendy05_leg_grp', u'L_bendy05_shoulder_grp',
              u'R_bendy00_leg_grp', u'R_bendy00_shoulder_grp', u'R_bendy01_leg_grp', u'R_bendy01_shoulder_grp',
              u'R_bendy02_leg_grp', u'R_bendy02_shoulder_grp', u'R_bendy03_leg_grp', u'R_bendy03_shoulder_grp',
              u'R_bendy04_leg_grp', u'R_bendy04_shoulder_grp', u'R_bendy05_leg_grp', u'R_bendy05_shoulder_grp']
    rig_boool_switch = rigBoolSwitch.RigBoolSwitch(control='C_control_settings_ctr',
                                                   attribute_name='secondary_controls')
    for each in pm.ls(bendis):
        rig_boool_switch.attribute_output >> each.visibility
def pole_vectors_visibility():
    pole_vector = [u'L_twistOrigin00_clavicle_grp', u'L_twistOrigin00_leg_grp', u'L_twistOrigin00_shoulder_grp',
     u'L_twistOrigin01_leg_grp', u'R_twistOrigin00_clavicle_grp', u'R_twistOrigin00_leg_grp',
     u'R_twistOrigin00_shoulder_grp', u'R_twistOrigin01_leg_grp']
    rig_boool_switch = rigBoolSwitch.RigBoolSwitch(control='C_control_settings_ctr',
                                                   attribute_name='twists_pole_vectors')
    for each in pm.ls(pole_vector):
        rig_boool_switch.attribute_output >> each.visibility


def facial_controls_visibility():
    facial_controls = [u'L_controls00_lowerLip_grp', u'L_controls00_upperLip_grp', u'R_controls00_lowerEye_grp', u'R_controls00_upperEye_grp', u'L_controls00_lowerEye_grp', u'L_controls00_upperEye_grp', u'C_controls00_tongue_grp', u'C_controls00_rig_grp']
    rig_boool_switch = rigBoolSwitch.RigBoolSwitch(control='C_control_settings_ctr',
                                                   attribute_name='facial_controls')
    for each in pm.ls(facial_controls):
        rig_boool_switch.attribute_output >> each.visibility
if __name__=='__main__':
    facial_controls_visibility()