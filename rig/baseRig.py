from RMPY import RMRigTools
from RMPY import RMRigShapeControls
from RMPY.AutoRig import RMSpaceSwitch
from RMPY import nameConvention
from RMPY.rig import systemStructure
from RMPY.rig import controls
# from RMPY.AutoRig import RigStructure
reload(systemStructure)

class BaseModel(object):
    def __init__(self, *args, **kwargs):
        self.joints = []
        self.reset_joints = []
        self.controls = []
        self.reset_controls = []


class BaseRig(object):
    def __init__(self, *args, **kwargs):
        self.rig_tools = kwargs.pop('rig_tools', RMRigTools.RMRigTools())
        self.rig_controls = kwargs.pop('rig_controls', controls.Controls())
        self.space_switch = kwargs.pop('space_switch', RMSpaceSwitch.RMSpaceSwitch())
        self.name_conv = kwargs.pop('name_conv', nameConvention.NameConvention())
        self.rig_system = kwargs.pop('rig_system', systemStructure.SystemStructure())

    def create_point_base(self, *args, **kwargs):
        self.setup_name_conv_node_base(args[0])

    def create_shape_base(self, *args, **kwargs):
        self.setup_name_conv_node_base(args[0])

    def setup_name_conv_node_base(self, *args):
        self.name_conv.default_names['system'] = self.name_conv.get_a_short_name(args[0])
        self.name_conv.default_names['side'] = self.name_conv.get_from_name(args[0], 'side')
        self.rig_tools.name_conv = self.name_conv
        self.rig_controls.name_conv = self.name_conv
        self.rig_system.name_conv = self.name_conv
        self.space_switch.name_conv = self.name_conv







