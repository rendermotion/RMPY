from RMPY import nameConvention
from RMPY.rig import systemStructure
from RMPY.creators import creators
from RMPY.core import config
import pymel.core as pm
from RMPY.core import main as rm


class BaseModel(object):
    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__()
        self.joints = []
        self.reset_joints = []
        self.controls = []
        self.reset_controls = []
        self.inputs = []
        self.outputs = []
        self.attach_points = dict(root=None, tip=None)
        self.creation_points = {'points'}


class RigBase(object):
    """
    Base rig is the base class to be used on any rig. it contains an instance of the main classes that
    will be used when creating a rig. 
    The members that contains the Base rig are the following.
    name_convention, an instance of the nameConvention class used to rename all elements on the rig.
    rig_system a class that contains the maya hierarchical structure used as base for all the systems
    rig_creators the functions used to create all kind of nodes on maya trough an interface that it is 
    easy to use and standard. 
    """

    def __init__(self, *args, **kwargs):
        """
        initializes all the variables on the rig
        by default looks for inherited properties, like name_conventionention, or system structure, that can be
        passed as kwargs.
        :name_convention:
        :rig_system: 
        """
        super(RigBase, self).__init__()
        self.name_convention = kwargs.pop('name_convention', nameConvention.NameConvention())
        self.rm = rm
        self.rig_system = kwargs.pop('rig_system', systemStructure.SystemStructure())
        self._joint_creation_kwargs = {}
        self._control_creation_kwargs = {}
        self.create = creators
        self._model = kwargs.pop('model', BaseModel())

    @property
    def root(self):
        if self.attach_points['root']:
            return self.attach_points['root']
        else:
            return self.reset_controls[0]

    @root.setter
    def root(self, value):
        self.attach_points['root'] = value

    @property
    def tip(self):
        if self.attach_points['tip']:
            return self.attach_points['tip']
        else:
            return self.joints[-1]

    @tip.setter
    def tip(self, value):
        self.attach_points['tip'] = value

    @property
    def joints(self):
        return self._model.joints

    @joints.setter
    def joints(self, value):
        self._model.joints = value

    @property
    def reset_joints(self):
        return self._model.reset_joints

    @reset_joints.setter
    def reset_joints(self, value):
        self._model.reset_joints = value

    @property
    def controls(self):
        return self._model.controls

    @controls.setter
    def controls(self, value):
        self._model.controls = value

    @property
    def reset_controls(self):
        return self._model.reset_controls

    @reset_controls.setter
    def reset_controls(self, value):
        self._model.reset_controls = value

    @property
    def inputs(self):
        return self._model.inputs

    @property
    def outputs(self):
        return self._model.outputs

    @property
    def attach_points(self):
        return self._model.attach_points

    def create_point_base(self, *args, **kwargs):
        """
        base function for point creation, it validates the args values and turn them in to points.
        it creates two arrays one of objects, one of points, and one of rotation vectors
        """
        self.setup_name_convention_node_base(*args, **kwargs)
        assert not hasattr(super(RigBase, self), 'create_point_base')

    def create_node_base(self, *args, **kwargs):
        """
        base function for node creation, it gets as input any kind of nodes and returns them as a 
        """
        self.setup_name_convention_node_base(*args, **kwargs)
        assert not hasattr(super(RigBase, self), 'node_base')

    def create_shape_base(self, *args, **kwargs):
        self.setup_name_convention_node_base(*args, **kwargs)

    def create_curve_base(self, *args, **kwargs):
        self.setup_name_convention_node_base(*args, **kwargs)

    def setup_name_convention_node_base(self, *args, **kwargs):
        pop_name = kwargs.pop('name', None)
        system_name = self.name_convention.get_from_name(args[0], 'system')
        if system_name == config.default_reference_system_name:
            if pop_name:
                self.name_convention.default_names['name'] = pop_name
            # else:
            #    self.name_convention.default_names['name'] = self.name_convention.get_a_short_name(args[0])
            self.name_convention.default_names['system'] = self.name_convention.get_a_short_name(args[0])
        else:
            if pop_name:
                self.name_convention.default_names['name'] = pop_name
            else:
                self.name_convention.default_names['name'] = self.name_convention.get_a_short_name(args[0])
            self.name_convention.default_names['system'] = self.name_convention.get_from_name(args[0], 'system')

        self.name_convention.default_names['side'] = self.name_convention.get_from_name(args[0], 'side')
        self.update_name_convention()
        assert not hasattr(super(RigBase, self), 'setup_name_convention_node_base')

    @property
    def joint_creation_kwargs(self):
        return self._joint_creation_kwargs

    @joint_creation_kwargs.setter
    def joint_creation_kwargs(self, kwargs_dict):
        self._joint_creation_kwargs = {}
        orient_type = kwargs_dict.pop('orient_type', None)
        if orient_type:
            self._joint_creation_kwargs['orient_type'] = orient_type

        joint_type = kwargs_dict.pop('joint_type', None)
        if joint_type:
            self._joint_creation_kwargs['joint_type'] = joint_type

    @property
    def control_creation_kwargs(self):
        return self._control_creation_kwargs

    @control_creation_kwargs.setter
    def control_creation_kwargs(self, kwargs_dict):
        self._control_creation_kwargs = {}
        size = kwargs_dict.pop('size', None)
        if size:
            self._control_creation_kwargs['size'] = size

        control_type = kwargs_dict.pop('control_type', None)

        if control_type:
            self._control_creation_kwargs['type'] = control_type

    def update_name_convention(self):
        self.rig_system.name_convention = self.name_convention
        for each in self.create.creators_list:
            each.name_convention = self.name_convention
        assert not hasattr(super(RigBase, self), 'update_name_convention')

    def create_selection_base(self, **kwargs):
        selection = pm.ls(selection=True)
        self.create_point_base(selection, **kwargs)
        assert not hasattr(super(RigBase, self), 'create_selection_base')

    def set_parent(self, rig_object):
        """
        This is the default function to parent modules, when you set parent an object it will look for the
        root on the dictionary attachments. If this has not being asigned the default value will be the first elementq
        of the list rig_reset_controls. So you can asign what ever point you want to be the driver of all the rig
        or let the rig find it by itself.
        :param rig_object: object or rig that you expect to be the parent of the module.
        :return:
        """

        if RigBase in type(rig_object).__mro__:
            self.create.constraint.node_base(rig_object.tip, self.root, mo=True)
        else:
            try:
                self.create.constraint.node_base(rig_object, self.root, mo=True)

            except AttributeError():
                raise AttributeError('not valid object to parent')
        assert not hasattr(super(RigBase, self), 'set_parent')

    def rename_as_skinned_joints(self, nub=True):
        if nub:
            rename_joints = self.joints[:-1]
        else:
            rename_joints = self.joints
        for each_joint in rename_joints:
            self.name_convention.rename_set_from_name(each_joint, 'skinjoint', 'objectType')

    def custom_world_align(self, *scene_objects):
        for each in scene_objects:
            scale_z = 1
            if self.name_convention.is_name_in_format(each):
                if self.name_convention.get_from_name(each, 'side') == 'R':
                    scale_z = -1
            rm.aim_vector_based(each, pm.datatypes.Vector(0.0, 0.0, 1.0),
                                pm.datatypes.Vector(0.0, 1.0, 0.0),
                                scale_z=scale_z)


if __name__ == '__main__':
    rig_base = RigBase()
    print type(rig_base)
