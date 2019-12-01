import pymel.core as pm
from RMPY.creators import creatorsBase


class Flow(object):
    def __init__(self):
        self._flow = None
        self._ffd = None
        self._lattice = None
        self._lattice_base = None

    @property
    def flow(self):
        return self._flow

    @flow.setter
    def flow(self, value):
        self._flow = value

    @property
    def ffd(self):
        return self._ffd

    @ffd.setter
    def ffd(self, value):
        self._ffd = value

    @property
    def lattice(self):
        return self._lattice

    @lattice.setter
    def lattice(self, value):
        self._lattice = value

    @property
    def lattice_base(self):
        return self._lattice_base

    @lattice_base.setter
    def lattice_base(self, value):
        self._lattice_base = value


class Creator(creatorsBase.Creator):
    def __init__(self, *args, **kwargs):
        super(Creator, self).__init__(*args, **kwargs)

    def geo_base(self, *args, **kwargs):
        self.setup_name_conv_node_base(args[0])
        flow_node = Flow()
        flow_node.flow, flow_node.ffd, flow_node.lattice, flow_node.lattice_base = pm.flow(*args, **kwargs)
        self.name_conv.rename_name_in_format(flow_node.flow, name='flow')
        self.name_conv.rename_name_in_format(flow_node.ffd, name='ffd')
        self.name_conv.rename_name_in_format(flow_node.lattice, name='lattice')
        self.name_conv.rename_name_in_format(flow_node.lattice_base, name='latticeBase')
        return flow_node


if __name__ == '__main__':
    pass