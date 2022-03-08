from RMPY.rig import rigStretchyIK
from RMPY.rig import rigFK
from RMPY.rig import rigBase
import pymel.core as pm
from RMPY.rig import rigSingleJoint


class IKQuadLegModel(rigBase.BaseModel):
    def __init__(self):
        super(IKQuadLegModel, self).__init__()
        self.rig_ik_leg = None
        self.rig_fk_palm = None
        self.rig_leg_palm = None
        self.root_controls = None

        self.controls_dict = {'poleVector': None, 'ikHandle': None}
        self.reset_controls_dict = {'poleVector': None, 'ikHandle': None}


class IKQuadLeg(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', IKQuadLegModel())
        super(IKQuadLeg, self).__init__(*args, **kwargs)

    @property
    def controls_dict(self):
        return self._model.controls_dict

    @property
    def reset_controls_dict(self):
        return self._model.reset_controls_dict

    @property
    def rig_ik_leg(self):
        return self._model.rig_ik_leg

    @property
    def rig_fk_palm(self):
        return self._model.rig_fk_palm

    @property
    def root_controls(self):
        return self._model.root_controls

    @property
    def rig_leg_palm(self):
        return self._model.rig_leg_palm

    def create_point_base(self, *args, **kwargs):
        super(IKQuadLeg, self).create_point_base(*args, **kwargs)
        self._model.rig_ik_leg = rigStretchyIK.StretchyIK(rig_system=self.rig_system)
        self.rig_ik_leg.create_point_base(*args[:-1], create_pole_vector=False,
                                          create_controls=False,
                                          make_stretchy=False)
        self.rig_ik_leg.create_pole_vector()
        self.rig_ik_leg.create_control_pole_vector()
        self.rig_ik_leg.make_stretchy()

        reset_controls, ik_control = self.create.controls.point_base(args[-1], name='ikControl', centered=True)
        self.controls_dict['ikHandle'] = ik_control
        self.reset_controls_dict['ikHandle'] = reset_controls

        self.controls_dict['poleVector'] = self.rig_ik_leg.controls_dict['poleVector']
        self.reset_controls_dict['poleVector'] = self.rig_ik_leg.reset_controls_dict['poleVector']

        pm.parent(reset_controls, self.rig_system.controls)
        self.custom_world_align(reset_controls)
        self.controls.append(ik_control)

        self.rig_ik_leg.expose_attributes_on_control(ik_control)

        self._model.rig_leg_palm = rigSingleJoint.RigSingleJoint(rig_system=self.rig_system)

        self.rig_leg_palm.create_point_base(ik_control)
        self.create.constraint.point(ik_control, self.rig_leg_palm.root)
        ankle_reset_joint, ankle_joint = self.rig_leg_palm.create.joint.point_base(args[-2], name='ankle',
                                                                                   orient_type='point_orient')
        palm_reset_joint, palm_joint = self.rig_leg_palm.create.joint.point_base(args[-1], name='palm')

        self.rm.aim_point_based(ankle_joint[0], ankle_joint[0], palm_joint[0], self.rig_ik_leg.pole_vector)
        self.create.constraint.orient(ankle_joint[0], self.rig_ik_leg.joints[-1])
        palm_joint[0].setParent(self.rig_ik_leg.joints[-1])
        self.rig_ik_leg.joints.append(palm_joint[0])

        ankle_joint[0].setParent(self.rig_leg_palm.joints[-1])
        self.rig_leg_palm.joints.append(ankle_joint[0])

        pm.delete(ankle_reset_joint, palm_reset_joint)

        self.create.constraint.node_base(self.rig_leg_palm.tip, self.rig_ik_leg.ik_handle, mo=True)
        offset_group = self.create.group.point_base(self.rig_leg_palm.controls[0])

        pm.addAttr(ik_control, ln='rotationFront', at='float', k=True)
        pm.addAttr(ik_control, ln='rotationSide', at='float', k=True)

        ik_control.rotationFront >> offset_group.rotateZ
        ik_control.rotationSide >> offset_group.rotateX

        self.joints.extend(self.rig_ik_leg.joints)
        self.reset_joints.extend(self.rig_ik_leg.reset_joints)
        self._model.root_controls = pm.group(empty=True, name='ikControls')

        self.rm.align(self.joints[0], self.root_controls)

        self.create.constraint.node_base(self.root_controls, self.reset_joints[0])

        for each_control in self.reset_controls_dict:
            self.reset_controls_dict[each_control].setParent(self.root_controls)

        self.root_controls.setParent(self.rig_system.controls)
        self.attach_points['root'] = self.root_controls


if __name__ == '__main__':
    leg_root_points = [u'{}_backLeg00_reference_pnt', u'{}_backLeg01_reference_pnt',
                       u'{}_backLeg02_reference_pnt', u'{}_paw00_reference_pnt']
    leg_root_points = pm.ls([each.format('R') for each in leg_root_points])
    quad_leg = IKQuadLeg()
    quad_leg.create_point_base(*leg_root_points)



