import pymel.core as pm
from RMPY.creators import creatorsBase
from RMPY.creators import follicle


class HairSystem(creatorsBase.CreatorsBase):
    def __init__(self, *args, **kwargs):
        super(HairSystem, self).__init__(*args, **kwargs)

        self._follicles = []
        self._node = None
        self._valid_connections = ['hairSystem', 'follicle']
        self.create(*args, **kwargs)

    @property
    def transform(self):
        return self._node.getParent()

    @property
    def node(self):
        return self._node

    @node.setter
    def node(self, value):
        self._node = value

    @property
    def follicles(self):
        return self._follicles

    @follicles.setter
    def follicles(self, value):
        self._follicles = value

    def create(self, *args, **kwargs):
        self._node = pm.createNode('hairSystem')
        self.name_convention.rename_name_in_format(self.transform, name='hairSystem')
        self._node.clumpWidth.set(0.00001)
        self._node.active.set(1)

        self._node.hairsPerClump.set(1)
        time_node = pm.ls(type='time')
        self.connect(*time_node)
        for init_connection in kwargs.keys():
            if init_connection in self._valid_connections:
                self.connect(kwargs[init_connection])

    def connect(self, *nodes):
        for each_node in nodes:
            if pm.objectType(each_node) == 'follicle':
                self._connect_follicle(each_node)

            elif pm.objectType(each_node) == 'time':
                self._connect_time(each_node)
            else:
                print ('connection with type {} not defined'.format())

    def _connect_time(self, time_node):
        pm.connectAttr('{}.outTime'.format(time_node), '{}.currentTime'.format(self._node), f=True)

    def _connect_follicle(self, node):
        connect_index = 0

        connect_index_list = self._node.outputHair.get(multiIndices=True)
        if connect_index_list:
            while connect_index in connect_index_list:
                connect_index = connect_index + 1

        self._node.outputHair[connect_index] >> node.currentPosition
        node.outHair >> self._node.inputHair[connect_index]

    def add_follicle(self):
        new_follicle = follicle.Follicle(name_convention=self.name_convention)

        new_follicle.hair_system = self.node
        new_follicle.build()
        self.connect(new_follicle.node)
        self.follicles.append(new_follicle)