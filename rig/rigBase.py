from RMPY import nameConvention
from RMPY.rig import SystemStructure
from RMPY.creators import creators
from RMPY.core import transform
from RMPY.core import config
import pymel.core as pm
from RMPY.core import rig_core as rm


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
        self.zero_joint = None


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
        if 'rig_system' in kwargs.keys():
            self.rig_system = kwargs.pop('rig_system', SystemStructure.SystemStructure())
            self.name_convention = self.rig_system.name_convention
        else:
            self.rig_system = SystemStructure.SystemStructure()

        self.rm = rm
        self._joint_creation_kwargs = {}
        self._control_creation_kwargs = {}
        self.create = creators
        self.transform = transform
        self._model = kwargs.pop('model', BaseModel())

    @property
    def zero_joint(self):
        """
        This property creates a zero joint that will be used for static rigs.
        The joint is created automatically if it doesn't exist.
        :return:
        """
        if not self._model.zero_joint:
            pm.select(clear=True)
            reset_joint, joint_list = self.create.joint.point_base(self.rig_system.joints)
            pm.parent(reset_joint, self.rig_system.joints)
            self._model.zero_joint = joint_list[0]
            self.name_convention.rename_name_in_format(self._model.zero_joint, name='zeroJoint', objectType='sknjnt')

        return self._model.zero_joint

    @property
    def root(self):
        """
        The root of a rig is a property that stores the transform group that whenever you want to create a parent for
        the rig you can move scale, or rotate this rig and all in the rig will follow.
        You can assign the root to what ever transform you want, but in the case you have not done this the property
         will return the first value stored on the reset_controls list.
        """
        if self.attach_points['root']:
            return self.attach_points['root']
        else:
            if self.reset_controls:
                return self.reset_controls[0]
            else:
                return None

    @property
    def world_scale_matrix(self):
        """
        This attribute returns an output of a maya node that contains the matrix correspondent to the world scale value of the rig.
        Notice that it is an attribute not a node, so should be treated as this.
        """
        if self.root:
            connections_list = pm.listConnections(self.root.scale, type='decomposeMatrix',
                                                  source=True)
            if connections_list:
                compose_matrix = pm.listConnections(connections_list[0].outputScale, type='composeMatrix',
                                                    source=True)
                return compose_matrix[0].outputMatrix

            else:
                decompose_matrix = pm.createNode('decomposeMatrix', name='worldScaleDecomposeMatrix')
                compose_matrix = pm.createNode('composeMatrix', name='worldScaleMatrix')
                self.name_convention.rename_name_in_format(compose_matrix, decompose_matrix, useName=True)
                self.root.worldMatrix[0] >> decompose_matrix.inputMatrix
                decompose_matrix.outputScale >> compose_matrix.inputScale
                return compose_matrix.outputMatrix
        else:
            raise AttributeError('The current rig does not have defined a root node')


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
        """
        The tip of a rig is a property that stores a transform where any other rig should attach to.
        """
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
        Base function for rig creation, it validates the args values and turn them in to points.
        it creates two arrays one of objects, one of points, and one of rotation vectors
        """
        self.setup_name_convention_node_base(*args, **kwargs)
        assert not hasattr(super(RigBase, self), 'create_point_base')

    def create_node_base(self, *args, **kwargs):
        """
        Base function for node creation, it gets as input any kind of nodes, usually this can be transforms.
        There is no real difference with create point base, other than create point base validates the input,
        and if no nodes are provided it will create them. Node base,  shoud only be used with maya nodes and it is an
        alternative to create_point_base.
        """
        self.setup_name_convention_node_base(*args, **kwargs)
        assert not hasattr(super(RigBase, self), 'node_base')

    def create_shape_base(self, *args, **kwargs):
        self.setup_name_convention_node_base(*args, **kwargs)

    def create_curve_base(self, *args, **kwargs):
        self.setup_name_convention_node_base(*args, **kwargs)

    def setup_name_convention_node_base(self, *args, **kwargs):
        """
        This function is used to set the name convention of all the tools on the class to match a specific transform.
        args only the first arg will be used to inherit the name, system and side of the name.
        If the name is in the name convention the tokens of the name will be used, in case it is not, the name will be
        made a shortName(strip all _) and will be used as the system  name.
        Notice that there is a special system name, defined on the config, (by default is reference) which if the point
         belogs to this system, means that is meant to be used to create a rig and the name of the locator will be used
         as the system.

        """
        pop_name = kwargs.pop('name', None)
        system_name = self.name_convention.get_from_name(args[0], 'system')
        if system_name == config.default_reference_system_name:
            self.name_convention.default_names['system'] = self.name_convention.get_a_short_name(args[0])
            if pop_name:
                self.name_convention.default_names['name'] = pop_name
            # else:
            #    self.name_convention.default_names['name'] = self.name_convention.get_a_short_name(args[0])

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
        """
        Updates the name convention on all the creators, and rig_system objects
        """
        self.rig_system.name_convention = self.name_convention
        for each in self.create.creators_list:
            each.name_convention = self.name_convention
        assert not hasattr(super(RigBase, self), 'update_name_convention')

    def create_selection_base(self, **kwargs):
        selection = pm.ls(selection=True)
        self.create_point_base(selection, **kwargs)
        assert not hasattr(super(RigBase, self), 'create_selection_base')

    def set_parent(self, rig_object, **kwargs):
        """
        This is the standardize function to parent modules, This works in union with the properties root and tip.
        When you call set_parent the rig object attribute can be a
        rig(that inherits at some point from rigBase), or a transform. If it is a rig, the function will look for the
        tip on the dictionary attachments. If this has not being assigned the default value will be the first element
        of the list rig_reset_controls. So you can assign what ever point you want to be the driver of all the rig
        or let the rig find it by itself.

        :param rig_object: object or rig that you expect to be the parent of the module.
        :kwargs:
            output_joint_rig: The output joint rig is a specific rig to create a hierarchy of joints
            create_hierarchy_joints:


        :return:
        """
        kwargs['mo'] = kwargs.pop('mo', True)
        create_hierarchy_joints = kwargs.pop('create_hierarchy_joints', False)
        output_joint_rig = kwargs.pop('output_joint_rig', None)
        # self.create.constraint.define_constraints(point=False, scale=True, parent=True, orient=False)

        if RigBase in type(rig_object).__mro__:
            # self.create.constraint.constraint_type
            print('{} in constraining {} {}'.format('matrix', rig_object.tip, self.root))
            self.create.constraint.matrix_node_base(rig_object.tip, self.root, **kwargs)
            # self.create.constraint.node_base(rig_object.tip, self.root, **kwargs)
        else:
            try:
                self.create.constraint.matrix_node_base(rig_object, self.root, **kwargs)
                # self.create.constraint.node_base(rig_object, self.root, **kwargs)
            except AttributeError:
                raise AttributeError('not valid object to parent')
        assert not hasattr(super(RigBase, self), 'set_parent')

        self._create_output_points(rig_object, create_hierarchy_joints=create_hierarchy_joints,
                                   output_joint_rig=output_joint_rig)

    def _create_output_points(self, rig_object, **kwargs):
        create_hierarchy_joints = kwargs.pop('create_hierarchy_joints', False)
        output_joint_rig = kwargs.pop('output_joint_rig', None)
        if create_hierarchy_joints and output_joint_rig:
            rig_joints = []
            for index, each in enumerate(self.joints):
                new_joint = pm.joint()
                self.name_convention.rename_based_on_base_name(each, new_joint, name='main')
                self._tag_joint(new_joint)
                rig_joints.append(new_joint)
                if index == 0:
                    if RigBase in type(rig_object).__mro__:
                        if rig_object.outputs:
                            new_joint.setParent(rig_object.outputs[-1], noInvScale=True, relative=True)
                        else:
                            new_joint.setParent(output_joint_rig.outputs[-1], noInvScale=True, relative=True)
                    else:
                        new_joint.setParent(output_joint_rig.outputs[-1], noInvScale=True, relative=True)
                else:
                    new_joint.setParent(rig_joints[index - 1], noInvScale=True, relative=True)
                self.create.constraint.matrix_node_base(each, new_joint)
                self.outputs.append(new_joint)

    def _tag_joint(self, each_joint):
            self.name_convention.rename_set_from_name(each_joint, 'skinjoint', 'objectType')
            side = self.name_convention.get_from_name(each_joint, 'side')
            each_joint.side.set(['C', 'L', 'R'].index(side))
            pm.setAttr('{}.type'.format(each_joint), 18)
            each_joint.otherType.set('{}{}'.format(self.name_convention.get_from_name(each_joint, 'name'),
                                                   self.name_convention.get_from_name(each_joint, 'system')))

    def rename_as_skinned_joints(self, nub=False, create_outputs=False):
        if nub:
            rename_joints = self.joints[:-1]
        else:
            rename_joints = self.joints

        for each_joint in rename_joints:
            self.name_convention.rename_set_from_name(each_joint, 'skinjoint', 'objectType')
            side = self.name_convention.get_from_name(each_joint, 'side')
            each_joint.side.set(['C', 'L', 'R'].index(side))
            pm.setAttr('{}.type'.format(each_joint), 18)
            each_joint.otherType.set('{}{}'.format(self.name_convention.get_from_name(each_joint, 'name'),
                                                   self.name_convention.get_from_name(each_joint, 'system')))

    def custom_world_align(self, *scene_objects):
        """
        This function can be used to align any object with the world paradigm which by default is x aiming front,
        This also takes in consideration if the object is on the right side, since controls are mirrored on Z axis.
        """
        for each in scene_objects:
            scale_z = 1
            if self.name_convention.is_name_in_format(each):
                if self.name_convention.get_from_name(each, 'side') == 'R':
                    scale_z = -1
            rm.aim_vector_based(each, pm.datatypes.Vector(0.0, 0.0, 1.0),
                                pm.datatypes.Vector(0.0, 1.0, 0.0),
                                scale_z=scale_z)

    def __getattr__(self, item):
        return getattr(self._model, item)


if __name__ == '__main__':
    rig_base = RigBase()
    print (type(rig_base))
