import pymel.core as pm
from RMPY.rig.biped.rig import clavicle


neck_points = pm.ls(u'R_clavicle01_reference_pnt', u'R_shoulder01_reference_pnt')
neck_head = clavicle.Clavicle()
print neck_points
neck_head.create_point_base(*neck_points)

neck_points = pm.ls(u'L_clavicle01_reference_pnt', u'L_shoulder01_reference_pnt')
neck_head = clavicle.Clavicle()
neck_head.create_point_base(*neck_points)
