#!/usr/bin/env python
# -*- coding: utf-8 -*- 
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
        r"""
        This function will create a new group per each scene node provided, this new node will be aligned in position and rotation, with the scene node.
        And its position on the hierarchy will depend on the "type" kwargs.
        :param scene_nodes:
            One or more nodes on the scene. This nodes can be strings or pymel nodes.
        :type scene_nodes: ``str``
        :param **kwargs:
            See below
        :Keword Arguments:
            * *type* (``str``)--
                A parameter to define how the new group is going to be
                in the hierarchy, valid values are
                "world","child","parent","inserted","sibling".
                Default value is inserted, meaning that the new group will be inserted on the hierarchy as parent of the nodes provided.
        """
        super(Group, self).point_base(*scene_nodes, **kwargs)
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
    groups.point_base('C_testPoint_reference_LOC', type='inserted')