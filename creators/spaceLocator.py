import pymel.core as pm
from RMPY import RMRigTools
from RMPY import RMNameConvention
reload(RMNameConvention)

class spaceLocator(object):
    def __init__(self):
        self.nodes = []
        self.name_conv = RMNameConvention.RMNameConvention()

    def create_vertex_base(self, *vertex_list):
        position = []
        for each in vertex_list:
            if each.__class__ == pm.general.MeshVertex:
                position.append(each.getPosition(space='world'))
            else:
                print each.__class__
        new_space_locator = pm.spaceLocator()
        self.name_conv.rename_name_in_format(new_space_locator)
        new_space_locator.translate.set(RMRigTools.average(*position))

    def create_node_base(self, *node_list):
        pass

    def create_point_base(self, *point_list):
        pass

if __name__ == '__main__':
    spcLoc = spaceLocator()
    spcLoc.name_conv.default_names['system'] = 'reference'
    selection = pm.ls(selection=True)
    spcLoc.create_vertex_base(*selection)
    #for each_vtx in selection:
    #    spcLoc.create_vertex_base(*each_vtx)
