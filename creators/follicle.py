import pymel.core as pm
from RMPY import RMRigTools
from RMPY.creators import creatorsBase
from RMPY.creators import motionPath

reload(creatorsBase)


class Creator(creatorsBase.Creator):
    def __init__(self, *args, **kwargs):
        super(Creator, self).__init__(*args, **kwargs)
        self._hair_system = None
        self._node = None
        self.surface = None
        self._output_curve = None
        self.motion_path = motionPath.Creator(name_conv=self.name_conv)

    @property
    def transform(self):
        return self._node.getParent()

    @property
    def node(self):
        return self._node

    @node.setter
    def node(self, value):
        self.node = value

    @property
    def output_curve(self):
        if not self._output_curve:
            self.create_output_curve()
        return self._output_curve

    @output_curve.setter
    def output_curve(self, value):
        self._output_curve = value

    @property
    def hair_system(self):
        return self._hair_system

    @hair_system.setter
    def hair_system(self, value):
        self._hair_system = value

    def point_base(self, *points, **kwargs):
        print 'follicle Naming {}'.format(points[0])
        self.setup_name_conv_node_base(points[0])
        print '{}'.format(self.name_conv.default_names)
        self.build()
        return self._node

    def curve_base(self, *args, **kwargs):
        control_points = kwargs.pop('control_points', None)
        if not self.node:
            self.point_base(*args, **kwargs)
        dynamic_curve_base = args[0]

        new_motion = self.motion_path.node_base(self.transform, curve=args[0])
        pm.delete(new_motion)
        if not control_points:
            rebuild_curve = pm.rebuildCurve(dynamic_curve_base, constructionHistory=True, replaceOriginal=0,
                                            rebuildType=0, endKnots=1, keepRange=0, keepControlPoints=1,
                                            keepEndPoints=1, keepTangents=0, spans=0, degree=1, tolerance=0.1)[0]
        else:
            rebuild_curve = pm.rebuildCurve(dynamic_curve_base, constructionHistory=True, replaceOriginal=0,
                                            rebuildType=0, endKnots=0, keepRange=0, keepControlPoints=0,
                                            keepEndPoints=0, keepTangents=1, spans=control_points, degree=1,
                                            tolerance=0.1)[0]

        shapes = rebuild_curve.getShapes()
        shapes[0].intermediateObject.set(True)
        pm.parent(shapes, dynamic_curve_base, r=True, s=True)
        shapes[0].local >> self.node.startPosition
        dynamic_curve_base.worldMatrix >> self.node.startPositionMatrix
        pm.parent(args[0], self.transform)
        pm.delete(rebuild_curve)
        self.create_output_curve()
        return self._node, self.output_curve

    def surface_base(self, nurbs_surface, **kwargs):
        self.setup_name_conv_node_base(nurbs_surface)
        nurbs_surface = RMRigTools.validate_pymel_nodes(nurbs_surface)
        self.surface = nurbs_surface.getShapes()[0]
        u_value = kwargs.pop('u_value', .5)
        v_value = kwargs.pop('v_value', .5)
        self.build()
        self._node.startDirection.set(1)
        self._node.parameterU.set(u_value)
        self._node.parameterV.set(v_value)
        self.connect_input_surface(self.surface)
        follicle_transform = self._node.getParent()
        self.connect_output_transform(follicle_transform)

        self._node.outTranslate >> self.transform.translate
        self._node.outRotate >> self.transform.rotate

        return self._node

    def create_output_curve(self):
        self._output_curve = pm.createNode('nurbsCurve')
        self.name_conv.rename_name_in_format(self._output_curve.getParent(), name='dynamicCurve')
        self._node.outCurve >> self._output_curve.create
        self._output_curve.getParent().setParent(self.transform)

    def build(self):
        self._node = pm.createNode('follicle')
        self.name_conv.rename_name_in_format(self._node.getParent())

    def connect_input_surface(self, surface):
        if surface or self.surface:
            if surface:
                self.surface = surface
            self.surface.local >> self._node.inputSurface
            self.surface.worldMatrix >> self._node.inputWorldMatrix

    def connect_output_transform(self, transform):
        self._node.outTranslate >> transform.translate
        self._node.outRotate >> transform.rotate


if __name__ == '__main__':
    new_fol = Creator()
    new_fol.surface_base('C_basePlane00_suspension_GRP')
if __name__ == '__main__':
    new_fol = Follicle()
    new_fol.surface_based('C_basePlane00_suspension_GRP')