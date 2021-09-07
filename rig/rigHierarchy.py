import pymel.core as pm


class RigHierarchyModel(object):
    def __init__(self):
        self.rig = None
        self.geometry = None
        self.systems = None
        self.joints = None


class RigHierarchy(object):
    def __init__(self):
        self._model = RigHierarchyModel()

    @property
    def rig(self):
        if not self._model.rig:
            self._create_rig()
        return self._model.rig

    @property
    def geometry(self):
        if not self._model.geometry:
            self._create_geometry()
        return self._model.geometry

    @property
    def joints(self):
        if not self._model.joints:
            self._create_joints()
        return self._model.joints

    @property
    def systems(self):
        if not self._model.systems:
            self._create_systems()
        return self._model.systems

    def _create_rig(self):
        rig_transform = pm.ls('rig')
        if rig_transform:
            self._model.rig = rig_transform[0]
        else:
            self._model.rig = pm.group(empty=True, name='rig')

    def _create_geometry(self):
        rig_transform = pm.ls('geometry')
        if rig_transform:
            self._model.geometry = rig_transform[0]
        else:
            self._model.geometry = pm.group(empty=True, name='geometry')
            self._model.geometry.setParent(self.rig)

    def _create_systems(self):
        rig_transform = pm.ls('systems')
        if rig_transform:
            self._model.systems = rig_transform[0]
        else:
            self._model.systems = pm.group(empty=True, name='systems')
            self._model.systems.setParent(self.rig)

    def _create_joints(self):
        rig_transform = pm.ls('joints')
        if rig_transform:
            self._model.joints = rig_transform[0]
        else:
            self._model.joints = pm.group(empty=True, name='joints')
            self._model.joints.setParent(self.rig)


if __name__ == '__main__':
    rig_hierarchy = RigHierarchy()
