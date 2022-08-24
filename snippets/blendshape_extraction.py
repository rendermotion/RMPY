import pymel.core as pm


def get_blend_shapes_in_history(scene_node):
    history_nodes = pm.listHistory(scene_node, interestLevel=2, pruneDagObjects=True)
    result = []
    for each_node in history_nodes:
        if pm.objectType(each_node) == 'blendShape':
            result.append(each_node)
    return result


def duplicate_targets(prefix):
    geometry_node = pm.ls(selection=True)[0]
    blend_shapes_parent = pm.ls('blendshapes')
    if not blend_shapes_parent:
        blend_shapes_parent = pm.group(empty=True, name='blendshapes')
    else:
        blend_shapes_parent = blend_shapes_parent[0]
    blend_shape = pm.ls(get_blend_shapes_in_history(geometry_node))[0]
    for each in blend_shape.weightIndexList():
        alias_name = pm.listAttr((blend_shape.weight[each]))[0]
        blend_shape.weight[each].set(1)
        new_geo = pm.duplicate(geometry_node)[0]
        if prefix not in 'LR':
            new_geo.rename('{}{}'.format(prefix, alias_name.title()))
        else:
            new_geo.rename('{}{}'.format(prefix, alias_name))

        new_geo.setParent(blend_shapes_parent)
        blend_shape.weight[each].set(0)