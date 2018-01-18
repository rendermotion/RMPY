import pymel.core as pm

class RigStructureModel():
    def __init__(self):
        self.kinematics = 'kinematics'
        self.joints = 'joints'
        self.controls = 'controls'
        self.world = 'world'

class RigStructure():
    def __init__(self):
        self._model = RigStructureModel()

        kinematics = pm.ls(self.kinematics)
        if kinematics:
            self._model.kinematics = kinematics[0]
        else:
            self._model.kinematics = pm.group(empty=True, name=self._model.kinematics)

        joints = pm.ls(self.joints)
        if joints:
            self._model.joints = joints[0]
        else:
            self._model.joints = pm.group(empty=True, name=self._model.joints)

        controls = pm.ls(self.controls)
        if controls:
            self._model.controls = controls[0]
        else:
            self._model.controls = pm.group(empty=True, name=self._model.controls)

        world = pm.ls(self.world)
        if world:
            self._model.world = world[0]
        else:
            self._model.world = pm.group(empty=True, name=self._model.world)

    @property
    def kinematics(self):
        return self._model.kinematics

    @property
    def joints(self):
        return self._model.joints

    @property
    def controls(self):
        return self._model.controls

    @property
    def world(self):
        return self._model.world

if __name__ == '__main__':
    RigStructure()