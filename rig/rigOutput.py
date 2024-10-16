import pymel.core as pm
from RMPY.rig import rigBase
from RMPY.core import config


class OutputModel(rigBase.BaseModel):
    def __init__(self):
        super(OutputModel, self).__init__()
        self.rigs = {}

class RigOutput(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        kwargs['model'] = kwargs.pop('model', OutputModel())
        super(RigOutput, self).__init__(*args, **kwargs)
        base_rig = args[0]
        self.add_rig(base_rig, name='world')
        new_group = pm.group(empty=True)
        base_rig.name_convention.rename_name_in_format(new_group, name='output')
        new_group.setParent(self.rig_system.joints)
        rig_joints=[]
        for index, each in enumerate(base_rig.joints):
            new_joint = pm.joint()
            base_rig.name_convention.rename_name_in_format(new_joint, type='skinjoint')
            rig_joints.append(new_joint)
            if index==0:
                new_joint.setParent(new_group)
            else:
                new_joint.setParent(rig_joints[index-1])
        self.rigs['world']['joints'] = rig_joints

    def add_rig(self, rig_node,  name=''):
        self.rigs[name] = {'rig':rig_node}

    def parent(self, child, parent):
        if not child in self.rigs or not parent in self.rigs:
            print('rig not found')
            return
        rig_joints = []
        for index, each in enumerate(self.rigs[child]['rig'].joints):
            new_joint = pm.joint()
            self.rigs[child]['rig'].name_convention.rename_name_in_format(new_joint, type='skinjoint')
            rig_joints.append(new_joint)
            if index == 0:
                new_joint.setParent(self.rigs[parent]['joints'][-1])
            else:
                new_joint.setParent(rig_joints[index - 1])
            self.create.constraint.matrix_node_base(each, new_joint)
        self.rigs[child]['joints'] = rig_joints



            








if __name__=='__main__':
    pass