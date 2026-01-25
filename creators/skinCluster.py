import maya.cmds as cmds
import pymel.core as pm
from RMPY.creators import creatorsBase
from RMPY.core import dataManager
from RMPY.core import polygon_tools


class SkinCluster(creatorsBase.CreatorsBase):
    """
    The main creator of skin clusters
    """
    def __init__(self, *args, **kwargs):
        super(SkinCluster, self).__init__(*args, **kwargs)
        self.node = None
        self.weights_dict = {}
        self.extra_path = '/skinClusters'

    @classmethod
    def by_name(cls, skin_node_name):
        """
        A base Classmethod that returns an instance of the SkinCluster class that contains as the main node (self.node)
        an skincluster with the name provided
        Args:
            skin_node_name(str): A string that contains the name of a skinCluster in the scene.
        Returns:
            SkinCluster: An instance of this SkinCluster class that has the skin_node_name assigned to the (self.node).
        """
        new_class_object = cls()
        if pm.objExists(skin_node_name):
            node_name = pm.ls(skin_node_name)[0]
            if node_name.__class__ == pm.nodetypes.SkinCluster:
                new_class_object.node = node_name
                return new_class_object
            else:
                print ("error couldn't create skin cluster, node class is :%s" % node_name.__class__)
        else:
            new_class_object.node = skin_node_name
            print ("WARNING: skinCluster object created, node doesn't exists")
            return new_class_object
        return None

    @classmethod
    def by_node(cls, node_name):
        if node_name.__class__ == pm.nodetypes.SkinCluster:
            skin_cluster = node_name
        else:
            skin_cluster = cls.get_skinCluster(node_name)
        if skin_cluster:
            new_class_object = cls()
            new_class_object.node = skin_cluster
            return new_class_object
        else:
            print ("error couldn't create skin cluster no skinCluster on history of object %s" % node_name)
        return None

    def save(self, *args, **kwargs):
        if len(args) >= 1:
            file_name = args[0]
        else:
            file_name = '{}'.format(self.node)
        data_manager = dataManager.DataManager()
        data_manager.file_path = '{}{}'.format(data_manager.file_path, self.extra_path)
        data_manager.save(file_name, self.get_weights_dictionary(), **kwargs)

    def load(self, *args, **kwargs):
        if len(args) >= 1:
            file_name = args[0]
        else:
            file_name = '{}'.format(self.node)
        data_manager = dataManager.DataManager()
        data_manager.file_path = '{}{}'.format(data_manager.file_path, self.extra_path)
        print('path to search = {}'.format(data_manager.file_path))
        self.weights_dict = data_manager.load(file_name, **kwargs)
        return self.weights_dict

    def influence(self):
        return cmds.skinCluster('%s' % self.node, influence=True, query=True)

    def get_weights_dictionary(self):
        weight_dictionary = {}
        vertex_index = cmds.getAttr('%s.weightList' % self.node, mi=True)
        weight_dictionary['influences'] = self.influence()
        weight_dictionary['weights'] = {}
        valid_indices = cmds.getAttr(f'{self.node}.matrix', mi=True)
        for each_vertex in vertex_index:
            joint_list = cmds.getAttr(f'{self.node}.weightList[{each_vertex}].weights', mi=True)
            weight_value = list(cmds.getAttr(f'{self.node}.weightList[{each_vertex}].weights')[0])
            validated_joints = []
            validated_weights = []
            invalid_joints = []
            for index_joint, weight_value in zip(joint_list, weight_value):
                if index_joint in valid_indices:
                    validated_joints.append(valid_indices.index(index_joint))
                    validated_weights.append(weight_value)
                else:
                    invalid_joints.append(index_joint)
            weight_dictionary['weights'][each_vertex] = [validated_joints, validated_weights]
        return weight_dictionary

    def apply_weights_dictionary(self, *args, **kwargs):
        if len(args) >= 1:
            weights_dictionary = args[0]
        else:
            weights_dictionary = self.weights_dict

        geometry = kwargs.pop('geometry', None)
        if not self.node or not pm.objExists(self.node) and pm.objExists(geometry):
            self.validate_joint_existence(*weights_dictionary['influences'])
            new_skin = pm.skinCluster(weights_dictionary['influences'], geometry, toSelectedBones=True)
            self.node = new_skin
            self.name_convention.rename_name_in_format(new_skin,
                                                       name=self.name_convention.get_a_short_name(geometry),
                                                       system=self.name_convention.get_from_name(geometry, 'system'))
            self.node = new_skin
        # load_type = kwargs.pop('type', 'by_index')
        cmds.setAttr('%s.normalizeWeights' % self.node, 0)

        # if load_type == 'by_index':
        for each_vertex in weights_dictionary['weights']:
            current_joint_list = cmds.getAttr('{}.weightList[{}].weights'.format(self.node, each_vertex), mi=True)
            weights_relation = weights_dictionary['weights'][each_vertex]
            joint_list = weights_relation[0]
            weight_values = weights_relation[1]
            if not joint_list or not current_joint_list:
                raise(RuntimeError('List of vertices out of range there is a \n '
                                   'mismatch on the skinning data you are trying \n'
                                   'to apply for node {}'.format(self.node)))

            for each_joint in list(set(joint_list + current_joint_list)):
                if each_joint in joint_list:
                    each_weight = weight_values[joint_list.index(each_joint)]
                else:
                    each_weight = 0
                cmds.setAttr('%s.weightList[%s].weights[%s]' % (self.node, each_vertex, each_joint),
                             each_weight)
        cmds.setAttr('%s.normalizeWeights' % self.node, 1)

    def create_dictionary_base(self):
        pass

    def validate_joint_existence(self, *joints):
        for each_joint in joints:
            if not pm.objExists(str(each_joint)):
                pm.joint(name=each_joint)


    @staticmethod
    def get_skinCluster(skined_geometry):
        for each in pm.listHistory(skined_geometry, interestLevel=2, pruneDagObjects=True):
            if each.__class__ == pm.nodetypes.SkinCluster:
                return each
        return None

    def copy_joint_to_joint(self, source_joint, destination_joint):
        if source_joint in self.weights_dict['influences'] and destination_joint in self.weights_dict['influences']:
            index_source_joint = self.weights_dict['influences'].index(source_joint)
            index_destination_joint = self.weights_dict['influences'].index(destination_joint)
            for each_vertex in self.weights_dict['weights']:
                vtx_joint_list, vtx_weights_list = self.weights_dict['weights'][each_vertex]
                if index_source_joint in vtx_joint_list:
                    source_weight_value = vtx_weights_list[vtx_joint_list.index(index_source_joint)]
                    if index_destination_joint in vtx_joint_list:
                        destination_weight_value = vtx_weights_list[vtx_joint_list.index(index_destination_joint)]

                        vtx_weights_list[vtx_joint_list.index(index_destination_joint)] = \
                        destination_weight_value + source_weight_value
                        vtx_weights_list[vtx_joint_list.index(index_source_joint)] = 0

                        cmds.setAttr('%s.weightList[%s].weights[%s]' % (self.node,
                                                                        each_vertex,
                                                                        index_destination_joint),
                        destination_weight_value + source_weight_value)
                        cmds.setAttr('{}.weightList[{}].weights[{}]'.format(self.node,
                                                                            each_vertex,
                                                                            index_source_joint), 0)
                    else:
                        vtx_joint_list.append(index_destination_joint)
                        vtx_weights_list.append(source_weight_value)
                        vtx_weights_list[vtx_joint_list.index(index_source_joint)] = 0
                        cmds.setAttr('%s.weightList[%s].weights[%s]' % (self.node,
                                                                        each_vertex,
                                                                        index_destination_joint),
                                                                        source_weight_value)
                        cmds.setAttr('{}.weightList[{}].weights[{}]'.format(self.node,
                                                                            each_vertex,
                                                                            index_source_joint), 0)
        else:
            print ('one of this joints is not on the skin cluster: {}, {}'.format(source_joint, destination_joint))

    def copy_by_definition(self, relation_dictionary, order_list=None):
        """Copies the skinning from joint to joint as described on the parameter relation dictionary.
        :param relation_dictionary: a dictionary of objects relations of which weights will be copyed where.
        And since the keys on the dictionary cant be repeated, the keys are the destination of the weights,
        and the value of the key is the joint from where the weights will be added.
        :param order_list: the order in which the copy should be done, since the dictionary doesnt have an order,
        this list should have the keys of the relation_dictionary.
        :return:
        """
        if not order_list:
            order_list = relation_dictionary.keys()

        self.weights_dict = self.get_weights_dictionary()
        for each_source in order_list:
            self.copy_joint_to_joint(each_source, relation_dictionary[each_source])
            self.weights_dict = self.get_weights_dictionary()

    def switch_skin(self, geometry, joint_switch_dictionary):
        """
        Switches the joints in an existing skinning

        :param joint_switch_dictionary:
        :param geometry: geometry where the skin wants to be changed.
        :return:
        """
        selection = pm.ls(geometry)
        for geometry in selection:
            skin_node = self.by_node(geometry)
            weights_dictionary = skin_node.get_weights_dictionary()
            self.replace_joint_name(joint_switch_dictionary)
            pm.delete(skin_node.node)
            skin_node.node = None
            skin_node.weights_dict = weights_dictionary
            skin_node.apply_weights_dictionary(geometry=geometry)

    def replace_joint_name(self, joint_switch_dictionary):
        for current_joint in self.weights_dict['influences']:
            if current_joint in joint_switch_dictionary:
                index = self.weights_dict['influences'].index(current_joint)
                self.weights_dict['influences'][index] = joint_switch_dictionary[current_joint]
        self.conform_dictionary()

    def conform_dictionary(self):
        new_list = list(set(self.weights_dict['influences']))
        index_dict = {}
        for old_index, each_token in enumerate(self.weights_dict['influences']):
                new_index = new_list.index(each_token)
                index_dict[old_index] = new_index
        for each_vertex in self.weights_dict['weights']:
            new_index_list = []
            new_weight_list = []
            for each_index, each_weight in zip(*self.weights_dict['weights'][each_vertex]):
                if not index_dict[int(each_index)] in new_index_list:
                    new_index_list.append(index_dict[int(each_index)])
                    new_weight_list.append(float(each_weight))
                else:
                    weight_index = new_index_list.index(index_dict[int(each_index)])
                    new_weight_list[weight_index] += float(each_weight)

            self.weights_dict['weights'][each_vertex] = [new_index_list, tuple(new_weight_list)]
        self.weights_dict['influences'] = new_list

    def copy_skin(self, *args):
        """
        Copy's the skinning between different meshes
        only by providing the meshes.\n
        args[0]: the source mesh, this geo \n
        args[1:]: the destination  meshes where the skin will be copied\n
        return: A list with all the skin clusters that where created during execution
        """
        source = args[0]
        destination = args[1:]
        skin_cluster_node = self.get_skin_cluster(source)
        skin_cluster_list = []
        if skin_cluster_node:
            list_joints = skin_cluster_node.influenceObjects()
            if destination:
                for each_node in destination:
                    new_skin_cluster = pm.skinCluster(list_joints, each_node)
                    skin_cluster_list.append(new_skin_cluster)
                    self.name_convention.rename_name_in_format(new_skin_cluster,
                                                               name=self.name_convention.get_a_short_name(each_node))
                    pm.copySkinWeights(source, destination, influenceAssociation=['label', 'name',
                                                                                  'closestJoint', 'oneToOne'])
        return new_skin_cluster

    @staticmethod
    def get_skin_cluster(skined_geometry):
        for each in pm.listHistory(skined_geometry, interestLevel=2, pruneDagObjects=True):
            if each.__class__ == pm.nodetypes.SkinCluster:
                return each
        return None

    def _representation(self):
        return self.get_weights_dictionary()

    def shell_skin(self, geometry):
        shells_list = polygon_tools.shells(geometry)
        weights_dictionary = self.get_weights_dictionary()
        for each_shell in shells_list:
            average_influence_list = []
            average_weight_list = []
            for each_vertex in list(each_shell):
                vertex_influence_list = weights_dictionary['weights'][each_vertex][0]
                weight_list = weights_dictionary['weights'][each_vertex][1]
                for index, each_influence in enumerate(vertex_influence_list):
                    if each_influence not in average_influence_list:
                        average_influence_list.append(each_influence)
                        average_weight_list.append(0.0)
                    average_weight_list[average_influence_list.index(each_influence)] += weight_list[index]

            average_weight_list = [each/float(len(average_influence_list)) for each in average_weight_list]
            for each_vertex in each_shell:
                weights_dictionary['weights'][each_vertex] = [average_influence_list, average_weight_list]
        self.apply_weights_dictionary(weights_dictionary)
        pm.skinPercent(self.node, normalize=True)


if __name__ == '__main__':
    selection = pm.ls(selection=True)
    from pprint import pprint as pp
    skin_cluster01 = SkinCluster.by_node(selection[0])
    pp(skin_cluster01.get_weights_dictionary())
    # skin_cluster01.shell_skin(each)