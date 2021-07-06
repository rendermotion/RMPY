from RMPY.rig import rigBase
import pymel.core as pm


class RigObjectsOnCurveModel(rigBase.BaseModel):
    def __init__(self):
        super(RigObjectsOnCurveModel, self).__init__()
        self.curve = None
        self.motion_path_list = []
        self.up_vector = None
        self.up_vector_array = []


class RigObjectsOnCurve(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(RigObjectsOnCurve, self).__init__(*args, **kwargs)
        self._model = RigObjectsOnCurveModel()
        if args:
            self.create_curve_base(*args, **kwargs)

    @property
    def curve(self):
        return self._model.curve

    @property
    def motion_path_list(self):
        return self._model.motion_path_list

    @property
    def up_vector(self):
        return self._model.up_vector

    @property
    def up_vector_array(self):
        return self._model.up_vector_array

    def create_curve_base(self, *args, **kwargs):
        self._model.curve = args[0]
        """
        creates a series of objects and then attaches them to a motion path using the Nodes on curve function,
        the objects it creates can be from joints, groups, or locators this is defined in objectType keyword Arg.
        number_of_nodes(int): the number of joints that will be created
        curve(nurbsCurve):the curve where the new objects will be attached.

        up_vector_type(string): the type of up vector it will use, valid values are "object"(New object will be created),
                     "list" an up_vector_list same length that Joint number should be provided, "world"
        object_type(string): the type of object that will create  valid Values are joint, group,
                    if anything else si written, will assume spaceLocator
        up_vector_array(list): The list of locators that will be used for each new created object
                       should be used in conjunction with UpVectorType : array
        """
        up_vector_object = kwargs.pop('up_vector_object', None)
        up_vector_type = kwargs.pop('up_vector_type', 'world')
        number_of_nodes = kwargs.pop('number_of_nodes', 10)
        object_type = kwargs.pop('object_type', 'spaceLocator')
        up_vector_array = kwargs.pop('up_vector_array', None)
        self._model.up_vector_array = up_vector_array

        if up_vector_type == "object":
            if not up_vector_object:
                self._model.up_vector = pm.group(empty=True, name='upVector')
                self.name_convention.rename_name_in_format(self.up_vector, useName=True)
            else:
                self._model._up_vector = up_vector_object

        for count in range(0, number_of_nodes):
            pm.select(cl=True)
            if object_type == 'joint':
                reset_joint, new_joints_list = self.create.joint.point_base(self.curve)
                new_joint = new_joints_list[0]
                self.outputs.append(reset_joint)
                self.joints.append(new_joint)
                reset_joint.setParent(self.rig_system.joints)

            elif object_type == 'group':
                new_joint = self.create.group.point_base(self.curve, type='world')
                new_joint.setParent(self.rig_system.kinematics)
                self.outputs.append(new_joint)
            else:
                new_joint = self.create.space_locator.point_base(self.curve)
                new_joint.setParent(self.rig_system.kinematics)
                self.outputs.append(new_joint)
            self.name_convention.rename_name_in_format(new_joint, useName=True)

            self.rig_system.settings.worldScale >> new_joint.scaleX
            self.rig_system.settings.worldScale >> new_joint.scaleY
            self.rig_system.settings.worldScale >> new_joint.scaleZ

        self._model._motion_paths = self.create.motion_path.node_base(*self.outputs, curve=self.curve,
                                                                      UpVectorType=up_vector_type,
                                                                      upVectorObject=self.up_vector,
                                                                      UpVectorArray=up_vector_array)


if __name__ == '__main__':
    aim_vector = RigObjectsOnCurve('C_mainCurve00_spine_shp', up_vector_type='world')
    up_vector = RigObjectsOnCurve('C_mainCurve01_spine_shp', up_vector_type='array', up_vector_array=aim_vector.outputs)



