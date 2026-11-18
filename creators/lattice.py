import maya.cmds as cmds
import maya.api.OpenMaya as om
import pymel.core as pm
from RMPY.creators import creatorsBase
from RMPY.core import dataManager


class Lattice(creatorsBase.CreatorsBase):
    """
    Creator of lattice (ffd) deformers, with save / load support.

    The data dictionary produced by get_weights_dictionary (and stored by save) contains:
        ffd, lattice, lattice_base: the node names, used to rename the nodes when the lattice is rebuilt.
        divisions: [s, t, u] divisions of the lattice shape.
        attributes: the ffd deformer settings (envelope, local influence, outside lattice...).
        base_matrix: world matrix of the base lattice.
        relative_matrix: matrix of the lattice relative to the base lattice
                         (lattice_world_matrix * base_world_matrix.inverse()).
        lattice_parent, base_parent: parents of the lattice and the base, if any.
        point_deltas: {'s_t_u': [x, y, z]} the object space difference between each lattice point
                      and its default (undeformed) position. Only points that were moved are saved.
        geometry: {transform: {'shape', 'point_count', 'weights'}} the per point weights of each
                  deformed geometry.
    """
    ffd_attributes = ['envelope', 'outsideLattice', 'outsideFalloffDist', 'local',
                      'localInfluenceS', 'localInfluenceT', 'localInfluenceU',
                      'usePartialResolution', 'partialResolution', 'freezeGeometry']
    delta_tolerance = 1e-6

    def __init__(self, *args, **kwargs):
        super(Lattice, self).__init__(*args, **kwargs)
        self._node = None
        self._lattice = None
        self._lattice_base = None
        self.ffd = None
        self.weights_dict = {}
        self.extra_path = '/lattices'

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

    def geo_base(self, *geometry, **kwargs):
        super(Lattice, self).geo_base(*geometry, **kwargs)
        divisions = kwargs.pop('divisions',  [2, 2, 2])
        pm.select(geometry)
        self.ffd, self._lattice, self._lattice_base = pm.lattice(divisions=divisions, objectCentered=True)
        self.name_convention.rename_name_in_format(self.ffd, self._lattice, self._lattice_base)
        return self.ffd, self._lattice, self._lattice_base

    # ------------------------------------------------------------------ #
    # finding existing lattices
    # ------------------------------------------------------------------ #
    @classmethod
    def by_name(cls, ffd_name):
        """Returns an instance of Lattice that uses the ffd node with the provided name.
        If the node doesn't exist, the instance is returned with only the name set, so load can rebuild it.
        """
        new_class_object = cls()
        if pm.objExists(ffd_name):
            node = pm.ls(ffd_name)[0]
            if node.__class__ == pm.nodetypes.Ffd:
                new_class_object.set_ffd(node)
                return new_class_object
            print("error couldn't create Lattice, node class is :%s" % node.__class__)
            return None
        new_class_object.ffd = ffd_name
        print("WARNING: Lattice object created, node doesn't exists")
        return new_class_object

    @classmethod
    def by_node(cls, node):
        """Returns an instance of Lattice from an ffd node, or from a geometry deformed by a lattice."""
        node = pm.ls(node)[0]
        if node.__class__ == pm.nodetypes.Ffd:
            ffd = node
        else:
            ffd = cls.get_ffd(node)
        if ffd:
            new_class_object = cls()
            new_class_object.set_ffd(ffd)
            return new_class_object
        print("error couldn't create Lattice, no ffd on history of object %s" % node)
        return None

    @staticmethod
    def get_ffd(deformed_geometry):
        for each in pm.listHistory(deformed_geometry, interestLevel=2, pruneDagObjects=True):
            if each.__class__ == pm.nodetypes.Ffd:
                return each
        return None

    def set_ffd(self, ffd):
        """Sets the ffd node and finds the lattice and base lattice transforms connected to it."""
        self.ffd = pm.PyNode(ffd)
        self._lattice = self._connected_transform('{}.deformedLatticeMatrix'.format(self.ffd))
        self._lattice_base = self._connected_transform('{}.baseLatticeMatrix'.format(self.ffd))

    @staticmethod
    def _connected_transform(plug):
        shapes = cmds.listConnections(plug, source=True, destination=False, shapes=True) or []
        if not shapes:
            return None
        if cmds.objectType(shapes[0], isAType='transform'):
            return pm.PyNode(shapes[0])
        return pm.PyNode(cmds.listRelatives(shapes[0], parent=True)[0])

    @property
    def lattice_shape(self):
        return cmds.listRelatives(str(self._lattice), shapes=True, type='lattice')[0]

    # ------------------------------------------------------------------ #
    # save / load
    # ------------------------------------------------------------------ #
    def save(self, *args, **kwargs):
        if len(args) >= 1:
            file_name = args[0]
        else:
            file_name = '{}'.format(self.ffd)
        data_manager = dataManager.DataManager()
        data_manager.file_path = '{}{}'.format(data_manager.file_path, self.extra_path)
        data_manager.save(file_name, self.get_weights_dictionary())

    def load(self, *args, **kwargs):
        """Loads a lattice file and, unless apply=False, applies it.
        If the ffd doesn't exist in the scene, a new lattice is created on the saved geometries.
        """
        apply_data = kwargs.pop('apply', True)
        if len(args) >= 1:
            file_name = args[0]
        else:
            file_name = '{}'.format(self.ffd)
        data_manager = dataManager.DataManager()
        data_manager.file_path = '{}{}'.format(data_manager.file_path, self.extra_path)
        print('path to search = {}'.format(data_manager.file_path))
        self.weights_dict = data_manager.load(file_name)
        if self.weights_dict and apply_data:
            self.apply_weights_dictionary(self.weights_dict)
        return self.weights_dict

    def _representation(self):
        return self.get_weights_dictionary()

    # ------------------------------------------------------------------ #
    # reading
    # ------------------------------------------------------------------ #
    def get_weights_dictionary(self):
        ffd = str(self.ffd)
        base_matrix = om.MMatrix(cmds.xform(str(self._lattice_base), query=True, worldSpace=True, matrix=True))
        lattice_matrix = om.MMatrix(cmds.xform(str(self._lattice), query=True, worldSpace=True, matrix=True))
        relative_matrix = lattice_matrix * base_matrix.inverse()

        data = dict(ffd=ffd,
                    lattice=str(self._lattice),
                    lattice_base=str(self._lattice_base),
                    divisions=self.get_divisions(),
                    attributes=self.get_ffd_attributes(),
                    base_matrix=list(base_matrix),
                    relative_matrix=list(relative_matrix),
                    lattice_parent=self._parent(self._lattice),
                    base_parent=self._parent(self._lattice_base),
                    point_deltas=self.get_point_deltas(),
                    geometry={})

        for shape, geo_index in self.deformed_geometry():
            transform = cmds.listRelatives(shape, parent=True)[0]
            weights = self.get_geometry_weights(geo_index, self.point_count(shape))
            data['geometry'][transform] = dict(shape=shape, point_count=len(weights), weights=weights)
        return data

    def deformed_geometry(self):
        """Returns a list of [shape, geometry_index] for every geometry deformed by the ffd."""
        ffd = str(self.ffd)
        shapes = cmds.deformer(ffd, query=True, geometry=True) or []
        indices = cmds.deformer(ffd, query=True, geometryIndices=True) or []
        return list(zip(shapes, indices))

    def get_divisions(self):
        shape = self.lattice_shape
        return [cmds.getAttr('{}.{}Divisions'.format(shape, axis)) for axis in 'stu']

    def get_ffd_attributes(self):
        ffd = str(self.ffd)
        return {each: cmds.getAttr('{}.{}'.format(ffd, each)) for each in self.ffd_attributes
                if cmds.attributeQuery(each, node=ffd, exists=True)}

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

    def get_geometry_weights(self, geo_index, point_count):
        """Weights are stored sparse, any point without a stored value has a weight of 1.0"""
        weights = [1.0] * point_count
        plug = '{}.weightList[{}].weights'.format(self.ffd, geo_index)
        indices = cmds.getAttr(plug, multiIndices=True) or []
        if not indices:
            return weights
        values = cmds.getAttr(plug)
        if isinstance(values, (list, tuple)) and values and isinstance(values[0], (list, tuple)):
            values = values[0]
        if not isinstance(values, (list, tuple)):
            values = [values]
        if len(values) != len(indices):
            values = [cmds.getAttr('{}[{}]'.format(plug, each)) for each in indices]
        for index, value in zip(indices, values):
            if index < point_count:
                weights[index] = value
        return weights

    # ------------------------------------------------------------------ #
    # writing
    # ------------------------------------------------------------------ #
    def apply_weights_dictionary(self, *args, **kwargs):
        """Applies a dictionary created by get_weights_dictionary: rebuilds the lattice if it doesn't exist,
        then restores divisions, ffd attributes, transforms, point deltas and weights."""
        data = args[0] if args else self.weights_dict
        if not self.ffd or not pm.objExists(str(self.ffd)):
            if pm.objExists(data['ffd']):
                self.set_ffd(data['ffd'])
            else:
                self.rebuild(data)

        self.set_divisions(data['divisions'])
        self.set_ffd_attributes(data.get('attributes', {}))
        self.set_matrices(data)
        self.set_point_deltas(data.get('point_deltas', {}), data['divisions'])
        self.set_weights(data.get('geometry', {}))

    def rebuild(self, data):
        geometry = [each for each in data['geometry'] if cmds.objExists(each)]
        if not geometry:
            raise RuntimeError('none of the geometries saved for lattice {} exist in the scene'.format(data['ffd']))
        self.geo_base(*geometry, divisions=data['divisions'])
        # restore the saved names so the node keeps matching its file
        for node_attr, key in [('ffd', 'ffd'), ('_lattice', 'lattice'), ('_lattice_base', 'lattice_base')]:
            node = getattr(self, node_attr)
            if not cmds.objExists(data[key]):
                node.rename(data[key])
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

    def set_ffd_attributes(self, attributes):
        ffd = str(self.ffd)
        for attribute, value in attributes.items():
            plug = '{}.{}'.format(ffd, attribute)
            if cmds.objExists(plug) and cmds.getAttr(plug, settable=True):
                cmds.setAttr(plug, value)

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

    def set_weights(self, geometry_data):
        ffd = str(self.ffd)
        for shape, geo_index in self.deformed_geometry():
            transform = cmds.listRelatives(shape, parent=True)[0]
            geo_data = geometry_data.get(transform)
            if not geo_data:
                print('no lattice weights saved for {}'.format(transform))
                continue
            weights = geo_data['weights']
            count = self.point_count(shape)
            if count != len(weights):
                raise RuntimeError('point count mismatch on {}: scene has {}, data has {}'.format(
                    transform, count, len(weights)))
            cmds.setAttr('{}.weightList[{}].weights[0:{}]'.format(ffd, geo_index, count - 1),
                         *weights, size=count)

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
    def point_count(shape):
        if cmds.objectType(shape) == 'mesh':
            return cmds.polyEvaluate(shape, vertex=True)
        return len(cmds.ls('{}.cp[*]'.format(shape), flatten=True))

    @staticmethod
    def _parent(node):
        parent = cmds.listRelatives(str(node), parent=True)
        return parent[0] if parent else None


if __name__ == '__main__':
    new_lattice = Lattice()
    new_lattice.geo_base('L_EYE_01_HIGH', name='Leye')
    # new_lattice.save()
    # Lattice.by_name('<ffd name>').load()
