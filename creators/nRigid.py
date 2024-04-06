import pymel.core as pm
from RMPY import RMRigTools
from RMPY.creators import creatorsBase


class NRigid(creatorsBase.CreatorsBase):
    def __init__(self, *args, **kwargs):
        super(NRigid, self).__init__(*args, **kwargs)

        self._node = pm.createNode('nRigid')
        mesh = kwargs.pop('mesh', None)
        time = pm.ls(type='time')
        self.mesh = []
        if mesh:
            self.mesh = mesh
            self.connect(*([mesh] + time))

    @property
    def transform(self):
        return self._node.getParent()

    @property
    def node(self):
        return self._node

    @node.setter
    def node(self, value):
        self._node = value

    def create_from_mesh(self, *geo):
        self.connect(geo[0])

    def connect(self, *nodes):
        for each_node in nodes:
            if pm.objectType(each_node) == 'transform':
                evaluation_node = each_node.getShapes()[0]
            else:
                evaluation_node = each_node
            if pm.objectType(evaluation_node) == 'time':
                self._connect_time(evaluation_node)
            if pm.objectType(evaluation_node) == 'mesh':
                self._connect_mesh(evaluation_node)

    def _connect_time(self, time_node):
        pm.connectAttr('{}.outTime'.format(time_node), '{}.currentTime'.format(self._node), f=True)

    def _connect_mesh(self, collision_mesh):
        pm.connectAttr('{}.worldMesh[0]'.format(collision_mesh), '{}.inputMesh'.format(self.node))
        self.mesh = collision_mesh
