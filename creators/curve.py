import pymel.core as pm
import maya.cmds as cmds
from RMPY.core import dataValidators
from RMPY.creators import creatorsBase
from RMPY.core import dataManager


class Curve(creatorsBase.CreatorsBase):
    def __init__(self, *args, **kwargs):
        super(Curve, self).__init__(*args, **kwargs)

    def curve_base(self, curve, **kwargs):
        super(Curve, self).curve_base(curve, **kwargs)
        spans = kwargs.pop('spans', 4)
        rebuild_type = kwargs.pop('rebuildType', 0)
        keep_range = kwargs.pop('keepRange', 2)
        curve = dataValidators.as_pymel_nodes(curve)


        if curve.form() == 'periodic':
            if spans >= 3:
                curve = pm.rebuildCurve(curve, rebuildType=rebuild_type, spans=spans, keepRange=keep_range,
                                        **kwargs)[0]
                return curve
            else:
                return None
        else:
            if spans >= 1:
                curve = pm.rebuildCurve(curve, rebuildType=rebuild_type, spans=spans, keepRange=keep_range,
                                        **kwargs)[0]
                return curve
            else:
                return None

        return curve

    def on_surface_point_base(self, *points, **kwargs):
        surface = kwargs.pop('surface', None)
        periodic = kwargs.pop('periodic', False)
        degree = kwargs.pop('degree', 3)
        points = [dataValidators.as_2d_vector(each_point) for each_point in points]
        if surface:
            surface = dataValidators.as_pymel_nodes(surface)
            if not periodic:
                curve = pm.curveOnSurface(surface, degree=degree, positionUV=points,
                                          name=self.name_convention.set_name_in_format(
                                              name='curveOnSurface', objectType='nurbsCurve'))
            else:
                full_list_point = points + points[:3]
                number_of_elements = len(full_list_point)
                knot_vector = range(-degree + 1, 0) + range(number_of_elements)
                curve = pm.curveOnSurface(surface, degree=degree, positionUV=full_list_point, periodic=periodic,
                                          name=self.name_convention.set_name_in_format(
                                              name='curveOnsurface', objectType='nurbsCurve'), k=knot_vector)
            return curve
        else:
            print 'must provide a surface as key word argument'
        return None

    def animation_base(self, animated_node):
        end_play_back = pm.playbackOptions(q=True, maxTime=True)
        start_play_back = pm.playbackOptions(q=True, minTime=True)
        positions = []
        for each_frame_index in range(int(start_play_back), int(end_play_back)):
            pm.currentTime(each_frame_index, edit=True)
            positions.append(dataValidators.as_vector_position(animated_node))
        return self.point_base(positions)

    def point_base(self, *list_of_points, **kwargs):
        super(Curve, self).point_base(*list_of_points, **kwargs)
        periodic = kwargs.pop('periodic', False)
        degree = kwargs.pop('degree', 3)
        ep = kwargs.pop('ep', False)

        list_of_points = [dataValidators.as_vector_position(each_point) for each_point in list_of_points]

        if not periodic:
            if ep:
                curve = pm.curve(degree=degree, ep=list_of_points, name='line', **kwargs)
            else:
                curve = pm.curve(degree=degree, p=list_of_points, name='line', **kwargs)
        else:
            if ep:
                full_list_point = list_of_points + list_of_points[:3]
                num_elements = len(full_list_point)
                knot_vector = range(-degree + 1, 0) + range(num_elements)
                curve = pm.curve(degree=degree, periodic=True, p=full_list_point, k=knot_vector, name='line', **kwargs)
                for ep_point, position_point in zip(curve.ep, list_of_points):
                    pm.select()
                    pm.move(ep_point, *position_point, moveXYZ=True, worldSpace=True)
            else:
                full_list_point = list_of_points + list_of_points[:3]
                num_elements = len(full_list_point)
                knot_vector = range(-degree + 1, 0) + range(num_elements)
                curve = pm.curve(degree=degree, p=full_list_point, periodic=periodic, name='line', k=knot_vector, **kwargs)
        self.name_convention.rename_name_in_format(curve, name=str(curve))
        return curve

    @staticmethod
    def fix_shape_name(object_list):
        """
        :param object_list: receives a list of an object name, and renames the shapes to match the objects name.
        :return:no return value
        """
        for each_object in object_list:
            shapes = each_object.getShapes()
            for each_shape in shapes:
                index = 0
                if each_shape.intermediateObject.get():
                    print 'found intermediate'
                else:
                    print 'found Shape'
                    if index > 0:
                        each_shape.rename('%sShape%s' % (each_object, index))
                    else:
                        each_shape.rename('%sShape' % each_object)
                    index += 1

    @staticmethod
    def turn_to_one(curveArray):
        for eachCurve in curveArray[1:]:
            shapesInCurve = pm.listRelatives(eachCurve, s=True, children=True)
            for eachShape in shapesInCurve:
                pm.parent(eachShape, curveArray[0], shape=True, add=True)
                pm.delete(eachCurve)





if __name__ == '__main__':
    selection = pm.ls('C_cuerda00_reference_grp')[0]
    nurbs_curve = Curve()
    nurbs_curve.point_base(*selection.getChildren(), ep=True)