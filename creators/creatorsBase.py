from RMPY import nameConvention
from RMPY.core import config


class CreatorBase(object):
    def __init__(self, *args, **kwargs):
        self.name_conv = kwargs.pop('name_conv', nameConvention.NameConvention())

    def point_base(self, *args, **kwargs):
        self.setup_name_conv_node_base(args[0], **kwargs)

    def shape_base(self, *args, **kwargs):
        self.setup_name_conv_node_base(args[0], **kwargs)

    def setup_name_conv_node_base(self, *args, **kwargs):
        if kwargs.pop('name') == config.default_reference_system_name:
            self.name_conv.default_names['system'] = self.name_conv.get_a_short_name(args[0])
        else:
            self.name_conv.default_names['name'] = self.name_conv.get_a_short_name(args[0])
            self.name_conv.default_names['system'] = self.get_from_name(args[0], 'system')

        self.name_conv.default_names['side'] = self.name_conv.get_from_name(args[0], 'side')

print 'done'