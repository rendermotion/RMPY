import re
import maya.cmds as cmds


class RMNameConvention(object):
    def __init__(self, DefaultValues = ["Character", "C", "Object", "UDF", 'Rig'], convention = None):
        if convention == None:
            self.NameConvention = {
                "lastName": 0,
                "name": 2,
                'side': 1,
                'objectType': 3,
                "system": 4
            }
            convention = self.NameConvention
        else:
            self.NameConvention = convention

        '''
        self.validation = {'side': ['LF', 'RH', 'C'],'objectType' : ['JNT','SKNJNT','NUB','SKN','UDF','SHP','MSH','RMSH','GRP','PNC',
                                                                'ORC','PRC','PVC','CTRL','pnt','IKH','IKF','RVS','MULT','CND','BLT','CUI',
                                                                'DBTW','CLS','PMA','B2A','MPH','FFD','BS','AIM','CFME','LFT','PSFI','GUIDE']}
        self.translator = {'objectType':{
                            "joint": "JNT",
                            "skinjoint": "SKNJNT",
                            "GUIDE":'GUIDE',
                            "nub": "NUB",
                            "skin": "SKN",
                            "undefined": "UDF",
                            "nurbsCurve": "SHP",
                            "mesh": "MSH",
                            "renderMesh": "RMSH",
                            "transform": "GRP",
                            "pointConstraint": "PNC",
                            "orientConstraint": "ORC",
                            "parentConstraint": "PRC",
                            "poleVectorConstraint": "PVC",
                            "control": "CTRL",
                            "locator": "pnt",
                            "ikHandle": "IKH",
                            "ikEffector": "IKF",
                            "reverse": "RVS",
                            "multiplyDivide": "MULT",
                            "condition": "CND",
                            "baseLattice": "BLT",
                            "curveInfo": "CUI",
                            "distanceBetween": "DBTW",
                            "cluster": "CLS",
                            "plusMinusAverage": "PMA",
                            "blendTwoAttr": "B2A",
                            "motionPath": "MPH",
                            "ffd": "FFD",
                            "blendShape": "BS",
                            "aimConstraint": "AIM",
                            "curveFromMeshEdge": "CFME",
                            "loft": "LFT",
                            "pointOnSurfaceInfo": "PSFI"
                            },
                            'side':{'left':'LF', 'right':'RH', 'middle':'M'}
                            }
        '''
        self.validation = {'side': ['LF', 'RH', 'C'],
                           'objectType': ['jnt', 'sknjnt', 'nub', 'skn', 'UDF', 'shp', 'msh', 'rmsh', 'grp', 'pnc',
                                          'orc', 'prc', 'pvc', 'ctr', 'pnt', 'ikh', 'ikf', 'rvs', 'mult', 'cnd', 'blt',
                                          'cui',
                                          'dbtw', 'cls', 'pma', 'b2a', 'mph', 'ffd', 'bs', 'aim', 'cfme', 'lft', 'psfi',
                                          'guide']}
        self.translator = {'objectType': {
            "joint": "jnt",
            "skinjoint": "sknjnt",
            "guide": 'guide',
            "nub": "nub",
            "skin": "skn",
            "undefined": "udf",
            "nurbsCurve": "shp",
            "mesh": "msh",
            "renderMesh": "rmsh",
            "transform": "grp",
            "pointConstraint": "pnc",
            "orientConstraint": "orc",
            "parentConstraint": "prc",
            "poleVectorConstraint": "pvc",
            "control": "ctr",
            "locator": "pnt",
            "ikHandle": "ikh",
            "ikEffector": "ikf",
            "reverse": "rvs",
            "multiplyDivide": "mult",
            "condition": "cnd",
            "baseLattice": "blt",
            "curveInfo": "cui",
            "distanceBetween": "dbtw",
            "cluster": "cls",
            "plusMinusAverage": "pma",
            "blendTwoAttr": "b2a",
            "motionPath": "mph",
            "ffd": "ffd",
            "blendShape": "bs",
            "aimConstraint": "aim",
            "curveFromMeshEdge": "cfme",
            "loft": "lft",
            "pointOnSurfaceInfo": "psfi"
        },
            'side': {'left': 'LF', 'right': 'RH', 'middle': 'M'}
        }


        self.ShapeDictionary = {
            "nurbsCurve": "shp",
            "mesh": "msh",
            "baseLattice": "blt",
            "locator": "loc"
        }

        self.DefaultNames = {}
        for eachName in self.NameConvention:
            self.DefaultNames[eachName] = DefaultValues[self.NameConvention[eachName]]

    def RMTokenValidation(self, Token , TokenName):
        if TokenName in self.validation:
            if Token in self.validation[TokenName]:
                return Token
            else:
                if Token in self.translator[TokenName]:
                    return self.translator[TokenName][Token]
                else:
                    return self.DefaultNames[TokenName]
        else:
            return Token

    def RMGetFromName(self, ObjName, Token):
        if Token in self.NameConvention:
            if self.RMIsNameInFormat(ObjName):
                splitString = ObjName.split("_")
                return splitString[self.NameConvention[Token]]
            else:
                return self.DefaultNames[Token]
        else:
            print 'Error no such token in name convention'
            return None

    def RMSetFromName(self, ObjName, TextString, Token, mode = "regular"):
        'Valid Modes are regular and add'
        returnTuple = ()
        if (type(ObjName) == str) or (type(ObjName) == unicode):
            ObjectList = [ObjName]
        elif (type(ObjName) == list):
            ObjectList = ObjName
        else:
            ObjectList = []
        for eachObj in ObjectList:
            splitString = eachObj.split("_")
            if mode == 'regular':
               splitString[self.NameConvention[Token]] = self.RMTokenValidation(TextString, Token)
            elif mode == 'add':
                splitString[self.NameConvention[Token]] = self.RMAddToNumberedString(
                    splitString[self.NameConvention[Token]], TextString)
            elif mode == 'prefix':
                splitString[self.NameConvention[Token]] = self.RMAddToNumberedString(TextString, splitString[self.NameConvention[Token]])
            returnTuple += tuple(["_".join(splitString)])
        if len(returnTuple) == 1:
            return str(returnTuple[0])
        else:
            return returnTuple

    def RMRenameSetFromName(self, ObjName, TextString, Token, mode="regular"):
        returnListType = False
        if (type(ObjName) == str) or (type(ObjName) == unicode):
            ObjectList = [ObjName]
            returnListType = False
        elif (type(ObjName) == list):
            ObjectList = ObjName
            returnListType = True
        else:
            ObjectList = []
        returnList = []
        newName = ""
        for eachObj in ObjectList:
            newName = self.RMSetFromName(eachObj, TextString, Token, mode = mode)
            newName = self.RMUniqueName(newName)
            cmds.rename(eachObj, newName)
            returnList.append(newName)
        if returnListType == True:
            return returnList
        else:
            return newName

    def RMStringPlus1(self, NameString):
        Value = re.split(r"([0-9]+$)", NameString)
        Name = Value[0]
        if len(Value) >= 2:
            Number = str(int(Value[1]) + 1)
        else:
            Number = "0"
        return Name + Number.zfill(2)

    def RMAddToNumberedString(self, Name, AddName):
        Value = re.split(r"([0-9]+$)", Name)
        if len(Value) >= 2:
            return Value[0].title() + (AddName.title()) + Value[1]
        else:
            return Value[0].title() + (AddName.title())

    def RMUniqueName(self, currentName):
        ObjName = self.RMGetFromName(currentName, 'name')
        Value = re.split(r"([0-9]+$)", ObjName)
        Name = Value[0]
        currentName = self.RMSetFromName(currentName, self.RMStringPlus1(Name), 'name')
        while (cmds.objExists(currentName)):
            Name = self.RMStringPlus1(Name)
            currentName = self.RMSetFromName(currentName, Name, 'name')
        return currentName

    def RMGetTypeFromKey(self, Type):
        if Type in self.translator['objectType']:
            return self.translator['objectType'][Type]
        else:
            return self.translator['objectType']['undefined']

    def RMSetNameInFormat(self, wantedNameDic):
        '''the wanted Name Dic should be on the form {tokenName: wantedToken} where all the tokenName keys are part of the NameConvention Dictionary'''
        nameDic={}
        for eachKey in self.NameConvention:
            if eachKey in wantedNameDic:
                nameDic[eachKey] = wantedNameDic[eachKey]
            else:
                nameDic[eachKey] = self.DefaultNames[eachKey]

        for eachToken in self.NameConvention:
            nameDic[eachToken] = self.RMTokenValidation(nameDic[eachToken], eachToken)

        returnName = []
        for keys in sorted(self.NameConvention, key=self.NameConvention.get):
            returnName.append(nameDic[keys])
        ReturnNameInFormat = "_".join(returnName)
        return self.RMUniqueName(ReturnNameInFormat)

    def RMRenameNameInFormat(self, Name, wantedNameDic, useName = False):
        NewNameArray = ()
        NameList = []
        if type(Name) == list:
            NameList = Name
        elif type(Name) in [str, unicode]:
            NameList = [Name]
        else:
            print 'Error no Valid type on RMRenameNameInFromat should be string or list'

        for Names in NameList:
            NameTokens = Names.split("_")
            NewName = ""
            for eachToken in NameTokens:
                NewName += eachToken
            if useName:
                wantedNameDic['name'] = NewName
            NewName = self.RMSetNameInFormat(wantedNameDic)
            Names = cmds.rename(Names, NewName)
            if not 'objectType' in wantedNameDic :
                NewNameArray += tuple([self.RMRenameGuessTypeInName(Names)])
            else :
                Token = self.RMTokenValidation('objectType', wantedNameDic['objectType'])

                NewNameArray += tuple([self.RMSetFromName(Names,'objectType',Token)])

        if len(NewNameArray) == 1:
            return NewNameArray[0]
        return NewNameArray

    def RMIsNameInFormat(self, ObjName):
        splitString = ObjName.split("_")
        valid = True
        if len(splitString) == len(self.NameConvention.keys()):
            for keys in self.validation:
                if keys in self.NameConvention:
                    if splitString[self.NameConvention[keys]] in self.validation[keys]:
                        valid = valid and True
                    else :
                        print 'key not found: %s'%keys
                        print '%s not found in %s'% (splitString[self.NameConvention[keys]], self.validation[keys])
                        valid = False
            return valid
        else:
            print 'Not same token number'
            return False

    def RMGuessObjType(self, Obj):
        ObjType = cmds.objectType(Obj)
        ObjType = self.RMTokenValidation(ObjType,'objectType')

        if cmds.objectType(Obj) == "transform":
            children = cmds.listRelatives(Obj, shapes=True)
            if children:
                ShapeType = cmds.objectType(children[0])
                if ShapeType in self.ShapeDictionary:
                    ObjType = self.translator['objectType'][ShapeType]
                else:
                    ObjType = self.translator['objectType']["transform"]
            else:
                return ObjType
        if ObjType == self.translator['objectType']['undefined']:
            print 'Type not identified:', cmds.objectType(Obj)
        return ObjType

    def RMRenameGuessTypeInName(self, currentName):
        ''' this functions renames a name in format and adds the correct objectType described on the type dictionary
            to acomplish this, will look the objectType maya command and will match the type on the dictionary,
            this token will be placed on the objectType token place, and the object will be renamed to the new name.
        '''
        NewNameArray = []
        NameList = []
        if type(currentName) == list:
            NameList = currentName
        elif type(currentName) in [str, unicode]:
            NameList = [currentName]
        for currentName in NameList:
            NewName = currentName
            if cmds.objExists(NewName):
                if self.RMIsNameInFormat(NewName):
                    Type = self.RMGuessObjType(currentName)
                    NewName = self.RMSetFromName(NewName, Type, "objectType")
            NewName = self.RMUniqueName(NewName)
            cmds.rename(currentName, NewName)
            NewNameArray.append(NewName)

        if len(NewNameArray) == 1:
            return NewNameArray[0]
        else:
            return NewNameArray

    def RMRenameBasedOnBaseName(self, BaseName, ObjToRename, wantedNameDic):
        wantedNameCreated={}
        if self.RMIsNameInFormat(BaseName):
            baseNameTokens = BaseName.split('_')
            for eachToken in self.NameConvention:
                if eachToken in wantedNameDic:
                    wantedNameCreated[eachToken] = wantedNameDic [eachToken]
                else:
                    wantedNameCreated[eachToken] = baseNameTokens[self.NameConvention[eachToken]]

                wantedNameCreated['objectType']= self.RMGuessObjType(ObjToRename)
        else:
            for eachToken in self.NameConvention:
                if eachToken in wantedNameDic:
                    wantedNameCreated[eachToken] = wantedNameDic [eachToken]
                else:
                    wantedNameCreated[eachToken] = self.DefaultNames [eachToken]
            if not 'name' in wantedNameDic:
                NamesList = ObjToRename.split("_")
                NewName = ""
                for names in NamesList:
                    NewName += names
                wantedNameCreated['name'] = NewName

        if cmds.objExists(ObjToRename):
            NewName = self.RMSetNameInFormat(wantedNameCreated)
            cmds.rename(ObjToRename, NewName)
            return NewName
        else:
            return False

    def RMGetAShortName(self, Node):
        if self.RMIsNameInFormat(Node):
            Value = re.split(r"([0-9]+$)", self.RMGetFromName(Node, 'name'))
            return Value[0]
        else:
            Value = re.split(r"([0-9]+$)", Node)
            return Value[0]





            # NameConv = RMNameConvention()
            # NewName = NameConv.RMGuessObjType("joint1")




            #
            # print NameConv.RMSetFromName ("Character01_LF_pinky00_jnt_Rig",NameConv.RMStringPlus1("pinky"), 'Name')
