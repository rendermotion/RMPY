import pymel.core as pm
from RMPY.rig import rigBase
from RMPY.rig import rigSplineIK


class RigChainModel(rigBase.BaseModel):
    def __init__(self):
        super(RigChainModel, self).__init__()

        self.rig_joints_on_curve = None
        self.curve = None


class RigChain(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', RigChainModel())

        super(RigChain, self).__init__(*args, **kwargs)
        self.geometry = kwargs.pop('geometry', None)
        self.name = kwargs.pop('name', 'chainRigA')
        self.simplify_curves_factor = kwargs.pop('simplify_curves_factor', 10.0)
        if self.geometry:
            if self.geometry.__class__ == list:
                self.geometry = pm.ls(self.geometry)
        else:
            self.geometry = pm.ls(self.geometry)[0]
        self.index_min = 32
        self.index_max = 39
        self.index_list = kwargs.pop('index_list', [4, 5, 22, 32, 42, 52, 62, 72, 82, 92])
        self.shells_vtx_list = []
        self.joints_reference_points = kwargs.pop('joints_reference_points', [])
        self.build()

    @property
    def curve(self):
        return self._model.curve

    @property
    def rig_joints_on_curve(self):
        return self._model.rig_joints_on_curve

    def build(self):
        do_cleanup = False

        if not self.joints_reference_points and self.geometry:
            self._create_reference_points()
        do_cleanup = True
        self._create_joints_on_points()
        self._create_base_shape()
        if self.geometry:
            self._skin_geometry()
        if do_cleanup:
            self._cleanup()

    def _create_base_shape(self):
        new_curve = self.rig_create.nurbs_curve.point_base(*self.joints_reference_points, ep=True)

        num_spans = len(self.joints_reference_points) / self.simplify_curves_factor
        if num_spans < 4:
            num_spans = 4

        self._model.curve = self.rig_create.nurbs_curve.curve_base(new_curve, spans=num_spans)
        self._model.rig_joints_on_curve = rigSplineIK.RigSplineIK(rig_system=self.rig_system)
        self._model.rig_joints_on_curve.create_point_base(*self.joints_reference_points, curve=new_curve,
                                                          joints=self.joints,
                                                          reset_joints=self.reset_joints, connect_length=False)

        # self.rig_system.settings.length.set(0.6)

    def _create_reference_points(self):
        if self.geometry.__class__ == list:
            self._multiple_geometries_reference_points()

        else:
            self._single_geometry_reference_points()

    def _multiple_geometries_reference_points(self):
        print('creating multiple geos {}'.format(self.geometry))
        for each_geo in self.geometry:
            short_vertex_list = [each_geo.vtx[each] for each in self.index_list]
            space_loc = self.rig_create.space_locator.point_base(short_vertex_list)
            self.joints_reference_points.append(space_loc)

    def _single_geometry_reference_points(self):
        print('creating single geos {} {}'.format(self.geometry, self.geometry.__class__))
        # Creates all the reference points based on the vertex of the chains,
        # the index_min and index_max can help determine which are the vertices where this points should be created,
        # on each shell of the geo.
        current_index = 0
        max_components = self.geometry.vtx.totalSize()
        points_list = []
        while current_index < max_components:
            pm.select(self.geometry.vtx[current_index], r=True)
            face = pm.ls(pm.polyListComponentConversion(self.geometry.vtx[current_index], fromVertex=True, toFace=True))[0]
            pm.polySelect(*pm.polyListComponentConversion(self.geometry.vtx[current_index], fromVertex=True, toFace=True),
                          extendToShell=face.indices()[0],
                          replace=True)
            pm.polyEvaluate(pm.polyListComponentConversion(self.geometry.vtx[current_index],
                                                           fromVertex=True, toFace=True), activeShells=True)
            # selection = pm.ls(selection=True)
            vertex_list = pm.ls(pm.polyListComponentConversion(fromFace=True, toVertex=True))[0]
            indices_list = vertex_list.indices()
            # short_list = indices_list[self.index_min:self.index_max]
            short_list = [indices_list[each] for each in self.index_list]
            self.shells_vtx_list.append(indices_list)
            current_index = indices_list[-1] + 1
            short_vertex_list = [self.geometry.vtx[each] for each in short_list]
            space_loc = self.rig_create.space_locator.point_base(short_vertex_list)
            self.joints_reference_points.append(space_loc)
            points_list.extend(short_vertex_list)

        self.name_convention.rename_name_in_format(*self.joints_reference_points,
                                             system=self.name,
                                             name='points',
                                             side='C')

    def _create_joints_on_points(self):
        reset, rig_joints = self.rig_create.joint.point_base(*self.joints_reference_points)

        pm.parent(reset, self.rig_system.joints)
        self.reset_joints.append(reset)
        self.joints.extend(rig_joints)
        self.rename_as_skinned_joints(nub=False)

    def _skin_geometry(self):
        if self.geometry.__class__ == list:
            self._skin_multpiple_geometries()
        else:
            self._skin_single_geometry()

    def _skin_multpiple_geometries(self):
        print('joints on file {}'.format(self.joints))

        pm.select(clear=True)
        for each_joint, each_geo in zip(self.joints, self.geometry):
            print('skinning {} to {}'.format(each_joint, each_geo))
            pm.skinCluster(each_joint, each_geo, toSelectedBones=True)

    def _skin_single_geometry(self):
        print('doing skin of all geometry')

        pm.skinCluster(self.joints, self.geometry)
        skin_cluster = self.rig_create.SkinCluster.SkinCluster.by_node(self.geometry)
        weights_dictionary = skin_cluster.get_weights_dictionary()
        new_weights = {}
        for index, (current_joint, vertex_list) in enumerate(zip(self.joints, self.shells_vtx_list)):
            for each_vertex in vertex_list:
                new_weights[each_vertex] = [[index], [1]]
        weights_dictionary['weights'] = new_weights
        skin_cluster.apply_weights_dictionary(weights_dictionary)

    def _cleanup(self):
        pm.delete(self.joints_reference_points)


if __name__ == '__main__':
    powerCable = pm.ls('C_powerCable00_reference_GRP')[0]
    geometry = ['C_chain_0017_GES', 'C_chain_0019_GES', 'C_chain_0021_GES', 'C_chain_0023_GES', 'C_chain_0025_GES',
                'C_chain_0027_GES', 'C_chain_0029_GES', 'C_chain_0031_GES']
    RigChain(geometry=geometry, joints_reference_points=powerCable.getChildren(), name='chainB')