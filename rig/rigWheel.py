from RMPY.rig import rigBase
import pymel.core as pm


class RigWheelModel(rigBase.BaseModel):
    def __init__(self):
        super().__init__()
        self.circle = None


class RigWheel(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', RigWheelModel())
        super(RigWheel, self).__init__(*args, **kwargs)

    def create_point_base(self, *points, **kwargs):
        super(RigWheel, self).__init__(*points, **kwargs)

        self._model.circle, circle_creator = pm.circle(normal=[0, 0, 1], degree=1)
        self.name_convention.rename_name_in_format(self.circle, circle_creator, name='wheelCylinder')
        pm.matchTransform(self.circle, points[0])
        forward_vector = self.create.space_locator.node_base(points[0], name='forwardVector')[0]
        previous_position = self.create.space_locator.node_base(points[0], name='previousPosition')[0]
        self.root = self.create.group.point_base(self.circle, name='rootMovement')
        pm.parent(forward_vector, self.root)
        pm.move(1, forward_vector, moveX=True, localSpace=True)
        pm.parent(self.root, self.rig_system.kinematics)
        pm.parent(previous_position, self.rig_system.kinematics)
        pm.addAttr(self.rig_system.settings, longName='startFrame', k=True, min=0)
        pm.addAttr(self.rig_system.settings, longName='radius', proxy=circle_creator.radius)

        expression_text = 'vector $current_position = `xform -q -t -ws {}`;\n'.format(self.circle)
        expression_text +='vector $prev_position = `xform -q -t -ws {}`;\n'.format(previous_position)
        expression_text +='if ((`currentTime -q`) <= ({}.startFrame))\n'.format(self.rig_system.settings)
        expression_text +='{\n'
        expression_text +='    {}.rotateZ = 0;\n'.format(self.circle)
        expression_text +='}\n'
        expression_text += 'else'
        expression_text += '{\n'
        expression_text += 'vector $reference_front_vector = `xform -q -t -ws {}`;\n'.format(forward_vector)
        expression_text += 'vector $delta_distance =  $current_position - $prev_position;\n'
        expression_text += 'vector $forward_direction = $reference_front_vector - $current_position;\n'
        expression_text += 'float $direction_multiplier = dotProduct($forward_direction, $delta_distance, 1);\n'
        expression_text += '{}.rotateZ = {}.rotateZ - (rad_to_deg(mag($delta_distance)/'.format(self.circle, self.circle)+ \
                           '{}.radius)* $direction_multiplier);\n'.format(self.rig_system.settings)
        expression_text += '}\n'
        expression_text += ' xform -translation ($current_position.x) ($current_position.y) ($current_position.z) ' \
                           '-worldSpace  {};\n'.format(previous_position)
        pm.expression(string=expression_text)


if __name__ == '__main__':
    my_wheel = RigWheel()
    my_wheel.create_point_base('L_wheel00_reference_pnt')
    my_wheel.set_parent('locator2', mo=False)



