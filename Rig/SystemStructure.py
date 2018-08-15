import pymel.core as pm
from RMPY import nameConvention
reload(nameConvention)
class RigStructureModel():
    def __init__(self):
        self.kinematics = None
        self.joints = None
        self.controls = None
        self.world = None
        self.settings = None
        self.root = None

class SystemStructure():
    def __init__(self, *args):
        self._model = RigStructureModel()
        self.name_conv = nameConvention.NameConvention()
        if args:
            self.name_conv.default_names['system'] = self.name_conv.get_a_short_name(args[0])
            self.name_conv.default_names['side'] = self.name_conv.get_from_name(args[0], 'side')

    def create(self):
        kinematics_name = self.name_conv.set_name_in_format(name='kinematics')
        kinematics = pm.ls(kinematics_name)
        if kinematics:
            self._model.kinematics = kinematics[0]
        else:
            self._model.kinematics = pm.group(empty=True, name='kinematics')
            self.name_conv.rename_name_in_format(self._model.kinematics, useName=True)

        joints_name = self.name_conv.set_name_in_format(name='joints')
        joints = pm.ls(joints_name)
        if joints:
            self._model.joints = joints[0]
        else:
            self._model.joints = pm.group(empty=True, name='joints')
            self.name_conv.rename_name_in_format(self._model.joints, useName=True)

        controls_name = self.name_conv.set_name_in_format(name='controls')
        controls = pm.ls(controls_name)
        if controls:
            self._model.controls = controls[0]
        else:
            self._model.controls = pm.group(empty=True, name='controls')
            self.name_conv.rename_name_in_format(self._model.controls, useName=True)

        world_name = 'world'
        world = pm.ls(world_name)
        if world:
            self._model.world = world[0]
        else:
            self._model.world = pm.group(empty=True, name=world_name)

        system_name = self.name_conv.set_name_in_format(name='system')
        system = pm.ls(system_name)
        if controls:
            self._model.root = system[0]
        else:
            self._model.root = pm.group(empty=True, name='system')
            self.name_conv.rename_name_in_format(self._model.root, useName=True)

        settings_name = self.name_conv.set_name_in_format(name='settings')
        settings = pm.ls(system_name)
        if controls:
            self._model.settings = settings[0]
        else:
            self._model.settings = pm.spaceLocator(name='settings')
            self.name_conv.rename_name_in_format(self._model.settings, useName=True)
        pm.addAttr(self._model.settings, ln='worldScale', at='double', k=True)

        self._model.settings.worldScale.set(1)

        self._model.controls.setParent(self._model.root)
        self._model.joints.setParent(self._model.root)
        self._model.kinematics.setParent(self._model.root)
        self._model.settings.setParent(self._model.root)


    @property
    def kinematics(self):
        if not self._model.kinematics:
           self.create()
        return self._model.kinematics

    @property
    def joints(self):
        if not self._model.joints:
            self.create()
        return self._model.joints

    @property
    def controls(self):
        if not self._model.controls:
            self.create()
        return self._model.controls
    @property
    def settings(self):
        if not self._model.settings:
            self.create()
        return self._model.settings
    @property
    def world(self):
        if not self._model.world:
            self.create()
        return self._model.world

    @property
    def root(self):
        if not self._model.root:
            self.create()
        return self._model.root

if __name__ == '__main__':
    selection = pm.ls(selection=True)
    sys = SystemStructure(selection[0])
    sys.create()
