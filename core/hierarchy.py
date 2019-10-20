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


if __name__ == '__main__':
    insert_in_hierarchy('R_arm00_reference_GRP', 'null1', insert_type='children')