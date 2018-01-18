import re
import maya.cmds as cmds

class validator(object):
    def __init__(self):
        self._translator={}
        self._validator =[]
        self._default = ''
    @property
    def translator(self):
        return self.translator

    @translator.setter
    def translator(self,value):
        self.translator = value
        self._validator = []
        for each_value in self._translator:
            each._validator.append(self._translator[each_value])

    def validate(self, value):
        if value in self._validator:
            return value
        elif value in self._translator:
            return self._translator[value]
        elif self._translator=={}:
            return value
        elif self._default=='':
            raise RuntimeError('no valid validator, assign a default value, or a dictionary')
        else:
            return self._default
    @property
    def default(self):
        return self._default
    @default.setter
    def default(self,new_value):
        self._default = self.validate(new_value)
    @classmethod
    def validator_from_default(cls, default_value):
        new_instance = cls()
        new_instance.default = default_value
        return new_instance
    @classmethod
    def validator_from_dictionary(cls, translator_dictionary):
        new_instance = cls()
        new_instance.translator = translator_dictionary
        return new_instance
    @classmethod
    def validator_from_dictionary_default(cls, translator_dictionary, default_value):
        new_instance = cls()
        new_instance.translator = translator_dictionary
        new_instance.default = default_value
        return new_instance


def validate_input_nodes(nodes):
    if type(nodes) == list:
        return [str(str_node) for str_node in nodes]
    return str(nodes)


class RMNameConvention(object):
    def __init__(self, DefaultValues = ["C", "Object", 'Rig', "UDF"], convention = None):
        if convention == None:
            self.NameConvention = {
                "name": 1,
                'side': 0,
                'objectType': 3,
                "system": 2
            }
            convention = self.NameConvention
        else:
            self.NameConvention = convention

        '''
        self.validation = {'side': ['LF', 'RH', 'MD'],'objectType' : ['JNT','SKNJNT','NUB','SKN','UDF','SHP','MSH','RMSH','GRP','PNC',
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
                            'side':{'left':'LF', 'right':'RH', 'middle':'MD'}
                            }
        '''
        self.validation = {'side': ['L', 'R', 'C'],
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
            "undefined": "UDF",
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
            'side': {'left': 'L', 'right': 'R', 'center': 'C'}
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
        'Valid Modes are regular add, and prefix'
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
        ObjName = validate_input_nodes(ObjName)
        returnListType = False
        if (type(ObjName) == str) or (type(ObjName) == unicode):
            ObjectList = [ObjName]
            returnListType = False
        elif (type(ObjName) == list):
            ObjectList = ObjName
            returnListType = True
        else:
            print 'error not valid object on RMRenameSetFromName :%s' % ObjName
            return
        returnList = []
        newName = ""
        for eachObj in ObjectList:
            fullNameToken = eachObj.split('|')
            if len(fullNameToken) > 1:
                simpleName = fullNameToken[len(fullNameToken)-1]
                complement = '|'.join(fullNameToken[:-1])
            else:
                simpleName = fullNameToken[0]
                complement = ''

            newName = self.RMSetFromName(simpleName, TextString, Token, mode=mode)
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
                nameDic[eachKey] = str(wantedNameDic[eachKey])
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
        Name = validate_input_nodes(Name)

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
            if 'objectType' not in wantedNameDic:
                NewNameArray += tuple([self.RMRenameGuessTypeInName(Names)])
            else:
                Token = self.RMTokenValidation(wantedNameDic['objectType'], 'objectType')
                NewNameArray += tuple([self.RMRenameSetFromName(Names,Token, 'objectType')])

        if len(NewNameArray) == 1:
            return NewNameArray[0]
        return NewNameArray

    def RMIsNameInFormat(self, obj_name):
        obj_name = validate_input_nodes(obj_name)
        splitString = obj_name.split("_")
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

    def RMGuessObjType (self, scene_object):
        scene_object = validate_input_nodes(scene_object)
        ObjType = cmds.objectType(scene_object)
        ObjType = self.RMTokenValidation(ObjType,'objectType')

        if cmds.objectType(scene_object) == "transform":
            children = cmds.listRelatives(scene_object, shapes=True)
            if children:
                ShapeType = cmds.objectType(children[0])
                if ShapeType in self.ShapeDictionary:
                    ObjType = self.translator['objectType'][ShapeType]
                else:
                    ObjType = self.translator['objectType']["transform"]
            else:
                return ObjType
        if ObjType == self.translator['objectType']['undefined']:
            print 'Type not identified:', cmds.objectType(scene_object)
        return ObjType

    def RMRenameGuessTypeInName(self, current_name):
        ''' this functions renames a name in format and adds the correct objectType described on the type dictionary
            to acomplish this, will look the objectType maya command and will match the type on the dictionary,
            this token will be placed on the objectType token place, and the object will be renamed to the new name.
        '''
        current_name = validate_input_nodes(current_name)

        NewNameArray = []
        NameList = []
        if type(current_name) == list:
            NameList = current_name
        elif type(current_name) in [str, unicode]:
            NameList = [current_name]
        for current_name in NameList:
            NewName = current_name
            if cmds.objExists(NewName):
                if self.RMIsNameInFormat(NewName):
                    Type = self.RMGuessObjType(current_name)
                    NewName = self.RMSetFromName(NewName, Type, "objectType")
            NewName = self.RMUniqueName(NewName)
            cmds.rename(current_name, NewName)
            NewNameArray.append(NewName)

        if len(NewNameArray) == 1:
            return NewNameArray[0]
        else:
            return NewNameArray

    def RMRenameBasedOnBaseName(self, base_name, obj_to_rename, wantedNameDic):

        obj_to_rename =validate_input_nodes(obj_to_rename)
        base_name = validate_input_nodes(base_name)

        wantedNameCreated={}
        if self.RMIsNameInFormat(base_name):
            baseNameTokens = base_name.split('_')
            for eachToken in self.NameConvention:
                if eachToken in wantedNameDic:
                    wantedNameCreated[eachToken] = str(wantedNameDic [eachToken])
                else:
                    wantedNameCreated[eachToken] = baseNameTokens[self.NameConvention[eachToken]]

                wantedNameCreated['objectType']= self.RMGuessObjType(obj_to_rename)
        else:
            for eachToken in self.NameConvention:
                if eachToken in wantedNameDic:
                    wantedNameCreated[eachToken] = str(wantedNameDic [eachToken])
                else:
                    wantedNameCreated[eachToken] = self.DefaultNames [eachToken]
            if not 'name' in wantedNameDic:
                NamesList = obj_to_rename.split("_")
                NewName = ""
                for names in NamesList:
                    NewName += names
                wantedNameCreated['name'] = NewName

        if cmds.objExists(obj_to_rename):
            NewName = self.RMSetNameInFormat(wantedNameCreated)
            cmds.rename(obj_to_rename, NewName)
            return NewName
        else:
            return False

    def RMGetAShortName(self, scene_object):
        scene_object = validate_input_nodes(scene_object)
        if self.RMIsNameInFormat(scene_object):
            Value = re.split(r"([0-9]+$)", self.RMGetFromName(scene_object, 'name'))
            return Value[0]
        else:
            Value = re.split(r"([0-9]+$)", scene_object)
            return Value[0]





            # NameConv = RMNameConvention()
            # NewName = NameConv.RMGuessObjType("joint1")




            #
            # print NameConv.RMSetFromName ("Character01_LF_pinky00_jnt_Rig",NameConv.RMStringPlus1("pinky"), 'Name')
