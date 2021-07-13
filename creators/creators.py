from RMPY.creators import curve as CurveCreator
from RMPY.creators import spaceLocator
from RMPY.creators.skinCluster import SkinCluster
from RMPY.creators import group as groupCreator
from RMPY.creators import joint as jointCreator
from RMPY.creators import connect as connectCreator
from RMPY.creators import controls as controlsCreator
from RMPY.creators import constraint as constraintCreator
from RMPY.creators import cluster as clusterCreator
from RMPY.creators import follicle as follicleCreator
from RMPY.creators import motionPath as motionPathCreator

constraint = constraintCreator.Constraint()
controls = controlsCreator.Controls()
cluster = clusterCreator.Cluster()
curve = CurveCreator.Curve()
space_locator = spaceLocator.SpaceLocator()
skin_cluster = SkinCluster()
group = groupCreator.Group()
joint = jointCreator.Joint()
connect = connectCreator.Connect()
motion_path = motionPathCreator.MotionPath()
follicle = follicleCreator.Follicle()

creators_list = [follicle, constraint, cluster, curve, space_locator, skin_cluster,
                 group, joint, connect, controls, motion_path]





