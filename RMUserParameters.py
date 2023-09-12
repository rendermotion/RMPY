import maya.cmds as cmds

class RMUserParameters(object):
    def __init__ (self, objectBaseName):
        self.object = objectBaseName

    def addNumeric (self, Name, limits = [0,10]):
        AttributeList = cmds.listAttr(self.object)
        if Name  in AttributeList:
            print ("the Object Allready has an Attribute with this name, the type is:",cmds.getAttr (self.object + "." + Name,type = True))
            return False
        else :
            cmds.addAttr(self.object,at = "float", ln=Name,  hnv=1, hxv=1, h=0, k=1, smn=limits[0], smx=limits[1])
            return True