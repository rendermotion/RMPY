import pymel.core as pm
from RMPY.rig import rigBase
from RMPY.core import config


class RigOutput(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(RigOutput, self).__init__(*args, **kwargs)
        self.name_convention.default_names['system'] = 'output'
        self.name_convention.default_names['name'] = 'main'
        self.update_name_convention()
        self.outputs.append(self.rig_system.joints)


if __name__ == '__main__':
    pass