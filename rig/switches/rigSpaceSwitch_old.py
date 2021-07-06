from RMPY.rig import rigBase
import pymel.core as pm


class RigSpaceSwitchModel(rigBase.BaseModel):
    def __init__(self, *args, **kwargs):
        super(RigSpaceSwitchModel, self).__init__(*args, **kwargs)
        self.control_object = None
        self.affected_object_list = []
        self.space_object_list = []


class RigSpaceSwitch(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        if 'model' not in kwargs.keys():
            kwargs['model'] = RigSpaceSwitchModel()
        super(RigSpaceSwitch, self).__init__(*args, **kwargs)

    def create_point_base(self, *points, **kwargs):
        space_objects = kwargs.pop('space_objects', None)
        control_object = kwargs.pop('control', None)
        attribute_name = kwargs.pop('attribute_name', 'space_switch')
        constraint_type = kwargs.pop('constraint_type ', 'parent')
        switch_type = kwargs.pop('switch_type ', 'parent')

        if len(space_objects) == 2:
            if switch_type == "enum":
                space_object_short_name = []
                for eachObject in space_objects:
                    space_object_short_name.append(self.name_convention.get_a_short_name(eachObject))
                self.add_enum_parameters(space_object_short_name, control_object, Name=attribute_name)
            else:
                if attribute_name == "":
                    index = 0
                    SwitchName = 'SW'
                    for eachString in space_objects:
                        SwitchName = SwitchName + self.name_convention.get_a_short_name(eachString).title()
                        index = index + 1
                    attribute_name = SwitchName

                self.add_numeric_attribute(control_object, name=attribute_name)

            reverse = pm.shadingNode('reverse', asUtility=True, name=attribute_name + "SWReverse")
            multiply = pm.shadingNode('multiplyDivide', asUtility=True, name=attribute_name + "SWMultDiv")

            # pm.connectAttr(control_object + "." + attribute_name, reverse + ".inputX")
            pm.connectAttr(control_object + "." + attribute_name, multiply + ".input1X")
            pm.setAttr(multiply + ".input2X", 10)
            pm.setAttr(multiply + ".operation", 2)
            pm.connectAttr(multiply + ".outputX", reverse + ".inputX")

            controled_object = points[0]
            for eachObject in space_objects:
                if constraint_type == "point":
                    parent_constraint = pm.pointConstraint(eachObject, controled_object, **kwargs)
                    weight_alias_list = pm.pointConstraint(parent_constraint, q=True, weightAliasList=True)

                elif constraint_type == "orient":
                    parent_constraint = pm.orientConstraint(eachObject, controled_object, **kwargs)
                    weight_alias_list = pm.orientConstraint(parent_constraint, q=True, weightAliasList=True)

                elif constraint_type == "parent":
                    parent_constraint = pm.parentConstraint(eachObject, controled_object, **kwargs)
                    weight_alias_list = pm.parentConstraint(parent_constraint, q=True, weightAliasList=True)

            pm.setAttr("%s.interpType" % parent_constraint, 0)

            if self.name_convention.is_name_in_format(controled_object):
                self.name_convention.rename_based_on_base_name(controled_object, reverse, name=reverse)
                self.name_convention.rename_based_on_base_name(controled_object, multiply, name=multiply)
                self.name_convention.rename_based_on_base_name(controled_object, parent_constraint, name=attribute_name)

            else:
                self.name_convention.rename_name_in_format(reverse)
                self.name_convention.rename_name_in_format(multiply)
                self.name_convention.rename_name_in_format(parent_constraint)

            pm.connectAttr(multiply + ".outputX", weight_alias_list[1])
            pm.connectAttr(reverse + ".outputX", weight_alias_list[0])

            # pm.connectAttr(control_object + "." + Name, parentConstraint[0] + "." + WA[1])
            # pm.connectAttr(reverse + ".outputX", parentConstraint[0] + "." + WA[0])

    def add_enum_parameters(self, enum, scene_object, **kwargs):
        name = kwargs.pop('name', 'spaceSwitch')
        if name in pm.listAttr(scene_object):
            if pm.getAttr(scene_object + "." + name, type=True) == 'enum':
                enums_in_object = self.get_control_enums(scene_object)
                for eachEnum in enum:
                    if not eachEnum in enums_in_object:
                        enums_in_object.append(eachEnum)
                pm.addAttr(scene_object + '.' + name, e=True, ln=name, en=":".join(enums_in_object))
                index = 0
                return_index_dictionary = {}
                for eachEnum in enums_in_object:
                    return_index_dictionary[eachEnum] = index
                    index += 1
                return return_index_dictionary
        else:
            pm.addAttr(scene_object, at="enum", ln=name, k=1, en=":".join(enum))
        return None

    def get_control_enums(self, scene_node, **kwargs):
        space_switch_name = kwargs.pop('space_switch_name', 'spaceSwitch')
        attribute_list = pm.listAttr(scene_node)
        if space_switch_name in attribute_list:
            if pm.getAttr(scene_node + "." + space_switch_name, type=True) == 'enum':
                valid_values = pm.addAttr(scene_node + "." + space_switch_name, q = True, enumName=True)
                valid_values_list = valid_values.split(":")
                return valid_values_list
        else:
            return []

    def add_numeric_attribute(self, scene_object, **kwargs):
        name = kwargs.pop('name', 'spaceSwitch')
        min_value = kwargs.pop('min', 0)
        max_value = kwargs.pop('max', 10)
        if name in pm.listAttr(scene_object):
            return False
        else:
            pm.addAttr(scene_object, at="float", ln=name,  keyable=True, min=min_value, max=max_value)
            return True


if __name__ == '__main__':
    control_space_switch = pm.ls('C_control_spaceSwitch_shp')[0]
    space_switch_rig = RigSpaceSwitch()
    space_switch_rig.create_point_base('pCube1', control_object= 'C_control_spaceSwitch_shp',
                                       space_objects=['pCylinder1', 'pSphere1'], mo=False)
