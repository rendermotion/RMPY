from RMPY.core import dataValidators
import pymel.core as pm


def insert_in_hierarchy(base_object, insert_object, insert_type="parent"):
    base_object = dataValidators.as_pymel_nodes(base_object)
    insert_object = dataValidators.as_pymel_nodes(insert_object)
    if insert_type == "parent":
        parent = base_object.getParent()
        if parent:
            pm.parent(insert_object, parent)
        pm.parent(base_object, insert_object)
    else:
        children = base_object.getChildren()
        pm.parent(insert_object, base_object)
        pm.parent(children, insert_object)


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


if __name__ == '__main__':
    selection = pm.ls(selection=True)
    reorder_hierarchy(*selection)
    # insert_in_hierarchy('R_arm00_reference_GRP', 'null1', insert_type='children')