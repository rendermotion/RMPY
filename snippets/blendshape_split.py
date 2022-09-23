from maya.api import OpenMaya
from maya.api import OpenMayaAnim
import maya.cmds as cmds
import pymel.core as pm


def split_blendshape(base_geometry, blendshape, delete_blendshapes=True):
    blendshape_geo = get_mfn_mesh(blendshape)
    base_geo = get_mfn_mesh(base_geometry)

    x_geometry = cmds.duplicate(base_geometry, name='x')[0]
    y_geometry = cmds.duplicate(base_geometry, name='y')[0]
    z_geometry = cmds.duplicate(base_geometry, name='z')[0]

    xn_geometry = cmds.duplicate(base_geometry, name='xn')[0]
    yn_geometry = cmds.duplicate(base_geometry, name='yn')[0]
    zn_geometry = cmds.duplicate(base_geometry, name='zn')[0]

    base_geo_points = base_geo.getPoints(space=OpenMaya.MSpace.kObject)
    blendsape_geo_points = blendshape_geo.getPoints(space=OpenMaya.MSpace.kObject)

    base_geo_x = get_mfn_mesh(x_geometry)
    base_geo_y = get_mfn_mesh(y_geometry)
    base_geo_z = get_mfn_mesh(z_geometry)

    base_geo_xn = get_mfn_mesh(xn_geometry)
    base_geo_yn = get_mfn_mesh(yn_geometry)
    base_geo_zn = get_mfn_mesh(zn_geometry)

    x_points = base_geo_x.getPoints(space=OpenMaya.MSpace.kObject)
    y_points = base_geo_y.getPoints(space=OpenMaya.MSpace.kObject)
    z_points = base_geo_z.getPoints(space=OpenMaya.MSpace.kObject)

    xn_points = base_geo_x.getPoints(space=OpenMaya.MSpace.kObject)
    yn_points = base_geo_y.getPoints(space=OpenMaya.MSpace.kObject)
    zn_points = base_geo_z.getPoints(space=OpenMaya.MSpace.kObject)

    # deltas_index_list = []

    for index, each_point_blendshape in enumerate(blendsape_geo_points):
        if base_geo_points[index].x < each_point_blendshape.x:
            x_points[index].x = each_point_blendshape.x
        else:
            xn_points[index].x = each_point_blendshape.x

        if base_geo_points[index].y < each_point_blendshape.y:
            y_points[index].y = each_point_blendshape.y
        else:
            yn_points[index].y = each_point_blendshape.y

        if base_geo_points[index].z < each_point_blendshape.z:
            z_points[index].z = each_point_blendshape.z
        else:
            zn_points[index].z = each_point_blendshape.z

    base_geo_x.setPoints(x_points)
    base_geo_y.setPoints(y_points)
    base_geo_z.setPoints(z_points)

    base_geo_xn.setPoints(xn_points)
    base_geo_yn.setPoints(yn_points)
    base_geo_zn.setPoints(zn_points)

    splited = pm.duplicate(base_geometry, name='{}Splited'.format(blendshape))[0]
    blend_shape_node = pm.ls(pm.blendShape(splited))[0]

    pm.blendShape(blend_shape_node, edit=True, target=[splited, 0,  x_geometry, 1.0])
    pm.blendShape(blend_shape_node, edit=True, target=[splited, 1, y_geometry, 1.0])
    pm.blendShape(blend_shape_node, edit=True, target=[splited, 2, z_geometry, 1.0])

    pm.blendShape(blend_shape_node, edit=True, target=[splited, 3, xn_geometry, 1.0])
    pm.blendShape(blend_shape_node, edit=True, target=[splited, 4, yn_geometry, 1.0])
    pm.blendShape(blend_shape_node, edit=True, target=[splited, 5, zn_geometry, 1.0])
    if delete_blendshapes:
        pm.delete(x_geometry, y_geometry, z_geometry, xn_geometry, yn_geometry, zn_geometry)


def copy_vertex_position(source, destination):
    source_mfn_msh = get_mfn_mesh(source)
    destination_mfn_msh = get_mfn_mesh(destination)
    source_points = source_mfn_msh.getPoints()
    destination_mfn_msh.setPoints(source_points)


def get_mfn_mesh(name):
    sel = OpenMaya.MSelectionList()
    try:
        sel.add(str(name))
    except RuntimeError as e:
        return e

    dagPath = sel.getDagPath(0)
    return OpenMaya.MFnMesh(dagPath)


if __name__ == '__main__':
    selection = pm.ls(selection=True)
    # split_blendshape('Neutral', str(selection[0]))
    copy_vertex_position(*selection)