import pymel.core as pm
from RMPY import RMRigTools
from RMPY.rig import genericRig
from core import validate

reload(genericRig)
reload(validate)

class SpaceLocator(genericRig.GenericRig):
    def __init__(self, *args):
        super(SpaceLocator, self).__init__(*args)
        self.name_conv.default_names['system'] = 'reference'

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

    def create_point_base(self, *point_list):
        for each in point_list:
            position = validate.as_vector(each)
            new_locator = pm.spaceLocator()
            self.name_conv.rename_name_in_format(new_locator)
            new_locator.translate.set([position[0],position[1],position[2]])

if __name__ == '__main__':
    selection = pm.ls(orderedSelection=True)
    spcLoc = SpaceLocator()
    spcLoc.create_point_base(*selection)
    #for each_vtx in selection:
    #    spcLoc.create_vertex_base(*each_vtx)
