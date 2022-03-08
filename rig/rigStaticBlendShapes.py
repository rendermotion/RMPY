import pymel.core as pm
from RMPY.rig import rigBase


class StaticBlendShapes(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        """
        Connects all the static blendshapes that are required. the static connections shows which geo,
        will connect with which

        :param args: list of sets first element is the geometry that will be plugged in the second element
        (blendshapeGeo,'destinationGeo')
        :param kwargs:
        """
        kwargs['model'] = kwargs.pop('model', rigBase.BaseModel())
        super(StaticBlendShapes, self).__init__(*args, **kwargs)
        self.static_connections = args[0]
        self.build()

    def build(self):
        for geo_static, geo_destination in self.static_connections:
            self.add_target(geo_destination, geo_static)

    @staticmethod
    def get_blend_shapes_in_history(scene_node):
        history_nodes = pm.listHistory(scene_node, interestLevel=2, pruneDagObjects=True)
        result = []
        for each_node in history_nodes:
            if pm.objectType(each_node) == 'blendShape':
                result.append(each_node)
        return result

    def add_target(self, geo_destination, geo_new_target):
        blend_shapes_list = self.get_blend_shapes_in_history(geo_destination)
        if blend_shapes_list:
            blend_shape_node = blend_shapes_list[0]
            number_of_targets = len(blend_shape_node.weightIndexList())
            pm.blendShape(blend_shape_node, e=True, target=[geo_destination, number_of_targets + 1, geo_new_target, 1.0])
            blend_shape_node.weight[number_of_targets + 1].set(1)
        else:
            blend_shape_node = pm.blendShape(geo_destination, before=True)
            self.name_convention.rename_name_in_format(blend_shape_node,
                                                       name=self.name_convention.get_a_short_name(geo_destination),
                                                       system='staticRig')
            blend_shape_pm = pm.ls(blend_shape_node)[0]
            pm.blendShape(blend_shape_node, e=True, target=[geo_destination, 0, geo_new_target, 1.0])
            blend_shape_pm.weight[0].set(1)