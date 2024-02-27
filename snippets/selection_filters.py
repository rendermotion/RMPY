from RMPY.core import search_hierarchy
import pymel.core as pm
selection = pm.ls(selection=True)
result_list = []
for each in selection:
    result_list.extend(search_hierarchy.type_in_hierarchy(each))
pm.select(result_list)


from RMPY.core import search_hierarchy
import pymel.core as pm
selection = pm.ls(selection=True)
result_list = []
for each in selection:
    result_list.extend(search_hierarchy.skinned_mesh_in_hierarchy(each))
pm.select(result_list)


from RMPY.core import search_hierarchy
import pymel.core as pm
selection = pm.ls(selection=True)
result_list = []
for each in selection:
    result_list.extend(search_hierarchy.none_skinned_mesh_in_hierarchy(each))
pm.select(result_list)


from RMPY.core import search_hierarchy
import pymel.core as pm
selection = pm.ls(selection=True)
result_list = []
for each in selection:
    result_list.extend(search_hierarchy.by_token_in_name(each, '_ctl'))
pm.select(result_list)




