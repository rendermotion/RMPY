from RMPY.creators import curve as CurveCreator
from RMPY.creators import spaceLocator
from RMPY.creators.skinCluster import SkinCluster
from RMPY.creators import group as groupCreator
from RMPY.creators import joint as jointCreator
from RMPY.creators import connect as connectCreator

curve = CurveCreator.Curve()
space_locator = spaceLocator.SpaceLocator()
skin_cluster = SkinCluster()
group = groupCreator.Group()
joint = jointCreator.Joint()
connect = connectCreator.Connect()

creators_list = [curve, space_locator, skin_cluster, group, joint, connect]





