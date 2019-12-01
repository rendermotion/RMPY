import pymel.core as pm
from RMPY.rig import rigBase
from RMPY.creators import nucleus
from RMPY.rig import rig
from pprint import pprint as pp



class DynamicHairModel(object):
    def __init__(self):
        self.nucleus = None
        self.original_curves = []
        self.created_output_curves = []
        self.reset_follicles = None
        self.dynamics = None
        self.reset_joints = []
        self.joints = []
        self.up_vectors = []
        self.follicles_index = []


class DynamicHair(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(DynamicHair, self).__init__(*args, **kwargs)

        self._model = DynamicHairModel()
        existing_nucleus = False
        if 'nucleus' in kwargs.keys():
            existing_nucleus = True
            self.nucleus = kwargs.pop('nucleus')
        else:
            self.nucleus = nucleus.Creator(name_conv=self.name_conv)
            self.nucleus.node.enable.set(0)

        if not existing_nucleus:
            self.nucleus.node.setParent(self.dynamics)

        self.dynamic_output_curves = pm.group(empty=True)
        self.name_conv.rename_name_in_format(self.dynamic_output_curves, name='output')
        self.dynamic_output_curves.setParent(self.dynamics)

        self.nucleus.add_hair_system()
        self.hair_system_index = len(self.nucleus.hair_systems) - 1

        self.name_conv.rename_name_in_format(self.nucleus.hair_systems[self.hair_system_index].transform,
                                             name='hairSystem')

        self.nucleus.hair_systems[self.hair_system_index].transform.setParent(self.dynamics)

        self.laces_system = laces.Laces(rig_system=self.rig_system)

    @property
    def created_output_curves(self):
        return self._model.created_output_curves

    @property
    def follicles_index(self):
        return self._model.follicles_index

    @property
    def follicles(self):
        return [self.nucleus.hair_systems[self.hair_system_index].follicles[index] for index in self.follicles_index]

    @property
    def reset_joints(self):
        return self._model.reset_joints

    @property
    def joints(self):
        return self._model.joints

    @property
    def up_vectors(self):
        return self._model.up_vectors

    @property
    def dynamics(self):
        if not self._model.dynamics:
            self._model.dynamics = pm.group(empty=True)

            self.name_conv.rename_name_in_format(self._model.dynamics, name='dynamics')
            self._model.dynamics.setParent(self.rig_system.kinematics)
        return self._model.dynamics

    @property
    def reset_follicles(self):
        if not self._model.reset_follicles:
            self._model.reset_follicles = pm.group(empty=True)

            self.name_conv.rename_name_in_format(self._model.reset_follicles, name='follicles')
            self._model.reset_follicles.setParent(self.dynamics)
        return self._model.reset_follicles

    @reset_follicles.setter
    def reset_follicles(self, value):
        self._model.reset_follicles = value

    @property
    def original_curves(self):
        return self._model.original_curves

    @original_curves.setter
    def original_curves(self, value):
        self._model.original_curves = value

    @property
    def hair_system(self):
        return self._model.nucleus.hair_systems[self.hair_system_index]

    @property
    def output_curves(self):
        return [[follicles.output_curve for follicles in hair_system.follicles] for hair_system in
                [nucleus_hair_system for nucleus_hair_system in self.nucleus.hair_systems]]

    @property
    def nucleus(self):
        return self._model.nucleus

    @nucleus.setter
    def nucleus(self, value):
        self._model.nucleus = value

    def create_point_base(self, *points, **kwargs):
        super(DynamicHair, self).create_point_base(*points, **kwargs)

        self.nucleus.name_conv = self.name_conv
        controls_number = kwargs.pop('controls_number', None)
        keepRange = kwargs.pop('keepRange', 2)
        periodic = kwargs.pop('periodic', False)
        rebuildType = kwargs.pop('rebuildType', 0)
        ep = kwargs.pop('ep', True)

        curve = self.rig_create.nurbs_curve.point_base(*points, periodic=periodic, ep=ep)

        if controls_number:
            if controls_number < 4:
                controls_number = 4

        if controls_number:
            # base_curve = self.rig_create.nurbs_curve.curve_base(curve, spans=controls_number, keepRange=keepRange,
            # rebuildType=rebuildType)

            base_curve = pm.rebuildCurve(curve, rebuildType=rebuildType, spans=controls_number, keepRange=keepRange)[0]
        else:
            base_curve = curve
        self.original_curves.append(base_curve)
        # self.original_curve.setParent(self.dynamics)
        self._create_dynamic_curve(self.original_curves[-1], **kwargs)

    def _create_dynamic_curve(self, *args, **kwargs):
        joint_count = kwargs.pop('joint_count', 10)

        self.follicles_index.append(len(self.nucleus.hair_systems[self.hair_system_index].follicles))
        self.nucleus.hair_systems[self.hair_system_index].add_follicle()
        self.nucleus.hair_systems[self.hair_system_index].follicles[-1].curve_base(args[0], **kwargs)
        self.nucleus.hair_systems[self.hair_system_index].follicles[-1].transform.setParent(self.reset_follicles)
        self.nucleus.hair_systems[self.hair_system_index].follicles[-1].node.startDirection.set(1)
        self.nucleus.hair_systems[self.hair_system_index].follicles[-1].output_curve.getParent().setParent(
            self.dynamic_output_curves)
        output_curve = self.nucleus.hair_systems[self.hair_system_index].follicles[-1].output_curve.getParent()

        self.created_output_curves.append(output_curve)
        # for curve_list in self.output_curves:
        # pm.parent(curve_list, self.dynamic_output_curves)
        if joint_count:
            self._create_joints_on_curve(output_curve, joint_count)

    def _create_joints_on_curve(self, curve, joint_count):
        joints_dict = self.laces_system.joints_on_curve(joint_count, curve=curve, UpVectorType="object")

        new_parent = pm.group(empty=True, name='curveJoints')
        self.name_conv.rename_name_in_format(new_parent)
        new_parent.setParent(self.rig_system.joints)
        self.reset_joints.append(new_parent)
        self.joints.append(joints_dict['joints'])
        self.name_conv.rename_name_in_format(joints_dict['joints'], name='curveJoint')
        pm.parent(joints_dict['joints'], new_parent)
        self.up_vectors.append(joints_dict['UpVector'])
        joints_dict['UpVector'].setParent(self.dynamics)
        joints_dict['UpVector'].translateY.set(13)
        joints_dict['UpVector'].rotateZ.set(90)

    def add_collision(self, *mesh):
        for each_geo in mesh:
            self.nucleus.add_collision_mesh(each_geo)
            self.nucleus.collision[-1].transform.setParent(self.dynamics)


if __name__ == '__main__':
    hair_root = pm.ls('C_dynamicSpl00_reference_GRP')[0]
    dynamic_hair = DynamicHair()
    dynamic_hair.create_point_base(*hair_root.getChildren())