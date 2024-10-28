from RMPY.rig import rigBase
import pymel.core as pm
from RMPY.core import dataValidators


class RigUVPinModel(rigBase.BaseModel):
    def __init__(self):
        super(RigUVPinModel, self).__init__()
        self.uvPin = None
        self.closest_point_on_mesh = None
        self.position_reference_locator = None


class RigUVPin(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', RigUVPinModel())
        super(RigUVPin, self).__init__(*args, **kwargs)

    @property
    def uvPin(self):
        return self._model.uvPin

    @property
    def closest_point_on_mesh(self):
        return self._model.closest_point_on_mesh

    @property
    def position_reference_locator(self):
        return self._model.position_reference_locator

    def create_point_base(self, scene_node, **kwargs):
        super(RigUVPin, self).create_point_base(scene_node, **kwargs)
        geometry = kwargs.pop('geometry', None)
        scene_node = dataValidators.as_pymel_nodes(scene_node)[0]

        if geometry:
            geometry = dataValidators.as_pymel_nodes(geometry)[0]

            all_shapes_list = geometry.getShapes()
            attach_shape = None
            original_shape = None
            for each_shape in all_shapes_list:
                if not each_shape.intermediateObject.get():
                    attach_shape = each_shape
                if not pm.listConnections(each_shape.inMesh):
                    original_shape = each_shape
            if not original_shape:
                original_shape = attach_shape

            if attach_shape:
                self._model.closest_point_on_mesh = pm.general.createNode('closestPointOnMesh')
                pm.connectAttr('{}.worldMesh'.format(geometry), '{}.inMesh'.format(self.closest_point_on_mesh))
                self._model.position_reference_locator = pm.spaceLocator(name='pointOnSurface')
                self.position_reference_locator.setParent(self.rig_system.kinematics)

                self.name_convention.rename_name_in_format(self.position_reference_locator, name='pointOnSurface')

                pm.connectAttr('{}.worldPosition'.format(self.position_reference_locator),
                               '{}.inPosition'.format(self.closest_point_on_mesh))

                # reference_offset = pm.group(empty=True)

                attachment = pm.spaceLocator()
                self.name_convention.rename_name_in_format(attachment, name='meshAttachPoint')
                attachment.setParent(self.rig_system.kinematics)
                pm.matchTransform(self.position_reference_locator, scene_node)

                self._model.uvPin = pm.createNode('uvPin')
                self.uvPin.outputMatrix[0] >> attachment.offsetParentMatrix

                attach_shape.worldMesh >> self.uvPin.deformedGeometry
                original_shape.outMesh >> self.uvPin.originalGeometry

                self.closest_point_on_mesh.parameterU >> self.uvPin.coordinate[0].coordinateU
                self.closest_point_on_mesh.parameterV >> self.uvPin.coordinate[0].coordinateV
                # pm.parentConstraint(attachment, scene_node, mo=True)
                self.tip = attachment
        else:
            raise KeyError('should provide geometry as keyword attribute with some mesh geo')

    def clean_up(self):
        coordinateU = self.uvPin.coordinate[0].coordinateU.get()
        coordinateV = self.uvPin.coordinate[0].coordinateV.get()
        pm.delete(self.closest_point_on_mesh)
        pm.delete(self.position_reference_locator)
        self.uvPin.coordinate[0].coordinateU.set(coordinateU)
        self.uvPin.coordinate[0].coordinateV.set(coordinateV)


if __name__ == '__main__':
    new_uv_pin = RigUVPin()
    new_uv_pin.create_point_base('C_point01_reference_LOC', geometry='C_geo_system_MSH')
    new_uv_pin.clean_up()
    # pm.parentConstraint(new_point_on_poly.tip, 'pCube2')