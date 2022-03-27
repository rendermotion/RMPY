import pymel.core as pm
from RMPY.rig import rigBase


class RigControlsForPoints(rigBase.RigBase):
    """
       Simple rig class inherits from RigBase, creates a control on each point and parent
       constraints the controls to move the input points
    """
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model',  rigBase.BaseModel())
        super(RigControlsForPoints, self).__init__(*args, **kwargs)

    def create_point_base(self, *points, **kwargs):
        super(RigControlsForPoints, self).create_point_base(*points, **kwargs)
        world_align = kwargs.pop('world_align', False)
        link_type = kwargs.pop('link_type', 'standard')

        for each_point in points:
            reset_control, control = self.create.controls.point_base(each_point, **kwargs)
            self.reset_controls.append(reset_control)
            self.controls.append(control)
            if world_align:
                reset_control.rotate.set([0, 0, 0])

        if link_type == 'standard':
            self.create.constraint.node_list_base(self.controls, points, parent=True, mo=True)
        elif link_type == 'static':
            for each_control, point in zip(self.controls, points):
                each_control.translate >> point.translate
                each_control.rotate >> point.rotate
                each_control.scale >> point.scale
        else:
            print 'unknown link type {}'.format(link_type)


if __name__ == '__main__':
    selection = pm.ls(selection=True)
    rig_controls = RigControlsForPoints()
    rig_controls.create_point_base(*selection, world_align=True)




