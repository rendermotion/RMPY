import re
import maya.cmds as cmds


class validator(object):
    def __init__(self):
        self._translator = {}
        self._validator = []
        self._default = ''

    @property
    def translator(self):
        return self.translator

    @translator.setter
    def translator(self, value):
        self.translator = value
        self._validator = []
        for each_value in self._translator:
            self._validator.append(self._translator[each_value])

    def validate(self, value):
        if value in self._validator:
            return value
        elif value in self._translator:
            return self._translator[value]
        elif self._translator == {}:
            return value
        elif self._default == '':
            raise RuntimeError('no valid validator, assign a default value, or a dictionary')
        else:
            return self._default

    @property
    def default(self):
        return self._default

    @default.setter
    def default(self, new_value):
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
    if type(nodes) == list or type(nodes) == tuple:
        return [str(str_node) for str_node in nodes]
    return str(nodes)


class NameConvention(object):
    def __init__(self, *tokens, **values):

        if len(tokens) == 0:
            tokens = ['side', 'name', 'system', 'objectType']

        self.name_convention = {}
        for index, each in enumerate(tokens):
            self.name_convention[each] = index

        self.validation = {'side': ['L', 'R', 'C'],
                           'objectType': ['jnt', 'sknjnt', 'nub', 'skn', 'UDF', 'shp', 'msh', 'rmsh', 'grp', 'pnc',
                                          'orc', 'prc', 'scc', 'pvc', 'ctr', 'pnt', 'ikh', 'ikf', 'rvs', 'mult', 'cnd',
                                          'blt', 'cui', 'dbtw', 'cls', 'clsh', 'pma', 'b2a', 'mph', 'ffd', 'bs', 'aim',
                                          'cfme', 'lft', 'psfi', 'guide', 'unc', 'skn', 'dmx', 'mmx', 'nrb', 'ffm','vcp']}
        self.translator = {'objectType': {
            "joint": "jnt",
            "skinjoint": "sknjnt",
            "guide": 'guide',
            "nub": "nub",
            "skin": "skn",
            'decomposeMatrix': 'dmx',
            "undefined": "UDF",
            "nurbsCurve": "shp",
            'multMatrix': 'mmx',
            "mesh": "msh",
            "renderMesh": "rmsh",
            "transform": "grp",
            "pointConstraint": "pnc",
            "orientConstraint": "orc",
            "parentConstraint": "prc",
            "scaleConstraint": "scc",
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
            'unitConversion': 'unc',
            "cluster": "cls",
            'clusterHandle': 'clsh',
            "plusMinusAverage": "pma",
            "blendTwoAttr": "b2a",
            "motionPath": "mph",
            "ffd": "ffd",
            "blendShape": "bs",
            "aimConstraint": "aim",
            "curveFromMeshEdge": "cfme",
            "loft": "lft",
            "pointOnSurfaceInfo": "psfi",
            "skinCluster": 'skn',
            'fourByFourMatrix': 'ffm',
            'vectorProduct': 'vcp',
            'NurbsSurface': 'nrb'
        },
            'side': {'left': 'L', 'right': 'R', 'center': 'C'}
        }

        self.ShapeDictionary = {
            "nurbsCurve": "shp",
            "mesh": "msh",
            'clusterHandle': 'clsh',
            "baseLattice": "blt",
            "locator": "loc",
            'NurbsSurface': 'nrb'
        }
        self.default_names = {}
        for eachName in self.name_convention.keys():
            if eachName in values.keys():
                self.default_names[eachName] = values[eachName]
            else:
                if eachName == 'name':
                    self.default_names[eachName] = 'object'
                elif eachName == 'side':
                    self.default_names[eachName] = 'C'
                elif eachName == 'objectType':
                    self.default_names[eachName] = 'UDF'
                elif eachName == 'system':
                    self.default_names[eachName] = 'rig'
                else:
                    raise f'error must provide a default value for each token not token found {eachName}'

    def token_validation(self, Token, TokenName):
        if TokenName in self.validation:
            if Token in self.validation[TokenName]:
                return Token
            else:
                if Token in self.translator[TokenName]:
                    return self.translator[TokenName][Token]
                else:
                    return self.default_names[TokenName]
        else:
            return Token

    def get_from_name(self, ObjName, Token):
        if Token in self.name_convention:
            if self.is_name_in_format(ObjName):
                splitString = ObjName.split("_")
                return splitString[self.name_convention[Token]]
            else:
                return self.default_names[Token]
        else:
            print ('Error no such token in name convention')
            return None

    def set_from_name(self, ObjName, TextString, Token, mode="regular"):
        'Valid Modes are regular add, and prefix'
        returnTuple = ()
        if type(ObjName) == str:
            ObjectList = [ObjName]
        elif type(ObjName) == list:
            ObjectList = ObjName
        else:
            ObjectList = []
        for eachObj in ObjectList:
            splitString = eachObj.split("_")
            if mode == 'regular':
                splitString[self.name_convention[Token]] = self.token_validation(TextString, Token)
            elif mode == 'add':
                splitString[self.name_convention[Token]] = self.add_to_numbered_string(
                    splitString[self.name_convention[Token]], TextString)
            elif mode == 'prefix':
                splitString[self.name_convention[Token]] = self.add_to_numbered_string(TextString, splitString[
                    self.name_convention[Token]])
            returnTuple += tuple(["_".join(splitString)])
        if len(returnTuple) == 1:
            return str(returnTuple[0])
        else:
            return returnTuple

    def rename_set_from_name(self, ObjName, TextString, Token, mode="regular"):
        ObjName = validate_input_nodes(ObjName)
        returnListType = False
        if type(ObjName) == str:
            ObjectList = [ObjName]
            returnListType = False
        elif (type(ObjName) == list):
            ObjectList = ObjName
            returnListType = True
        else:
            print ('error not valid object on RMRenameSetFromName :{}'.format(ObjName))
            return
        returnList = []
        newName = ""
        for eachObj in ObjectList:
            fullNameToken = eachObj.split('|')
            if len(fullNameToken) > 1:
                simpleName = fullNameToken[len(fullNameToken) - 1]
                complement = '|'.join(fullNameToken[:-1])
            else:
                simpleName = fullNameToken[0]
                complement = ''

            newName = self.set_from_name(simpleName, TextString, Token, mode=mode)
            newName = self.unique_name(newName)
            cmds.rename(eachObj, newName)
            returnList.append(newName)
        if returnListType == True:
            return returnList
        else:
            return newName

    def string_plus_1(self, NameString):
        Value = re.split(r"([0-9]+$)", NameString)
        Name = Value[0]
        if len(Value) >= 2:
            Number = str(int(Value[1]) + 1)
        else:
            Number = "0"
        return Name + Number.zfill(2)

    def add_to_numbered_string(self, Name, AddName):
        Value = re.split(r"([0-9]+$)", Name)
        if len(Value) >= 2:
            return Value[0].title() + (AddName.title()) + Value[1]
        else:
            return Value[0].title() + (AddName.title())

    def unique_name(self, currentName):
        ObjName = self.get_from_name(currentName, 'name')
        Value = re.split(r"([0-9]+$)", ObjName)
        Name = Value[0]
        currentName = self.set_from_name(currentName, self.string_plus_1(Name), 'name')
        while (cmds.objExists(currentName)):
            Name = self.string_plus_1(Name)
            currentName = self.set_from_name(currentName, Name, 'name')
        return currentName

    def get_type_from_key(self, Type):
        if Type in self.translator['objectType']:
            return self.translator['objectType'][Type]
        else:
            return self.translator['objectType']['undefined']

    def set_name_in_format(self, **wantedNameDic):
        ''' the wanted Name Dic should be on the form {tokenName: wantedToken}
        where all the tokenName keys are part of the NameConvention Dictionary'''
        nameDic = {}
        for eachKey in self.name_convention:
            if eachKey in wantedNameDic:
                nameDic[eachKey] = str(wantedNameDic[eachKey])
            else:
                nameDic[eachKey] = self.default_names[eachKey]

        for eachToken in self.name_convention:
            nameDic[eachToken] = self.token_validation(nameDic[eachToken], eachToken)

        return_name = []
        for keys in sorted(self.name_convention, key=self.name_convention.get):
            return_name.append(nameDic[keys])
        return_name_in_format = "_".join(return_name)
        return self.unique_name(return_name_in_format)

    def rename_name_in_format(self, *current_name, **wanted_name_dictionary):
        useName = wanted_name_dictionary.pop('useName', False)
        string_name_list = validate_input_nodes(current_name)
        new_name_array = ()
        for each_object in string_name_list:
            # name_tokens = each_object.split("|")
            # new_name = ""
            # for eachToken in name_tokens:
            #     new_name += eachToken
            if useName:
                # print ' ****** remove ns Use name'
                # print self.remove_namespace(each_object)
                # print self.get_a_short_name(self.remove_namespace(each_object))
                wanted_name_dictionary['name'] = self.get_a_short_name(self.remove_namespace(each_object))

            if 'objectType' not in wanted_name_dictionary:
                wanted_name_dictionary['objectType'] = self.guess_object_type(each_object)

            wanted_name_dictionary['objectType'] = self.token_validation(wanted_name_dictionary['objectType'],
                                                                         'objectType')

            new_name = self.set_name_in_format(**wanted_name_dictionary)
            cmds.rename(each_object, new_name)
            new_name_array += tuple([new_name])

        if len(new_name_array) == 1:
            return new_name_array[0]
        return new_name_array

    def is_name_in_format(self, obj_name):
        obj_name = validate_input_nodes(obj_name)
        string_in_name = str(obj_name)
        splitString = string_in_name.split("_")
        valid = True
        if len(splitString) == len(self.name_convention.keys()):
            for keys in self.validation:
                if keys in self.name_convention:
                    if splitString[self.name_convention[keys]] in self.validation[keys]:
                        valid = valid and True
                    else:
                        print ('key not found: %s' % keys)
                        print ('%s not found in %s' % (splitString[self.name_convention[keys]], self.validation[keys]))
                        valid = False
            return valid
        else:
            print('Not same token number in name {} '.format(obj_name))
            return False

    def guess_object_type(self, scene_object):
        scene_object = validate_input_nodes(scene_object)
        ObjType = cmds.objectType(scene_object)
        ObjType = self.token_validation(ObjType, 'objectType')

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
            print('Type not identified:', cmds.objectType(scene_object))
        return ObjType

    def rename_guess_type_in_name(self, current_name):
        """
            This functions renames a name in format and adds the correct objectType described on the type dictionary
            to acomplish this, will look the objectType maya command and will match the type on the dictionary,
            this token will be placed on the objectType token place, and the object will be renamed to the new name.
        """
        current_name = validate_input_nodes(current_name)

        new_name_array = []
        name_list = []
        if type(current_name) == list:
            name_list = current_name
        elif type(current_name) in [str]:
            name_list = [current_name]
        for current_name in name_list:
            new_name = current_name
            if cmds.objExists(new_name):
                if self.is_name_in_format(new_name):
                    object_type = self.guess_object_type(current_name)
                    new_name = self.set_from_name(new_name, object_type, "objectType")
            new_name = self.unique_name(new_name)
            cmds.rename(current_name, new_name)
            new_name_array.append(new_name)

        if len(new_name_array) == 1:
            return new_name_array[0]
        else:
            return new_name_array

    def rename_based_on_base_name(self, base_name, obj_to_rename, **wantedNameDic):

        obj_to_rename = validate_input_nodes(obj_to_rename)
        base_name = validate_input_nodes(base_name)

        wantedNameCreated = {}
        if self.is_name_in_format(base_name):
            baseNameTokens = base_name.split('_')
            for eachToken in self.name_convention:
                if eachToken in wantedNameDic:
                    wantedNameCreated[eachToken] = str(wantedNameDic[eachToken])
                else:
                    wantedNameCreated[eachToken] = baseNameTokens[self.name_convention[eachToken]]

                wantedNameCreated['objectType'] = self.guess_object_type(obj_to_rename)
        else:
            for eachToken in self.name_convention:
                if eachToken in wantedNameDic:
                    wantedNameCreated[eachToken] = str(wantedNameDic[eachToken])
                else:
                    wantedNameCreated[eachToken] = self.default_names[eachToken]
            if not 'name' in wantedNameDic:
                NamesList = obj_to_rename.split("_")
                NewName = ""
                for names in NamesList:
                    NewName += names
                wantedNameCreated['name'] = NewName

        if cmds.objExists(obj_to_rename):
            NewName = self.set_name_in_format(**wantedNameCreated)
            cmds.rename(obj_to_rename, NewName)
            return NewName
        else:
            return False

    def get_a_short_name(self, scene_object):
        scene_object = validate_input_nodes(scene_object)
        if self.is_name_in_format(scene_object):
            Value = re.split(r"([0-9]+$)", self.get_from_name(scene_object, 'name'))
            return Value[0]
        else:
            Value = re.split(r"([0-9]+$)", scene_object)
            return Value[0]

    def remove_namespace(self, name):
        tokens = name.split(':')
        name_token = tokens[len(tokens) - 1].split('|')
        return name_token[len(name_token) - 1]

    def set_defaults_from_name(self, base_name, **read_tokens):
        if self.is_name_in_format(base_name):
            for each_token in read_tokens.keys():
                if each_token in self.default_names:
                    self.default_names[each_token] = re.split(r"([0-9]+$)", self.get_from_name(base_name,
                                                                                               each_token))[0]


if __name__ == '__main__':
    import pymel.core as pm
    # locator = pm.ls('locator1')[0]
    name_convention = NameConvention()
    print (name_convention.remove_namespace('C_joint00_tail_jnt'))
    # name_convention.set_defaults_from_name('L_main_now_msh', side=True, name=True, system=True, objectType=True)
