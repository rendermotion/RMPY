import pymel.core as pm
from RMPY.creators import creatorsBase
from RMPY.creators import hairSystem
from RMPY.creators import nRigid


class Creator(creatorsBase.Creator):
    def __init__(self, *args, **kwargs):
        super(Creator, self).__init__(*args, **kwargs)
        self._node = None
        self.create()

    @property
    def indices(self):
        return self._node.componentIndices[0]

    @indices.setter
    def indices(self, value):
        self._node.componentIndices[0].set(value)

    @property
    def node(self):
        return self._node

    @node.setter
    def node(self, value):
        self._node = value

    def create(self):
        self.node = pm.createNode('nComponent')
        self.name_conv.rename_name_in_format(self._node)

    def connect(self, *nodes):
        for each_node in nodes:
            if pm.objectType(each_node) == 'hairSystem':
                self._connect_hair_system(each_node)
            else:
                print 'component connection with type {} not defined'.format(pm.objectType(each_node))

    def _connect_hair_system(self, hair_system):
        hair_system.nucleusId >> self._node.objectId




if __name__ == '__main__':
 hair_system = pm.ls('C_hairSystem01_rig_GRPShape')[0]
 component = Creator()
 component.create()
 component.connect(hair_system)
 print pm.getAttr('{}.componentIndices'.format(component.node))
