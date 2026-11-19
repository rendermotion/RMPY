import maya.cmds as cmds
import pymel.core as pm
from RMPY.creators import creatorsBase
from RMPY.core import dataManager


class ShrinkWrap(creatorsBase.CreatorsBase):
    """
    Creator of shrinkWrap deformers, with save / load support.

    The data dictionary produced by get_weights_dictionary (and stored by save) contains:
        node: the shrinkWrap node name, used to rename the node when it is rebuilt.
        target: the transform of the target geometry the deformed geometry is wrapped to.
        attributes: the shrinkWrap settings (projection, offset, inflation, falloff...).
        geometry: {transform: {'shape', 'point_count', 'weights'}} the per point weights of each
                  deformed geometry.
    """
    shrink_wrap_attributes = ['envelope', 'projection', 'closestIfNoIntersection', 'reverse', 'bidirectional',
                              'boundingBoxCenter', 'axisReference', 'alongX', 'alongY', 'alongZ',
                              'offset', 'targetInflation', 'targetSmoothLevel', 'falloff', 'falloffIterations',
                              'shapePreservationEnable', 'shapePreservationSteps', 'shapePreservationReprojection']
    # attributes of the target mesh shape that drive the smoothing of the target inside the shrinkWrap,
    # Maya connects them when creating the deformer from the menu.
    target_connections = ['continuity', 'smoothUVs', 'keepBorder', 'boundaryRule',
                          'keepHardEdge', 'propagateEdgeHardness', 'keepMapBorders']

    def __init__(self, *args, **kwargs):
        super(ShrinkWrap, self).__init__(*args, **kwargs)
        self.node = None
        self.weights_dict = {}
        self.extra_path = '/shrinkWraps'

    def geo_base(self, *geometry, **kwargs):
        """Creates a shrinkWrap on the geometry, wrapped to the geometry provided on the target keyword."""
        target = kwargs.pop('target', None)
        if not target:
            raise RuntimeError('a target geometry is needed to create a shrinkWrap, use target=<geometry>')
        super(ShrinkWrap, self).geo_base(*geometry, **kwargs)
        self.node = pm.PyNode(cmds.deformer(*[str(each) for each in geometry], type='shrinkWrap')[0])
        self.connect_target(target)
        self.node = pm.PyNode(self.name_convention.rename_name_in_format(str(self.node)))
        return self.node

    # ------------------------------------------------------------------ #
    # finding existing shrinkWraps
    # ------------------------------------------------------------------ #
    @classmethod
    def by_name(cls, node_name):
        """Returns an instance of ShrinkWrap that uses the shrinkWrap node with the provided name.
        If the node doesn't exist, the instance is returned with only the name set, so load can rebuild it.
        """
        new_class_object = cls()
        if pm.objExists(node_name):
            if cmds.objectType(node_name) == 'shrinkWrap':
                new_class_object.node = pm.PyNode(node_name)
                return new_class_object
            print("error couldn't create ShrinkWrap, node type is :%s" % cmds.objectType(node_name))
            return None
        new_class_object.node = node_name
        print("WARNING: ShrinkWrap object created, node doesn't exists")
        return new_class_object

    @classmethod
    def by_node(cls, node):
        """Returns an instance of ShrinkWrap from a shrinkWrap node, or from a geometry deformed by one."""
        if cmds.objectType(str(node)) == 'shrinkWrap':
            shrink_wrap = pm.PyNode(node)
        else:
            shrink_wrap = cls.get_shrink_wrap(node)
        if shrink_wrap:
            new_class_object = cls()
            new_class_object.node = shrink_wrap
            return new_class_object
        print("error couldn't create ShrinkWrap, no shrinkWrap on history of object %s" % node)
        return None

    @staticmethod
    def get_shrink_wrap(deformed_geometry):
        for each in pm.listHistory(deformed_geometry, interestLevel=2, pruneDagObjects=True):
            if pm.objectType(each) == 'shrinkWrap':
                return each
        return None

    # ------------------------------------------------------------------ #
    # target
    # ------------------------------------------------------------------ #
    @property
    def target(self):
        """The transform of the target geometry, None if no target is connected."""
        shapes = cmds.listConnections('{}.targetGeom'.format(self.node), source=True,
                                      destination=False, shapes=True) or []
        if not shapes:
            return None
        if cmds.objectType(shapes[0], isAType='transform'):
            return shapes[0]
        return cmds.listRelatives(shapes[0], parent=True)[0]

    def connect_target(self, target):
        """Connects the target geometry to the shrinkWrap, the same way Maya does when creating it from the menu."""
        node = str(self.node)
        target_shape = self._shape(target)
        cmds.connectAttr('{}.worldMesh[0]'.format(target_shape), '{}.targetGeom'.format(node), force=True)
        for each in self.target_connections:
            if cmds.attributeQuery(each, node=target_shape, exists=True) and \
                    cmds.attributeQuery(each, node=node, exists=True):
                cmds.connectAttr('{}.{}'.format(target_shape, each), '{}.{}'.format(node, each), force=True)

    # ------------------------------------------------------------------ #
    # save / load
    # ------------------------------------------------------------------ #
    def save(self, *args, **kwargs):
        if len(args) >= 1:
            file_name = args[0]
        else:
            file_name = '{}'.format(self.node)
        data_manager = dataManager.DataManager()
        data_manager.file_path = '{}{}'.format(data_manager.file_path, self.extra_path)
        data_manager.save(file_name, self.get_weights_dictionary())

    def load(self, *args, **kwargs):
        """Loads a shrinkWrap file and, unless apply=False, applies it.
        If the shrinkWrap doesn't exist in the scene, a new one is created on the saved geometries.
        """
        apply_data = kwargs.pop('apply', True)
        if len(args) >= 1:
            file_name = args[0]
        else:
            file_name = '{}'.format(self.node)
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
        data = dict(node=str(self.node),
                    target=self.target,
                    attributes=self.get_attributes(),
                    geometry={})
        for shape, geo_index in self.deformed_geometry():
            transform = cmds.listRelatives(shape, parent=True)[0]
            weights = self.get_geometry_weights(geo_index, self.point_count(shape))
            data['geometry'][transform] = dict(shape=shape, point_count=len(weights), weights=weights)
        return data

    def deformed_geometry(self):
        """Returns a list of [shape, geometry_index] for every geometry deformed by the shrinkWrap."""
        node = str(self.node)
        shapes = cmds.deformer(node, query=True, geometry=True) or []
        indices = cmds.deformer(node, query=True, geometryIndices=True) or []
        return list(zip(shapes, indices))

    def get_attributes(self):
        node = str(self.node)
        return {each: cmds.getAttr('{}.{}'.format(node, each)) for each in self.shrink_wrap_attributes
                if cmds.attributeQuery(each, node=node, exists=True)}

    def get_geometry_weights(self, geo_index, point_count):
        """Weights are stored sparse, any point without a stored value has a weight of 1.0"""
        weights = [1.0] * point_count
        plug = '{}.weightList[{}].weights'.format(self.node, geo_index)
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
        """Applies a dictionary created by get_weights_dictionary: rebuilds the shrinkWrap if it doesn't exist,
        reconnects the target if needed, then restores the attributes and the weights."""
        data = args[0] if args else self.weights_dict
        if not self.node or not pm.objExists(str(self.node)):
            if pm.objExists(data['node']):
                self.node = pm.PyNode(data['node'])
            else:
                self.rebuild(data)

        saved_target = data.get('target')
        if saved_target and self.target != saved_target:
            if cmds.objExists(saved_target):
                self.connect_target(saved_target)
            else:
                print('WARNING: target {} of shrinkWrap {} does not exist'.format(saved_target, self.node))

        self.set_attributes(data.get('attributes', {}))
        self.set_weights(data.get('geometry', {}))

    def rebuild(self, data):
        geometry = [each for each in data['geometry'] if cmds.objExists(each)]
        if not geometry:
            raise RuntimeError('none of the geometries saved for shrinkWrap {} exist in the scene'.format(data['node']))
        target = data.get('target')
        if not target or not cmds.objExists(target):
            raise RuntimeError('the target {} of shrinkWrap {} does not exist in the scene'.format(target,
                                                                                                   data['node']))
        self.geo_base(*geometry, target=target)
        # restore the saved name so the node keeps matching its file
        if not cmds.objExists(data['node']):
            self.node.rename(data['node'])

    def set_attributes(self, attributes):
        node = str(self.node)
        for attribute, value in attributes.items():
            plug = '{}.{}'.format(node, attribute)
            if cmds.objExists(plug) and cmds.getAttr(plug, settable=True):
                cmds.setAttr(plug, value)

    def set_weights(self, geometry_data):
        node = str(self.node)
        for shape, geo_index in self.deformed_geometry():
            transform = cmds.listRelatives(shape, parent=True)[0]
            geo_data = geometry_data.get(transform)
            if not geo_data:
                print('no shrinkWrap weights saved for {}'.format(transform))
                continue
            weights = geo_data['weights']
            count = self.point_count(shape)
            if count != len(weights):
                raise RuntimeError('point count mismatch on {}: scene has {}, data has {}'.format(
                    transform, count, len(weights)))
            cmds.setAttr('{}.weightList[{}].weights[0:{}]'.format(node, geo_index, count - 1),
                         *weights, size=count)

    # ------------------------------------------------------------------ #
    # utilities
    # ------------------------------------------------------------------ #
    @staticmethod
    def point_count(shape):
        if cmds.objectType(shape) == 'mesh':
            return cmds.polyEvaluate(shape, vertex=True)
        return len(cmds.ls('{}.cp[*]'.format(shape), flatten=True))

    @staticmethod
    def _shape(geometry):
        geometry = str(geometry)
        if cmds.objectType(geometry) == 'mesh':
            return geometry
        shapes = cmds.listRelatives(geometry, shapes=True, noIntermediate=True, type='mesh') or []
        if not shapes:
            raise RuntimeError('the shrinkWrap target {} has no mesh shape'.format(geometry))
        return shapes[0]


if __name__ == '__main__':
    new_shrink_wrap = ShrinkWrap()
    new_shrink_wrap.geo_base('C_shirt_01_HIGH', target='C_body_01_HIGH')
    # new_shrink_wrap.save()
    # ShrinkWrap.by_name('<shrinkWrap name>').load()
