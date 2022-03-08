from RMPY.core import dataValidators
import pymel.core as pm


def insert_in_hierarchy(base_object, insert_object, insert_type="parent"):
    base_object = dataValidators.as_pymel_nodes(base_object)
    insert_object = dataValidators.as_pymel_nodes(insert_object)
    if insert_type == "parent":
        parent = base_object.getParent()
        if parent:
            pm.parent(insert_object, parent)
            # fix scale in case the parent is scaled we want it affected by the scale
            insert_object.scale.set(1, 1, 1)
        pm.parent(base_object, insert_object)
    else:
        children = base_object.getChildren()
        pm.parent(insert_object, base_object)
        pm.parent(children, insert_object)


def find_in_hierarchy(scene_object, grandson):
    return_array = [scene_object]
    if scene_object == grandson:
        return return_array
    all_descendents = pm.listRelatives(scene_object, allDescendents=True)
    if all_descendents:
        if grandson in all_descendents:
            children = pm.listRelatives(scene_object, children=True)
            if children:
                for eachChildren in children:
                    family = find_in_hierarchy(eachChildren, grandson)
                    return_array.extend(family)
                return return_array
    return []


def descendents_list(transform_node):
    result_list = pm.listRelatives(transform_node, type='transform', allDescendents=True)
    result_list = list(reversed(result_list))
    result_list.insert(0, transform_node)
    return result_list


def reorder_hierarchy(*objects_list):
    objects_list = pm.ls(objects_list)
    if objects_list[0] == objects_list[1].getParent():
        pm.parent(objects_list[1:], objects_list[0].getParent())
    else:
        for index, each_object in enumerate(objects_list[1:]):
            each_object.setParent(objects_list[index])


def custom_pick_walk(transform_node, depth, maya_node_type='joint', direction="down"):
    """
    :param transform_node: The node where the search in the hierarchy will start
    :param depth: how many children or parents should look for.

    :param direction: Valid values of Direction ar up and down, defines if the search will happen on the children or in the
                parents of the transform_node object up/parents down/childrens.
    :param maya_node_type: the type of maya node where the search will ocurre .

    :returns: a list of objects that are in the hierarchy as parents or childs, from transform_node object.

    """

    if direction == "down":
        childs = pm.listRelatives(transform_node, children=True, type=maya_node_type)
    else:
        childs = pm.listRelatives(transform_node, parent=True, type=maya_node_type)

    return_value = [transform_node]
    if childs:
        if not (depth == 0 or len(childs) == 0):
            for eachChildren in childs:
                if pm.nodeType(eachChildren) == maya_node_type:
                    return_value.extend(custom_pick_walk(eachChildren,depth - 1,  maya_node_type=maya_node_type, direction=direction))
    return return_value


if __name__ == '__main__':
    selection = pm.ls(selection=True)
    reorder_hierarchy(*selection)
    # insert_in_hierarchy('R_arm00_reference_GRP', 'null1', insert_type='children')