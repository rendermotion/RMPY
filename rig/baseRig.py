from RMPY import nameConvention
from RMPY.rig import systemStructure
from RMPY.creators import creators
from RMPY.core import config
import pymel.core as pm
reload(systemStructure)


class BaseModel(object):
    def __init__(self, *args, **kwargs):
        self.joints = []
        self.reset_joints = []
        self.controls = []
        self.reset_controls = []
        self.inputs = []
        self.outputs = []
        self.attach_points = dict(root=None, tip=None)


class BaseRig(object):
    def __init__(self, *args, **kwargs):
        self.name_convention = kwargs.pop('name_convention', nameConvention.NameConvention())
        self.rig_system = kwargs.pop('rig_system', systemStructure.SystemStructure())
        self.creators = creators
        self.model = BaseModel()

    @property
    def joints(self):
        return self.model.joints

    @property
    def reset_joints(self):
        return self.model.reset_joints

    @property
    def controls(self):
        return self.model.controls

    @property
    def reset_controls(self):
        return self.model.reset_controls

    @property
    def inputs(self):
        return self.model.inputs

    @property
    def outputs(self):
        return self.model.outputs

    @property
    def attach_points(self):
        return self.model.attach_points

    def create_point_base(self, *args, **kwargs):
        self.setup_name_convention_node_base(args[0])

    def create_shape_base(self, *args, **kwargs):
        self.setup_name_convention_node_base(args[0], **kwargs)

    def setup_name_convention_node_base(self, *args, **kwargs):
        pop_name = kwargs.pop('name')
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

    def update_name_convention(self):
        self.rig_system.name_convention = self.name_convention
        for each in self.creators.creators_list:
            each.name_convention = self.name_convention

    def create_selection_base(self, **kwargs):
        selection = pm.ls(selection=True)
        self.create_point_base(selection, **kwargs)





