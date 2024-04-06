import pymel.core as pm
from RMPY import RMRigTools


def oposite(scene_object):
    if scene_object.__class__ is list:
        return_list = True
    else:
        return_list = False
        scene_object = [scene_object]
    object_result = []
    for each_object in scene_object:
        tokens = each_object.split('|')
        result_token = []
        for each_token in tokens:
            oposite = get_oposite(each_token)
            if oposite:
                result_token.append(oposite)
            else:
                result_token.append(each_token)
        object_result.append('|'.join(result_token))
    return object_result


def get_oposite(scene_object):
    if scene_object.__class__ is list:
        return_list = True
    else:
        return_list = False
        scene_object = [scene_object]
    result_list = []
    for each_object in scene_object:
        each_object = RMRigTools.validate_pymel_nodes(each_object)
        namespace_tokens = each_object.split(':')
        if len(namespace_tokens) > 1:
            namespace = '%s:' % namespace_tokens[0]
            splitName = namespace_tokens[1]
        else:
            namespace = ''
            splitName = str(each_object)

        token_list = splitName.split('_')
        if token_list[1] in ['FR', 'MR', 'BR', 'FL','ML', 'BL', 'C', 'R','L']:
            if 'L' in token_list[1]:
                token_list[1] = token_list[1].replace('L', 'R')
            else:
                if 'R' in token_list[1]:
                    token_list[1] = token_list[1].replace('R', 'L')
            if pm.objExists('%s%s' % (namespace, '_'.join(token_list))):
                result_list.append(RMRigTools.validate_pymel_nodes('%s%s' % (namespace, '_'.join(token_list))))
            else:
                print ('no oposite found for object {}'.format(each_object))
        else:
            if token_list[0] in ['FR', 'MR', 'BR', 'FL', 'ML', 'BL', 'C', 'R', 'L']:
                if 'L' in token_list[0]:
                    token_list[0] = token_list[0].replace('L', 'R')
                else:
                    if 'R' in token_list[0]:
                        token_list[0] = token_list[0].replace('R', 'L')
                if pm.objExists('%s%s' % (namespace, '_'.join(token_list))):
                    result_list.append(RMRigTools.validate_pymel_nodes('%s%s' % (namespace, '_'.join(token_list))))
                else:
                    print ('no oposite found for object {}'.format(each_object))
    if return_list:
        return result_list
    else:
        if len(result_list) == 1:
            return result_list[0]
        else:
            return None


def get_skinCluster(skined_geometry):
    for each in pm.listHistory(skined_geometry, interestLevel=2, pruneDagObjects=True):
        if each.__class__ == pm.nodetypes.SkinCluster:
            return each


def mirror_skinBinding(scene_objects):
    for each_object in scene_objects:
        current_tokens = each_object.split('_')
        if current_tokens[0] in ['FR', 'MR', 'BR', 'R']:
            mirror_inverse = True
        else:
            mirror_inverse = False

        skin_cluster = get_skinCluster(each_object)
        if skin_cluster:
            skin_joints = get_oposite(skin_cluster.influenceObjects())
            oposite_object = get_oposite(each_object)
            if not get_skinCluster(oposite_object):
                destination_skin_cluster = pm.skinCluster(skin_joints, oposite_object, bindMethod=0, toSelectedBones=True)
                pm.copySkinWeights(ss=skin_cluster, ds=destination_skin_cluster, mirrorMode='YZ',
                                   influenceAssociation='oneToOne', mirrorInverse=mirror_inverse)
                destination_skin_cluster.skinningMethod.set(skin_cluster.skinningMethod.get())
            else:
                print ('object %s not processed, already skin cluster attached'.format(oposite_object))


def copy_mirror_skin_binding(source, destination):
    """
    :param source: the source object from where the skinning will be copied
    :param destination:
    :return:
    """
    mirror_inverse = True
    print('copying from {} to {}'.format(source, destination))
    skin_cluster = get_skinCluster(source)
    if skin_cluster:
        skinJoints = get_oposite(skin_cluster.influenceObjects())
        oposite_object = destination
        if not get_skinCluster(oposite_object):
            destination_skinCluster = pm.skinCluster(skinJoints, oposite_object, bindMethod=0, toSelectedBones=True)
            pm.copySkinWeights(ss=skin_cluster, ds=destination_skinCluster, mirrorMode='YZ',
                               influenceAssociation='oneToOne', mirrorInverse=mirror_inverse)
            destination_skinCluster.skinningMethod.set(skin_cluster.skinningMethod.get())
        else:
            print ('object {} not processed, allready skin cluster attached'.format(oposite_object))
    else:
        print("Did'nt find skinCluster in source object")


def copy_skin_binding_structure(source, destination):
    match_structure = []
    # analysis.Main(source, destination)
    from pprint import pprint as pp
    pp(match_structure)
    done = 'coping from to:\n'
    for each_object in match_structure.match_dictionary:
        skin_cluster = get_skinCluster(each_object)
        if skin_cluster:
            skin_joints = skin_cluster.influenceObjects()
            new_skin = pm.skinCluster(skin_joints, match_structure.match_dictionary[each_object],
                                      bindMethod=0, toSelectedBones=True)
            pm.copySkinWeights(sourceSkin=skin_cluster, destinationSkin=new_skin, surfaceAssociation='closestPoint',
                               noMirror=True)
            done += '%s -> %s\n' % (each_object, match_structure.match_dictionary[each_object])
    print(done)


def copy_skin_binding(source_object, destination_object):
    skin_cluster = get_skinCluster(source_object)
    if skin_cluster:
        skin_joints = skin_cluster.influenceObjects()
        dest_skin = get_skinCluster(destination_object)
        if dest_skin:
            pm.delete(dest_skin)
        new_skin = pm.skinCluster(skin_joints, destination_object, bindMethod=0, toSelectedBones=True)
        pm.copySkinWeights(sourceSkin=skin_cluster, destinationSkin=new_skin, surfaceAssociation='closestPoint',
                           influenceAssociation=['label', 'name', 'oneToOne'],
                           noMirror=True)
    print ('{} -> {}\n'.format(source_object, destination_object))


def change_skinning_method(object_list):
    # for each_object in object_list:
    #     skin = get_skinCluster(each_object)[0]
        # set_value = not skin.skinningMethod.get()
    for each in object_list:
        skin = get_skinCluster(each)
        # skin.skinningMethod.set(set_value)
        skin.weightDistribution.set(1)


def copy_skinning(*scene_objects):
    for each in scene_objects[1:]:
        copy_skin_binding(scene_objects[0], each)


if __name__ == '__main__':
 selection = pm.ls(selection=True)
 copy_skinning(*selection)
 # change_skinning_method(selection)
 # print oposite(selection[0])
 # change_skining_method(selection)
 # mirror_skinBinding(selection)
 # copy_skinBinding_sturcture()
 # copy_mirror_skin_binding(selection[0], selection[1])

 # matchStructure = analysis.Main(selection[0], selection[1])

