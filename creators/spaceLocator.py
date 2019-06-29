import pymel.core as pm
from RMPY import RMRigTools
from RMPY.creators import creatorsBase
from RMPY.core import dataValidators


def average(*args):
    result = pm.datatypes.Vector(0, 0, 0)
    for each in args:
        result += dataValidators.as_vector(each)
    result = result / len(args)
    return result


class SpaceLocator(creatorsBase.creatorsBase):
    def __init__(self, *args):
        super(SpaceLocator, self).__init__(*args)
        self.name_convention.default_names['system'] = 'reference'

    def create_vertex_base(self, *vertex_list):
        position = []
        for each in vertex_list:
            if each.__class__ == pm.general.MeshVertex:
                for each_vtx in each:
                    position.append(each_vtx.getPosition(space='world'))
            else:
                print each.__class__
        new_space_locator = pm.spaceLocator()
        self.name_convention.rename_name_in_format(new_space_locator)
        new_space_locator.translate.set(RMRigTools.average(*position))

    def point_base(self, *point_list):
        for each in point_list:
            position = dataValidators.as_vector(each)
            new_locator = pm.spaceLocator()
            self.name_convention.rename_name_in_format(new_locator)
            new_locator.translate.set([position[0], position[1], position[2]])

if __name__ == '__main__':
    #selection = pm.ls(orderedSelection=True)
    #spcLoc = SpaceLocator()
    #spcLoc.point_base(*selection)
    print 'done'

    #for each_vtx in selection:
    #    spcLoc.create_vertex_base(*each_vtx)
