import pymel.core as pm
from RMPY.core import dataValidators
from RMPY.core import config
from RMPY.core import transform
from RMPY.core import hierarchy
from RMPY.creators import creatorsBase


class Group(creatorsBase.CreatorsBase):
    def __init__(self, *args, **kwargs):
        super(Group, self).__init__(*args, **kwargs)

    def point_base(self, *scene_nodes, **kwargs):
        super(Group, self).point_base(*scene_nodes, **kwargs)
        """
            type of group can be: "world","child","parent","inserted","sibling"
        """
        group_type = kwargs.pop('type', "inserted")
        name = kwargs.pop('name', None)
        scene_nodes = dataValidators.as_pymel_nodes(scene_nodes)
        new_groups_result = []

        for each_node in scene_nodes:
            new_group = pm.group(empty=True)
            transform.align(each_node, new_group)
            self.setup_name_convention_node_base(each_node, name=name)
            self.name_convention.rename_name_in_format(new_group)

            new_groups_result.append(new_group)

            parent = pm.listRelatives(each_node, parent=True)
            if not (group_type == "world"):
                if group_type == "inserted":
                    if parent:
                        hierarchy.insert_in_hierarchy(each_node, new_group)
                    else:
                        pm.parent(each_node, new_group)
                elif group_type == "parent":
                    pm.parent(each_node, new_group)
                elif group_type == "child":
                    pm.parent(new_group, each_node)
                elif group_type == "sibling":
                    pm.parent(new_group, parent)

        if len(new_groups_result) > 1:
            return new_groups_result
        else:
            return new_groups_result[0]


if __name__ == '__main__':
    groups = Group()
    groups.point_base('C_lasserAimCenter_reference_LOC', type='parent')