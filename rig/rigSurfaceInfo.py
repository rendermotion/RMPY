import pymel.core as pm
from RMPY.rig import rigBase
from RMPY.core import dataValidators
if 'matrixNodes' not in pm.pluginInfo(query=True, listPlugins=True):
    pm.loadPlugin('matrixNodes.so')


class SurfaceInfoModel(rigBase.BaseModel):
    def __init__(self):
        super(SurfaceInfoModel, self).__init__()
        self.surface_info = None
        self.matrix = None
        self.decomposition = None


class SurfaceInfo(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', SurfaceInfoModel())
        super(SurfaceInfo, self).__init__(*args, **kwargs)
        follow_v = kwargs.pop('follow_v', False)
        surface = dataValidators.as_pymel_nodes(args[0])[0]

        if pm.objectType(surface) != 'nurbsSurface':
            if pm.objectType(surface.getShapes()[0]) == 'nurbsSurface':
                surface = surface.getShapes()[0]
        else:
            raise AttributeError

        self.surface_info = pm.createNode('pointOnSurfaceInfo')
        self.name_convention.rename_name_in_format(self.surface_info, name='surfaceInfo')
        self.matrix = pm.createNode('fourByFourMatrix')
        self.name_convention.rename_name_in_format(self.matrix, name='surfaceInfoMatrix')
        self.decomposition = pm.createNode('decomposeMatrix')
        self.name_convention.rename_name_in_format(self.decomposition, name='surfaceInfoResult')

        self.vector_product = pm.createNode('vectorProduct')

        self.name_convention.rename_name_in_format(self.vector_product, name='uVectorResult')
        self.vector_product.operation.set(2)

        pm.connectAttr('{}.worldSpace[0]'.format(surface), '{}.inputSurface'.format(self.surface_info))

        pm.connectAttr('{}.normalizedNormalX'.format(self.surface_info), '{}.in10'.format(self.matrix))
        pm.connectAttr('{}.normalizedNormalY'.format(self.surface_info), '{}.in11'.format(self.matrix))
        pm.connectAttr('{}.normalizedNormalZ'.format(self.surface_info), '{}.in12'.format(self.matrix))

        pm.connectAttr('{}.normalizedTangentVX'.format(self.surface_info), '{}.in20'.format(self.matrix))
        pm.connectAttr('{}.normalizedTangentVY'.format(self.surface_info), '{}.in21'.format(self.matrix))
        pm.connectAttr('{}.normalizedTangentVZ'.format(self.surface_info), '{}.in22'.format(self.matrix))

        pm.connectAttr('{}.normalizedTangentV'.format(self.surface_info), '{}.input1'.format(self.vector_product))
        pm.connectAttr('{}.normalizedNormal'.format(self.surface_info), '{}.input2'.format(self.vector_product))

        if follow_v:
            pm.connectAttr('{}.outputX'.format(self.vector_product), '{}.in00'.format(self.matrix))
            pm.connectAttr('{}.outputY'.format(self.vector_product), '{}.in01'.format(self.matrix))
            pm.connectAttr('{}.outputZ'.format(self.vector_product), '{}.in02'.format(self.matrix))

        else:
            pm.connectAttr('{}.normalizedTangentUX'.format(self.surface_info), '{}.in00'.format(self.matrix))
            pm.connectAttr('{}.normalizedTangentUY'.format(self.surface_info), '{}.in01'.format(self.matrix))
            pm.connectAttr('{}.normalizedTangentUZ'.format(self.surface_info), '{}.in02'.format(self.matrix))

        pm.connectAttr('{}.output'.format(self.matrix), '{}.inputMatrix'.format(self.decomposition))

    @property
    def surface_info(self):
        return self._model.surface_info

    @surface_info.setter
    def surface_info(self, value):
        self._model.surface_info = value

    @property
    def matrix(self):
        return self._model.matrix

    @matrix.setter
    def matrix(self, value):
        self._model.matrix = value

    @property
    def decomposition(self):
        return self._model.decomposition

    @decomposition.setter
    def decomposition(self, value):
        self._model.decomposition = value

    def connect_rotate(self, scene_node):
        pm.connectAttr('{}.outputRotate'.format(self.decomposition), '{}.rotate'.format(scene_node))

    def connect_translate(self, scene_node):
        pm.connectAttr('{}.position'.format(self.surface_info), '{}.translate'.format(scene_node))

    def connect(self, scene_node):
        pm.connectAttr('{}.position'.format(self.surface_info), '{}.translate'.format(scene_node))
        pm.connectAttr('{}.outputRotate'.format(self.decomposition), '{}.rotate'.format(scene_node))

    @property
    def parameter_u_attribute(self):
        return '{}.parameterU'.format(self.surface_info)

    @property
    def parameter_v_attribute(self):
        return '{}.parameterV'.format(self.surface_info)

    @property
    def parameter_u(self):
        return pm.getAttr(self.parameter_u_attribute)

    @parameter_u.setter
    def parameter_u(self, value):
        pm.setAttr(self.parameter_u_attribute, value)

    @property
    def parameter_v(self):
        return pm.getAttr(self.parameter_v_attribute)

    @parameter_v.setter
    def parameter_v(self, value):
        pm.setAttr(self.parameter_v_attribute, value)

    def delete(self):
        pm.delete(self.matrix)

