from RMPY.rig import rigSingleJoint
from RMPY.rig import rigBase
import pymel.core as pm


class RigPropModel(rigBase.BaseModel):
    def __init__(self):
        super(RigPropModel, self).__init__()
        self.single_joints = []


class RigProp(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        if 'model' not in kwargs.keys():
            kwargs['model'] = RigPropModel()
        super(RigProp, self).__init__(*args, **kwargs)

    @property
    def single_joints(self):
        return self._model.single_joints

    def create_point_base(self, *points, **kwargs):
        """
        :param points:
        :param kwargs:
            depth: the number of controls that will be nested inside each reference point default 2
            size: size of the controls default 1
            step size: a multiplier for each one of the nested controls, default will be size /10
            align: the alignment of the controls
                'point' each control will be aligned to each one of the points
                'world' each control will align to the world
        :return:
        """

        depth = kwargs.pop('depth', 2)
        size = kwargs.pop('size', 1.0)
        size_step = kwargs.pop('size_step', -size/10.0)
        align = kwargs.pop('align', 'point')
        offset_visibility = kwargs.pop('offset_visibility', False)

        single_joint = rigSingleJoint.RigSingleJoint()
        self.single_joints.append(single_joint)
        for each_point in points:
            for index in range(depth):
                single_joint.create_point_base(each_point, size=size + size_step*index, **kwargs)
                if index >= 1:
                    single_joint.reset_controls[-1].setParent(single_joint.controls[-2])
                    if offset_visibility:
                        single_joint.controls[0].offset_visibility >> single_joint.reset_controls[-1].visibility
                else:
                    if offset_visibility:
                        single_joint.controls[0].addAttr('offset_visibility', at='bool', k=True)

                if align == 'world':
                    self.custom_world_align(single_joint.reset_controls[-1])
            self.joints.extend(single_joint.joints)
            self.controls.extend(single_joint.controls)
            self.reset_joints.extend(single_joint.reset_joints)

        # self.controls = single_joint.controls
        # self.reset_controls = single_joint.reset_controls
        # self.joints = single_joint.joints
        # self.reset_joints = single_joint.reset_joints


if __name__ == '__main__':
    reference_points = pm.ls('C_box00_reference_pnt')[0]
    rig_prop = RigProp()
    rig_prop.create_point_base(reference_points, depth=2, type='box', centered=True, align='world')