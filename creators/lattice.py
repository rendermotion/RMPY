import maya.cmds as cmds
import maya.api.OpenMaya as om
import pymel.core as pm
from RMPY.creators import deformerBase


class Lattice(deformerBase.WeightGeometryFilterBase):
    """
    Creator of lattice (ffd) deformers, with save / load support.

    On top of the data of WeightGeometryFilterBase (node, attributes, geometry) the dictionary contains:
        lattice, lattice_base: the node names, used to rename the nodes when the lattice is rebuilt.
        divisions: [s, t, u] divisions of the lattice shape.
        base_matrix: world matrix of the base lattice.
        relative_matrix: matrix of the lattice relative to the base lattice
                         (lattice_world_matrix * base_world_matrix.inverse()).
        lattice_parent, base_parent: parents of the lattice and the base, if any.
        point_deltas: {'s_t_u': [x, y, z]} the object space difference between each lattice point
                      and its default (undeformed) position. Only points that were moved are saved.
    """
    node_type = 'ffd'
    extra_path = '/lattices'
    deformer_attributes = ['envelope', 'outsideLattice', 'outsideFalloffDist', 'local',
                           'localInfluenceS', 'localInfluenceT', 'localInfluenceU',
                           'usePartialResolution', 'partialResolution', 'freezeGeometry']
    delta_tolerance = 1e-6

    def __init__(self, *args, **kwargs):
        super(Lattice, self).__init__(*args, **kwargs)
        self._lattice = None
        self._lattice_base = None

    @property
    def ffd(self):
        return self.node

    @ffd.setter
    def ffd(self, value):
        self.node = value

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

    @property
    def lattice_shape(self):
        return cmds.listRelatives(str(self._lattice), shapes=True, type='lattice')[0]

    def geo_base(self, *geometry, **kwargs):
        super(Lattice, self).geo_base(*geometry, **kwargs)
        divisions = kwargs.pop('divisions',  [2, 2, 2])
        pm.select(geometry)
        self.node, self._lattice, self._lattice_base = pm.lattice(divisions=divisions, objectCentered=True)
        self.name_convention.rename_name_in_format(self.node, self._lattice, self._lattice_base)
        return self.node, self._lattice, self._lattice_base

    def set_node(self, node):
        """Sets the ffd node and finds the lattice and base lattice transforms connected to it."""
        super(Lattice, self).set_node(node)
        self._lattice = self._connected_transform('{}.deformedLatticeMatrix'.format(self.node))
        self._lattice_base = self._connected_transform('{}.baseLatticeMatrix'.format(self.node))

    @staticmethod
    def get_ffd(deformed_geometry):
        return Lattice.get_deformer(deformed_geometry)

    @staticmethod
    def _connected_transform(plug):
        shapes = cmds.listConnections(plug, source=True, destination=False, shapes=True) or []
        if not shapes:
            return None
        if cmds.objectType(shapes[0], isAType='transform'):
            return pm.PyNode(shapes[0])
        return pm.PyNode(cmds.listRelatives(shapes[0], parent=True)[0])

    # ------------------------------------------------------------------ #
    # reading
    # ------------------------------------------------------------------ #
    def get_weights_dictionary(self):
        data = super(Lattice, self).get_weights_dictionary()
        base_matrix = om.MMatrix(cmds.xform(str(self._lattice_base), query=True, worldSpace=True, matrix=True))
        lattice_matrix = om.MMatrix(cmds.xform(str(self._lattice), query=True, worldSpace=True, matrix=True))
        relative_matrix = lattice_matrix * base_matrix.inverse()
        data.update(lattice=str(self._lattice),
                    lattice_base=str(self._lattice_base),
                    divisions=self.get_divisions(),
                    base_matrix=list(base_matrix),
                    relative_matrix=list(relative_matrix),
                    lattice_parent=self._parent(self._lattice),
                    base_parent=self._parent(self._lattice_base),
                    point_deltas=self.get_point_deltas())
        return data

    def get_divisions(self):
        shape = self.lattice_shape
        return [cmds.getAttr('{}.{}Divisions'.format(shape, axis)) for axis in 'stu']

    def get_point_deltas(self):
        """Returns {'s_t_u': [x, y, z]} with the object space offset of each moved lattice point
        from its default position."""
        shape = self.lattice_shape
        deltas = {}
        for (s, t, u), default in self._default_points(self.get_divisions()):
            position = cmds.xform('{}.pt[{}][{}][{}]'.format(shape, s, t, u),
                                  query=True, objectSpace=True, translation=True)
            delta = [position[i] - default[i] for i in range(3)]
            if any(abs(each) > self.delta_tolerance for each in delta):
                deltas['{}_{}_{}'.format(s, t, u)] = delta
        return deltas

    # ------------------------------------------------------------------ #
    # writing
    # ------------------------------------------------------------------ #
    def apply_data(self, data):
        """Restores divisions, ffd attributes, transforms, point deltas and weights."""
        self.set_divisions(data['divisions'])
        self.set_attributes(data.get('attributes', {}))
        self.set_matrices(data)
        self.set_point_deltas(data.get('point_deltas', {}), data['divisions'])
        self.set_weights(data.get('geometry', {}))

    def rebuild(self, data):
        self.geo_base(*self.saved_geometry(data), divisions=data['divisions'])
        for node_attr, key in [('_lattice', 'lattice'), ('_lattice_base', 'lattice_base')]:
            if data.get(key) and not cmds.objExists(data[key]):
                getattr(self, node_attr).rename(data[key])
        for node, parent in [(self._lattice, data.get('lattice_parent')),
                             (self._lattice_base, data.get('base_parent'))]:
            if parent and cmds.objExists(parent):
                pm.parent(node, parent)

    def set_divisions(self, divisions):
        if self.get_divisions() == list(divisions):
            return
        shape = self.lattice_shape
        for axis, value in zip('stu', divisions):
            cmds.setAttr('{}.{}Divisions'.format(shape, axis), value)

    def set_matrices(self, data):
        base_matrix = om.MMatrix(data['base_matrix'])
        lattice_matrix = om.MMatrix(data['relative_matrix']) * base_matrix
        cmds.xform(str(self._lattice_base), worldSpace=True, matrix=list(base_matrix))
        cmds.xform(str(self._lattice), worldSpace=True, matrix=list(lattice_matrix))

    def set_point_deltas(self, point_deltas, divisions):
        """Sets every lattice point to its default position plus the saved delta,
        points without a delta are reset to their default position."""
        shape = self.lattice_shape
        for (s, t, u), default in self._default_points(divisions):
            delta = point_deltas.get('{}_{}_{}'.format(s, t, u), [0.0, 0.0, 0.0])
            cmds.xform('{}.pt[{}][{}][{}]'.format(shape, s, t, u), objectSpace=True,
                       translation=[default[i] + delta[i] for i in range(3)])

    # ------------------------------------------------------------------ #
    # utilities
    # ------------------------------------------------------------------ #
    @staticmethod
    def _default_points(divisions):
        """Yields ((s, t, u), [x, y, z]) with the default object space position of every lattice point,
        a lattice is a unit cube from -0.5 to 0.5 on each axis, the transform gives it its size."""
        def coordinate(index, count):
            return -0.5 + float(index) / (count - 1) if count > 1 else 0.0
        s_div, t_div, u_div = divisions
        for s in range(s_div):
            for t in range(t_div):
                for u in range(u_div):
                    yield (s, t, u), [coordinate(s, s_div), coordinate(t, t_div), coordinate(u, u_div)]

    @staticmethod
    def _parent(node):
        parent = cmds.listRelatives(str(node), parent=True)
        return parent[0] if parent else None


if __name__ == '__main__':
    new_lattice = Lattice()
    new_lattice.geo_base('L_EYE_01_HIGH', name='Leye')
    # new_lattice.save()
    # Lattice.by_name('<ffd name>').load()
