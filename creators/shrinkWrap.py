import maya.cmds as cmds
import pymel.core as pm
from RMPY.creators import deformerBase


class ShrinkWrap(deformerBase.WeightGeometryFilterBase):
    """
    Creator of shrinkWrap deformers, with save / load support.

    On top of the data of WeightGeometryFilterBase (node, attributes, geometry) the dictionary contains:
        target: the transform of the target geometry the deformed geometry is wrapped to.
    """
    node_type = 'shrinkWrap'
    extra_path = '/shrinkWraps'
    deformer_attributes = ['envelope', 'projection', 'closestIfNoIntersection', 'reverse', 'bidirectional',
                           'boundingBoxCenter', 'axisReference', 'alongX', 'alongY', 'alongZ',
                           'offset', 'targetInflation', 'targetSmoothLevel', 'falloff', 'falloffIterations',
                           'shapePreservationEnable', 'shapePreservationSteps', 'shapePreservationReprojection']
    # attributes of the target mesh shape that drive the smoothing of the target inside the shrinkWrap,
    # Maya connects them when creating the deformer from the menu.
    target_connections = ['continuity', 'smoothUVs', 'keepBorder', 'boundaryRule',
                          'keepHardEdge', 'propagateEdgeHardness', 'keepMapBorders']

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

    @staticmethod
    def get_shrink_wrap(deformed_geometry):
        return ShrinkWrap.get_deformer(deformed_geometry)

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
        return self.transform_of(shapes[0])

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
    def get_weights_dictionary(self):
        data = super(ShrinkWrap, self).get_weights_dictionary()
        data['target'] = self.target
        return data

    def apply_data(self, data):
        """Reconnects the target if needed, then restores the attributes and the weights."""
        saved_target = data.get('target')
        if saved_target and self.target != saved_target:
            if cmds.objExists(saved_target):
                self.connect_target(saved_target)
            else:
                print('WARNING: target {} of shrinkWrap {} does not exist'.format(saved_target, self.node))
        super(ShrinkWrap, self).apply_data(data)

    def rebuild(self, data):
        target = data.get('target')
        if not target or not cmds.objExists(target):
            raise RuntimeError('the target {} of shrinkWrap {} does not exist in the scene'.format(target,
                                                                                                   data['node']))
        self.geo_base(*self.saved_geometry(data), target=target)

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
