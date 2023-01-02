from RMPY.rig import rigFK
import pymel.core as pm
from RMPY.core import rig_core as rm


class Finger(rigFK.RigFK):
    def __init__(self, *args, **kwargs):
        super(Finger, self).__init__(*args, **kwargs)

    def create_point_base(self, *args, **kwargs):
        orient_type = kwargs.pop('orient_type', 'point_orient')
        kwargs['orient_type'] = orient_type
        super(Finger, self).create_point_base(*args, **kwargs)


if __name__ == '__main__':
    root_finger = pm.ls('L_index01_reference_pnt')[0]
    finger_points = rm.descendents_list(root_finger)
    finger = Finger()
    finger.create_point_base(*finger_points)
