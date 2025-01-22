from RMPY.rig import rigBase


class RigTemplateModel(rigBase.BaseModel):
    def __init__(self):
        super(RigTemplateModel, self).__init__()
        self.geometry = 'pCube1'


class RigTemplate(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', RigTemplateModel())
        super(RigTemplate, self).__init__(*args, **kwargs)


if __name__ == '__main__':
    my_rig = RigTemplate()
    print(my_rig.geometry)