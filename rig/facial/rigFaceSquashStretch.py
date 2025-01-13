# a specific squash and stretch rig for the face.
from RMPY.rig import rigBase


class FaceSquashStretchModel(rigBase.BaseModel):
    def __init__(self):
        super(FaceSquashStretchModel, self).__init__()
        self.curve = None


class RigFaceSquashStretch(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', FaceSquashStretchModel())
        super(RigFaceSquashStretch, self).__init__(*args, **kwargs)

    def create_point_base(self, *points, **kwargs):
        super(RigFaceSquashStretch, self).create_point_base(*points, **kwargs)
        self.create.curve.point_base(*points, degree=2,)





if __name__=='__main__':
    my_rig = RigFaceSquashStretch()
    print(my_rig.geometry)