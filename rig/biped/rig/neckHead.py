from RMPY.rig import rigFK
from RMPY.rig import rigBase
import pymel.core as pm
from RMPY.rig.biped.rig import rigRibonTwistJoint
from RMPY.rig import rigSegmentScaleCompensate


class NeckHeadModel(rigBase.BaseModel):
    def __init__(self, **kwargs):
        super(NeckHeadModel, self).__init__(**kwargs)
        self.head = None
        self.neck = None
        self.twist_neck = None


class NeckHead(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', NeckHeadModel())
        super(NeckHead, self).__init__(*args, **kwargs)

    @property
    def head(self):
        if not self._model.head:
            self._model.head = rigFK.RigFK(rig_system=self.rig_system)
        return self._model.head

    @property
    def neck(self):
        if not self._model.neck:
            self._model.neck = rigFK.RigFK(rig_system=self.rig_system)
        return self._model.neck

    @property
    def twist_neck(self):
        return self._model.twist_neck

    def create_point_base(self, *args, **kwargs):
        super(NeckHead, self).create_point_base(*args, **kwargs)

        align_args = []
        for each in args:
            align_args.append(self.create.space_locator.node_base(each)[0])
            self.name_convention.rename_name_in_format(align_args[-1], name=self.name_convention.get_a_short_name(each),
                                                       system='reference')
        args = align_args
        for index,  each in enumerate(args[:-1]):
            self.transform.aim_point_based(each, each, args[index+1], use_destination_up_axis=True)

        orient_type = kwargs.pop('orient_type', 'point_orient')
        kwargs['orient_type'] = orient_type

        self.neck.create_point_base(*args[:-1], **kwargs)
        self.neck.tip = self.neck.joints[0]
        kwargs['type'] = 'head'

        self.head.create_point_base(*args[-2:], **kwargs)

        pm.parent(self.head.reset_controls[0], self.neck.controls[0])
        rig_scale_compensate = rigSegmentScaleCompensate.RigSegmentScaleCompensate()
        rig_scale_compensate.create_node_base(self.head.reset_controls[0])

        self.reset_controls.extend(self.neck.reset_controls)
        self.reset_controls.extend(self.head.reset_controls)
        self.controls.extend(self.neck.controls)
        self.controls.extend(self.head.controls)
        self._model.twist_neck = rigRibonTwistJoint.RibbonTwistJoint(rig_system=self.rig_system)
        self.twist_neck.create_point_base(self.root, self.neck.joints[0], self.head.joints[0], folicule_number=5)

        # pm.parent(self.head.joints[0], self.neck.joints[0])
        # pm.delete(self.neck.joints[1], self.head.reset_joints[0])
        self.joints.extend(self.twist_neck.joints)
        self.joints.extend(self.head.joints)
        pm.delete(align_args)


if __name__ == '__main__':

    neck_points = pm.ls(u'C_neck00_reference_pnt', u'C_head00_reference_pnt', u'C_headTip00_reference_pnt')
    neck_head = NeckHead()
    neck_head.create_point_base(*neck_points)
    print(neck_head.joints)
    # neck_head.rename_as_skinned_joints()



