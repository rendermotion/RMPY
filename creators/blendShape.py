import maya.cmds as cmds
import pymel.core as pm
from RMPY.creators import creatorsBase
from RMPY.core import dataManager


class BlendShape(creatorsBase.CreatorsBase):
    def __init__(self, *args, **kwargs):
        super(BlendShape, self).__init__()
        self.node = None
        self.geometry_node = None
        self.weights_dict = {}
        self.extra_path = '/blendShapes'

    @classmethod
    def by_name(cls, blend_shape_name):
        new_class_object = cls()
        if pm.objExists(blend_shape_name):
            node_name = pm.ls(blend_shape_name)[0]
            if pm.objectType(node_name) == 'blendShape':
                new_class_object.node = node_name
                return new_class_object
            else:
                print("error couldn't create blendShape, node class is :%s" % node_name.__class__)
        else:
            new_class_object.node = blend_shape_name
            print("WARNING: BlendShape object created, node doesn't exists")
            return new_class_object
        return None

    @classmethod
    def by_node(cls, node_name, **kwargs):
        new_class_object = cls()
        if node_name.__class__ == pm.nodetypes.BlendShape:
            blend_shape = node_name
        else:
            blend_shape = new_class_object.get_blend_shape(node_name, **kwargs)

        if blend_shape:
            new_class_object.node = blend_shape
            return new_class_object
        else:
            print("error couldn't create blendShape no blendShape on history of object {} \n " \
            "or object it is not a blendShape".format(node_name))
        return None

    def save(self, *args, **kwargs):
        if len(args) >= 1:
            file_name = args[0]
        else:
            file_name = '%s' % self.node
        data_manager = dataManager.DataManager()
        data_manager.scene_path = '{}{}'.format(data_manager.scene_path, self.extra_path)
        data_manager.save(file_name, self.get_weights_dictionary(), **kwargs)

    def load(self, *args, **kwargs):
        if len(args) >= 1:
            file_name = args[0]
        else:
            file_name = '%s' % self.skin_node
        data_manager = dataManager.DataManager()
        data_manager.scene_path = '{}{}'.format(data_manager.scene_path, self.extra_path)
        self.weights_dict = data_manager.load(file_name, **kwargs)
        return self.weights_dict

    def get_weights_dictionary(self, **kwargs):
        index_source = kwargs.pop('index', None)
        if not index_source:
            target_index_list = pm.getAttr(("{}.inputTarget[0].inputTargetGroup".format(self.node)), mi=True)
            if self.weights_dict:
                self.weights_dict = {}
            self.weights_dict['type'] = 'blendShape'
            self.weights_dict['node'] = str(self.node)
            self.weights_dict['data'] = {}
            self.weights_dict['data'][-1] = self.get_weights_by_index(-1)
            for each_index in target_index_list:
                self.weights_dict['data'][each_index] = self.get_weights_by_index(each_index)

            return self.weights_dict

        else:
            return self.get_weights_by_index(index_source)

    def get_weights_by_index(self, index_source):
        if index_source != -1:
            source_weights_token = 'inputTargetGroup[%s].targetWeights' % index_source
        else:
            source_weights_token = 'baseWeights'

        weights_list = cmds.getAttr("%s.inputTarget[0].%s" % (self.node, source_weights_token),
        multiIndices=True)

        if weights_list:
            weights = cmds.getAttr("%s.inputTarget[0].%s[*]" % (self.node, source_weights_token))
        else:
            print ('weights doesnt exist on index source {}'.format(index_source))
            weights = []
            weights_list = []
        return {'weights': weights, 'weights_list': weights_list}

    def apply_weights_dictionary(self, **kwargs):
        index_source = kwargs.pop('index', None)
        if not index_source:
            target_index_list = pm.getAttr(("{}.inputTarget[0].inputTargetGroup".format(self.node)), mi=True)
            target_index_list.append(-1)
            print (self.weights_dict['data'].keys())
            print (target_index_list)
            self.apply_weights_by_index(-1)
            for each_index in target_index_list:
                if str(each_index) in self.weights_dict['data'].keys():
                    self.apply_weights_by_index(each_index)
                    print ('applying index {}'.format(each_index))
                else:
                    print ('index not found in data {}'.format(each_index))
        else:
            self.apply_weights_by_index(index_source)

    def apply_weights_by_index(self, index_destination):
        weights_list = self.weights_dict['data'][str(index_destination)]['weights_list']
        weights = self.weights_dict['data'][str(index_destination)]['weights']
        if index_destination != -1:
            destination_weights_token = 'inputTargetGroup[%s].targetWeights' % index_destination
        else:
            destination_weights_token = 'baseWeights'

        current_weight_list = cmds.getAttr("%s.inputTarget[0].%s" %(self.node, destination_weights_token), multiIndices=True)
        if current_weight_list:
            total_weight_list = set(weights_list + current_weight_list)
        else:
            total_weight_list = weights_list
        for each_index in total_weight_list:
            if each_index in weights_list:
                value = weights[weights_list.index(each_index)]
                cmds.setAttr("%s.inputTarget[0].%s[%s]" % (self.node, destination_weights_token, each_index), value)
            else:
                pm.removeMultiInstance("{}.inputTarget[0].{}[{}]".format(self.node, destination_weights_token, each_index))

    def clear_channel(self, **kwargs):
        index_destination = kwargs.pop('index_destination', -1)

        if index_destination != -1:
            destination_weights_token = 'inputTargetGroup[%s].targetWeights' % index_destination
        else:
            destination_weights_token = 'baseWeights'

        current_weight_list = cmds.getAttr("%s.inputTarget[0].%s" % (self.node, destination_weights_token), multiIndices=True)
        if current_weight_list:
            for each_value in current_weight_list:
                pm.removeMultiInstance("{}.inputTarget[0].{}[{}]".format(self.node, destination_weights_token, each_value))

    def create_dictionary_base(self):
        pass

    def get_blend_shape(self, blend_shape_geometry, index=0, create=True):
        self.geometry_node = blend_shape_geometry
        blend_shapes_list = self.get_blend_shape_list(blend_shape_geometry)
        if blend_shapes_list:
            return blend_shapes_list[index]
        if create:
            return pm.ls(pm.blendShape(blend_shape_geometry, name=self.name_convention.set_name_in_format(name='blendShape')))[0]
        return None

    @staticmethod
    def get_blend_shape_list(blend_shape_geometry):
        blend_shapes_list = []
        for each in pm.listHistory(blend_shape_geometry, interestLevel=2, pruneDagObjects=True):
            if each.__class__ == pm.nodetypes.BlendShape:
                blend_shapes_list.append(each)
        return blend_shapes_list

    def add_as_target(self, *geometry, **kwargs):
        set_value = kwargs.pop('set_value', 1)
        for geo_new_target in geometry:
            number_of_targets = len(self.node.weightIndexList())
            pm.blendShape(self.node, topologyCheck=False, e=True, target=[self.geometry_node, number_of_targets + 1, geo_new_target, 1.0])
            self.node.weight[number_of_targets + 1].set(set_value)


if __name__ == '__main__':
    selection = pm.ls(selection=True)
    blend_shape = BlendShape.by_node(selection[1])
    blend_shape.add_as_target(selection[0])
    # skin_cluster01.save('BackBar')