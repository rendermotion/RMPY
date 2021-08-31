from RMPY.rig import rigFK
import pymel.core as pm


class NeckHeadModel(rigFK.RigFKModel):
    def __init__(self, **kwargs):
        rig_system = kwargs.pop('rig_system', None)
        super(NeckHeadModel, self).__init__(**kwargs)
        if rig_system:
            self.head = rigFK.RigFK(rig_system=self.rig_system)
        else:
            self.head = rigFK.RigFK()


class NeckHead(rigFK.RigFK):
    def __init__(self, *args, **kwargs):
        super(NeckHead, self).__init__(*args, **kwargs)
        self._model = NeckHeadModel()

    @property
    def head(self):
        return self._model.head

    def create_point_base(self, *args, **kwargs):
        orient_type = kwargs.pop('orient_type', 'point_orient')
        kwargs['orient_type'] = orient_type
        super(NeckHead, self).create_point_base(*args[:-1], **kwargs)
        self.head.create_point_base(*args[-2:], type='head', **kwargs)
        self.head.set_parent(self)

    def rename_as_skinned_joints(self, nub=True):
        super(NeckHead, self).rename_as_skinned_joints(nub=nub)
        self.head.rename_as_skinned_joints(nub=nub)


if __name__ == '__main__':
    neck_points = pm.ls(u'C_neck00_reference_pnt', u'C_head00_reference_pnt', u'C_headTip00_reference_pnt')
    neck_head = NeckHead()
    neck_head.create_point_base(*neck_points)


