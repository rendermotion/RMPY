import pymel.core as pm
from RMPY.rig import rigBase


class RigControlsForPoints(rigBase.RigBase):
    """
       Simple rig class inherits from RigBase, creates a control on each point and parent
       constraints the controls to move the input points
    """
    def __init__(self, *args, **kwargs):
        super(RigControlsForPoints, self).__init__(*args, **kwargs)
        self._model = rigBase.BaseModel()

    def create_point_base(self, *points, **kwargs):
        super(RigControlsForPoints, self).create_point_base(*points, **kwargs)
        world_align = kwargs.pop('world_align', False)

        for each_point in points:
            reset_controls, controls = self.create.controls.point_base(each_point, **kwargs)
            self.reset_controls.append(reset_controls)
            self.controls.append(controls)
            if world_align:
                reset_controls.rotate.set([0, 0, 0])
        self.create.constraint.node_list_base(self.controls, points, mo=True)


if __name__ == '__main__':
    selection = pm.ls(selection=True)
    rig_controls = RigControlsForPoints()
    rig_controls.create_point_base(*selection, world_align=True)




