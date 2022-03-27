from RMPY import nameConvention
from RMPY.core import config


class CreatorsBase(object):
    def __init__(self, *args, **kwargs):
        self.name_convention = kwargs.pop('name_convention', nameConvention.NameConvention())

    def point_base(self, *args, **kwargs):
        self.setup_name_convention_node_base(args[0], **kwargs)

    def node_base(self, *args, **kwargs):
        self.setup_name_convention_node_base(args[0], **kwargs)

    def curve_base(self, *args, **kwargs):
        self.setup_name_convention_node_base(args[0], **kwargs)

    def setup_name_convention_node_base(self, *args, **kwargs):
        pop_name = kwargs.pop('name', None)
        if args[0].__class__ != list:
            system_name = self.name_convention.get_from_name(args[0], 'system')
            if system_name == config.default_reference_system_name:
                if pop_name:
                    self.name_convention.default_names['name'] = pop_name
                self.name_convention.default_names['system'] = self.name_convention.get_a_short_name(args[0])
            else:
                if pop_name:
                    self.name_convention.default_names['name'] = pop_name
                else:
                    self.name_convention.default_names['name'] = self.name_convention.get_a_short_name(args[0])
                self.name_convention.default_names['system'] = self.name_convention.get_from_name(args[0], 'system')

            self.name_convention.default_names['side'] = self.name_convention.get_from_name(args[0], 'side')
        else:
            if pop_name:
                self.name_convention.default_names['name'] = pop_name
            print 'a list was provided {}'.format(args[0])

    def _dictionary(self):
        result_dict = dict(type=str(self.__class__.__name__),
                           data=self._representation())
        return result_dict

    def _representation(self):
        return 'no _representation defined for function'



