import pymel.core as pm
from RMPY.creators import creatorsBase
from RMPY.creators import hairSystem
from RMPY.creators import nRigid
from RMPY.core import dataValidators


class Nucleus(creatorsBase.CreatorsBase):
    def __init__(self, *args, **kwargs):
        super(Nucleus, self).__init__(*args, **kwargs)

        self._node = None
        self._hair_systems = []
        self._collision = []

        if args:
            self._node = pm.ls(args[0])[0]
        else:
            self.create()

    @property
    def transform(self):
        return self._node.getParent()

    @property
    def collision(self):
        return self._collision

    @collision.setter
    def collision(self):
        return self._collision

    @property
    def hair_systems(self):
        return self._hair_systems

    @hair_systems.setter
    def hair_systems(self):
        return self._hair_systems

    @property
    def node(self):
        return self._node

    @node.setter
    def node(self, value):
        self._node = dataValidators.as_pymel_nodes(value)

    @property
    def start_frame(self):
        return self._node.startFrame

    @start_frame.setter
    def start_frame(self, value):
        self._node.startFrame.set(value)

    def create(self):
        self._node = pm.createNode('nucleus')
        self.name_convention.rename_name_in_format(self._node)
        self.start_frame = pm.playbackOptions(q=True, min=True)
        time_node = pm.ls(type='time')
        self.connect(*time_node)

    def connect(self, *nodes):
        for each_node in nodes:
            if pm.objectType(each_node) == 'time':
                self._connect_time(each_node)
            elif pm.objectType(each_node) == 'hairSystem':
                self._connect_hair_system(each_node)
            elif pm.objectType(each_node) == 'nRigid':
                self._connect_nRigid(each_node)

    def _connect_time(self, time_node):
        pm.connectAttr('{}.outTime'.format(time_node), '{}.currentTime'.format(self._node), f=True)

    def _connect_hair_system(self, node):
        connect_index = 0

        connect_index_list = self._node.inputActive.get(multiIndices=True)
        if connect_index_list:
            while connect_index in connect_index_list:
                connect_index = connect_index + 1

        pm.connectAttr('{}.currentState'.format(node),
                       '{}.inputActive[{}]'.format(self._node, connect_index))
        pm.connectAttr('{}.startState'.format(node),
                       '{}.inputActiveStart[{}]'.format(self._node, connect_index))

        self._node.outputObjects[connect_index] >> node.nextState

        pm.connectAttr('{}.startFrame'.format(self._node), '{}.startFrame'.format(node))

    def _connect_nRigid(self, nRigidNode):
        pm.connectAttr('{}.startFrame'.format(self.node), '{}.startFrame'.format(nRigidNode))

        connect_index_list = self.node.inputPassive.get(multiIndices=True)
        # print 'got connect index {}, for {} connection'.format(connect_index_list, nRigidNode)
        connect_index = 0
        if connect_index_list:
            while connect_index in connect_index_list:
                connect_index = connect_index + 1

        pm.connectAttr('{}.currentState'.format(nRigidNode),
                       '{}.inputPassive[{}]'.format(self.node, connect_index))

        pm.connectAttr('{}.startState'.format(nRigidNode),
                       '{}.inputPassiveStart[{}]'.format(self.node, connect_index))

    def add_hair_system(self):
        new_hair_system = hairSystem.HairSystem(name_convention=self.name_convention)

        self.connect(new_hair_system.node)
        self.hair_systems.append(new_hair_system)

    def add_collision_mesh(self, *mesh):
        mesh = dataValidators.as_pymel_nodes(mesh)

        for each_mesh in mesh:
            new_nrigid = nRigid.NRigid(name_convention=self.name_convention, mesh=each_mesh)
            self.connect(new_nrigid.node)
            for each_hair_system in self.hair_systems:
                for each_follicle in each_hair_system.follicles:
                    each_mesh.outMesh >> each_follicle.node.inputMesh
                    each_mesh.worldMatrix[0] >> each_follicle.node.inputWorldMatrix
            self.collision.append(new_nrigid)


if __name__ == '__main__':
    nucleus = Creator('C_object00_centerCables_NCL')
    nucleus.add_collision_mesh('defaultDefault_C_hip_0001_low_GEP')