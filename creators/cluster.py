import pymel.core as pm
from RMPY.creators import creatorsBase


class Cluster(creatorsBase.CreatorsBase):
    def __init__(self, *args, **kwargs):
        super(Cluster, self).__init__(*args, **kwargs)

    def curve_base(self, *args, **kwargs):
        super(Cluster, self).curve_base(*args, **kwargs)
        self.name_convention.default_names['name'] = kwargs.pop('name', 'clusterOnCurve')
        curve = pm.ls(*args)[0]
        node_list = []
        handle_list = []
        for each_cv in range(curve.numCVs()):
            cluster_node, cluster_handle = pm.cluster(curve.cv[each_cv], relative=True)
            self.name_convention.rename_name_in_format([cluster_node, cluster_handle])
            cluster_set = pm.listConnections(cluster_node, type="objectSet")[0]
            if len(args) > 1:
                for each_curve in args[1:]:
                    pm.sets(cluster_set, add="{}.cv[{}]".format(each_curve, str(each_cv)))
            node_list.append(cluster_node)
            handle_list.append(cluster_handle)
        return node_list, handle_list


if __name__ == '__main__':
    Cluster().curve_base('C_lineBetween01_rig_shp', 'C_lineBetween02_rig_shp')


