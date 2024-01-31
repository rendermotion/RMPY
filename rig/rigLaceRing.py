from RMPY.rig import rigLaces
from RMPY.rig import rigSingleJoint
import pymel.core as pm
from RMPY.rig import rigPointOnSurface
from RMPY.rig import rigUVPin
import importlib


class LaceRingModel(rigSingleJoint.ModelSingleJoint):
def __init__(self):
    super(LaceRingModel, self).__init__()
    self.lace_rig = None
    self.surface = None
    self.geometry_output = None
    self.uvPin_list = []


class LaceRing(rigSingleJoint.RigSingleJoint):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', LaceRingModel())
        super(LaceRing, self).__init__(*args, **kwargs)

def create_point_base(self, *args, **kwargs):
    link_type = kwargs.pop('link_type', 'regular')
    r_l_order_change = kwargs.pop('r_l_order_change', False)
    create_path_surface = kwargs.pop('create_path_surface', False)
    self._model.surface = kwargs.pop('surface', None)
    nurbs_to_poly_output = kwargs.pop('nurbs_to_poly_output', False)

    kwargs['offset_by_points'] = kwargs.pop('offset_by_points', True)
    kwargs['curve_distance'] = kwargs.pop('curve_distance', 0.4)
    kwargs['no_controls'] = kwargs.pop('no_controls', True)
    periodic = kwargs.pop('periodic', False)
    kwargs['periodic'] = periodic

    self._model.lace_rig = rigLaces.RigLaces(rig_system=self.rig_system)
    if len(args) < 4:
        kwargs['controls_number'] = kwargs.pop('controls_number', len(args) + 2)

    self.lace_rig.create_point_base(*args, **kwargs)
    # controls_rig = singleJointRig.SingleJointRig(rig_system=self.lace_rig.rig_system)

    self.lace_rig.rename_as_skinned_joints(nub=False)

    if r_l_order_change:
        if not periodic:
            points_order, clusters_order, middle_point = self._split_in_the_middle(*args,
            cluster_list=self.lace_rig.clusters[1:-1])
        else:
            new_list = list(self.lace_rig.clusters[2:])
            new_list.append(self.lace_rig.clusters[0])
            points_order, clusters_order, middle_point = self._split_in_the_middle(*args[1:],
            cluster_list=new_list)
            points_order.append(args[0])
            clusters_order.append(self.lace_rig.clusters[1])

    else:
        points_order = args
        clusters_order = self.lace_rig.clusters[1:-1]
        middle_point = len(args) - 1
    index = 0
    for each_child, each_cluster in zip(points_order, clusters_order):
        super(LaceRing, self).create_point_base(each_child, link_type=link_type)
        pm.parentConstraint(self.joints[-1], each_cluster, mo=True)
        if not periodic:
            if index == 0:
                pm.parentConstraint(self.joints[0], self.lace_rig.clusters[0], mo=True)
                # pm.parentConstraint('L_laceJoint06_sideStrap_JNT', controls_rig.reset_controls[0], mo=True)
            if index == middle_point:
                pm.parentConstraint(self.joints[-1], self.lace_rig.clusters[-1], mo=True)
                # pm.parentConstraint('R_laceJoint05_sideStrap_JNT', controls_rig.reset_controls[-1], mo=True)
        index += 1
    if create_path_surface:
        self._model.surface = pm.loft(self.lace_rig.curve, self.lace_rig.upVectorCurve, ch=False)[0]
        self.name_conv.rename_name_in_format(self.surface)
        self.surface.setParent(self.rig_system.kinematics)

        if nurbs_to_poly_output:
            self._model.geometry_output = pm.nurbsToPoly(self.surface, matchNormalDir=1, constructionHistory=1,
                                                        format=2, polygonType=1, chordHeightRatio=0.9,
                                                        fractionalTolerance=0.01,
                                                        minEdgeLength=0.001, delta=0.1, uType=1,
                                                        uNumber=2, vType=1, vNumber=int(len(args) * 2),
                                                        useChordHeight=0,
                                                        useChordHeightRatio=0, chordHeight=0.2, edgeSwap=1,
                                                        normalizeTrimmedUVRange=1, matchRenderTessellation=0,
                                                        useSurfaceShader=1)[0]
            self._model.geometry_output = pm.ls(self.geometry_output)[0]
            self.name_conv.rename_name_in_format(self.geometry_output, name='driverGeometry')
            self.geometry_output.setParent(self.rig_system.kinematics)

            for each in self.reset_controls:
                new_uv_pin = rigUVPin.RigUVPin(rig_system=self.rig_system)
                new_uv_pin.create_point_base(each, geometry=self.geometry_output)
                new_uv_pin.clean_up()
                pm.parentConstraint(new_uv_pin.tip, each, mo=True)
                self.uvPin_list.append(new_uv_pin)
                pm.delete(self.surface)
                self._model.surface = None

        else:
            for each in self.reset_controls:
                point_on_surface = rigPointOnSurface.RigPointOnSurface(self.surface, rig_system=self.rig_system)
                point_on_surface.create_point_base(each)
                pm.parentConstraint(point_on_surface.tip, each, mo=True)

    else:
        if self.surface:
            for each in self.reset_controls:
                point_on_surface = rigPointOnSurface.RigPointOnSurface(self.surface, rig_system=self.rig_system)
                point_on_surface.create_point_base(each)
                pm.parentConstraint(point_on_surface.tip, each, mo=True)


def static_connection(self, control, action_element):
    # deprecated
    reset_joint, joint = self.rig_create.joint.point_base(control, type='world', name='static')
    reset_joint.setParent(self.rig_system.joints)
    self.reset_joints.append(reset_joint)
    self.joints.extend(joint)
    self.rig_create.connect.static_connection(control, joint[0])
    pm.parentConstraint(joint[0], action_element, mo=True)

def _split_in_the_middle(self, *args, **kwargs):
    cluster_list = kwargs.pop('cluster_list', None)
    points_order = []
    clusters_order = []
    if len(args) % 2 == 0:
        middle_point = int(len(args) / 2)
    else:
        middle_point = int((len(args) + 1) / 2)
    points_order.extend(list(args[0:middle_point]))
    points_order.extend([each for each in reversed(args[middle_point:])])
    clusters_order.extend(cluster_list[0:middle_point])
    clusters_order.extend([each for each in reversed(cluster_list[middle_point:])])
    return points_order, clusters_order, middle_point


if __name__ == '__main__':
    pass
    strap_points = pm.ls('c_spine00_reference_pnt')[0]
    lace_ring = LaceRing()
    lace_ring.create_point_base(*strap_points.getChildren(), r_l_order_change=True, link_type='static')

