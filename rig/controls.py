import pymel.core as pm
from RMPY import RMRigTools
import os
from RMPY.core import config
from RMPY import nameConvention
from RMPY.core import transform
from RMPY.core import validate
reload(config)

class Controls(object):
    def __init__(self, NameConv=None):
        if NameConv is None:
            self.name_conv = nameConvention.NameConvention()
        else:
            self.name_conv = NameConv
        self.rigTools = RMRigTools.RMRigTools(NameConv=self.name_conv)

    def turn_to_one(self, curveArray):
        for eachCurve in curveArray[1:]:
            shapesInCurve = pm.listRelatives(eachCurve, s=True, children=True)
            for eachShape in shapesInCurve:
                pm.parent(eachShape, curveArray[0], shape=True, add=True)
                pm.delete(eachCurve)

    def create_cube_line(self, height, length, width, centered=False,
                         offset_x=float(0.0), offset_y=float(0.0), offset_z=float(0.0), name=""):
        if centered:
            if config.axis_order[0] in 'Xx':
                offset_x = offset_x - float(height) / 2.0
            if config.axis_order[0] in 'Yy':
                offset_y = offset_y - float(length) / 2.0
            if config.axis_order[0] in 'Zz':
                offset_z = offset_z - float(width) / 2.0
        if name == "":
            defaultName = "CubeLine"
        else:
            defaultName = name
        pointArray = [
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
        curve = pm.curve(d=1, p=pointArray, name=defaultName)
        return curve

    def create_point_base(self, *points, **kwargs):
        object_type = kwargs.pop('type', 'box')
        size = kwargs.pop('size', False)
        if size:
            if object_type == 'box':
                kwargs['x_ratio'] = size
                kwargs['y_ratio'] = size
                kwargs['z_ratio'] = size
            elif object_type == 'circular':
                kwargs['radius'] = size

        if object_type == 'box':
            for each in points:
                self.create_box_ctrl(each, **kwargs)

        elif object_type == 'circular':
            for each in points:
                self.create_circular_control(each, ** kwargs)

    def create_box_ctrl(self, Obj, x_ratio=1, y_ratio=1, z_ratio=1,
                        parent_base_size=False, custom_size=0, name="", centered=False):

        Obj = validate.as_pymel_nodes(Obj)
        if name == "":
            defaultName = "BoxControl"
        else:
            defaultName = name

        Parents = pm.listRelatives(Obj, parent=True)

        if Parents and len(Parents) != 0 and parent_base_size == True:
            JntLength = RMRigTools.RMLenghtOfBone(Parents[0])
            Ctrl = self.create_cube_line(JntLength * x_ratio, JntLength * y_ratio, JntLength * z_ratio, name=defaultName,
                                    centered=centered)
        else:
            if custom_size != 0:
                JntLength = custom_size

            elif pm.objectType(Obj) == "joint":
                JntLength = RMRigTools.RMLenghtOfBone(Obj)

            else:
                JntLength = 1
            Ctrl = self.create_cube_line(JntLength * x_ratio, JntLength * y_ratio, JntLength * z_ratio, name=defaultName,
                                    centered=centered)

        if name == '' and self.name_conv.is_name_in_format(Obj):
            self.name_conv.rename_based_on_base_name(Obj, Ctrl)
        else:
            self.name_conv.rename_based_on_base_name(Obj, Ctrl, name=Ctrl)

        self.name_conv.rename_set_from_name(Ctrl, "control", "objectType")

        transform.align(Obj, Ctrl)

        ResetGroup = self.rigTools.RMCreateGroupOnObj(Ctrl)
        return ResetGroup, Ctrl

    def create_circular_control(self, Obj, **kwargs):
        radius = kwargs.pop('radius', 1)
        axis = kwargs.pop('axis', config.axis_order.upper()[0])
        name = kwargs.pop('name', 'circle')

        Obj = validate.as_pymel_nodes(Obj)
        if name == '':
            defaultName = "circularControl"
        else:
            defaultName = name
        if axis in "yY":
            Ctrl, Shape = pm.circle(normal=[0, 1, 0], radius=radius, name=defaultName)
        elif axis in "zZ":
            Ctrl, Shape = pm.circle(normal=[0, 0, 1], radius=radius, name=defaultName)
        elif axis in "xX":
            Ctrl, Shape = pm.circle(normal=[1, 0, 0], radius=radius, name=defaultName)

        if name == 'circularControl':
            if self.name_conv.is_name_in_format(Obj):
                self.name_conv.rename_based_on_base_name(Obj, Ctrl)
            else:
                self.name_conv.rename_name_in_format(Ctrl, name=name, objectType='control')
        else:
            self.name_conv.rename_name_in_format(Ctrl, name=name, objectType='control')
        transform.align(Obj, Ctrl)

        ResetGroup = self.rigTools.RMCreateGroupOnObj(Ctrl)

        return ResetGroup, Ctrl

    def file_control(self, Obj, scale=1, name='', Type="move"):
        Obj = validate.as_pymel_nodes(Obj)
        MoversTypeDic = {
            "move": {"filename": "ControlMover.mb", "object": "MoverControl"},
            "v": {"filename": "ControlV.mb", "object": "VControl"},
            "head": {"filename": "ControlHead.mb", "object": "HeadControl"},
            "circleDeform": {"filename": "ControlCircularDeform.mb", "object": "CircularDeform"}
        }
        print 'inside Iport move control'
        path = os.path.dirname(RMRigTools.__file__)
        RMPYPATH = os.path.split(path)
        FinalPath = os.path.join(RMPYPATH[0], "RMPY\AutoRig\RigShapes", MoversTypeDic[Type]["filename"])
        if os.path.isfile(FinalPath):
            pm.importFile(FinalPath, i=True, type="mayaBinary", ignoreVersion=True, mergeNamespacesOnClash=False,
                    rpr="ControlMover", pr=False)
            #pm.importFile(FinalPath, i=True, type="mayaBinary", ignoreVersion=True, mergeNamespacesOnClash=False,
            #          rpr="ControlMover", pr=False)
        else:
            print "archivo no encontrado %s , %s, %s "% (path, RMPYPATH, FinalPath)
            return None
        Ctrl = pm.ls(MoversTypeDic[Type]["object"])[0]

        if pm.objExists(Ctrl):
            if name != '':
                Ctrl = pm.rename(Ctrl, name)

            pm.setAttr(Ctrl + ".scale", scale, scale, scale)

            pm.makeIdentity(Ctrl, apply=True, t=1, r=1, s=1)

            if name != '' and self.name_conv.is_name_in_format(Obj):

                self.name_conv.rename_based_on_base_name(Obj, Ctrl)

            else:
                self.name_conv.rename_based_on_base_name(Obj, Ctrl, name=Ctrl)

            self.name_conv.rename_set_from_name(Ctrl, "control", "objectType")
            transform.align(Obj, Ctrl)

            ParentGroup = self.rigTools.RMCreateGroupOnObj(Ctrl)
            return ParentGroup, Ctrl
        else:
            print "Error importing Shape File"
            return None

def combine_shapes(curveArray):
    for eachCurve in curveArray[1:]:
        shapesInCurve = pm.listRelatives(eachCurve, s=True, children=True)
        for eachShape in shapesInCurve:
            pm.parent(eachShape, curveArray[0], shape=True, add=True)
            pm.delete(eachCurve)

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

if __name__ == '__main__':
    joint = pm.ls('C_space00_test_jnt')[0]
    locator = pm.ls('C_space_test_loc')[0]
    shapeControls = Controls()
    shapeControls.create_point_base(joint, centered=True)
