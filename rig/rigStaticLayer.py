"""
It receives  as input a list of geometries that are part of this static layer,
The static layers rig is intended to simplify the task of creating static rigs with multiple pieces.
and it will duplicate the objects and will blendshape them to
the original geometry.
"""

import pymel.core as pm
from RMPY.rig import rigBase
from RMPY.rig import rigStaticBlendShapes


class StaticLayerModel(rigBase.BaseModel):
    def __init__(self):
        super(StaticLayerModel, self).__init__()
        self.geometries = []
        self.static_geometries = []
        self.root_geos = None
        self.blend_shape_rig = None


class StaticLayer(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', StaticLayerModel())
        super(StaticLayer, self).__init__(*args, **kwargs)
        self.geometries.extend(args)
        self.name_convention.default_names['system'] = kwargs.pop('name', 'staticGeometry')
        self.update_name_convention()
        self.build()

    @property
    def geometries(self):
        return self._model.geometries

    @property
    def static_geometries(self):
        return self._model.static_geometries

    def build(self):
        parent_group = pm.group(empty=True)
        self.name_convention.rename_name_in_format(parent_group, name='rootGeo')
        parent_group.setParent(self.rig_system.kinematics)
        for each_geo in self.geometries:
            new_geo = pm.duplicate(each_geo)[0]
            new_geo.setParent(parent_group)
            if self.name_convention.is_name_in_format(each_geo):
                tokens = each_geo.split('_')
                self.name_convention.rename_name_in_format(new_geo, side=tokens[0], name=tokens[1])
            else:
                tokens = each_geo.split('_')
                self.name_convention.rename_name_in_format(new_geo, name=''.join(tokens))
            self.static_geometries.append(new_geo)
        self._model.blend_shape_rig = rigStaticBlendShapes.StaticBlendShapes(zip(self.static_geometries,
                                                                                 self.geometries))



if __name__ == '__main__':
    StaticLayer('', name='')