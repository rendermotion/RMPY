import pymel.core as pm
from RMPY.rig import rigBase
from RMPY.rig import rigBiaseControl


if not 'MayaMuscle' in pm.pluginInfo(q=True, listPlugins=True):
    pm.loadPlugin('MayaMuscle')
else:
    print('plugin maya muscle already loaded')


class MuscleSpline(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(MuscleSpline, self).__init__(*args, **kwargs)
        self.spline = None
        self.controls = []
        self.reset_controls = []
        self.joints = []
        self.reset_joints = []
        self.fullScale = None
        self.biased_control = kwargs.pop('biased_control', None)
        self.user_scale_nodes_list = []
        self.user_add_nodes_list = []

    def create_curve_base(self, *curves, **kwargs):
        super(MuscleSpline, self).create_curve_base(*curves, **kwargs)
        point_list = []
        for each_point in range(3):
            point_list.append(self.rig_create.space_locator.point_base(curves[0]))
        self.rig_create.motion_path.node_base(*point_list, curve=curves[0], followAxis='Y', upAxis='X')
        self.create_point_base(*point_list, **kwargs)
        pm.delete(point_list)

    def create_point_base(self, *points, **kwargs):
        super(MuscleSpline, self).create_point_base(*points, **kwargs)
        spline = pm.createNode('cMuscleSpline')
        type = kwargs.pop('type', 'box')
        kwargs['type'] = type
        centered = kwargs.pop('centered', True)
        kwargs['centered'] = centered
        self.spline = spline
        self.name_convention.rename_name_in_format(spline.getParent(), name='muscleSpline')
        self.name_convention.rename_name_in_format(spline, name='muscleSplineShape')
        pm.parent(self.spline.getParent(), self.rig_system.kinematics)

        pm.addAttr(spline, ln='curLen', k=True)
        pm.addAttr(spline, ln='pctSquash', k=True)
        pm.addAttr(spline, ln='pctStretch', k=True)

        for reference_point, each in zip(points, range(len(points))):
            print ('*****reference_point = {}'.format(reference_point))
            reset_control, control = self.create.controls.point_base(reference_point, **kwargs)
            self.controls.append(control)
            self.reset_controls.append(reset_control)

            for each_attribute, default_value in [('tangentLength', 1), ('jiggle', 0), ('jiggleX', 0), ('jiggleY', 0),
                                                  ('jiggleZ', 0), ('jiggleImpact', 0), ('jiggleImpactStart', 1000),
                                                  ('jiggleImpactStop', 0.001), ('cycle', 12), ('rest', 24)]:
                if each_attribute not in pm.listAttr(control):
                    pm.addAttr(control, ln=each_attribute, k=True)
                pm.Attribute('{}.{}'.format(control, each_attribute)).set(default_value)
                pm.connectAttr('{}.{}'.format(control, each_attribute),
                               '{}.controlData[{}].{}'.format(spline, each, each_attribute))
            pm.connectAttr('{}.worldMatrix'.format(control, each),
                           '{}.controlData[{}].insertMatrix'.format(spline, each))
            pm.parent(reset_control, self.rig_system.controls)

        pm.connectAttr('time1.outTime', '{}.inTime'.format(spline))

        spline_len = self.spline.outLen.get()
        self.spline.lenDefault.set(spline_len)
        self.spline.lenSquash.set(spline_len*0.5)
        self.spline.lenStretch.set(spline_len*2.0)

        pm.connectAttr(self.spline.outLen, self.spline.curLen)
        pm.connectAttr(self.spline.outPctSquash, self.spline.pctSquash)
        pm.connectAttr(self.spline.outPctStretch, self.spline.pctStretch)

    def create_joints_on_curve(self, joint_number):
        if joint_number > 1:
            step = 1.0/(joint_number-1)
        else:
            step = 0.5
        root_group = pm.group(empty=True)
        self.name_convention.rename_name_in_format(root_group, name='joints')
        root_group.setParent(self.rig_system.joints)
        self.reset_joints.append(root_group)
        for index in range(joint_number):
            new_joint = pm.joint()
            self.joints.append(new_joint)
            new_joint.setParent(None)
            self.name_convention.rename_name_in_format(new_joint, objectType='skinjoint')
            pm.addAttr(new_joint, ln='UValue', k=True)
            if joint_number > 1:
                new_joint.UValue.set(float(index) * step)
            else:
                new_joint.UValue.set(step)
            pm.connectAttr('{}.UValue'.format(new_joint), '{}.readData[{}].readU'.format(self.spline, index))
            pm.connectAttr('{}.rotateOrder'.format(new_joint),
                           '{}.readData[{}].readRotOrder'.format(self.spline, index))
            pm.connectAttr('{}.outputData[{}].outTranslate'.format(self.spline, index),
                           '{}.translate'.format(new_joint))
            pm.connectAttr('{}.outputData[{}].outRotate'.format(self.spline, index),
                           '{}.rotate'.format(new_joint))
            pm.parent(new_joint, root_group)
            new_joint.jointOrient.set(0, 0, 0)

    def biased_scale(self):
        self.fullScale = pm.createNode('plusMinusAverage')
        self.name_convention.rename_name_in_format(self.fullScale, name='stretchScaleValue')
        self.fullScale.operation.set(2)

        self.spline.pctSquash >> self.fullScale.input1D[0]
        self.spline.pctStretch >> self.fullScale.input1D[1]
        self.controls_multiplier()
        if not self.biased_control:
            self.biased_control = rigBiaseControl.BiasedControl(rig_system=self.rig_system)
            # self.biased_control.build(len(new_spline.joints))# curve_points=[[0, 0, 0], [0, 0, 1], [.5, 0, 1], [1, 0, 1], [1, 0, 0]])
            self.biased_control.build(number_of_points=len(new_spline.joints),
                                      curve_points=[[0, 0, 0], [0, 0, 1], [.5, 0, 1], [1, 0, 1], [1, 0, 0]])
        self.biased_control.connect(['{}.input1X'.format(each) for each in self.user_scale_nodes_list])

    def controls_multiplier(self):
        for each_joint in self.joints:
            scale_factor = pm.createNode('multiplyDivide')
            self.user_scale_nodes_list.append(scale_factor)
            self.name_convention.rename_name_in_format(scale_factor, name='userScaleValue')
            self.fullScale.output1D >> scale_factor.input2X
            scale_factor.input1X.set(1)
            final_addition = pm.createNode('plusMinusAverage')
            self.user_add_nodes_list.append(final_addition)
            final_addition.input1D[0].set(1)
            scale_factor.outputX >> final_addition.input1D[1]
            final_addition.output1D >> each_joint.scaleX
            final_addition.output1D >> each_joint.scaleZ


if __name__ == '__main__':
 points = ['L_dynamicBreast00_reference_pnt', 'L_dynamicBreast01_reference_pnt', 'L_dynamicBreast02_reference_pnt']
 new_spline = MuscleSpline()
 new_spline.create_point_base(*points)
 #new_spline.create_curve_base('C_muscle_reference_SHP')
 new_spline.create_joints_on_curve(3)
 new_spline.biased_scale()