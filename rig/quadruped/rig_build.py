from RMPY.rig.quadruped import rigQuadruped
from RMPY.rig import rigHierarchy
from RMPY.core import controls
from RMPY.core import data_save_load
import pymel.core as pm
from RMPY.rig.switches import rigBoolSwitch


def build():
    load_sources()
    build_rig()
    hierarchy()
    load_data()
    finalize()


def load_sources():
    data_save_load.import_all_available_maya_files()


def build_rig():
    rig_biped = rigQuadruped.RigQuadruped()
    rig_biped.build()
    controls.color_now_all_ctrls()


def hide_rigs():
    settings_rig_sistems = pm.ls('*_settings*_pnt')
    for each in settings_rig_sistems:
        each.visibility.set(False)


def visibility_switch():
    bool_switch = rigBoolSwitch.RigBoolSwitch(control='C_settings00_world_ctr', attribute_name='low_high_rez')
    bool_switch.attribute_output >> pm.ls('C_dog00_highRez_grp')[0].visibility
    bool_switch.attribute_output_false >> pm.ls('C_dog00_lowRez_grp')[0].visibility


def hierarchy():
    rig_hierarchy = rigHierarchy.RigHierarchy()
    pm.parent('geo', rig_hierarchy.geometry)


def load_data():
    controls_list = pm.ls('*ctr')
    data_save_load.load_curves(*controls_list)

    geometry = pm.ls(u'R_metalFeet00_backLeg_msh', u'L_metalFeet00_backLeg_msh',
                     u'R_metalFeet00_frontLeg_msh', u'L_metalFeet00_frontLeg_msh',
                     u'C_dog_lowRez_lowmsh', u'L_metalFeet00_frontLeg_lowmsh', u'R_metalFeet00_frontLeg_lowmsh',
                     u'R_metalFeet00_backLeg_lowmsh', u'L_metalFeet00_backLeg_lowmsh')

    data_save_load.load_skin_cluster(*geometry)


def finalize():
    hide_rigs()
    pm.delete('C_reference_points_pnt')
    pm.delete('measures_ref_grp')


if __name__ == '__main__':
    selection = pm.ls(selection=True)
    # data_save_load.load_skin_cluster(*selection)
    # build()
    # visibility_switch()
    # load_data()
    # hide_rigs()
    # controls.color_now_all_ctrls()
    # data_save_load.save_skin_cluster()
