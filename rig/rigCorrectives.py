import pymel.core as pm
import maya.cmds as cmds
from RMPY.rig import rigBase
from RMPY.creators import mesh
from RMPY.creators import blendShape
from RMPY.core import transform
rotation_axis = ['xyz', 'yzx', 'zxy', 'xzy', 'yxz', 'zyx']


def right_list(list_objects):
    """
        swithchs the token L to R in any given list of objects.

    """
    result = []
    for each in list_objects:
        tokens = each.split('_')
        for index, each_token in enumerate(tokens):
            if each_token == 'L':
                tokens[index] = 'R'
        result.append('_'.join(tokens))
    return result


def normalize_list(data_list):
    """
    Normalizes a list of numbers to 1.
    :param data_list: a list of numbers [12, 34, 90]
    :return: The list, normalized to 1 in this case it would return [12/90, 34/90,  1]
    """
    higher_value = data_list[len(data_list)-1]
    return [float(each)/higher_value for each in data_list]


class CorrectiveBlendShapes(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(CorrectiveBlendShapes, self).__init__(*args, **kwargs)
        self.correctives_definition = kwargs.pop('definition', None)
        self.base_mesh = self.correctives_definition.base_mesh
        self.name_convention.default_names['system'] = 'corrective'
        self.mesh_creator = None
        self.blend_shape_match_dict = {}

    def build(self):
        self.build_blendshape_correctives()
        self.build_rig_correctives()

    def build_blendshape_correctives(self):
        # self.create_right_side_correctives()
        self.apply_corrective_blend_shapes()

    def init_mirror(self, base_mesh):
        self.mesh_creator = mesh.Mesh()
        self.mesh_creator.build_mirror_index(base_mesh)

    def create_right_side_correctives(self):
        for each_base_mesh in self.base_mesh:
            print ('doing mesh :{}'.format(each_base_mesh))
            self.init_mirror(each_base_mesh)
            correctives = self.base_mesh[each_base_mesh]
            for each_corrective_list in correctives:
                for each_corrective in correctives[each_corrective_list]:
                    if self.name_convention.get_from_name(each_corrective, 'side') == 'L':
                        right_side_mesh = pm.duplicate(each_corrective)[0]
                        self.mesh_creator.mirror_geo(right_side_mesh)
                        self.name_convention.rename_name_in_format(right_side_mesh,
                                                             side='R',
                                                             name=self.name_convention.get_a_short_name(each_corrective),
                                                             system=self.name_convention.get_from_name(each_corrective,
                                                                                                 'system'))

    def apply_corrective_blend_shapes(self):
        for each_base_mesh in self.base_mesh:
            print ('requesting blendShape  on {}'.format(each_base_mesh))
            blend_shape = blendShape.BlendShape.by_node(each_base_mesh, index=-1, create=True)
            blend_shape_node = blend_shape.node
            # name = 'C_{}_0001_BS'.format(each_base_mesh.split('_')[2])

            self.blend_shape_match_dict[each_base_mesh] = blend_shape_node
            index = blend_shape_node.getWeightCount() + 1

            for each_corrective in self.correctives_definition.corrective_order:
                if each_corrective in self.base_mesh[each_base_mesh]:
                    last_target = self.base_mesh[each_base_mesh][each_corrective][-1]

                    side = self.name_convention.get_from_name(last_target, 'side')

                    if side in 'LR':
                        self.apply_blendShapes(each_base_mesh, blend_shape_node,
                                               right_list(self.base_mesh[each_base_mesh][each_corrective]), index,
                                               normalize_list(
                                                   self.correctives_definition.config_correctives[each_corrective][
                                                       'targets']),
                                               'R{}'.format(each_corrective))
                        index += 1

                        self.apply_blendShapes(each_base_mesh, blend_shape_node,
                                               self.base_mesh[each_base_mesh][each_corrective], index,
                                               normalize_list(
                                                   self.correctives_definition.config_correctives[each_corrective]['targets']),
                                               'L{}'.format(each_corrective))
                        index += 1

                    else:
                        self.apply_blendShapes(each_base_mesh, blend_shape_node,
                                               self.base_mesh[each_base_mesh][each_corrective], index,
                                               normalize_list(
                                                   self.correctives_definition.config_correctives[each_corrective]['targets']),
                                               '{}'.format(each_corrective))
                        index += 1

    def apply_blendShapes(self, base_mesh, blendshape_node, correctives_list, index, weights_list, target_name):
            last_target = correctives_list[-1]
            cmds.rename(last_target, target_name)
            pm.blendShape(blendshape_node, e=True, target=[base_mesh,
                                                           index,
                                                           target_name, 1.0])
            cmds.rename(target_name, last_target)
            target_value = weights_list[:-1]

            for corrective_mesh, index_value in zip(correctives_list[:-1], target_value):
                pm.blendShape(blendshape_node, e=True, ib=True, target=[base_mesh,
                                                                        index,
                                                                        corrective_mesh,
                                                                        index_value])

    def build_rig_correctives(self):
        for each_corrective in self.correctives_definition.corrective_order:
            for each_geo in self.base_mesh:
                if each_corrective in self.base_mesh[each_geo].keys():
                    last_target = self.base_mesh[each_geo][each_corrective][-1]
                    side = self.name_convention.get_from_name(last_target, 'side')
                    print ('found side {}'.format(side))

            if each_corrective in self.correctives_definition.config_correctives:
                drivers = self.correctives_definition.config_correctives[each_corrective]['drivers']
                rotation_order = self.correctives_definition.config_correctives[each_corrective]['rotationOrder']
                targets = self.correctives_definition.config_correctives[each_corrective]['targets']

                if side == 'L':
                    self.rig_correctives(drivers, rotation_order, targets, each_corrective, side)
                    side = 'R'
                    right_drivers = []
                    for index, each_driver in enumerate(drivers):
                        if self.name_convention.get_from_name(each_driver, 'side') == 'L':
                            name_right_side = self.name_convention.set_from_name(each_driver, 'R', 'side')
                            right_drivers.append(name_right_side)
                        else:
                            right_drivers.append(each_driver)

                    if 'RFlip' in self.correctives_definition.config_correctives[each_corrective].keys():
                        if self.correctives_definition.config_correctives[each_corrective]['RFlip']:
                            res_list = [-1 * each for each in targets]
                            print ('connecting {}{} with {} in A'.format(side, each_corrective, res_list))
                            self.rig_correctives(right_drivers, rotation_order, res_list, each_corrective, side)
                        else:
                            print ('connecting {}{} with {} in B'.format(side, each_corrective, targets))
                            self.rig_correctives(right_drivers, rotation_order, targets, each_corrective, side)
                    else:
                        print ('connecting {}{} with {} in C'.format(side, each_corrective, targets))
                        self.rig_correctives(right_drivers, rotation_order, targets, each_corrective, side)
                else:
                    print ('connecting {}{} with {} in D'.format(side, each_corrective, targets))
                    self.rig_correctives(drivers, rotation_order, targets, each_corrective, side)

    def rig_correctives(self, drivers, rotation_order, targets, weight_name, side):

        default_name = self.name_convention.get_a_short_name(weight_name)
        self.name_convention.default_names['system'] = 'correctiveBS'
        self.name_convention.default_names['side'] = side
        zero_locator = pm.spaceLocator()
        self.name_convention.rename_name_in_format(zero_locator, name='zero{}'.format(default_name.capitalize()))
        driver_locator = pm.spaceLocator()
        zero_locator.rotateOrder.set(rotation_axis.index(rotation_order))
        self.name_convention.rename_name_in_format(driver_locator, name='driver{}'.format(default_name.capitalize()))
        print ('drivers:{}'.format(drivers))
        print (str(drivers[1]), str(driver_locator))
        transform.align(str(drivers[1]), str(zero_locator))
        driver_locator.setParent(zero_locator)
        driver_locator.rotateOrder.set(rotation_axis.index(rotation_order))

        transform.align(str(drivers[1]), str(driver_locator))
        zero_locator.setParent(self.rig_system.kinematics)

        pm.parentConstraint(drivers[0], zero_locator, mo=True)
        pm.parentConstraint(drivers[1], driver_locator, mo=True)
        anim_curve = None

        for each_geo in self.base_mesh:
            index = 0
            blendShape_node = self.blend_shape_match_dict[each_geo]

            if side in 'LR':
                side_weight_name = '{}{}'.format(side, weight_name)
            else:
                side_weight_name = weight_name

            if weight_name in self.base_mesh[each_geo]:
                if index == 0 and (side_weight_name not in pm.listAttr(self.rig_system.settings)):
                    pm.addAttr(self.rig_system.settings, ln=side_weight_name, k=True)
                    pm.addAttr(self.rig_system.settings, ln='{}Multiply'.format(side_weight_name), k=True)
                    pm.addAttr(self.rig_system.settings, ln='{}Addition'.format(side_weight_name), k=True)
                    self.rig_system.settings.attr('{}Multiply'.format(side_weight_name)).set(1)

                    side_multiplier = pm.createNode('multiplyDivide')
                    user_multiplier = pm.createNode('multiplyDivide')
                    self.name_convention.rename_name_in_format(side_multiplier, name='sideRotationDimmer')
                    self.name_convention.rename_name_in_format(user_multiplier, name='userDimmer')
                    self.create.connect.with_limits(
                        driver_locator.attr('rotate{}'.format(rotation_order[1].capitalize())),
                        side_multiplier.input2X, [[-45, 0], [0, 1], [45, 0]],
                        post_infinity_type='constant', pre_infinity_type='constant')

                    if targets[0] > 0:
                        connections_list = zip([0] + targets, [0] + normalize_list(targets))
                        # plus_minus, anim_curve =
                        self.create.connect.with_limits(driver_locator.attr('rotate{}'.format(
                            rotation_order[0].capitalize())),
                            side_multiplier.input1X, connections_list,
                            post_infinity_type='constant', pre_infinity_type='constant')

                    else:
                        connections_list = zip(list(reversed(targets)) + [0], list(reversed(normalize_list(targets))) + [0])
                        self.create.connect.with_limits(driver_locator.attr('rotate{}'.format(
                            rotation_order[0].capitalize())),
                            side_multiplier.input1X, connections_list,
                            post_infinity_type='constant', pre_infinity_type='constant')

                    side_multiplier.outputX >> user_multiplier.input1X
                    self.rig_system.settings.attr('{}Multiply'.format(side_weight_name)) >> user_multiplier.input2X
                    user_multiplier.outputX >> self.rig_system.settings.attr(side_weight_name)
                    self.create.connect.attributes(self.rig_system.settings.attr('{}Addition'.format(side_weight_name)),
                                                       self.rig_system.settings.attr(side_weight_name))

                self.rig_system.settings.attr(side_weight_name) >> blendShape_node.attr(side_weight_name)

            index += 1


if __name__ == '__main__':
    pass