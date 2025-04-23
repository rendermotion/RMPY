from RMPY.rig import rigBase
import pymel.core as pm
import math


class RigFacial(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(RigFacial, self).__init__(*args, **kwargs)
        self.rig_definition = args[0]
        self.build(**kwargs)

    def build(self, **kwargs):
        for each_definition in self.rig_definition:
            if self.rig_definition[each_definition]['type'] == 'blend_shape_definition':
                SingleDefinition(self.rig_definition[each_definition], **kwargs)
                if self.rig_definition[each_definition]['isSymetrical']:
                    right_definition = {'blendShapes': {},
                                        'attributes': self.rig_definition[each_definition]['attributes'],
                                        'control': self.rig_definition[each_definition]['control'].replace('L', 'R'),
                                        'baseMesh': self.rig_definition[each_definition]['baseMesh'],
                                        'type': self.rig_definition[each_definition]['type'],
                                        'order': self.rig_definition[each_definition]['order']}
                    for each_key in self.rig_definition[each_definition]['blendShapes'].keys():
                        right_definition['blendShapes'][f'R{each_key[1:]}'] = self.rig_definition[each_definition]['blendShapes'][each_key]
                    SingleDefinition(right_definition, **kwargs)


class SingleDefinition(rigBase.RigBase):
    """
    class that reads a definition and creates a blendshape connection between the controls and the objects.
    """

    def __init__(self, definition, **kwargs):
        super(SingleDefinition, self).__init__(**kwargs)
        if pm.ls(definition['baseMesh']):
            self.base_mesh = pm.ls(definition['baseMesh'])[0]
        else:
            print('the object baseMesh {} doesnt exists'.format(definition['baseMesh']))
            raise RuntimeError

        # A list with the objects that will have a prefix geometry
        self.prefix_geometry_list = kwargs.pop('prefix_geometry_list', [])

        # self.is_symetrical = definition['isSymetrical']
        try:
            self.control = pm.ls(definition['control'])[0]

        except:
            print('{} doesnt exist'.format(definition['control']))
            raise RuntimeError
        self.blendShapes = definition['blendShapes']
        self.attributes = definition['attributes']
        blend_shapes_list = self.get_blend_shapes_in_history(self.base_mesh)
        if blend_shapes_list:
            blend_shape_node_index = kwargs.pop('blend_shape_node_index', 0)
            self.blend_shape_node = blend_shapes_list[blend_shape_node_index]

        else:
            print(f'no blendshape node found on {self.base_mesh}')
            self.blend_shape_node = pm.blendShape(self.base_mesh)[0]
        # self.attributes = definition['attributes']
        self.order = definition['order']
        self.blend_shapes_by_connection = {}
        self.split_blend_shapes_by_connection()
        self.build(**kwargs)

    def build(self, **kwargs):
        self.apply_blend_shapes(**kwargs)
        self.create_attributes()
        self.connect_definition(**kwargs)

    def connect_definition(self, **kwargs):
        for plug_attribute in self.blend_shapes_by_connection:
            if self.blend_shapes_by_connection[plug_attribute]['positive'][0]:
                bs_index = self.blend_shapes_by_connection[plug_attribute]['positive_index']
                max_value = sorted(self.blend_shapes_by_connection[plug_attribute]['positive_full_value'][1])[-1]
                connector = self.create.connect.with_limits(
                    self.control.attr(plug_attribute),
                    self.blend_shape_node.weight[bs_index], [[0, 0], [max_value, 1]], pre_infinity_type='constant')

                self.connect_prefix_geometry(connector, pm.aliasAttr(self.blend_shape_node.weight[bs_index], q=True), **kwargs)
            if self.blend_shapes_by_connection[plug_attribute]['negative'][0]:
                bs_index = self.blend_shapes_by_connection[plug_attribute]['negative_index']
                max_value = sorted(self.blend_shapes_by_connection[plug_attribute]['negative_full_value'][1])[-1]
                connector = self.create.connect.with_limits(
                    self.control.attr(plug_attribute),
                    self.blend_shape_node.weight[bs_index], [[-max_value, 1], [0, 0]],
                    post_infinity_type='constant')
                self.connect_prefix_geometry(connector, pm.aliasAttr(self.blend_shape_node.weight[bs_index], q=True), **kwargs)

    def connect_prefix_geometry(self, connector, blend_shape_plug, **kwargs):
        for each_geometry in self.prefix_geometry_list:
            each_geometry_blend_shape = self.get_blend_shapes_in_history(each_geometry)[0]
            main_blendshape = self.get_blend_shapes_in_history(self.base_mesh)[0]
            input_connection_plug = pm.listConnections(main_blendshape.attr(blend_shape_plug), plugs=True,
                                                       destination=False)[0]
            alias_in_blend_shape = {pm.aliasAttr('{}.weight[{}]'.format(each_geometry_blend_shape, each),
                                                 q=True) for each in each_geometry_blend_shape.weightIndexList()}
            if blend_shape_plug in alias_in_blend_shape:
                print(connector)
                input_connection_plug >> each_geometry_blend_shape.attr(blend_shape_plug)

    def create_attributes(self):
        for each_attribute in self.order:
            if each_attribute not in pm.listAttr(self.control):
                pm.addAttr(self.control, ln=each_attribute, k=True, hnv=True, hxv=True,
                           at=self.attributes[each_attribute]['type'],
                           min=self.attributes[each_attribute]['min'],
                           max=self.attributes[each_attribute]['max'])

    def apply_blend_shapes(self, **kwargs):
        from pprint import pprint as pp
        pp(self.blend_shapes_by_connection)
        for plug_attribute in self.blend_shapes_by_connection:
            if self.blend_shapes_by_connection[plug_attribute]['positive'][0]:
                index = self.add_target_list(*self.blend_shapes_by_connection[plug_attribute]['positive'], **kwargs)
                self.add_target_list_to_prefix(*self.blend_shapes_by_connection[plug_attribute]['positive'], **kwargs)
                self.blend_shapes_by_connection[plug_attribute]['positive_index'] = index
            if self.blend_shapes_by_connection[plug_attribute]['negative'][0]:
                index = self.add_target_list(*self.blend_shapes_by_connection[plug_attribute]['negative'], **kwargs)
                self.add_target_list_to_prefix(*self.blend_shapes_by_connection[plug_attribute]['negative'], **kwargs)
                self.blend_shapes_by_connection[plug_attribute]['negative_index'] = index

    def split_blend_shapes_by_connection(self):
        """
        On the blendshapes list, can be multiple blendshapes connected to the same connection plug.
        This happens when the blendshapes are intermediate blendshapes.
        This function will look in to the facial definition blendshapes key, look for blendshapes that
        correspond to the same connection and group them on a list.
        Then it will organize and normalize the values so the highest corresponds to a blendshape value of 1.
        :return:
        """
        for each_target in self.blendShapes:
            if pm.objExists(each_target):
                connection = self.blendShapes[each_target]['connection']
                if connection not in self.blend_shapes_by_connection:
                    self.blend_shapes_by_connection[connection] = {'positive': [[], []],
                                                                   'negative': [[], []],
                                                                   'positive_full_value': [[], []],
                                                                   'negative_full_value': [[], []],
                                                                   }
                if self.blendShapes[each_target]['value'] > 0:
                    self.blend_shapes_by_connection[connection]['positive_full_value'][0].append(each_target)
                    self.blend_shapes_by_connection[connection]['positive_full_value'][1].append(self.blendShapes[each_target]['value'])
                else:
                    self.blend_shapes_by_connection[connection]['negative_full_value'][0].append(each_target)
                    self.blend_shapes_by_connection[connection]['negative_full_value'][1].append(self.blendShapes[each_target]['value']
                                                                                             * -1)

        for each_connection in self.blend_shapes_by_connection:
            if self.blend_shapes_by_connection[each_connection]['positive_full_value'][0]:
                self.blend_shapes_by_connection[each_connection]['positive'] = self.normalize_target_list(
                    *self.blend_shapes_by_connection[each_connection]['positive_full_value'])
            if self.blend_shapes_by_connection[each_connection]['negative_full_value'][0]:
                self.blend_shapes_by_connection[each_connection]['negative'] = self.normalize_target_list(
                    *self.blend_shapes_by_connection[each_connection]['negative_full_value'])

    @staticmethod
    def get_blend_shapes_in_history(scene_node):
        history_nodes = pm.listHistory(scene_node, interestLevel=2, pruneDagObjects=True)
        result = []
        for each_node in history_nodes:
            if pm.objectType(each_node) == 'blendShape':
                result.append(each_node)
        if result:
            return result
        else:
            return None

    def add_target_list_to_prefix(self, target_list, value_list, **kwargs):
        sufix_list = self.prefix_geometry_list # kwargs.pop('prefix_geometry_list', [])
        custom_target_name = kwargs.pop('custom_target_name', False)
        for each_geometry in sufix_list:
            base_mesh = each_geometry
            blend_shape_node = self.create.BlendShape.by_node(base_mesh)
            if not blend_shape_node:
                blend_shape_node = pm.blendShape(base_mesh)[0]
            else:
                blend_shape_node = blend_shape_node.node
            target_number = len(blend_shape_node.weightIndexList())
            for geo_new_target, each_value in zip(reversed(target_list), reversed(value_list)):
                target_name = '{}{}'.format(geo_new_target, each_geometry)
                print('searchint target name {} for blendshape node {}'.format(target_name, blend_shape_node))
                if pm.objExists(target_name):
                    pm.blendShape(blend_shape_node,
                                  topologyCheck=False, e=True, target=[base_mesh, target_number,
                                                                       target_name,
                                                                       float((math.trunc(each_value * 100)) / 100.0)])
                    if each_value == 1:
                        if custom_target_name:
                            pm.aliasAttr(custom_target_name, '{}.weight[{}]'.format(blend_shape_node, target_number))
                        else:
                            pm.aliasAttr(geo_new_target, '{}.weight[{}]'.format(blend_shape_node, target_number))

    def add_target_list(self, target_list, value_list, **kwargs):
        custom_target_name = kwargs.pop('custom_target_name', False)
        target_number = len(self.blend_shape_node.weightIndexList())
        for geo_new_target, each_value in zip(reversed(target_list), reversed(value_list)):
            pm.blendShape(self.blend_shape_node,
                          topologyCheck=False, e=True, target=[self.base_mesh, target_number,
                                                               geo_new_target,
                                                               float((math.trunc(each_value * 100))/100.0)])
            if each_value == 1 and custom_target_name:
                if custom_target_name:
                    pm.aliasAttr(custom_target_name, '{}.weight[{}]'.format(self.blend_shape_node, target_number))
                else:
                    pm.aliasAttr(geo_new_target, '{}.weight[{}]'.format(self.blend_shape_node, target_number))
        return target_number

    def normalize_target_list(self, target_list, value_list):
        # print 'data {}, {}'.format(target_list, value_list)
        normalized_value_list = []
        ordered_target_list = []
        if not value_list:
            number_of_elements = len(target_list)
            for index, each_target in enumerate(target_list):
                normalized_value_list.append((1.0 / number_of_elements) * index + 1)
                ordered_target_list.append(each_target)
        else:
            max_value_list = [each for each in sorted(value_list)]

            for each_value in max_value_list:
                normalized_value_list.append(float(each_value) / max_value_list[-1])
                ordered_target_list.append(target_list[value_list.index(each_value)])
        return ordered_target_list, normalized_value_list

    def add_target(self, geo_destination, geo_new_target):
        blend_shapes_list = self.get_blend_shapes_in_history(geo_destination)

        if blend_shapes_list:
            blend_shape_node = blend_shapes_list[0]
            number_of_targets = len(blend_shape_node.weightIndexList())
            pm.blendShape(blend_shape_node, e=True, target=[geo_destination, number_of_targets + 1, geo_new_target, 1.0])
            blend_shape_node.weight[number_of_targets + 1].set(1)
        else:
            blend_shape_node = pm.blendShape(geo_destination, before=True)
            blendShape_pm = pm.ls(blend_shape_node)[0]
            pm.blendShape(blend_shape_node, e=True, target=[geo_destination, 0, geo_new_target, 1.0])
            blendShape_pm.weight[0].set(1)


if __name__ == '__main__':
    # RigFacial(facial_definition.correctives_jaw, blend_shape_node_index=-1)
    pass
