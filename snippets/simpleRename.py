from RMPY import nameConvention
import pymel.core as pm
name_conv = nameConvention.NameConvention()
name_conv.default_names['system'] = 'reference'
selection = pm.ls(selection=True)


def rename_selection():
	selection = pm.ls(selection=True)
	fix_shapes(*selection)
	for index, each in enumerate(selection):
		side = 'R'
		system_name = 'reference'
		name = 'grapplinHook'
		# name_conv.rename_name_in_format(each, side=side, system=system_name, name='shoe{}'.format(chr(65+index)))
		# name_conv.rename_name_in_format(each, side=side, system=system_name, name='finger{}'.format(chr(65 + index)))
		name_conv.rename_name_in_format(each, side=side, system=system_name, name=name)
		# name_conv.rename_name_in_format(each, side=side, system=system_name, name='muscle')


def set_in_name():
	selection = pm.ls(selection=True)
	for each in selection:
		name_conv.rename_set_from_name(each, 'R', 'side')


def fix_shapes(*scene_object_list):
	for index, each_object in enumerate(scene_object_list):
		each_object.rename('geometry{}'.format(65+index))
		shapes_list = each_object.getShapes()
		object_name = str(each_object).split('|')[-1]
		for each in shapes_list:
			each.rename('{}Shape'.format(object_name))


# set_in_name()
rename_selection()





