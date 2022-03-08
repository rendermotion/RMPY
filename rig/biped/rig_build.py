from RMPY.rig.biped import rigBiped
from RMPY.rig import rigHierarchy
from RMPY.core import controls
from RMPY.core import data_save_load
import pymel.core as pm
from RMPY.rig.customRig import tongue
reload(tongue)


def build():
    build_rig()
    hierarchy()
    load_data()
    finalize()


def build_rig():
    rig_biped = rigBiped.RigByped()
    rig_biped.build()
    controls.color_now_all_ctrls()
    tongue.build()


def hierarchy():
    rig_hierarchy = rigHierarchy.RigHierarchy()
    pm.parent('venom_geo_grp', rig_hierarchy.geometry)


def load_data():
    controls_list = pm.ls('*ctr')
    data_save_load.load_curves(*controls_list)

    geometry = pm.ls(u'venom_eye_left_geo', u'venom_eye_goo_left_geo', u'venom_body_geo', u'venom_eye_goo_right_geo',
                     u'venom_teethLower29_geo', u'venom_teethLower28_geo', u'venom_teethLower31_geo',
                     u'venom_teethLower30_geo', u'venom_teethLower25_geo', u'venom_teethLower24_geo',
                     u'venom_teethLower23_geo', u'venom_teethLower27_geo', u'venom_teethLower26_geo',
                     u'venom_teethLower20_geo', u'venom_teethLower19_geo', u'venom_teethLower22_geo',
                     u'venom_teethLower21_geo', u'venom_goo_R_geo', u'venom_goo_L_geo', u'venom_gumLower_geo',
                     u'venom_teethLower34_geo', u'venom_teethLower33_geo', u'venom_teethLower32_geo',
                     u'venom_gumUpper_geo', u'venom_teethLower35_geo', u'venom_teethLower15_geo',
                     u'venom_teethLower14_geo', u'venom_teethLower18_geo', u'venom_teethLower17_geo',
                     u'venom_teethLower16_geo', u'venom_teethLower11_geo', u'venom_teethLower10_geo',
                     u'venom_teethLower13_geo', u'venom_teethLower12_geo', u'venom_teethLower06_geo',
                     u'venom_teethLower05_geo', u'venom_teethLower09_geo', u'venom_teethLower08_geo',
                     u'venom_teethLower07_geo', u'venom_teethLower02_geo', u'venom_teethLower01_geo',
                     u'venom_teethLower04_geo', u'venom_teethLower03_geo', u'venom_teethUpper24_geo',
                     u'venom_teethUpper23_geo', u'venom_teethUpper31_geo', u'venom_teethUpper30_geo',
                     u'venom_teethUpper29_geo', u'venom_teethUpper19_geo', u'venom_teethUpper18_geo',
                     u'venom_teethUpper22_geo', u'venom_teethUpper21_geo', u'venom_teethUpper20_geo',
                     u'venom_teethUpper15_geo', u'venom_teethUpper14_geo', u'venom_teethUpper13_geo',
                     u'venom_teethUpper17_geo', u'venom_teethUpper16_geo', u'venom_teethUpper8_geo',
                     u'venom_teethUpper7_geo', u'venom_teethUpper12_geo', u'venom_teethUpper11_geo',
                     u'venom_teethUpper3_geo', u'venom_teethUpper2_geo', u'venom_eye_right_geo',
                     u'venom_teethUpper10_geo', u'venom_teethUpper9_geo', u'venom_teethUpper28_geo',
                     u'venom_teethUpper27_geo', u'venom_teethUpper26_geo', u'venom_teethUpper25_geo',
                     u'venom_teethUpper1_geo', u'venom_tounge_geo', u'venom_teethUpper6_geo',
                     u'venom_teethUpper5_geo', u'venom_teethUpper4_geo')
    data_save_load.load_skin_cluster(*geometry)


def finalize():
    pm.delete('C_reference_points_pnt')
    pm.delete('measures_ref_grp')


if __name__ == '__main__':
    build()