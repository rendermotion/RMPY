import pymel.core as pm
from RMPY import nameConvention


def get_from_node(node):
    """:returns a skin cluster asociated with the node"""
    history_nodes = pm.listHistory(node, interestLevel=2)

    for each in history_nodes:
        if each.__class__ == pm.nodetypes.SkinCluster:
            return each
    return None


class Creator():
    def __init__(self):
        self.name_conv = nameConvention.NameConvention()

    def create_from_skin(self, *args):
        """
        Creator that generates an skin cluster, you can copy the skining between diferent meshes
        only by providing the meshes.\n
        :args[0] the source mehs, this geo \n
        :args[1:] the destination  mehs where the skin will be copied\n
        :return a list with all the skin clusters that where created during execution
        """
        source = args[0]
        destination = args[1:]
        skin_cluster_node = get_from_node(source)
        skin_cluster_list = []
        if skin_cluster_node:
            list_joints = skin_cluster_node.influenceObjects()
            if destination:
                for each_node in destination:
                    new_skin_cluster = pm.skinCluster(list_joints, each_node)
                    skin_cluster_list.append(new_skin_cluster)
                    self.name_conv.rename_name_in_format(new_skin_cluster,
                                                         name=self.name_conv.get_a_short_name(each_node))
                    pm.copySkinWeights(source, destination, influenceAssociation=['label', 'name',
                                                                                  'closestJoint', 'oneToOne'])
        return new_skin_cluster

if __name__ == '__main__':
    selection = pm.ls(selection=True)
    skin_cluster = Creator()
    print skin_cluster.copy_skin(selection[0], selection[1])
