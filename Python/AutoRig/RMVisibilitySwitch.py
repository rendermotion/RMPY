import maya.cmds as cmds
import RMNameConvention
import RMRigTools

class RMVisibilitySwitch(object):
    def __init__(self,NameConv = None):
        if not NameConv:
            self.NameConv = RMNameConvention.RMNameConvention()
        else:
            self.NameConv = NameConv
        self.ControlObject = None 
        self.AfectedObjectList = []

    def getControlEnums (self, Node, attribute = 'Visibility'):
        '''
        returns all the enums in an object attribute 
        '''
        AttributeList = cmds.listAttr(Node)
        if attribute  in AttributeList:
            if cmds.getAttr (Node + "." + attribute,type=True)=='enum':
                ValidValues = cmds.addAttr(Node+"."+attribute,q = True,enumName=True)
                ValidValuesList = ValidValues.split(":")
                return ValidValuesList
        else:
            return []

    def GetEnumVisibilityList(self,ControlObject):
        '''
        returns all the attributes in the control object that are presumably visibility switches, it  checks two things, been an enum Attribute and have On Off Values. 
        '''
        VisibilityEnumList = []
        AttributeList = cmds.listAttr(ControlObject,visible=True,keyable = True )
        for eachEnum in AttributeList:
            if cmds.getAttr (ControlObject + "." + eachEnum, type = True) == 'enum':
                EnumValues = self.getControlEnums(ControlObject , attribute = eachEnum )
                if ( EnumValues [0]== "Off" and EnumValues [1]== "On"):
                    VisibilityEnumList.append(eachEnum)
        return VisibilityEnumList

    def AddEnumParameters(self,Object, VisibilitySwitch = 'visibility'):
        Enum = ["Off","On"]
        AttributeList = cmds.listAttr(Object)
        if VisibilitySwitch  in AttributeList:
            if cmds.getAttr (Object + "." + VisibilitySwitch, type = True)=='enum':
                return True
        else :
            cmds.addAttr(Object , at = "enum" , ln = VisibilitySwitch , k = 1, en =":".join(Enum))
            return True
        return None

    def ConstraintVisibility(self, Objects , ControlObject , VisibilitySwitch = 'visibility'):

        if (self.AddEnumParameters (ControlObject, VisibilitySwitch = VisibilitySwitch)):
            for eachObject in Objects:
                RMRigTools.RMLockAndHideAttributes(eachObject,"xxxxxxxxx1")
                cmds.connectAttr("%s.%s"%(ControlObject,VisibilitySwitch) , eachObject + ".visibility")
        else:
            print "Not Valid Object"
    
    def GetAfectedObjectsList(self, ControlObject, VisibilitySwitch = 'visibility'):
        '''

        '''
        inputConnections = cmds.listConnections("%s.%s" % (ControlObject,VisibilitySwitch),p = True)
        Afected = []
        if inputConnections:
            for eachConnection in inputConnections:
                Values = eachConnection.split(".")
                if Values [1] == "visibility":
                    Afected.append (Values[0])
        self.AfectedObjectList = Afected
        return self.AfectedObjectList

    def RemoveAffectedObject (self, ControlObject, removeObjectList , VisibilitySwitch = 'visibility'):
        AffectedObjectList = self.GetAfectedObjectsList(ControlObject,VisibilitySwitch = VisibilitySwitch)
        for eachObject in removeObjectList:
            if eachObject in AffectedObjectList:
                cmds.disconnectAttr( ("%s.%s"%(ControlObject,VisibilitySwitch)) , ("%s.visibility" % (eachObject)))

    def AddAffectedObject ( self, ControlObject, addObjectList , VisibilitySwitch = 'visibility'):
        for eachObject in addObjectList:
            inputConnections = cmds.listConnections("%s.visibility" % eachObject, plugs=True, destination = True)
            if len(inputConnections) > 0:
                cmds.disconnectAttr(inputConnections[0], "%s.visibility" % eachObject)
            cmds.connectAttr( "%s.%s"%(ControlObject,VisibilitySwitch), "%s.visibility" % eachObject, force = True)









