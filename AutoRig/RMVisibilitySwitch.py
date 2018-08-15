import pymel.core as pm
from RMPY import nameConvention
from RMPY import RMRigTools


class RMVisibilitySwitch(object):
    def __init__(self, NameConv=None):
        if not NameConv:
            self.NameConv = nameConvention.NameConvention()
        else:
            self.NameConv = NameConv
        self.ControlObject = None
        self.AfectedObjectList = []

    def getControlEnums(self, Node, attribute='Visibility'):
        '''
        returns all the enums in an object attribute 
        '''
        Node = RMRigTools.validate_pymel_nodes(Node)
        AttributeList = pm.listAttr(Node)
        if attribute in AttributeList:
            if pm.getAttr(Node + "." + attribute, type=True) == 'enum':
                ValidValues = pm.addAttr(Node + "." + attribute, q=True, enumName=True)
                ValidValuesList = ValidValues.split(":")
                return ValidValuesList
        else:
            return []

    def GetEnumVisibilityList(self, ControlObject):
        '''
        returns all the attributes in the control object that are presumably visibility switches, it  checks two things, been an enum Attribute and have On Off Values. 
        '''
        ControlObject = RMRigTools.validate_pymel_nodes(ControlObject)
        VisibilityEnumList = []
        AttributeList = None
        AttributeList = pm.listAttr(ControlObject, visible=True, keyable=True)
        if AttributeList != None:
            for eachEnum in AttributeList:
                if pm.getAttr(ControlObject + "." + eachEnum, type=True) == 'enum':
                    EnumValues = self.getControlEnums(ControlObject, attribute=eachEnum)
                    if (EnumValues[0] == "Off" and EnumValues[1] == "On"):
                        VisibilityEnumList.append(eachEnum)
        return VisibilityEnumList

    def AddEnumParameters(self, Object, VisibilitySwitch='visibility'):
        Object = RMRigTools.validate_pymel_nodes(Object)
        Enum = ["Off", "On"]
        AttributeList = pm.listAttr(Object)
        if VisibilitySwitch in AttributeList:
            if pm.getAttr(Object + "." + VisibilitySwitch, type=True) == 'enum':
                return True
        else:
            pm.addAttr(Object, at="enum", ln=VisibilitySwitch, k=1, en=":".join(Enum))
            return True
        return None

    def ConstraintVisibility(self, Objects, ControlObject, VisibilitySwitch='visibility', visibilityType="visibility"):
        Objects = RMRigTools.validate_pymel_nodes(Objects)
        ControlObject = RMRigTools.validate_pymel_nodes(ControlObject)
        '''visibilityType  valid values are overrideVisibility, lodVisibility or visibility'''
        if (self.AddEnumParameters(ControlObject, VisibilitySwitch=VisibilitySwitch)):
            for eachObject in Objects:
                RMRigTools.RMLockAndHideAttributes(eachObject, "xxxxxxxxxL")
                RMRigTools.RMLockAndHideAttributes(eachObject, "xxxxxxxxxh")
                # print ("connecting Visibility %s.%s to %s.%s"%(ControlObject,VisibilitySwitch,eachObject,visibilityType) )
                pm.connectAttr("%s.%s" % (ControlObject, VisibilitySwitch), "%s.%s" % (eachObject, visibilityType))
        else:
            print "Not Valid Object"

    def GetAfectedObjectsList(self, ControlObject, VisibilitySwitch='visibility'):
        ControlObject = RMRigTools.validate_pymel_nodes(ControlObject)
        '''

        '''
        inputConnections = pm.listConnections("%s.%s" % (ControlObject, VisibilitySwitch), p=True)
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
        ControlObject = RMRigTools.validate_pymel_nodes(ControlObject)
        removeObjectList = RMRigTools.validate_pymel_nodes(removeObjectList)
        '''visibilityType  valid values are overrideVisibility, lodVisibility or visibility'''
        AffectedObjectList = self.GetAfectedObjectsList(ControlObject, VisibilitySwitch=VisibilitySwitch)
        for eachObject in removeObjectList:
            if eachObject in AffectedObjectList:
                pm.disconnectAttr(("%s.%s" % (ControlObject, VisibilitySwitch)),
                                    ("%s.%s" % (eachObject, visibilityType)))

    def AddAffectedObject(self, ControlObject, addObjectList, VisibilitySwitch='visibility',
                          visibilityType="visibility"):
        ControlObject = RMRigTools.validate_pymel_nodes(ControlObject)
        addObjectList = RMRigTools.validate_pymel_nodes(addObjectList)
        '''visibilityType  valid values are overrideVisibility, lodVisibility or visibility'''
        for eachObject in addObjectList:
            inputConnections = pm.listConnections("%s.%s" % (eachObject, visibilityType), plugs=True,
                                                    destination=True)
            if inputConnections:
                if len(inputConnections) > 0:
                    pm.disconnectAttr(inputConnections[0], "%s.%s" % (eachObject, visibilityType))
            pm.connectAttr("%s.%s" % (ControlObject, VisibilitySwitch), "%s.%s" % (eachObject, visibilityType),
                             force=True)
