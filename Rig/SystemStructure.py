import pymel.core as pm
from RMPY import nameConvention


class RigStructureModel(object):
    """
        this class represents the system structure, by default the system structure of any rig system contains
        the following groups that can help you organize your rig.
        the settings group, its the group to control your rig system, it has a scale value that should control your rig.
        kinematics group, any node that performs an operation in the rig would be here.
        joints group,  any joint on the rig would be in this group.
        controls group,  all controls of the rig would be in this group
        display, the display group is intended to be any object that is on the rig that should be visible, but it should
        not be accessible to the animator, an example would be a curve showing the pole vector of an IK.

        By default the display of the kinematics and the joints groups are linked to the visibility of the settings
        group. To simplify the hiding of what the final user of the rig should or should not have accessible.
    """
    def __init__(self):
        self.kinematics = None
        self.joints = None
        self.controls = None
        self.display = None
        self.settings = None
        self.root = None


class SystemStructure(object):
    """
    This class is the interface to access the structure model, its an easy way to access it, and invoke his child nodes.
    It creates all the nodes as needed, you just need to access it in order to be created.
    """
    def __init__(self, *args):
        self._model = RigStructureModel()
        self.name_conv = nameConvention.NameConvention()
        if args:
            self.name_conv.default_names['system'] = self.name_conv.get_a_short_name(args[0])
            self.name_conv.default_names['side'] = self.name_conv.get_from_name(args[0], 'side')

    def create(self):
        """
        Creates all the members of the system structure its not necesary to call it unless you want
        to create all members at once, otherwise, they will be created as needed.
        :return:
        """
        self._create_root()

    def _create_kinematics(self):
        """
        Creates the kinematics group
        :return: none
        """
        kinematics_name = self.name_conv.set_name_in_format(name='kinematics')
        kinematics = pm.ls(kinematics_name)
        if kinematics:
            self._model.kinematics = kinematics[0]
        else:
            self._model.kinematics = pm.group(empty=True, name='kinematics')
            self.name_conv.rename_name_in_format(self._model.kinematics, useName=True)
            self.root.visibility >> self._model.kinematics.visibility


    def _create_joints(self):
        """
        Creates the joints group
        :return:
        """
        joints_name = self.name_conv.set_name_in_format(name='joints')
        joints = pm.ls(joints_name)
        if joints:
            self._model.joints = joints[0]
        else:
            self._model.joints = pm.group(empty=True, name='joints')
            self.name_conv.rename_name_in_format(self._model.joints, useName=True)
            self.root.visibility >> self._model.joints.visibility

    def _create_controls(self):
        """
        Creates the controls group
        :return:
        """
        controls_name = self.name_conv.set_name_in_format(name='controls')
        controls = pm.ls(controls_name)
        if controls:
            self._model.controls = controls[0]
        else:
            self._model.controls = pm.group(empty=True, name='controls')
            self.name_conv.rename_name_in_format(self._model.controls, useName=True)

        self._model.controls.setParent(self._model.root)
        self._model.joints.setParent(self._model.root)
        self._model.kinematics.setParent(self._model.root)

    def _create_display(self):
        system_name = self.name_conv.set_name_in_format(name='display')
        system = pm.ls(system_name)
        if system:
            self._model.display = system[0]
        else:
            self._model.display = pm.group(empty=True, name='display')
            self.name_conv.rename_name_in_format(self._model.root, useName=True)
            self._model.display.overrideEnabled.set(True)
            self._model.display.overrideDisplayType.set(1)

    def _create_root(self):
        """
        creates the base root node of the system
        :return: None
        """
        system_name = self.name_conv.set_name_in_format(name='system')
        system = pm.ls(system_name)
        if system:
            self._model.root = system[0]
        else:
            self._model.root = pm.group(empty=True, name='system')
            self.name_conv.rename_name_in_format(self._model.root, useName=True)

        settings_name = self.name_conv.set_name_in_format(name='settings')
        settings = pm.ls(settings_name)
        if settings:
            self._model.settings = settings[0]
        else:
            self._model.settings = pm.spaceLocator(name='settings')
            self.name_conv.rename_name_in_format(self._model.settings, useName=True)
            self._model.settings.setParent(self._model.root)
        pm.addAttr(self._model.settings, ln='worldScale', at='double', k=True)
        self._model.settings.worldScale.set(1)

    @property
    def kinematics(self):
        """
        A property to refer to the kinematics group as a pymel node
        """
        if not self._model.kinematics:
           self.create()
        return self._model.kinematics

    @property
    def joints(self):
        """
        A property to refer to the joints group as a pymel node
        """
        if not self._model.joints:
            self.create()
        return self._model.joints

    @property
    def controls(self):
        """
        A property to refer to the controls group as a pymel node
        """
        if not self._model.controls:
            self.create()
        return self._model.controls

    @property
    def settings(self):
        """
        A property to refer to the settings group as a pymel node
        """
        if not self._model.settings:
            self._create_root()
        return self._model.settings

    @property
    def root(self):
        """
        A property to refer to the root group of the system as a pymel node
        """
        if not self._model.root:
            self._create_root()
        return self._model.root


if __name__ == '__main__':
    selection = pm.ls(selection=True)
    sys = SystemStructure(selection[0])
    sys.create()
