import pymel.core as pm
from RMPY import RMRigTools
from RMPY.creators import creatorsBase
import importlib
reload(creatorsBase)

class Lattice(creatorsBase.CreatorsBase):
    def __init__(self, *args, **kwargs):
        super(Lattice, self).__init__(*args, **kwargs)
        self._node = None
        self._lattice = None
        self._lattice_base = None
        self.ffd = None

    def geo_base(self, *geometry, **kwargs):
        super(Lattice, self).geo_base(*geometry, **kwargs)
        divisions = kwargs.pop('divisions',  [2, 2, 2])
        pm.select(geometry)
        self.ffd, self._lattice, self._lattice_base = pm.lattice(divisions=divisions, objectCentered=True)
        self.name_convention.rename_name_in_format(self.ffd, self._lattice, self._lattice_base)
        return self.ffd, self._lattice, self._lattice_base


if __name__ == '__main__':
    new_lattice = Lattice()
    new_lattice.geo_base('L_EYE_01_HIGH', name='Leye')



