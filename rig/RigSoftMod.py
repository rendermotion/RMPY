import pymel.core as pm
from RMPY.core import dataValidators
from RMPY.rig import rigSingleJoint


class SoftModRig(rigSingleJoint.SingleJointRig):
    def __init__(self, *args, **kwargs):
        super(SoftModRig, self).__init__(*args, **kwargs)

        self._model.display_spheres = []
        self._model.soft_mod = []

    @property
    def display_spheres(self):
        return self._model.display_spheres

    @property
    def soft_mod(self):
        return self._model.soft_mod

    def create_point_base(self, *args, **kwargs):
        geometry = kwargs.pop('geo', None)
        if geometry.__class__ is not list:
            geometry = list(geometry)
        for each_geo in geometry:
            if not pm.objExists(each_geo):
                geometry.remove(each_geo)

        if geometry:

            if 'size' in kwargs:
                radius = kwargs['size']
            else:
                radius = 1
            previous_controls = len(self.controls)
            super(SoftModRig, self).create_point_base(*args, **kwargs)

            for each_point, control in zip(args, self.controls[previous_controls:]):
                position = dataValidators.as_vector_position(each_point)
                soft_mod, soft_mod_transform = pm.softMod(geometry[0])
                for each in geometry[1:]:
                    soft_mod.setGeometry(each)
                soft_mod_transform.setParent(self.rig_system.kinematics)
                soft_mod_transform.origin.set(position)
                self.soft_mod.append([soft_mod, soft_mod_transform])
                pm.xform(soft_mod_transform, pivots=position)
                soft_mod.falloffCenter.set(position)
                control.translate >> soft_mod_transform.translate
                control.rotate >> soft_mod_transform.rotate
                control.scale >> soft_mod_transform.scale
                self.create_sphere_display_control_base(control, radius)
                control.radius >> soft_mod.falloffRadius
        else:
            print('geo key word arg needs to be specified with valid scene geometry')

    def create_sphere_display_control_base(self, control, radius):
        new_sphere_transform, new_sphere_creator = pm.polySphere()
        self.display_spheres.append([new_sphere_transform, new_sphere_creator])
        pfx = pm.createNode('pfxToon')
        transform_pfx = pm.ls('pfxToon1')[0]
        new_sphere_transform.setParent(self.rig_system.kinematics)
        self.name_conv.rename_name_in_format(transform_pfx, name='display')
        self.name_conv.rename_name_in_format(pfx, name='displaypfx')
        self.name_conv.rename_name_in_format(new_sphere_transform, name='displaySphere')
        self.name_conv.rename_name_in_format(new_sphere_creator, name='displaySphereCreation')

        new_sphere_transform.outMesh >> pfx.inputSurface[0].surface
        new_sphere_transform.worldMatrix >> pfx.inputSurface[0].inputWorldMatrix
        pfx.displayPercent.set(100)
        pfx.screenspaceWidth.set(True)
        pfx.distanceScaling.set(1)
        pfx.minPixelWidth.set(1)
        pfx.maxPixelWidth.set(10)
        pfx.profileColor.set(0.5, 0.0, 0.0)
        len(pm.getAttr(pfx.inputSurface, mi=True))
        pfx.overrideEnabled.set(True)
        pfx.overrideDisplayType.set(2)
        pm.addAttr(control, ln='radius', at='float', k=True, hnv=True, min=0)
        pm.addAttr(control, ln='influenceDisplay', at='bool', k=True)
        control.radius >> new_sphere_creator.radius
        control.radius.set(radius)
        control.influenceDisplay.set(True)
        control.influenceDisplay >> transform_pfx.visibility
        pm.parentConstraint(control, new_sphere_transform)


if __name__ == '__main__':
    root_point = pm.ls('C_testPoint_reference_GRP')[0]
    new_soft = SoftModRig()
    # child_list = []
    # for each_children in root_points.getChildren():
    #    new_soft.create_point_base(*each_children.getChildren(), geo='C_static_collar_mid_GES',
    #                               type='box', size=.2, centered=True)
    geo = [u'pCube1', u'pCylinder1', u'pSphere1']

    new_soft.create_point_base(root_point, geo=geo,
                               type='box',
                               size=.2,
                               centered=True)