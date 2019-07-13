from RMPY.core import dataValidators
import pymel.core as pm
from RMPY.creators import creatorsBase


class Connect(creatorsBase.CreatorsBase):
    def __init__(self, *args, **kwargs):
        super(Connect, self).__init__(*args, **kwargs)

    @staticmethod
    def _validate_connection(attribute, input_attribute):
        input_attribute = dataValidators.as_pymel_nodes(input_attribute)
        if issubclass(attribute.__class__, pm.general.Attribute):
            attribute >> input_attribute
        else:
            input_attribute.set(attribute)

    def attributes(self, attribute_source, attribute_destination, operation=1):
        attribute_source = attribute_source
        attribute_destination = attribute_destination
        value = pm.listConnections(attribute_destination, destination=False, plugs=True, skipConversionNodes=False)
        value_nodes = pm.listConnections(attribute_destination, destination=False, skipConversionNodes=False)
        plus_minus = None
        if value:
            if pm.objectType(value_nodes[0]) == 'plusMinusAverage':
                plus_minus = value_nodes[0]
                if pm.getAttr(attribute_source, type=True) in ['float', 'double', 'doubleLinear',
                                                               'doubleAngle'] or pm.getAttr(
                    attribute_source).__class__ in [float, int]:
                    next_index = len(pm.getAttr('%s.input1D' % plus_minus, multiIndices=True))
                    pm.connectAttr(attribute_source, '{}.input1D[{}]'.format(plus_minus, next_index))

                # elif attribute_source.get(type=True) in [vector]:
                #    print 'connecting vector'
                elif pm.getAttr(attribute_source, type=True) in ['double3'] or pm.getAttr(
                        attribute_source).__class__ in [list, tuple]:

                    next_index = len(pm.getAttr('%s.input3D' % plus_minus, multiIndices=True)) % 3
                    pm.connectAttr(attribute_source, '{}.input3D[{}]'.format(plus_minus, next_index))

                else:
                    print 'could not add data type: %s, %s' % (pm.getAttr(attribute_source, type=True),
                                                               pm.getAttr(attribute_source).__class__)
            else:
                if pm.getAttr(attribute_source, type=True) in ['float', 'double', 'doubleLinear',
                                                               'doubleAngle'] or pm.getAttr(
                              attribute_source).__class__ in [float, int]:
                    plus_minus = pm.shadingNode("plusMinusAverage", asUtility=True)
                    plus_minus = self.name_convention.rename_name_in_format(plus_minus,
                                                                      name='addition{}'.format(
                                                                          attribute_destination.split('.')[1].title()))
                    pm.setAttr('{}.operation'.format(plus_minus), operation)
                    pm.disconnectAttr(value[0], attribute_destination)
                    pm.connectAttr(value[0], '{}.input1D[0]'.format(plus_minus))
                    pm.connectAttr(attribute_source, '{}.input1D[1]'.format(plus_minus))
                    pm.connectAttr('{}.output1D'.format(plus_minus), attribute_destination)

                elif pm.getAttr(attribute_source, type=True) in ['double3'] or pm.getAttr(
                        attribute_source).__class__ in [list, tuple]:

                    plus_minus = pm.shadingNode("plusMinusAverage", asUtility=True)
                    plus_minus = self.name_convention.rename_name_in_format(plus_minus,
                                                                      name='addition{}'.format(
                                                                          attribute_destination.split('.')[1].title()))

                    pm.setAttr('{}.operation'.format(plus_minus), operation)
                    pm.disconnectAttr(value[0], attribute_destination)
                    pm.connectAttr(value[0], '{}.input3D[0]'.format(plus_minus))
                    pm.connectAttr(attribute_source, '{}.input3D[1]'.format(plus_minus))
                    pm.connectAttr('{}.output3D'.format(plus_minus), attribute_destination)
                else:
                    print 'could not add data type: %s class: %s' % (pm.getAttr(attribute_source, type=True),
                                                                     pm.getAttr(attribute_source).__class__)
            return plus_minus
        else:
            pm.connectAttr(attribute_source, attribute_destination)
        return None

    def with_limits(self, attribute_x, attrribute_y, keys, operation=1, in_tangent_type='spline',
                    out_tangent_type='spline', post_infinity_type='linear', pre_infinity_type='linear'):
        """
        Pre/post InfinityType values: 'constant, 'linear', 'cycle', 'cycleRelative', 'oscillate'
        in/out TangentType values: 'global_', 'fixed', 'linear', 'flat', 'smooth', 'step', 'slow',
                'fast', 'clamped', 'plateau', 'stepNext', 'auto'
        :param attribute_x:
        :param attrribute_y:
        :param keys:
        :param operation:
        :param in_tangent_type:
        :param out_tangent_type:
        :param post_infinity_type:
        :param pre_infinity_type:
        :return:
        """
        attribute_x = dataValidators.as_pymel_nodes(attribute_x)
        attrribute_y = dataValidators.as_pymel_nodes(attrribute_y)
        value = pm.listConnections(attrribute_y, destination=False, plugs=True, skipConversionNodes=False)
        plus_minus = None
        if value:
            if pm.objectType(value[0].node()) == 'plusMinusAverage':
                plus_minus = value[0].node()
                if attribute_x.get(type=True) in ['double', 'doubleLinear', 'doubleAngle', 'float']:
                    for eachKey in keys:
                        pm.setDrivenKeyframe('%s' % plus_minus.input1D[len(plus_minus.input1D.elements())],
                                             currentDriver='%s' % attribute_x, inTangentType=in_tangent_type,
                                             outTangentType=out_tangent_type, dv=eachKey[0], v=eachKey[1])
                    animation_curve_node = \
                        pm.listConnections('%s' % plus_minus.input1D[len(plus_minus.input1D.elements())])[0]
                    self.name_convention.rename_name_in_format(animation_curve_node)
                elif attribute_x.get(type=True) in ['double3']:
                    for eachKey in keys:
                        pm.setDrivenKeyframe('%s' % plus_minus.input3D[len(plus_minus.input3D.elements()) % 3],
                                             currentDriver='%s' % attribute_x,
                                             inTangentType=in_tangent_type, outTangentType=out_tangent_type,
                                             dv=eachKey[0], v=eachKey[1])
                    animation_curve_node = \
                        pm.listConnections('%s' % plus_minus.input3D[len(plus_minus.input3D.elements()) % 3])[0]
                    self.name_convention.rename_name_in_format(animation_curve_node)
                else:
                    print 'could not add data type: %s' % attribute_x.get(type=True)
            else:
                if attribute_x.get(type=True) in ['double', 'doubleLinear', 'doubleAngle', 'float']:
                    plus_minus = pm.shadingNode("plusMinusAverage", asUtility=True, name="additiveConnection")
                    self.name_convention.rename_name_in_format(plus_minus)
                    plus_minus.operation.set(operation)
                    value[0] // attrribute_y
                    value[0] >> plus_minus.input1D[0]
                    plus_minus.output1D >> attrribute_y
                    for eachKey in keys:
                        pm.setDrivenKeyframe('%s' % plus_minus.input1D[1],
                                             currentDriver='%s' % attribute_x, dv=eachKey[0], v=eachKey[1],
                                             inTangentType=in_tangent_type, outTangentType=out_tangent_type)
                    animation_curve_node = pm.listConnections('%s' % plus_minus.input1D[1])[0]
                    self.name_convention.rename_name_in_format(animation_curve_node)
                elif attribute_x.get(type=True) in ['double3']:
                    plus_minus = pm.shadingNode("plusMinusAverage", asUtility=True, name="additiveConnection")
                    self.name_convention.rename_name_in_format(plus_minus)
                    plus_minus.operation.set(operation)
                    value[0] // attrribute_y
                    value[0] >> plus_minus.input3D[0]
                    plus_minus.output3D >> attrribute_y
                    for eachKey in keys:
                        pm.setDrivenKeyframe('%s' % plus_minus.input3D[1],
                                             currentDriver='%s' % attribute_x, dv=eachKey[0], v=eachKey[1],
                                             inTangentType=in_tangent_type, outTangentType=out_tangent_type)
                    animation_curve_node = pm.listConnections('%s' % plus_minus.input3D[1])[0]
                    self.name_convention.rename_name_in_format(animation_curve_node)
                else:
                    print 'could not add data type: %s' % attribute_x.get(type=True)
        else:
            for eachKey in keys:
                pm.setDrivenKeyframe('%s' % attrribute_y, currentDriver='%s' % attribute_x, dv=eachKey[0], v=eachKey[1],
                                     inTangentType=in_tangent_type, outTangentType=out_tangent_type)

            animation_curve_node = pm.listConnections('%s' % attrribute_y)[0]
            self.name_convention.rename_name_in_format(animation_curve_node)

        if issubclass(animation_curve_node.__class__, pm.nodetypes.AnimCurve):
            animation_curve_node.setPostInfinityType(post_infinity_type)
            animation_curve_node.setPreInfinityType(pre_infinity_type)
        return plus_minus, animation_curve_node

    def times_factor(self, attr_a, attr_b, factor=1, name='unitConversion'):
        unit_conversion = pm.createNode("unitConversion", name=name)
        self.name_convention.rename_name_in_format(unit_conversion, name=name)
        pm.setAttr('{}.conversionFactor'.format(unit_conversion), factor)
        pm.connectAttr(attr_a, '{}.input'.format(unit_conversion))
        pm.connectAttr('{}.output'.format(unit_conversion), attr_b)
        return unit_conversion
