import maya.cmds
import maya.api.OpenMaya as om
import RMNameConvention
reload(RMNameConvention)
import RMRigTools


class RMSpaceSwitch(object):
    def __init__(self,NameConv = None):
        if not NameConv:
            self.NameConv = RMNameConvention.RMNameConvention()
        else:
            self.NameConv = NameConv
    def CreateSpaceSwitchReverse(self,AfectedObject, SpaceObjects, ControlObject, Name = "spaceSwitch", sswtype = "enum"):
        if sswtype == "enum" and len(SpaceObjects) == 2:
            self.AddEnumParameter(SpaceObjects, ControlObject, Name = Name)

            reverse = cmds.shadingNode('reverse', asUtility=True, name = Name + "SWReverse")
            cmds.connectAttr(ControlObject + "." + Name, reverse + ".inputX")
            
            for eachObject in SpaceObjects:

                parentConstraint = cmds.parentConstraint (eachObject, AfectedObject, mo = True, name = AfectedObject + "SpaceSwitchConstraint")
            
            if self.NameConv.RMIsNameInFormat(AfectedObject):
                reverse = self.NameConv.RMRenameBasedOnBaseName(AfectedObject,reverse, NewName = reverse)
                parentConstraint[0] = self.NameConv.RMRenameBasedOnBaseName(AfectedObject,reverse, NewName = parentConstraint[0])

            else:
                reverse = self.NameConv.RMRenameNameInFormat(reverse)
                parentConstraint[0] = self.NameConv.RMRenameNameInFormat(parentConstraint[0])

            WA = cmds.parentConstraint (parentConstraint, q = True, weightAliasList = True)
            cmds.connectAttr(ControlObject + "." + Name, parentConstraint[0] + "." + WA[1])
            cmds.connectAttr(reverse + ".outputX", parentConstraint[0] + "." + WA[0])

    def CreateSpaceSwitch(self,AfectedObject, SpaceObjects, ControlObject, Name = "spaceSwitch", sswtype = "enum"):
        if sswtype == "enum":
            self.AddEnumParameter(SpaceObjects, ControlObject, Name = Name)
            index = 0
            for eachObject in SpaceObjects:
                parentConstraint = cmds.parentConstraint (eachObject, AfectedObject, mo = True, name = AfectedObject + "SpaceSwitchConstraint")
                Switch = cmds.shadingNode('condition', asUtility=True, name = Name + "SWCondition")
                cmds.connectAttr(ControlObject + "." + Name, Switch + ".firstTerm")
                cmds.setAttr (Switch +".secondTerm", index)
                cmds.setAttr (Switch +".operation", 0)
                cmds.setAttr (Switch +".colorIfTrueR", 1)
                cmds.setAttr (Switch +".colorIfFalseR", 0)
                WA = cmds.parentConstraint (parentConstraint, q = True, weightAliasList = True)
                cmds.connectAttr (Switch + ".outColorR", parentConstraint[0] + "." + WA[index])
                if self.NameConv.RMIsNameInFormat(AfectedObject):
                    Switch = self.NameConv.RMRenameBasedOnBaseName(AfectedObject, Switch, NewName = Switch)
                else:
                    Switch = self.NameConv.RMRenameNameInFormat(Switch)
                index += 1
            
            if self.NameConv.RMIsNameInFormat(AfectedObject):
                parentConstraint[0] = self.NameConv.RMRenameBasedOnBaseName(AfectedObject,reverse, NewName = parentConstraint[0])
            else:
                parentConstraint[0] = self.NameConv.RMRenameNameInFormat(parentConstraint[0])
    

    def AddNumericSpaceSwitch(self,Object, Name = 'spaceSwitch', valueRange = [0,10]):
        AttributeList = cmds.listAttr(Object)
        if Name  in AttributeList:
            print "the Object Allready has an Attribute with this name, the type is:",cmds.getAttr (Object + "." + Name,type=True)
        else :
            cmds.addAttr(Object,at="float", ln = Name,  hnv = 1, hxv = 1, h = 0, k = 1, smn = valueRange[0], smx = valueRange[1])



    def AddEnumParameter(self, Enum, Object, Name = 'spaceSwitch'):
        AttributeList = cmds.listAttr(Object)
        if Name  in AttributeList:
            if cmds.getAttr (Object + "." + Name,type=True)=='enum':
                print "the Object Allready has an spaceSwitch"
                print "Current Valid types are",cmds.addAttr (Object + "." + Name,q = True,enumName=True)
            return False
        else :
            Enumlist = []
            for objects in Enum:
                if self.NameConv.RMIsNameInFormat()

            cmds.addAttr(Object, at = "enum" , ln = Name , k = 1, en =":".join(Enum))
        return True

cmds.deleteAttr('pCube1',at = 'spaceSwitch')


cmds.
SW = RMSpaceSwitch()
SW.CreateSpaceSwitch('group1',['pSphere1','pSphere2'], 'pCube1')




