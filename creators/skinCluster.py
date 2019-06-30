import pymel.core as pm
from RMPY import nameConvention
import maya.cmds as cmds
import pymel.core as pm
from RMPY.creators import creatorsBase
from RMPY.core import dataManager


def get_from_node(node):
    """:returns a skin cluster asociated with the node"""
    history_nodes = pm.listHistory(node, interestLevel=2)

    for each in history_nodes:
        if each.__class__ == pm.nodetypes.SkinCluster:
            return each
    return None


class SkinCluster(creatorsBase.CreatorBase):
    def __init__(self, *args, **kwargs):
        super(SkinCluster, self).__init__(*args, **kwargs)
        self.skin_node = None
        self.weights_dict = {}

    @classmethod
    def by_name(cls, skin_node_name):
        new_class_object = cls()
        if pm.objExists(skin_node_name):
            node_name = pm.ls(skin_node_name)[0]
            if node_name.__class__ == pm.nodetypes.SkinCluster:
                new_class_object.skin_node = node_name
                return new_class_object
            else:
                print "error couldn't create skin cluster, node class is :%s" % node_name.__class__
        else:
            new_class_object.skin_node = skin_node_name
            print "WARNING: skinCluster object created, node doesn't exists"
            return new_class_object
        return None

    @classmethod
    def by_node(cls, node_name):
        if node_name.__class__ == pm.nodetypes.SkinCluster:
            skin_cluster = node_name
        else:
            skin_cluster = cls.get_skin_cluster(node_name)

        if skin_cluster:
            new_class_object = cls()
            new_class_object.skin_node = skin_cluster
            return new_class_object
        else:
            print "error couldn't create skin cluster no skinCluster on history of object %s" % node_name
        return None

    def save(self, *args, **kwargs):
        if len(args) >= 1:
            file_name = args[0]
        else:
            file_name = '%s' % self.skin_node
        data_manager = dataManager.DataManager()
        data_manager.save(file_name, self.get_weights_dictionary(), **kwargs)

    def load(self, *args, **kwargs):
        if len(args) >= 1:
            file_name = args[0]
        else:
            file_name = '%s' % self.skin_node
        data_manager = dataManager.DataManager()
        self.weights_dict = data_manager.load(file_name, **kwargs)
        return self.weights_dict

    def influence(self):
        return cmds.skinCluster('%s' % self.skin_node, influence=True, query=True)

    def get_weights_dictionary(self):
        weight_dictionary = {}
        vertex_index = cmds.getAttr('%s.weightList' % self.skin_node, mi=True)
        weight_dictionary['influences'] = self.influence()
        weight_dictionary['weights'] = {}

        for each_vertex in vertex_index:
            joint_list = cmds.getAttr('%s.weightList[%s].weights' % (self.skin_node, each_vertex), mi=True)
            weight_value = cmds.getAttr('%s.weightList[%s].weights' % (self.skin_node, each_vertex))[0]
            weight_dictionary['weights'][each_vertex] = [joint_list, weight_value]
        return weight_dictionary

    def apply_weights_dictionary(self, *args, **kwargs):
        if len(args) >= 1:
            weights_dictionary = args[0]
        else:
            weights_dictionary = self.weights_dict
        # t1 = time.time()
        geometry = kwargs.pop('geometry', None)
        if not self.skin_node or not pm.objExists(self.skin_node) and pm.objExists(geometry):
            new_skin = pm.skinCluster(weights_dictionary['influences'], geometry, toSelectedBones=True)
            pm.rename(new_skin, self.skin_node)
            self.skin_node = new_skin
        load_type = kwargs.pop('type', 'by_index')
        cmds.setAttr('%s.normalizeWeights' % self.skin_node, 0)
        if load_type == 'by_index':
            for each_vertex in weights_dictionary['weights']:
                current_joint_list = cmds.getAttr('%s.weightList[%s].weights' % (self.skin_node, each_vertex), mi=True)

                weights_relation = weights_dictionary['weights'][each_vertex]
                joint_list = weights_relation[0]
                weight_values = weights_relation[1]

                for each_joint in list(set(joint_list + current_joint_list)):
                    if each_joint in joint_list:
                        each_weight = weight_values[joint_list.index(each_joint)]
                    else:
                        each_weight = 0
                    cmds.setAttr('%s.weightList[%s].weights[%s]' % (self.skin_node, each_vertex, each_joint),
                                 each_weight)
        cmds.setAttr('%s.normalizeWeights' % self.skin_node, 1)
        # t2 = time.time()
        # print 'weights_loaded in %s' % (t2 - t1)

    def create_dictionary_base(self):
        pass

    def copy_skin(self, *args):
        """
        Copy's the skinning between different meshes
        only by providing the meshes.\n
        :args[0] the source mehs, this geo \n
        :args[1:] the destination  mehs where the skin will be copied\n
        :return a list with all the skin clusters that where created during execution
        """
        source = args[0]
        destination = args[1:]
        skin_cluster_node = get_from_node(source)
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


if __name__ == '__main__':
    skin_cluster01 = SkinCluster.by_node('skinCluster2')
    skin_cluster01.save('BackBar')
    # skin_cluster01.load('metal_ring_front')
    # skin_cluster01.apply_weights_dictionary(geometry='metalGrey_C_metalRing_0001_mid_GES')
