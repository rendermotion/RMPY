import pymel.core as pm
from pprint import pprint as pp


def export_shading(source_transform='__GEO__'):
    source_node = pm.ls(source_transform)[0]
    geometries = source_node.listRelatives(allDescendents=True, type='mesh')
    shading_engines = set(pm.listConnections(geometries, type='shadingEngine'))
    shading_data = {}
    for each in shading_engines:
        # print(pm.sets(each, q=True))
        shading_data[str(each)] =[str(each) for each in pm.sets(each, q=True)]
    pp(shading_data)

    # print(pm.objectType(selection))


if __name__ == '__main__':
    export_shading()