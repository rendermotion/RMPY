import maya.cmds as cmds
from RMPY import RMNameConvention
from RMPY import RMRigTools


class RMVisibilitySwitch(object):
    def __init__(self, NameConv=None):
        if not NameConv:
            self.NameConv = RMNameConvention.RMNameConvention()
        else:
            self.NameConv = NameConv
        self.ControlObject = None
        self.AfectedObjectList = []

    def getControlEnums(self, Node, attribute='Visibility'):
        '''
        returns all the enums in an object attribute 
        '''
        AttributeList = cmds.listAttr(Node)
        if attribute in AttributeList:
            if cmds.getAttr(Node + "." + attribute, type=True) == 'enum':
                ValidValues = cmds.addAttr(Node + "." + attribute, q=True, enumName=True)
                ValidValuesList = ValidValues.split(":")
                return ValidValuesList
        else:
            return []

    def GetEnumVisibilityList(self, ControlObject):
        '''
        returns all the attributes in the control object that are presumably visibility switches, it  checks two things, been an enum Attribute and have On Off Values. 
        '''
        VisibilityEnumList = []
        AttributeList = None
        AttributeList = cmds.listAttr(ControlObject, visible=True, keyable=True)
        if AttributeList != None:
            for eachEnum in AttributeList:
                if cmds.getAttr(ControlObject + "." + eachEnum, type=True) == 'enum':
                    EnumValues = self.getControlEnums(ControlObject, attribute=eachEnum)
                    if (EnumValues[0] == "Off" and EnumValues[1] == "On"):
                        VisibilityEnumList.append(eachEnum)
        return VisibilityEnumList

    def AddEnumParameters(self, Object, VisibilitySwitch='visibility'):
        Enum = ["Off", "On"]
        AttributeList = cmds.listAttr(Object)
        if VisibilitySwitch in AttributeList:
            if cmds.getAttr(Object + "." + VisibilitySwitch, type=True) == 'enum':
                return True
        else:
            cmds.addAttr(Object, at="enum", ln=VisibilitySwitch, k=1, en=":".join(Enum))
            return True
        return None

    def ConstraintVisibility(self, Objects, ControlObject, VisibilitySwitch='visibility', visibilityType="visibility"):
        '''visibilityType  valid values are overrideVisibility, lodVisibility or visibility'''
        if (self.AddEnumParameters(ControlObject, VisibilitySwitch=VisibilitySwitch)):
            for eachObject in Objects:
                RMRigTools.RMLockAndHideAttributes(eachObject, "xxxxxxxxxL")
                RMRigTools.RMLockAndHideAttributes(eachObject, "xxxxxxxxxh")
                # print ("connecting Visibility %s.%s to %s.%s"%(ControlObject,VisibilitySwitch,eachObject,visibilityType) )
                cmds.connectAttr("%s.%s" % (ControlObject, VisibilitySwitch), "%s.%s" % (eachObject, visibilityType))
        else:
            print "Not Valid Object"

    def GetAfectedObjectsList(self, ControlObject, VisibilitySwitch='visibility'):
        '''

        '''
        inputConnections = cmds.listConnections("%s.%s" % (ControlObject, VisibilitySwitch), p=True)
        Afected = []
        if inputConnections:
            for eachConnection in inputConnections:
                Values = eachConnection.split(".")
                if Values[1] == "visibility" or Values[1] == "lodVisibility" or Values[1] == "overrideVisibility":
                    Afected.append(Values[0])
        self.AfectedObjectList = Afected
        return self.AfectedObjectList

    def RemoveAffectedObject(self, ControlObject, removeObjectList, VisibilitySwitch='visibility',
                             visibilityType="visibility"):
        '''visibilityType  valid values are overrideVisibility, lodVisibility or visibility'''
        AffectedObjectList = self.GetAfectedObjectsList(ControlObject, VisibilitySwitch=VisibilitySwitch)
        for eachObject in removeObjectList:
            if eachObject in AffectedObjectList:
                cmds.disconnectAttr(("%s.%s" % (ControlObject, VisibilitySwitch)),
                                    ("%s.%s" % (eachObject, visibilityType)))

    def AddAffectedObject(self, ControlObject, addObjectList, VisibilitySwitch='visibility',
                          visibilityType="visibility"):
        '''visibilityType  valid values are overrideVisibility, lodVisibility or visibility'''
        for eachObject in addObjectList:
            inputConnections = cmds.listConnections("%s.%s" % (eachObject, visibilityType), plugs=True,
                                                    destination=True)
            if inputConnections:
                if len(inputConnections) > 0:
                    cmds.disconnectAttr(inputConnections[0], "%s.%s" % (eachObject, visibilityType))
            cmds.connectAttr("%s.%s" % (ControlObject, VisibilitySwitch), "%s.%s" % (eachObject, visibilityType),
                             force=True)
