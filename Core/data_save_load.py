from RMPY.representations import curve
from RMPY.creators import skinCluster
import pymel.core as pm
from RMPY.core import config
import os


def save_curve(*args):
    """
    :param args: the scene objects that will be saved if nothing is provide it it will try to save the selection.
    :return:
    """
    if args:
        scene_curves = args
    else:
        scene_curves = pm.ls(selection=True)
    saved_curves_list = []
    for each in scene_curves:
        try:
            if pm.objExists(each):
                curve_node = curve.Curve.by_name(each)
                curve_node.save()
                saved_curves_list.append(each)
            else:
                print "the curve {} doesn't exists".format(each)
        except RuntimeWarning('{} not saved'.format):
            pass
    print 'following curves where saved: {}'.format(saved_curves_list)


def load_curves(*args):
    """
        :param args: the scene objects that will be loaded if nothing is provide it it will try to load the selection.
        :return:
        """
    if args:
        scene_curves = args
    else:
        scene_curves = pm.ls(selection=True)

    for each in scene_curves:
        try:
            if pm.objExists(each):
                curve_node = curve.Curve.by_name(each)
                curve_node.load()
                curve_node.set_repr_dict()
            else:
                print "the curve {} doesn't exists".format(each)
        except RuntimeWarning('{} not loaded'.format):
            pass


def save_skin_cluster(*args):
    if args:
        scene_objects = args
    else:
        scene_objects = pm.ls(selection=True)

    saved_skin_cluster_list = []
    for each_node in scene_objects:
        try:
            skin_cluster01 = skinCluster.SkinCluster.by_node(each_node)
            if skin_cluster01:
                skin_cluster01.save('{}'.format(each_node))
                saved_skin_cluster_list.append(each_node)
            else:
                print "object {} does'nt have a skincluster".format(each_node)
        except RuntimeWarning('{} not saved'.format(each_node)):
            pass
    print 'following skin in nodes where saved: {}'.format(saved_skin_cluster_list)


def load_skin_cluster(*args):
    if args:
        scene_objects = args
    else:
        scene_objects = pm.ls(selection=True)

    for each_node in scene_objects:
        try:
            skin_cluster01 = skinCluster.SkinCluster()
            skin_cluster01.load('{}'.format(each_node))
            skin_cluster01.apply_weights_dictionary(geometry=each_node)
        except RuntimeWarning('{} not loaded'.format(each_node)):
            pass


def export_maya_file(**kwargs):
    file_name = kwargs.pop('file_name', 'reference_points')
    full_path = '{}/mayaFiles'.format(config.file_path)
    pm.exportSelected('{}/{}.ma'.format(full_path, file_name))


def import_maya_file(file_name):
    full_path = '{}/mayaFiles'.format(config.file_path)
    pm.importFile('{}/{}.ma'.format(full_path, file_name))


def import_all_available_maya_files():
    for each in available_maya_files():
        import_maya_file(each)


def available_maya_files():
    full_path = '{}/mayaFiles'.format(config.file_path)
    available_files = []
    for each in os.listdir(full_path):
        if '.ma' in each:
            available_files.append(each)
    return each


if __name__ == '__main__':
    save_curve()
