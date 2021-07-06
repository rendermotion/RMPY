import pymel.core as pm
from RMPY.rig import rigBase


class AttributeSplit(rigBase.RigBase):
    """
    Splits an attribute in two by an attribute value
    it has two inputs the attribute_split (the attribute that will be splited) and the attribute_compare
    the attribute that will compare with the other ones to create the main rotation.
    there are two outputs, the output_attribute_a, and the output_attribute_b

    If attribute split is under attribute compare, output_attribute_a will be equal to attribute_split,
    and output_attribute_b will be 0
    if it is greater output_attribute_a will be equal to attribute_split
    and output_attribute_b will be equal to the difference of attribute_split minus attribute_compare
    """

    def __init__(self, *args, **kwargs):
        super(AttributeSplit, self).__init__(*args, **kwargs)
        self.output_attribute_a = []
        self.output_attribute_b = []
        self.settings_group = None
        self.condition = None

    def create_attributes_based(self, attribute_split, attribute_compare, name='split'):
        pm.select(clear=True)
        self.settings_group = pm.group(name=name)
        self.name_convention.rename_name_in_format(self.settings_group, useName=True)
        self.settings_group.setParent(self.rig_system.kinematics)
        self.settings_group.addAttr('output01', at=float, k=True)
        self.output_attribute_a = self.settings_group.output01
        self.settings_group.addAttr('output02', at=float, k=True)
        self.output_attribute_b = self.settings_group.output02

        self.condition = pm.createNode('condition')
        self.name_convention.rename_name_in_format(self.condition, name=name)

        attribute_split >> self.condition.firstTerm
        attribute_compare >> self.condition.secondTerm
        attribute_compare >> self.condition.colorIfTrueR
        attribute_split >> self.condition.colorIfFalseR

        self.condition.outColorR >> self.output_attribute_a
        self.condition.operation.set(2)

        attribute_split >> self.condition.colorIfTrueG
        addition = pm.ls(self.create.connect.attributes(attribute_compare, self.condition.colorIfTrueG))[0]

        self.condition.colorIfFalseG.set(0)
        addition.operation.set(2)
        self.condition.outColorG >> self.output_attribute_b