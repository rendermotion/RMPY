import pymel.core as pm
from RMPY import RMRigTools
import os
from RMPY.core import config
from RMPY.core import transform
from RMPY.core import dataValidators
from pathlib import Path
from RMPY.creators import creatorsBase


class Controls(creatorsBase.CreatorsBase):
    def __init__(self, *args, **kwargs):
        super(Controls, self).__init__(*args, **kwargs)
        self.rigTools = RMRigTools.RMRigTools(NameConv=self.name_convention)
        self.file_types = ["move", 'v', 'head', 'circleDeform', 'b']

    def point_base(self, *points, **kwargs):
        super(Controls, self).point_base(*points, **kwargs)
        object_type = kwargs.pop('type', 'box')
        size = kwargs.pop('size', False)
        controls_list = []
        if size:
            if object_type == 'box':
                kwargs['x_ratio'] = size
                kwargs['y_ratio'] = size
                kwargs['z_ratio'] = size
            elif object_type == 'circular':
                kwargs['radius'] = size

        if object_type == 'box':
            for each in points:
                controls_list.append(self.create_box_ctrl(each, **kwargs))

        elif object_type == 'circular':
            for each in points:
                controls_list.append(self.create_circular_control(each, ** kwargs))
        elif object_type in self.file_types:
            kwargs['control_type'] = object_type
            if not size:
                kwargs['scale'] = 1.0
            else:
                kwargs['scale'] = size

            for each in points:
                controls_list.append(self.file_control(each, ** kwargs))

        if len(points) == 1:
            return controls_list[0]

        return controls_list

    def scale_controls(self, control):
        if self.name_convention.is_name_in_format(control):
            if self.name_convention.get_from_name(control, 'side') == 'R':
                if 'x' in config.mirror_controls_axis.lower():
                    control.scaleX.set(-1)
                if 'y' in config.mirror_controls_axis.lower():
                    control.scaleY.set(-1)
                if 'z' in config.mirror_controls_axis.lower():
                    control.scaleZ.set(-1)

    @staticmethod
    def create_cube_line(height, length, width, centered=False,
                         offset_x=float(0.0), offset_y=float(0.0), offset_z=float(0.0), name=""):
        if centered:
            if config.axis_order[0] in 'Xx':
                offset_x = offset_x - float(height) / 2.0
            if config.axis_order[0] in 'Yy':
                offset_y = offset_y - float(length) / 2.0
            if config.axis_order[0] in 'Zz':
                offset_z = offset_z - float(width) / 2.0
        if name == "":
            default_name = "CubeLine"
        else:
            default_name = name
        point_array = [
            [0 + offset_x, -length / 2.0 + offset_y, width / 2.0 + offset_z],
            [0 + offset_x, -length / 2.0 + offset_y, -width / 2.0 + offset_z],
            [height + offset_x, -length / 2.0 + offset_y, -width / 2.0 + offset_z],
            [height + offset_x, length / 2.0 + offset_y, -width / 2.0 + offset_z],
            [height + offset_x, length / 2.0 + offset_y, width / 2.0 + offset_z],
            [0 + offset_x, length / 2.0 + offset_y, width / 2.0 + offset_z],
            [0 + offset_x, length / 2.0 + offset_y, -width / 2.0 + offset_z],
            [height + offset_x, length / 2.0 + offset_y, -width / 2.0 + offset_z],
            [height + offset_x, -length / 2.0 + offset_y, -width / 2.0 + offset_z],
            [height + offset_x, -length / 2.0 + offset_y, width / 2.0 + offset_z],
            [height + offset_x, length / 2.0 + offset_y, width / 2.0 + offset_z],
            [height + offset_x, -length / 2.0 + offset_y, width / 2.0 + offset_z],
            [0 + offset_x, -length / 2.0 + offset_y, width / 2.0 + offset_z],
            [0 + offset_x, length / 2.0 + offset_y, width / 2.0 + offset_z],
            [0 + offset_x, length / 2.0 + offset_y, -width / 2.0 + offset_z],
            [0 + offset_x, -length / 2.0 + offset_y, -width / 2.0 + offset_z]
        ]
        curve = pm.curve(d=1, p=point_array, name=default_name)
        return curve

    def create_box_ctrl(self, reference_point, **kwargs):

        x_ratio = kwargs.pop('x_ratio', 1)
        y_ratio = kwargs.pop('y_ratio', 1)
        z_ratio = kwargs.pop('z_ratio', 1)
        parent_base_size = kwargs.pop('parent_base_size', False)
        custom_size = kwargs.pop('custom_size', 0)
        name = kwargs.pop('name', '')
        centered = kwargs.pop('centered', False)

        reference_point = dataValidators.as_pymel_nodes(reference_point)[0]
        if name == "":
            default_name = "BoxControl"
        else:
            default_name = name

        Parents = pm.listRelatives(reference_point, parent=True)

        if Parents and len(Parents) != 0 and parent_base_size == True:
            joint_length = transform.joint_length(Parents[0])
            control = self.create_cube_line(joint_length * x_ratio, joint_length * y_ratio, joint_length * z_ratio,
                                            name=default_name,
                                            centered=centered)
        else:
            if custom_size != 0:
                joint_length = custom_size

            elif pm.objectType(reference_point) == "joint":
                joint_length = transform.joint_length(reference_point)

            else:
                joint_length = 1
            control = self.create_cube_line(joint_length * x_ratio, joint_length * y_ratio, joint_length * z_ratio,
                                            name=default_name,
                                            centered=centered)

        # if name == '' and self.name_convention.is_name_in_format(Obj):
        #    self.name_convention.rename_based_on_base_name(Obj, control)
        # else:
        #    self.name_convention.rename_based_on_base_name(Obj, control, name=control)

        self.name_convention.rename_name_in_format(control, objectType='control')
        # self.name_convention.rename_set_from_name(control, "control", "objectType")

        transform.align(reference_point, control)

        reset_group = self.rigTools.RMCreateGroupOnObj(control)
        self.scale_controls(reset_group)
        return reset_group, control

    def create_circular_control(self, reference_point, **kwargs):
        radius = kwargs.pop('radius', 1)
        axis = kwargs.pop('axis', config.axis_order.upper()[0])
        name = kwargs.pop('name', 'circle')

        reference_point = dataValidators.as_pymel_nodes(reference_point)[0]
        if name == '':
            default_name = "circularControl"
        else:
            default_name = name
        if axis in "yY":
            control, shape = pm.circle(normal=[0, 1, 0], radius=radius, name=default_name)
        elif axis in "zZ":
            control, shape = pm.circle(normal=[0, 0, 1], radius=radius, name=default_name)
        elif axis in "xX":
            control, shape = pm.circle(normal=[1, 0, 0], radius=radius, name=default_name)

        if name == 'circularControl':
            if self.name_convention.is_name_in_format(reference_point):
                self.name_convention.rename_based_on_base_name(reference_point, control)
            else:
                self.name_convention.rename_name_in_format(control, name=name, objectType='control')
        else:
            self.name_convention.rename_name_in_format(control, name=name, objectType='control')
        transform.align(reference_point, control)

        reset_group = self.rigTools.RMCreateGroupOnObj(control)
        self.scale_controls(reset_group)
        return reset_group, control

    def file_control(self, scene_object, **kwargs):
        scale = kwargs.pop('scale', 1.0)
        name = kwargs.pop('name', None)
        control_type = kwargs.pop('control_type', 'Move')

        scene_object = dataValidators.as_pymel_nodes(scene_object)[0]
        MoversTypeDic = {
            "move": {"filename": "ControlMover.mb", "object": "MoverControl"},
            "v": {"filename": "ControlV.mb", "object": "VControl"},
            "head": {"filename": "ControlHead.mb", "object": "HeadControl"},
            "circleDeform": {"filename": "ControlCircularDeform.mb", "object": "CircularDeform"},
            'b':{"filename": "ControlB.mb", "object": "BControl"}
        }
        path = Path(RMRigTools.__file__)
        RMPYPATH = os.path.split(path)
        FinalPath = Path(Path(RMPYPATH[0]), Path("AutoRig/RigShapes"), MoversTypeDic[control_type]["filename"])
        if os.path.isfile(FinalPath):
            pm.importFile(FinalPath, i=True, type="mayaBinary", ignoreVersion=True, mergeNamespacesOnClash=False,
                                    rpr="ControlMover", pr=False)
        else:
            print ("file not found %s , %s, %s "% (path, RMPYPATH, FinalPath))
            return None

        control = pm.ls(MoversTypeDic[control_type]["object"])[0]

        if pm.objExists(control):
            if name:
                control = pm.rename(control, name)

            pm.setAttr(control + ".scale", scale, scale, scale)

            pm.makeIdentity(control, apply=True, t=1, r=1, s=1)

            self.name_convention.rename_name_in_format(control, objectType='control')

            pm.matchTransform(control, scene_object)

            reset_group = self.rigTools.RMCreateGroupOnObj(control)
            self.scale_controls(reset_group)
            return reset_group, control
        else:
            print ("Error importing Shape File")
            return None


def combine_shapes(curveArray):
    for eachCurve in curveArray[1:]:
        shapes_in_curve = pm.listRelatives(eachCurve, s=True, children=True)
        for eachShape in shapes_in_curve:
            pm.parent(eachShape, curveArray[0], shape=True, add=True)
            pm.delete(eachCurve)


if __name__ == '__main__':
    joint = pm.ls('C_hello00_reference_grp')[0]
    shapeControls = Controls()
    shapeControls.point_base(joint)
    # shapeControls.file_control(joint, control_type='head')
