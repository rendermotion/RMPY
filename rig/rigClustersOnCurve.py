import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel
from RMPY.rig import rigBase
from RMPY.core import config
from RMPY.core import transform


class RigClustersOnCurve(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(RigClustersOnCurve, self).__init__(*args, **kwargs)

    def create_curve_base(self, *curve):
        if type(curve) in [list, tuple]:
            master_curve = self.rm.dataValidators.as_pymel_nodes(curve[0])[0]
            mode = "multi"
        else:
            master_curve = self.rm.dataValidators.as_pymel_nodes(curve)[0]
            mode = "single"
        degree = pm.getAttr('%s.degree' % master_curve)
        spans = pm.getAttr('%s.spans' % master_curve)
        form = pm.getAttr('%s.form' % master_curve)
        #   form (open = 0, closed = 1, periodic = 2)

        cluster_list = []
        if form == 0 or form == 1:
            # print "Open Line"
            for i in range(0, (degree + spans)):
                cluster_node, cluster_transform = pm.cluster(master_curve + ".cv[" + str(i) + "]",
                                                             name='ClusterOnCurve')
                self.name_convention.rename_name_in_format(cluster_node, cluster_transform, useName=True)
                if mode == "multi":
                    self.add_to_cluster(i, curve[1:], cluster_node)
                cluster_list.append(cluster_transform)
                pm.setAttr(cluster_transform.visibility, 0)
                ##pm.cluster(cluster,edit=True,geometry = curve + ".["+str(i)+"]")
        if form == 2:
            # print "periodic Line"
            for i in range(0, spans):
                cluster_node, cluster_transform = pm.cluster(master_curve + ".cv[" + str(i) + "]",
                                                             name='ClusterOnCurve')
                self.name_conv.rename_name_in_format([str(cluster_node), str(cluster_transform)], useName=True)
                if mode == "multi":
                    self.add_to_cluster(i, curve[1:], cluster_node)
                cluster_list.append(cluster_transform)
                pm.setAttr(cluster_transform.visibility, 0)
                # pm.cluster(cluster,edit=True,geometry = curve + ".["+str(i)+"]")
        self.clusters = cluster_list
        return cluster_list

    def add_to_cluster(self, cv_index, membership_list, cluster):
        cluster_set = pm.listConnections(cluster, type="objectSet")
        for eachShape in membership_list:
            # pm.cluster(cluster, edit=True, geometry = eachShape + ".cv["+str(cvIndex)+"]" )
            pm.sets(cluster_set[0], add="{}.cv[{}]".format(eachShape, str(cv_index)))
