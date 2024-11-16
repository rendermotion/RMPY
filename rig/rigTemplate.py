from RMPY.rig import rigBase


class TemplateModel(rigBase.BaseModel):
    def __init__(self):
        super(TemplateModel, self).__init__()
        self.geometry='pCube1'


class TemplateRig(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', TemplateModel())
        super(TemplateRig, self).__init__(*args, **kwargs)


if __name__=='__main__':
    my_rig = TemplateRig()
    print(my_rig.geometry)