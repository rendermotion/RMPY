from RMPY.rig import rigFK
import pymel.core as pm


class ClavicleModel(rigFK.RigFKModel):
    def __init__(self, *args, **kwargs):
        super(ClavicleModel, self).__init__(*args, **kwargs)


class Clavicle(rigFK.RigFK):
    def __init__(self, *args, **kwargs):
        super(Clavicle, self).__init__(*args, **kwargs)

    def create_point_base(self, *args, **kwargs):
        super(Clavicle, self).create_point_base(*args, **kwargs)


if __name__ == '__main__':
    neck_points = pm.ls(u'R_clavicle01_reference_pnt', u'R_shoulder01_reference_pnt')
    neck_head = Clavicle()
    neck_head.create_point_base(*neck_points)

    neck_points = pm.ls(u'L_clavicle01_reference_pnt', u'L_shoulder01_reference_pnt')
    neck_head = Clavicle()
    neck_head.create_point_base(*neck_points)
