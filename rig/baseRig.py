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
    """Base rig is the base class to be used on any rig. it contains an instance of the main classes that 
    will be used when creating a rig. 
    The members that contains the Base rig are the following.
    name_conv, an instance of the nameConvention class used to rename all elements on the rig.
    rig_system a class that contains the maya hierarchical structure used as base for all the systems
    rig_creators the functions used to create all kind of nodes on maya trough an interface that it is 
    easy to use and standard. 
    
    """
    def __init__(self, *args, **kwargs):
        """
        initializes all the variables on the rig
        by default looks for inherited properties, like name_convention, or system structure, that can be 
        passed as kwargs.
        :name_conv:
        :rig_system: 
        """
        self.rig_tools = kwargs.pop('rig_tools', RMRigTools.RMRigTools())
        self.rig_controls = kwargs.pop('rig_controls', controls.Controls())
        self.space_switch = kwargs.pop('space_switch', RMSpaceSwitch.RMSpaceSwitch())
        self.name_conv = kwargs.pop('name_conv', nameConvention.NameConvention())
        self.rig_system = kwargs.pop('rig_system', systemStructure.SystemStructure())

    def create_point_base(self, *args, **kwargs):
        """
        base function for point creation, it validates the args values and turnthem in to points.
        it creates two arrays one of objects, one of points, and one of rotation vectors
        """
        self.setup_name_conv_node_base(args[0])
    def node_base(self, *args, **kwargs):
        """
        base function for node creation, it gets as input any kind of nodes and returns them as a 
        """
    def create_shape_base(self, *args, **kwargs):
    
        self.setup_name_conv_node_base(args[0])

    def setup_name_conv_node_base(self, *args):
        self.name_conv.default_names['system'] = self.name_conv.get_a_short_name(args[0])
        self.name_conv.default_names['side'] = self.name_conv.get_from_name(args[0], 'side')
        self.rig_tools.name_conv = self.name_conv
        self.rig_controls.name_conv = self.name_conv
        self.rig_system.name_conv = self.name_conv
        self.space_switch.name_conv = self.name_conv







