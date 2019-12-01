import pymel.core as pm
import maya.api.OpenMaya as om
from RMPY import nameConvention

from RMPY import RMRigTools


class RMSpaceSwitch(object):
    def __init__(self,NameConv = None):
        if not NameConv:
            self.NameConv = nameConvention.NameConvention()
        else:
            self.NameConv = NameConv
        self.ControlObject = None 
        self.AfectedObjectList = []
        self.SpaceObjectsList = []

    def CreateSpaceSwitchReverse(self, AfectedObject, SpaceObjects, ControlObject, Name = "spaceSwitch",
                                 constraintType = "parent", mo = True, sswtype = "enum"):
        '''
        Creates a simple space Switch that uses a reverse for simple solution it can only hold 2 spaces
        '''
        if len(SpaceObjects) == 2:
            if sswtype == "enum":
                SpaceObjectShortName =[]
                for eachObject in SpaceObjects:
                    SpaceObjectShortName.append(self.NameConv.get_a_short_name(eachObject))
                self.AddEnumParameters(SpaceObjectShortName, ControlObject, Name = Name)
            else:
                if Name=="":
                    index = 0
                    SwitchName = 'SW'
                    for eachString in SpaceObjects:
                        SwitchName = SwitchName + self.NameConv.get_a_short_name(eachString).title()
                        index = index + 1
                    Name = SwitchName

                self.AddNumericParameter( ControlObject, Name = Name)

            reverse = pm.shadingNode('reverse', asUtility=True, name = Name + "SWReverse")
            multiply = pm.shadingNode('multiplyDivide', asUtility=True, name = Name + "SWMultDiv")

            #pm.connectAttr(ControlObject + "." + Name, reverse + ".inputX")
            pm.connectAttr(ControlObject + "." + Name, multiply + ".input1X")
            pm.setAttr(multiply + ".input2X", 10)
            pm.setAttr(multiply + ".operation", 2)
            pm.connectAttr(multiply + ".outputX", reverse + ".inputX")
            
            for eachObject in SpaceObjects:
                if constraintType == "point":
                    parentConstraint = pm.pointConstraint(eachObject, AfectedObject, mo = mo, name = AfectedObject + "SpaceSwitchConstraint")
                    WA = pm.pointConstraint (parentConstraint, q = True, weightAliasList = True)
                elif constraintType == "orient":
                    parentConstraint = pm.orientConstraint (eachObject, AfectedObject, mo = mo, name = AfectedObject + "SpaceSwitchConstraint")
                    WA = pm.orientConstraint (parentConstraint, q = True, weightAliasList = True)
                elif constraintType == "parent":
                    parentConstraint = pm.parentConstraint (eachObject, AfectedObject, mo = mo, name = AfectedObject + "SpaceSwitchConstraint")
                    WA = pm.parentConstraint (parentConstraint, q=True, weightAliasList=True)
            
            pm.setAttr("%s.interpType"%parentConstraint, 0)

            if self.NameConv.is_name_in_format (AfectedObject):
                self.NameConv.rename_based_on_base_name(AfectedObject, reverse, name=reverse)
                self.NameConv.rename_based_on_base_name(AfectedObject, multiply, name=multiply)
                self.NameConv.rename_based_on_base_name(AfectedObject, parentConstraint
                                                        , name=Name)

            else:
                self.NameConv.rename_name_in_format(reverse)
                self.NameConv.rename_name_in_format(multiply)
                self.NameConv.rename_name_in_format(parentConstraint)

            pm.connectAttr( multiply + ".outputX", WA[1])
            pm.connectAttr( reverse  + ".outputX", WA[0])
            
            #pm.connectAttr(ControlObject + "." + Name, parentConstraint[0] + "." + WA[1])
            #pm.connectAttr(reverse + ".outputX", parentConstraint[0] + "." + WA[0])


    def CreateSpaceSwitch(self, AfectedObject, SpaceObjects, ControlObject, Name = "spaceSwitch",constraintType = "parent", mo = True):
        '''
        Creates a new SpaceSwitch using conditions so it can accept multiple spaces, 
        and it is compatible with the add and remove from Space Switch functions.
        Valid constraintTypes are "parent" , "point", "orient"
        '''
        SpaceObjectShortName =[]
        for eachObject in SpaceObjects:
            SpaceObjectShortName.append(self.NameConv.get_a_short_name(eachObject))

        self.AddEnumParameters(SpaceObjectShortName, ControlObject, Name = Name)

        index = 0
        for eachObject in SpaceObjects:
            if constraintType == "point":
                parentConstraint = pm.pointConstraint (eachObject, AfectedObject, mo = mo, name =self.NameConv.get_a_short_name(AfectedObject) + "SpaceSwitchConstraint")
            
            elif constraintType == "orient":
                parentConstraint = pm.orientConstraint (eachObject, AfectedObject, mo = mo, name =self.NameConv.get_a_short_name(AfectedObject) + "SpaceSwitchConstraint")
            
            else:
                parentConstraint = pm.parentConstraint (eachObject, AfectedObject, mo = mo, name =self.NameConv.get_a_short_name(AfectedObject) + "SpaceSwitchConstraint")

            Switch = pm.shadingNode('condition', asUtility=True, name = Name + "SWCondition")
            pm.connectAttr(ControlObject + "." + Name, Switch + ".firstTerm")
            pm.setAttr (Switch +".secondTerm", index)
            pm.setAttr (Switch +".operation", 0)
            pm.setAttr (Switch +".colorIfTrueR", 1)
            pm.setAttr (Switch +".colorIfFalseR", 0)
            if constraintType == "point":
                WA = pm.pointConstraint (parentConstraint, q = True, weightAliasList = True)
                TL = pm.pointConstraint (parentConstraint, q = True, targetList = True)
            elif constraintType == "orient":
                WA = pm.orientConstraint (parentConstraint, q = True, weightAliasList = True)
                TL = pm.orientConstraint (parentConstraint, q = True, targetList = True)
            else:
                WA = pm.parentConstraint (parentConstraint, q = True, weightAliasList = True)
                TL = pm.parentConstraint (parentConstraint, q = True, targetList = True)

            pm.connectAttr (Switch + ".outColorR", WA[index])
            if self.NameConv.is_name_in_format(AfectedObject):
                self.NameConv.rename_based_on_base_name(AfectedObject, Switch, name =Switch)
            else:
                self.NameConv.rename_name_in_format(Switch)
            index += 1
        
        if self.NameConv.is_name_in_format(AfectedObject):
            self.NameConv.rename_based_on_base_name(AfectedObject, parentConstraint, name=parentConstraint)
        else:
            self.NameConv.rename_name_in_format(parentConstraint)
    
    def IsSpaceSwitch(self, Control, SpaceSwitchName = "spaceSwitch"):
        AttributeList = pm.listAttr(Control)
        if SpaceSwitchName  in AttributeList:
            if pm.getAttr (Control + "." + SpaceSwitchName, type = True) == 'enum':
                Connections = pm.listConnections (Control + "." + SpaceSwitchName)
                if Connections != None:
                    for eachConnection in Connections:
                        if pm.objectType(eachConnection) == 'condition':
                            ConstraintsConnections = pm.listConnections(eachConnection+'.outColorR')
                            for eachConstraint in ConstraintsConnections:
                                if pm.objectType(eachConstraint) in ['parentConstraint', 'orientConstraint', 'orientConstraint']:
                                    return True
        return False

    def GetSpaceSwitchDic(self, control, SpaceSwitchName = "spaceSwitch"):
        Enums = self.getControlEnumsRelations(control,SpaceSwitchName = "spaceSwitch")
        ConstraintDictionary = self.ConstraintsDictionary(Enums[Enums.keys()[0]] ['condition'])
        return {'enums' : Enums , 'constraints' : ConstraintDictionary }

    def GetAfectedObjectsList(self,ControlObject,SpaceSwitchName = "spaceSwitch"):
        SpaceSwDic = self.GetSpaceSwitchDic(ControlObject, SpaceSwitchName = SpaceSwitchName)
        ReturnObjectsList=[]
        for keys in SpaceSwDic['constraints']:
            ReturnObjectsList.append(SpaceSwDic['constraints'][keys]['object'])
        return ReturnObjectsList

    def AddAffectedObject(self,ControlObject, AfectedObject,SpaceSwitchName = "spaceSwitch"):
        SpaceSwDic = self.GetSpaceSwitchDic(ControlObject,SpaceSwitchName = SpaceSwitchName)
        index = 0
        for eachEnum in SpaceSwDic['enums']:
            parentConstraint = pm.parentConstraint (SpaceSwDic['enums'][eachEnum]['object'], AfectedObject,
                                                    mo=True,
                                                    name=self.NameConv.get_a_short_name("%sSpaceSwitchConstraint" % AfectedObject))
            WA = pm.parentConstraint (parentConstraint, q = True, weightAliasList = True)
            pm.connectAttr (SpaceSwDic['enums'][eachEnum]['condition'] + ".outColorR", WA[index])
            index += 1
    def RemoveAffectedObject(self, ControlObject, AfectedObject, SpaceSwitchName = "spaceSwitch"):

        SpaceSwDic = self.GetSpaceSwitchDic(ControlObject, SpaceSwitchName = SpaceSwitchName)
        
        for allConstraints in SpaceSwDic['constraints']:
            if SpaceSwDic['constraints'][allConstraints]['object'] == AfectedObject:
                pm.delete(allConstraints)

        if len(SpaceSwDic['constraints'].keys()) == 1:
            for eachPlug in SpaceSwDic['enums']:
                pm.delete(SpaceSwDic['enums'][eachPlug]['condition'])

            self.DeleteSpaceSwitchAttr(ControlObject, SpaceSwitchName)
            


    def AddSpaceObject(self, ControlObject, SpaceObject, SpaceSwitchName = "spaceSwitch"):
        SpaceSwDic = self.GetSpaceSwitchDic( ControlObject, SpaceSwitchName = SpaceSwitchName)
        
        EnumDic = self.AddEnumParameters([self.NameConv.get_a_short_name(SpaceObject)], ControlObject)

        Switch = pm.shadingNode('condition', asUtility=True, name = SpaceSwitchName + "SWCondition")
        pm.connectAttr(ControlObject + "." + SpaceSwitchName, Switch + ".firstTerm")
        pm.setAttr (Switch +".secondTerm", EnumDic[self.NameConv.get_a_short_name(SpaceObject)])
        pm.setAttr (Switch +".operation", 0)
        pm.setAttr (Switch +".colorIfTrueR", 1)
        pm.setAttr (Switch +".colorIfFalseR", 0)

        if self.NameConv.is_name_in_format(ControlObject):
            self.NameConv.rename_based_on_base_name(ControlObject, Switch, name=Switch)
        else:
            self.NameConv.rename_name_in_format(Switch)

        for eachConstraint in SpaceSwDic['constraints']:
            Object = SpaceSwDic['constraints'][eachConstraint]['object']
            parentConstraint = pm.parentConstraint (SpaceObject, Object, mo = True)
            WA = pm.parentConstraint (parentConstraint, q = True, weightAliasList = True)
            TL = pm.parentConstraint (parentConstraint, q = True, targetList = True)
            if SpaceObject in TL:
                pm.connectAttr (Switch + ".outColorR", WA[TL.index(SpaceObject)])
            else:
                print "Error, cant find spaceobject in constraint targetList"

    def RemoveSpaceObject(self, ControlObject, SpaceObject, SpaceSwitchName = "spaceSwitch"):
        SpaceSwDic = self.GetSpaceSwitchDic( ControlObject, SpaceSwitchName = SpaceSwitchName)

        for eachConstraint in SpaceSwDic['constraints']:
            Object = SpaceSwDic['constraints'][eachConstraint]['object']
            pm.parentConstraint (SpaceObject, Object, remove = True)

        for eachEnum in SpaceSwDic['enums']:
            if  SpaceSwDic['enums'][eachEnum]['object'] == SpaceObject:
                self.deleteEnumParameter(ControlObject,eachEnum)
                pm.delete(SpaceSwDic['enums'][eachEnum]['condition'])
        
        enumDic = self.getEnumDictionary ( ControlObject, SpaceSwitchName = SpaceSwitchName)

        if enumDic:
            for eachEnum in enumDic:
                if eachEnum in SpaceSwDic['enums']:
                    EnumCond = SpaceSwDic['enums'][eachEnum]['condition']
                    pm.setAttr (EnumCond +".secondTerm", enumDic[eachEnum])

    def GetSpaceObjectsList(self, ControlObject, SpaceSwitchName = "spaceSwitch"):
        SpaceSwDic = self.GetSpaceSwitchDic( ControlObject, SpaceSwitchName = SpaceSwitchName)
        ObjList=[]
        for eachEnum in SpaceSwDic['enums']:
             ObjList.append(SpaceSwDic['enums'][eachEnum]['object'])
        return ObjList

    def AddNumericParameter(self, Object, Name = 'spaceSwitch', valueRange = [0,10]):
        AttributeList = pm.listAttr(Object)
        if Name  in AttributeList:
            #print "the Object Allready has an Attribute with this name, the type is:",pm.getAttr (Object + "." + Name,type = True)
            return False
        else :
            pm.addAttr(Object,at = "float", ln = Name,  hnv = 1, hxv = 1, h = 0, k = 1, smn = valueRange[0], smx = valueRange[1])
            return True

    def deleteEnumParameter(self, Object, Enum, SpaceSwitchName = 'spaceSwitch'):
        AttributeList = pm.listAttr(Object)
        if SpaceSwitchName in AttributeList:
            if pm.getAttr (Object + "." + SpaceSwitchName,type=True)=='enum':
                getControlEnums =self.getControlEnums(Object,SpaceSwitchName = SpaceSwitchName)
                if len(getControlEnums) > 1:
                    if Enum in getControlEnums:
                        getControlEnums.remove(Enum)
                        pm.addAttr(Object + '.' + SpaceSwitchName, e=True, en =":".join(getControlEnums))
                else:
                    self.DeleteSpaceSwitchAttr(Object, SpaceSwitchName)

    def AddEnumParameters(self, Enum, scene_object, Name ='spaceSwitch'):
        print 'object1111::: %s  %s'%(scene_object, scene_object.__class__)
        AttributeList = pm.listAttr(scene_object)
        if Name  in AttributeList:
            if pm.getAttr (scene_object + "." + Name, type=True)== 'enum':
                #print "the Object Allready has an spaceSwitch"
                #print "Current Valid types are", pm.addAttr (Object + "." + Name,q = True,enumName=True)
                EnumsInObject = self.getControlEnums(scene_object)
                for eachEnum in Enum:
                    if not eachEnum in EnumsInObject:
                        EnumsInObject.append(eachEnum)
                pm.addAttr(scene_object + '.' + Name, e=True, ln = Name, en =":".join(EnumsInObject))
                index = 0
                returnIndexDic = {}
                for eachEnum in EnumsInObject:
                    returnIndexDic[eachEnum] = index
                    index += 1
                return returnIndexDic
        else :
            pm.addAttr(scene_object, at ="enum", ln = Name, k = 1, en =":".join(Enum))
        return None

    def DeleteSpaceSwitchAttr (self, Object, Name = 'spaceSwitch'):
        AttributeList = pm.listAttr(Object)
        if Name  in AttributeList:
            pm.deleteAttr (Object,at = Name)
        else:
            print "The Attribute %s could not be found on obj %s" % (Name , Object)

    def ConstraintsDictionary (self, Condition):
        returnedDic = {}
        ObjectsConnected = pm.listConnections(Condition +'.outColorR')
        for eachConstraint in ObjectsConnected:
            returnedDic[eachConstraint] = self.getParentConstraintDic(eachConstraint)
        return returnedDic


    def getSwitchPlugsDictionary(self, Condition):
        returnedDic = {}
        ObjectsConnected = pm.listConnections(Condition +'.outColorR')
        plugs = pm.listConnections(Condition +'.outColorR', plugs = True)
        for eachPlug in plugs:
            splitPlug = eachPlug.split(".")
            if splitPlug[0] in ObjectsConnected:
                returnedDic[splitPlug[0]] = (splitPlug[1])
        return returnedDic

    def getParentConstraintDic (self, parentConstraint) :
        returnedDic = {'alias':{}, "object":None }
        aliasDic={}
        if pm.objectType(parentConstraint)=="parentConstraint":
            WA = pm.parentConstraint (parentConstraint, q = True, weightAliasList = True)
            TL = pm.parentConstraint (parentConstraint, q = True, targetList = True)
        
        elif pm.objectType(parentConstraint)=="orientConstraint":
            WA = pm.orientConstraint (parentConstraint, q = True, weightAliasList = True)
            TL = pm.orientConstraint (parentConstraint, q = True, targetList = True)
        
        elif pm.objectType(parentConstraint)=="pointConstraint":
            WA = pm.pointConstraint (parentConstraint, q = True, weightAliasList = True)
            TL = pm.pointConstraint (parentConstraint, q = True, targetList = True)
        
        else:
            "error No constraint Type identified"
        
        if len(WA) == len(TL):
            for eachWAIndex in range(0,len(WA)):
                aliasDic[WA[eachWAIndex]] = TL[eachWAIndex]
        
        returnedDic["object"] = pm.listConnections(parentConstraint + ".constraintRotateX")[0]
        returnedDic["alias"] = aliasDic
        return returnedDic

    def getEnumDictionary(self,Node,SpaceSwitchName = 'spaceSwitch'):
        AttributeList = pm.listAttr(Node)
        if SpaceSwitchName  in AttributeList:
            if pm.getAttr (Node + "." + SpaceSwitchName,type=True)=='enum':
                ValidValues = pm.addAttr(Node+"."+SpaceSwitchName,q = True,enumName=True)
                returnDictionary = {}
                index = 0
                for eachValue in ValidValues.split(":"):
                    returnDictionary[eachValue] = index
                    index+=1
                return returnDictionary
        return None



    def getControlEnums (self, Node, SpaceSwitchName = 'spaceSwitch'):
        AttributeList = pm.listAttr(Node)
        if SpaceSwitchName  in AttributeList:
            if pm.getAttr (Node + "." + SpaceSwitchName,type=True)=='enum':
                ValidValues = pm.addAttr(Node+"."+SpaceSwitchName,q = True,enumName=True)
                ValidValuesList = ValidValues.split(":")
                return ValidValuesList
        else:
            return []

    def getControlEnumsRelations(self, Node, SpaceSwitchName = 'spaceSwitch'):
        EnumRelationDic = {}
        AsummedConditions = pm.listConnections( Node+'.'+SpaceSwitchName)
        enumList = self.getControlEnums(Node, SpaceSwitchName = 'spaceSwitch')
        for eachAssumedCondition in AsummedConditions:
            if pm.objectType(eachAssumedCondition) == 'condition':
                index = pm.getAttr(eachAssumedCondition+".secondTerm")
                EnumRelationDic[enumList[int(index)]] = {}
                EnumRelationDic[enumList[int(index)]]['condition']= eachAssumedCondition
                EnumRelationDic[enumList[int(index)]]['index'] = int(index)
        for eachCondition in EnumRelationDic:
            EnumRelationDic[eachCondition]['plugs'] = self.getSwitchPlugsDictionary(EnumRelationDic[eachCondition]['condition'])

        for eachEnumRD in EnumRelationDic:
            EnumRelationDic [eachEnumRD]['object'] = ""
            for eachPlug in EnumRelationDic[eachEnumRD]['plugs']:
                ConstraintDic = self.getParentConstraintDic(eachPlug)
                if EnumRelationDic[eachEnumRD]['object'] == "":
                    EnumRelationDic[eachEnumRD]['object'] = ConstraintDic['alias'][EnumRelationDic[eachEnumRD]['plugs'][eachPlug]]
                elif EnumRelationDic[eachEnumRD]['object'] != ConstraintDic['alias'][EnumRelationDic[eachEnumRD]['plugs'][eachPlug]]:
                    print "Object mismatch  on Plug" , EnumRelationDic[eachEnumRD]['object'] , ConstraintDic['alias'][EnumRelationDic[eachEnumRD]['plugs'][eachPlug]]
        return EnumRelationDic

    def RMCreateListConstraintSwitch(self,Constrained, Constraints ,ControlObject, SpaceSwitchName = 'spaceSwitch', reverse = False):
        SWMultDiv = ""
        if (self.AddNumericParameter (ControlObject, Name = SpaceSwitchName)):
            SWMultDiv = pm.shadingNode("multiplyDivide",asUtility = True ,name = SpaceSwitchName + "SWMultDivide" )
            self.NameConv.rename_based_on_base_name(ControlObject, SWMultDiv, name=SWMultDiv)
            pm.connectAttr(ControlObject+"."+SpaceSwitchName ,SWMultDiv+".input1X")
            pm.setAttr(SWMultDiv+".input2X",10)
            pm.setAttr(SWMultDiv+".operation",2)
        
        else:
            
            SWMultDiv = pm.listConnections(ControlObject + "." + SpaceSwitchName, type = "multiplyDivide")[0]

        if reverse == True:
            ConnectionsList = pm.listConnections(SWMultDiv + ".outputX", type = "reverse")
            reverseSW = ""
            if ConnectionsList and len(ConnectionsList) >= 1:
                reverseSW = ConnectionsList[0]
            else :
                reverseSW = pm.shadingNode('reverse', asUtility=True, name = SpaceSwitchName + "SWReverse")
                self.NameConv.rename_based_on_base_name(ControlObject, reverseSW, name="SWReverse")
                pm.connectAttr( SWMultDiv + ".outputX", reverseSW + ".inputX")

                if self.NameConv.is_name_in_format (ControlObject):
                    self.NameConv.rename_based_on_base_name(ControlObject, reverseSW, name=reverseSW)
                else:
                    self.NameConv.rename_name_in_format(reverseSW)

            self.RMListConstraint(Constrained, Constraints, reverseSW + ".outputX")

        else:

            self.RMListConstraint(Constrained, Constraints, SWMultDiv + ".outputX")
    
    
    def RMListConstraint(self,Constrained, Constraint, Connection):
        index = 0
        for eachObject in Constrained:
            constraint = pm.parentConstraint(Constraint[index], eachObject, name = "SpaceSwitch" + self.NameConv.get_a_short_name(eachObject))
            self.NameConv.rename_based_on_base_name(eachObject, constraint, name=self.NameConv.get_a_short_name(constraint))
            WA = pm.parentConstraint (constraint, q = True, weightAliasList = True)
            TL = pm.parentConstraint (constraint, q = True, targetList = True)
            ConstraintIndex = TL.index(Constraint[index])
            pm.connectAttr(Connection, WA[ConstraintIndex])
            index += 1

    def ConstraintVisibility(self, Objects , ControlObject , SpaceSwitchName = 'spaceSwitch', reverse=False):
        if (self.AddNumericParameter (ControlObject, Name = SpaceSwitchName)):
            SWMultDiv = pm.shadingNode("multiplyDivide",asUtility = True ,name = SpaceSwitchName + "SWMultDivide" )
            self.NameConv.rename_based_on_base_name(ControlObject, SWMultDiv, name=SWMultDiv)
            pm.connectAttr(ControlObject+"."+SpaceSwitchName ,SWMultDiv+".input1X")
            pm.setAttr(SWMultDiv+".input2X", 10)
            pm.setAttr(SWMultDiv+".operation", 2)
        else:
            SWMultDiv = pm.listConnections(ControlObject + "." + SpaceSwitchName, type="multiplyDivide")[0]

        if reverse == True:
            ConnectionsList = pm.listConnections (SWMultDiv + ".outputX", type="reverse")
            reverseSW = ""
            if ConnectionsList and len(ConnectionsList) >= 1:
                reverseSW = ConnectionsList[0]
            else:
                reverseSW = pm.shadingNode('reverse', asUtility=True, name = SpaceSwitchName + "SWReverse")
                self.NameConv.rename_based_on_base_name(ControlObject, reverseSW, name="SWReverse")
                pm.connectAttr( SWMultDiv + ".outputX", reverseSW + ".inputX")

                if self.NameConv.is_name_in_format (ControlObject):
                    self.NameConv.rename_based_on_base_name(ControlObject, reverseSW, name=reverseSW)
                else:
                    self.NameConv.rename_name_in_format(reverseSW)
            for eachObject in Objects:
                pm.connectAttr(reverseSW + ".outputX", eachObject + ".visibility")
        
        else:
            for eachObject in Objects:
                pm.connectAttr(SWMultDiv + ".outputX", eachObject + ".visibility")



#SW.DeletSpaceSwitchAttr('pCube1')
#SW.CreateSpaceSwitch('group1',['pSphere1','pSphere2'], 'pCube1')
#Node = "pCube1"

#SW.DeleteSpaceSwitchAttr(Node)

#SpaceSwitchName = "spaceSwitch"

#pprint.pprint (SW.GetSpaceSwitchDic(Node))

#print SW.IsSpaceSwitch("pSphere2")
# 

#SW.AddEnumParameters(["Hola","Mundo"], Node, SpaceSwitchName)







