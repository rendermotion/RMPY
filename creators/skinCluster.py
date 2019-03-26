import pymel.core as pm
from RMPY.nameConvention import NameConvention


def get_from_node(node):
    """:returns a skin cluster asociated with the node"""
    history_nodes = pm.listHistory(node, interestLevel=2)

    for each in history_nodes:
        if each.__class__ == pm.nodetypes.SkinCluster:
            return each
    return None


class Creator():
    def __init__(self):
        self.name_conv = NameConvention()

    def create_from_skin(self, source, *destination):
        skin_cluster_node = get_from_node(source)
        if skin_cluster_node:
            list_joints = skin_cluster_node.influenceObjects()
            if destination:
                for each_node in destination:
                    new_skin_cluster = pm.skinCluster(list_joints, each_node)
                    self.name_conv.rename_name_in_format(new_skin_cluster,
                                                         name=self.name_conv.get_a_short_name(each_node))
                    pm.copySkinWeights(source, destination, influenceAssociation=['label', 'name',
                                                                                  'closestJoint', 'oneToOne'])

if __name__ == '__main__':
    selection = pm.ls(selection=True)
    skin_cluster = Creator()
    print skin_cluster.copy_skin(selection[0], selection[1])


