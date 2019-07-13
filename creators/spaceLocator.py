import pymel.core as pm
from RMPY import RMRigTools
from RMPY.creators import creatorsBase
from RMPY.core import dataValidators


class SpaceLocator(creatorsBase.CreatorsBase):
    def __init__(self, *args):
        super(SpaceLocator, self).__init__(*args)
        self.name_convention.default_names['system'] = 'reference'

    def create_vertex_base(self, *vertex_list):
        position = []
        for each in vertex_list:
            if each.__class__ == pm.general.MeshVertex:
                for each_vtx in each:
                    position.append(each_vtx.getPosition(space='world'))
            else:
                print each.__class__
        new_space_locator = pm.spaceLocator()
        self.name_convention.rename_name_in_format(new_space_locator)
        new_space_locator.translate.set(RMRigTools.average(*position))

    def point_base(self, *point_list):
        for each in point_list:
            position = dataValidators.as_vector(each)
            new_locator = pm.spaceLocator()
            self.name_convention.rename_name_in_format(new_locator)
            new_locator.translate.set([position[0], position[1], position[2]])


import pymel.core as pm
from RMPY import RMRigTools
from RMPY.creators import creatorsBase
from RMPY.creators import motionPath
from RMPY.core import dataValidators
from RMPY.core import config
from RMPY.core import transform
import maya.api.OpenMaya as om
import math

reload(motionPath)
reload(creatorsBase)
reload(transform)


