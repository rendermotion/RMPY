from RMPY.rig.biped import rigBiped
from RMPY.rig import rigHierarchy
from RMPY.core import controls
from RMPY.core import data_save_load
import pymel.core as pm
from RMPY.core import search_hierarchy
from RMPY.rig.switches import rigBoolSwitch
# from RMPY.rig.customRig import tongue


def build():
    load_sources()
    build_rig()
    hierarchy()
    load_data()
    finalize()


def load_sources():
    data_save_load.import_all_available_maya_files()


def build_rig():
    rig_biped = rigBiped.RigByped()
    rig_biped.build()
    controls.color_now_all_ctrls()
    visibility_switch()
    # tongue.build()


def hide_rigs():
    settings_rig_sistems = pm.ls('*_settings*_pnt')
    for each in settings_rig_sistems:
        each.visibility.set(False)


def hierarchy():
    rig_hierarchy = rigHierarchy.RigHierarchy()
    pm.parent('geo', rig_hierarchy.geometry)


def load_data():
    controls_list = pm.ls('*ctr')
    data_save_load.load_curves(*controls_list)

    geometry = search_hierarchy.shape_type_in_hierarchy(pm.ls('geometry')[0], mesh_list=[], object_type='mesh')
    data_save_load.load_skin_cluster(*geometry)


def visibility_switch():
    secondary_controls_visibility = rigBoolSwitch.RigBoolSwitch(control='C_settings00_world_ctr', attribute_name='secondaryControls')
    for each in {u'L_bendy00_shoulder_grp', u'L_bendy01_shoulder_grp', u'L_bendy02_shoulder_grp',
                 u'L_bendy03_shoulder_grp', u'L_bendy04_shoulder_grp', u'L_bendy05_shoulder_grp',
                 u'R_bendy00_shoulder_grp', u'R_bendy01_shoulder_grp', u'R_bendy02_shoulder_grp',
                 u'R_bendy03_shoulder_grp', u'R_bendy04_shoulder_grp', u'R_bendy05_shoulder_grp', u'L_bendy00_leg_grp',
                 u'L_bendy01_leg_grp', u'L_bendy02_leg_grp', u'L_bendy03_leg_grp', u'L_bendy04_leg_grp',
                 u'L_bendy05_leg_grp', u'L_twistOrigin00_leg_grp', u'L_twistOrigin01_leg_grp',
                 u'R_twistOrigin00_leg_grp', u'R_bendy00_leg_grp', u'R_bendy01_leg_grp', u'R_bendy02_leg_grp',
                 u'R_twistOrigin01_leg_grp', u'R_bendy03_leg_grp', u'R_bendy04_leg_grp', u'R_bendy05_leg_grp',
                 u'R_twistOrigin00_clavicle_grp', u'R_twistOrigin00_shoulder_grp', u'L_twistOrigin00_clavicle_grp',
                 u'L_twistOrigin00_shoulder_grp'}:
        secondary_controls_visibility.attribute_output >> pm.ls(each)[0].visibility

    geo_rez_switch = rigBoolSwitch.RigBoolSwitch(control='C_settings00_world_ctr', attribute_name='high_rez')
    geo_rez_switch.attribute_output >> pm.ls('C_rider00_high_grp')[0].visibility
    geo_rez_switch.attribute_output_false >> pm.ls('C_rider00_low_grp')[0].visibility


def finalize():
    hide_rigs()
    pm.delete('reference_points')
    # pm.delete('measures_ref_grp')


if __name__ == '__main__':
    finalize()
    # data_save_load.save_curve()