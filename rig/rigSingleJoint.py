import pymel.core as pm
from RMPY import nameConvention
from RMPY import RMRigTools
from RMPY.rig import rigBase
from RMPY.rig import systemStructure
from RMPY import RMRigShapeControls


class ModelSingleJoint(rigBase.BaseModel):
    def __init__(self):
        super(ModelSingleJoint, self).__init__()


class RigSingleJoint(rigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(RigSingleJoint, self).__init__(*args, ** kwargs)
        self.system = None

        self.control_shapes = RMRigShapeControls.RMRigShapeControls()

    def create_point_base(self, *locatorList, **kwargs):
        static = kwargs.pop('static', False)
        scaleXZ = kwargs.pop('scaleXZ', False)
        self.system = systemStructure.SystemStructure(locatorList[0])
        for each in locatorList:
            reset_joint = pm.group(empty=True, name='resteJoint')
            RMRigTools.RMAlign(each, reset_joint, 3)
            joint = pm.joint(name='joint')
            RMRigTools.RMAlign(joint, reset_joint, 3)

            self.joints.append(joint)
            self.system.name_conv.rename_name_in_format(reset_joint)
            self.system.name_conv.rename_name_in_format(joint)

            joint.setParent(reset_joint)
            reset_control, control = self.control_shapes.RMCreateBoxCtrl(joint, centered=True)
            reset_control.setParent(self.system.controls)
            reset_joint.setParent(self.system.joints)
            if static:
                control.translate >> joint.translate
                control.rotate >> joint.rotate
            else:
                pm.parentConstraint(control, joint)

            if scaleXZ:
                pm.addAttr(control, longName='scaleXZ', at=float, k=True)
                control.scaleXZ.set(1)
                control.scaleXZ >> control.scaleX
                control.scaleXZ >> control.scaleZ
                control.scaleXZ >> joint.scaleX
                control.scaleXZ >> joint.scaleZ


if __name__ == '__main__':
    selection = pm.ls(selection=True)
    rigjoint =RigSingleJoint()
    rigjoint.create_locator_base(*selection, static=True, scaleXZ=True)









