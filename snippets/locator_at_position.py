import pymel.core as pm
from RMPY import RMRigTools
reload(RMRigTools)

def locator_at_vertex_position(vertex_list):
    locator = pm.spaceLocator()
    pm.xform(locator, translation=average_vertex_position(vertex_list), worldSpace=True)
    return locator

def average_vertex_position(vertex_list):
    position_list = []
    for each in vertex_list:
        if each.__class__ == pm.general.MeshVertex:
            for each_vertex in each:
                position = each_vertex.getPosition(space='world')
                if len(position) == 3:
                    position_list.append([position[0], position[1], position[2]])
    return RMRigTools.average(*position_list)

if __name__ == '__main__':
    selection = pm.ls(selection=True)
    locator_at_vertex_position(selection)
