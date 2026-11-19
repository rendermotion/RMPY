import maya.cmds as cmds
import pymel.core as pm
from RMPY.creators import creatorsBase
from RMPY.core import dataManager


class DeformerBase(creatorsBase.CreatorsBase):
    """
    Base class for the creators of deformers that can be saved and loaded.

    Subclasses define:
        node_type: the maya node type of the deformer, e.g. 'skinCluster', 'ffd', 'shrinkWrap'.
        extra_path: the sub folder where the files are saved, e.g. '/skinClusters'.
        apply_on_load: if load applies the data to the scene after reading it.
        get_weights_dictionary() and apply_weights_dictionary(data)
    """
    node_type = None
    extra_path = ''
    apply_on_load = True

    def __init__(self, *args, **kwargs):
        super(DeformerBase, self).__init__(*args, **kwargs)
        self.node = None
        self.weights_dict = {}

    # ------------------------------------------------------------------ #
    # finding existing deformers
    # ------------------------------------------------------------------ #
    @classmethod
    def by_name(cls, node_name):
        """Returns an instance of the class that uses the deformer with the provided name.
        If the node doesn't exist, the instance is returned with only the name set, so load can rebuild it.
        """
        new_class_object = cls()
        if pm.objExists(str(node_name)):
            node_type = cmds.objectType(str(node_name))
            if node_type == cls.node_type:
                new_class_object.set_node(node_name)
                return new_class_object
            print("error couldn't create {}, node type is :{}".format(cls.__name__, node_type))
            return None
        new_class_object.node = node_name
        print("WARNING: {} object created, node doesn't exists".format(cls.__name__))
        return new_class_object

    @classmethod
    def by_node(cls, node):
        """Returns an instance of the class from a deformer node, or from a geometry deformed by one."""
        if pm.objExists(str(node)) and cmds.objectType(str(node)) == cls.node_type:
            deformer = node
        else:
            deformer = cls.get_deformer(node)
        if deformer:
            new_class_object = cls()
            new_class_object.set_node(deformer)
            return new_class_object
        print("error couldn't create {}, no {} on history of object {}".format(cls.__name__, cls.node_type, node))
        return None

    @classmethod
    def get_deformer(cls, deformed_geometry):
        """Returns the first deformer of node_type found on the history of the geometry."""
        for each in pm.listHistory(deformed_geometry, interestLevel=2, pruneDagObjects=True):
            if pm.objectType(each) == cls.node_type:
                return each
        return None

    def set_node(self, node):
        """Sets the main node, subclasses can extend it to find related nodes."""
        self.node = pm.PyNode(node)

    # ------------------------------------------------------------------ #
    # save / load
    # ------------------------------------------------------------------ #
    def data_manager(self):
        data_manager = dataManager.DataManager()
        data_manager.file_path = '{}{}'.format(data_manager.file_path, self.extra_path)
        return data_manager

    def save(self, *args, **kwargs):
        if len(args) >= 1:
            file_name = args[0]
        else:
            file_name = '{}'.format(self.node)
        self.data_manager().save(file_name, self.get_weights_dictionary())

    def load(self, *args, **kwargs):
        """Reads the file and, if apply is True (default apply_on_load), applies it to the scene."""
        apply_data = kwargs.pop('apply', self.apply_on_load)
        if len(args) >= 1:
            file_name = args[0]
        else:
            file_name = '{}'.format(self.node)
        data_manager = self.data_manager()
        print('path to search = {}'.format(data_manager.file_path))
        self.weights_dict = data_manager.load(file_name)
        if self.weights_dict and apply_data:
            self.apply_weights_dictionary(self.weights_dict)
        return self.weights_dict

    def get_weights_dictionary(self):
        raise NotImplementedError('get_weights_dictionary not implemented on {}'.format(self.__class__.__name__))

    def apply_weights_dictionary(self, *args, **kwargs):
        raise NotImplementedError('apply_weights_dictionary not implemented on {}'.format(self.__class__.__name__))

    def _representation(self):
        return self.get_weights_dictionary()

    # ------------------------------------------------------------------ #
    # geometry and attribute utilities
    # ------------------------------------------------------------------ #
    def deformed_geometry(self):
        """Returns a list of [shape, geometry_index] for every geometry deformed by the node."""
        node = str(self.node)
        shapes = cmds.deformer(node, query=True, geometry=True) or []
        indices = cmds.deformer(node, query=True, geometryIndices=True) or []
        return list(zip(shapes, indices))

    @staticmethod
    def transform_of(shape):
        return cmds.listRelatives(shape, parent=True)[0]

    @staticmethod
    def point_count(shape):
        if cmds.objectType(shape) == 'mesh':
            return cmds.polyEvaluate(shape, vertex=True)
        return len(cmds.ls('{}.cp[*]'.format(shape), flatten=True))

    def get_attributes(self, attribute_list):
        """Returns {attribute: value} for each attribute on the list that exists on the node."""
        node = str(self.node)
        return {each: cmds.getAttr('{}.{}'.format(node, each)) for each in attribute_list
                if cmds.attributeQuery(each, node=node, exists=True)}

    def set_attributes(self, attributes):
        """Sets {attribute: value} on the node, skipping attributes that don't exist or are connected/locked."""
        node = str(self.node)
        for attribute, value in attributes.items():
            plug = '{}.{}'.format(node, attribute)
            if cmds.objExists(plug) and cmds.getAttr(plug, settable=True):
                cmds.setAttr(plug, value)