class Creator(creatorsBase.Creator):
    def __init__(self, *args, **kwargs):
        super(Creator, self).__init__(*args, **kwargs)

    def node_base(self, *transforms_list, **kwargs):
        transforms_list = dataValidators.as_pymel_nodes(transforms_list)
        rotation = kwargs.pop('rotation', True)
        name = kwargs.pop('name', None)
        locator_list = []
        for each in transforms_list:
            if each.__class__ == pm.general.MeshVertex:
                for each_vertex in each:
                    locator = pm.spaceLocator()
                    vector = RMRigTools.vector_position(each_vertex)
                    locator.translate.set(vector)
            else:
                locator = pm.spaceLocator()
                vector = RMRigTools.vector_position(each)
                locator.translate.set(vector)
                if rotation:
                    transform.align(each, locator, translate=False)
            locator_list.append(locator)
            if name:
                self.name_conv.rename_name_in_format(locator, name=name)
            else:
                self.name_conv.rename_name_in_format(locator)
        return locator_list

    def aim_base(self, *points, **kwargs):
        name = kwargs.pop('name', None)
        locator = pm.spaceLocator()
        transform.aim_point_based(locator, *points, **kwargs)
        # RMRigTools.point_based_aim(locator, *points, **kwargs)
        if name:
            self.name_conv.rename_name_in_format(locator, name=name)
        else:
            self.name_conv.rename_name_in_format(locator)
        return locator

    def point_base(self, *points, **kwargs):
        name = kwargs.pop('name', None)
        points = dataValidators.as_pymel_nodes(points)
        points_list = []
        for each in points:
            if each.__class__ == pm.general.MeshVertex:
                for each_vertex in each:
                    vector = RMRigTools.vector_position(each_vertex)
                    points_list.append([vector[0], vector[1], vector[2]])
            else:
                vector = RMRigTools.vector_position(each)
                points_list.append([vector[0], vector[1], vector[2]])
        new_locator = pm.spaceLocator()
        new_locator.translate.set(RMRigTools.mid_point(*points_list))

        if name:
            self.name_conv.rename_name_in_format(new_locator, name=name)
        else:
            self.name_conv.rename_name_in_format(new_locator)
        return new_locator

    def in_between_points(self, obj01, obj02, number_of_points, name="inBetween", align="FirstObj"):
        """Valid Values in align are FirstObj, SecondObject, and World"""
        obj01 = dataValidators.as_pymel_nodes(obj01)
        obj02 = dataValidators.as_pymel_nodes(obj02)
        locator_list = []
        position01, position02 = pm.xform(obj01, q=True, ws=True, rp=True), pm.xform(obj02, q=True, ws=True,
                                                                                     rp=True)
        vector01, vector02 = om.MVector(position01), om.MVector(position02)
        result_vector = vector02 - vector01
        distance = om.MVector(result_vector).length()
        delta_vector = (distance / (number_of_points + 1)) * result_vector.normal()
        for index in range(0, number_of_points):
            new_locator = pm.spaceLocator(name=name)
            self.name_conv.rename_name_in_format(str(new_locator), name=name)
            locator_list.append(new_locator)
            obj_position = vector01 + delta_vector * (index + 1)
            pm.xform(locator_list[index], ws=True, t=obj_position)
            if align == "FirstObj":
                transform.align(obj01, locator_list[index], translate=False)
            elif align == "SecondObject":
                transform.align(obj02, locator_list[index], translate=False)
        return locator_list

    def pole_vector(self, *node_list):
        """
        :param node_list: list of 3 nodes where the pole vector will be calculated.
        :return: a space locator that it is located where the pole vector should be.
        """
        if len(node_list) == 3:
            VP1 = om.MVector(pm.xform(node_list[0], a=True, ws=True, q=True, rp=True))
            VP2 = om.MVector(pm.xform(node_list[1], a=True, ws=True, q=True, rp=True))
            VP3 = om.MVector(pm.xform(node_list[2], a=True, ws=True, q=True, rp=True))
            PoleVector = pm.spaceLocator(name="poleVector")
            PoleVector = self.name_conv.rename_based_on_base_name(node_list[1], PoleVector, name=PoleVector)
            pm.xform(PoleVector, ws=True, t=self.pole_vector_point(VP1, VP2, VP3))
            return PoleVector
        else:
            raise AttributeError('3 attributes needed for creating a pole vector')

    def pole_vector_point(self, vp1, vp2, vp3):
        V1 = vp2 - vp1
        V2 = vp3 - vp2
        Angle = math.radians((math.degrees(V1.angle(V2)) + 180) / 2 - 90)

        if transform.is_close(Angle, 0.0, rel_tol=1e-05, abs_tol=1e-05):
            V2 = om.MVector([0, -1, 0])
            Angle = math.radians((math.degrees(V1.angle(V2)) + 180) / 2 - 90)
            if transform.is_close(Angle, 0.0, rel_tol=1e-05, abs_tol=1e-05):
                V2 = om.MVector([-1, 0, 0])
                Angle = math.radians((math.degrees(V1.angle(V2)) + 180) / 2 - 90)

        zAxis = (V1 ^ V2).normal()
        yAxis = (V2 ^ zAxis).normal()
        xAxis = V2.normal()

        Y1 = math.cos(Angle)
        X1 = -math.sin(Angle)
        Vy = yAxis * Y1
        Vx = xAxis * X1

        Length = (V1.length() + V2.length()) / 2
        result = ((Vy + Vx) * Length) + vp2
        return result

    def curve_base(self, *curves, **kwargs):
        motion_path = motionPath.Creator()

        number_of_points = kwargs.pop('number_of_points', 5)
        followAxis = kwargs.pop('followAxis', 'Y')
        upAxis = kwargs.pop('upAxis', 'X')

        main_list_of_points = []
        for each_curve in curves:
            point_list = []
            for each_point in range(number_of_points):
                point_list.append(self.point_base(each_curve))
            print point_list
            motion_path_node = motion_path.node_base(*point_list, curve=each_curve,
                                                     followAxis=followAxis, upAxis=upAxis, **kwargs)
            pm.delete(motion_path_node)
            main_list_of_points.append(point_list)
        return main_list_of_points


if __name__ == '__main__':
    # selection = pm.ls('C_line_arm_SHP')
    root = pm.ls(selection=True)
    space_locator = Creator()
    space_locator.in_between_points(root[0], root[1], 10)
    # selection = pm.ls(selection=True)
    # space_locator.curve_base(*selection, name='arm')

    # space_locator.point_based(*selection)
    # space_locator.node_based(*selection)

