from RMPY.rig import rigFK
import pymel.core as pm


class NeckHeadModel(rigFK.RigFKModel):
    def __init__(self, **kwargs):
        super(NeckHeadModel, self).__init__(**kwargs)
        self.head = None


class NeckHead(rigFK.RigFK):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', NeckHeadModel())
        super(NeckHead, self).__init__(*args, **kwargs)

    @property
    def head(self):
        if not self._model.head:
            self._model.head = rigFK.RigFK(rig_system=self.rig_system)
        return self._model.head

    def create_point_base(self, *args, **kwargs):
        orient_type = kwargs.pop('orient_type', 'point_orient')
        kwargs['orient_type'] = orient_type
        super(NeckHead, self).create_point_base(*args[:-1], **kwargs)
        self.head.create_point_base(*args[-2:], type='head', **kwargs)
        self.head.set_parent(self)
        self.reset_controls.extend(self.head.reset_controls)
        self.controls.extend(self.head.controls)
        self.joints.extend(self.head.joints)
        self.reset_controls.extend(self.head.reset_controls)


if __name__ == '__main__':
    neck_points = pm.ls(u'C_neck00_reference_pnt', u'C_head00_reference_pnt', u'C_headTip00_reference_pnt')
    neck_head = NeckHead()
    neck_head.create_point_base(*neck_points)


