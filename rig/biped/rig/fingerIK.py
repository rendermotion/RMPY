from RMPY.rig import rigSimpleIk
import pymel.core as pm
from RMPY.core import main as rm
reload(rigSimpleIk)


class Finger(rigSimpleIk.SimpleIK):
    def __init__(self, *args, **kwargs):
        super(Finger, self).__init__(*args, **kwargs)

    def create_point_base(self, *args, **kwargs):
        # orient_type = kwargs.pop('orient_type', 'point_orient')
        # kwargs['orient_type'] = orient_type
        super(Finger, self).create_point_base(*args, **kwargs)
        self.create_pole_vector()
        self.create_controls()


if __name__ == '__main__':
    root_finger = pm.ls('L_index01_reference_pnt')[0]
    finger_points = rm.descendents_list(root_finger)
    finger = Finger()
    finger.create_point_base(*finger_points)
