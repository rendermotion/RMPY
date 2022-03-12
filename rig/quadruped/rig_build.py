from RMPY.rig.quadruped import rigQuadruped
from RMPY.rig import rigHierarchy
from RMPY.core import controls
from RMPY.core import data_save_load
import pymel.core as pm


def build():
    load_sources()
    build_rig()
    # hierarchy()
    load_data()
    # finalize()


def load_sources():
    data_save_load.import_all_available_maya_files()


def build_rig():
    rig_biped = rigQuadruped.RigQuadruped()
    rig_biped.build()
    controls.color_now_all_ctrls()


def hierarchy():
    rig_hierarchy = rigHierarchy.RigHierarchy()
    pm.parent('geo_grp', rig_hierarchy.geometry)


def load_data():
    controls_list = pm.ls('*ctr')
    data_save_load.load_curves(*controls_list)

    # geometry = pm.ls('')
    # data_save_load.load_skin_cluster(*geometry)


def finalize():
    pm.delete('C_reference_points_pnt')
    pm.delete('measures_ref_grp')


if __name__ == '__main__':
    # selection = pm.ls(selection=True)
    # data_save_load.save_curve(*selection)
    build()
    # load_data()
    '''low_rez_geo = [u'dog_model_V03:group401', u'dog_model_V03:polySurface809', u'dog_model_V03:polySurface304',
                   u'dog_model_V03:polySurface302', u'dog_model_V03:group409', u'dog_model_V03:polySurface834',
                   u'dog_model_V03:group5__body2_pasted__polySurface1', u'dog_model_V03:polySurface835',
                   u'dog_model_V03:group31_group27__heart__body_pasted__polySurface1', u'dog_model_V03:polySurface271',
                   u'dog_model_V03:group176', u'dog_model_V03:group564|dog_model_V03:pasted__Hard_Surface_Mesh_1986',
                   u'dog_model_V03:group563|dog_model_V03:pasted__Hard_Surface_Mesh_1986',
                   u'dog_model_V03:group563|dog_model_V03:pasted__Hard_Surface_Mesh_2070',
                   u'dog_model_V03:group564|dog_model_V03:pasted__Hard_Surface_Mesh_2070',
                   u'dog_model_V03:C_mainChest00_innerBody_msh', u'dog_model_V03:pasted__polySurface5',
                   u'dog_model_V03:pasted__pCube3', u'dog_model_V03:pasted__polySurface30',
                   u'dog_model_V03:pasted__pCube7',
                   u'dog_model_V03:group35_group3_group_pasted__heart_pasted__body_pasted__polySurface1',
                   u'dog_model_V03:C_main00_backLegs_msh', u'dog_model_V03:C_main00_frontLegs_msh',
                   u'dog_model_V03:polySurface124',
                   u'dog_model_V03:polySurface94']'''