class WeightGeometryFilterBase(DeformerBase):
    """
    Base class for deformers with one weight per point (weightGeometryFilter nodes like ffd, shrinkWrap, cluster,
    wrap...), the weights live on node.weightList[geometry_index].weights[point_index].

    The data dictionary contains:
        node: the deformer name, used to rename the node when it is rebuilt.
        attributes: the values of the attributes listed in deformer_attributes.
        geometry: {transform: {'shape', 'point_count', 'weights'}} the per point weights of each
                  deformed geometry.
    Subclasses add their own data on get_weights_dictionary, read it on apply_data and implement rebuild.
    """
    deformer_attributes = ['envelope']

    def get_weights_dictionary(self):
        data = dict(node=str(self.node),
                    attributes=self.get_attributes(self.deformer_attributes),
                    geometry=self.get_weights())
        return data

    def apply_weights_dictionary(self, *args, **kwargs):
        """Finds the node (rebuilding it if it doesn't exist) and applies the data."""
        data = args[0] if args else self.weights_dict
        if not self.node or not pm.objExists(str(self.node)):
            if pm.objExists(data['node']):
                self.set_node(data['node'])
            else:
                self.rebuild(data)
                # restore the saved name so the node keeps matching its file
                if not cmds.objExists(data['node']):
                    self.rename_node(data['node'])
        self.apply_data(data)

    def apply_data(self, data):
        """Applies the data to the existing node, subclasses extend it to restore their own data."""
        self.set_attributes(data.get('attributes', {}))
        self.set_weights(data.get('geometry', {}))

    def rebuild(self, data):
        raise NotImplementedError('rebuild not implemented on {}'.format(self.__class__.__name__))

    def rename_node(self, name):
        self.node.rename(name)

    def saved_geometry(self, data):
        """The saved geometries that exist in the scene, raises an error if none exist."""
        geometry = [each for each in data['geometry'] if cmds.objExists(each)]
        if not geometry:
            raise RuntimeError('none of the geometries saved for {} exist in the scene'.format(data['node']))
        return geometry

    # ------------------------------------------------------------------ #
    # weights
    # ------------------------------------------------------------------ #
    def get_weights(self):
        """Returns {transform: {'shape', 'point_count', 'weights'}} for every deformed geometry."""
        result = {}
        for shape, geo_index in self.deformed_geometry():
            weights = self.get_geometry_weights(geo_index, self.point_count(shape))
            result[self.transform_of(shape)] = dict(shape=shape, point_count=len(weights), weights=weights)
        return result

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

    def set_weights(self, geometry_data):
        """Applies {transform: {'weights'}} matching the saved geometries by transform name."""
        for shape, geo_index in self.deformed_geometry():
            transform = self.transform_of(shape)
            geo_data = geometry_data.get(transform)
            if not geo_data:
                print('no {} weights saved for {}'.format(self.node_type, transform))
                continue
            weights = geo_data['weights']
            count = self.point_count(shape)
            if count != len(weights):
                raise RuntimeError('point count mismatch on {}: scene has {}, data has {}'.format(
                    transform, count, len(weights)))
            self.set_geometry_weights(geo_index, weights)

    def set_geometry_weights(self, geo_index, weights):
        # one setAttr for the whole range, much faster than one per point
        cmds.setAttr('{}.weightList[{}].weights[0:{}]'.format(self.node, geo_index, len(weights) - 1),
                     *weights, size=len(weights))
