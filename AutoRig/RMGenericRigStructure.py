import maya.cmds as cmds

try:
    from MetacubeScripts import MetacubeFileNameConvention
except:
    pass


class genericRigStructure(object):
    def __init__(self):
        self.groups = {
            "mesh": {"group": "mesh_grp",
                     "subGroup": ["body_grp", "cloth_grp", "accesories_grp", "hair_grp", "trackers_grp",
                                  "collision_grp", "pxycloth_grp", "pxyhair_grp", "dynspline_grp"]},
            "rig": {"group": "rig_grp", "subGroup": None},
            "controls": {"group": "control_grp", "subGroup": None}
        }
        try:
            self.FileNameConv = MetacubeFileNameConvention.MetacubeFileNameConvention()
        except:
            self.FileNameConv = None
        self.CreateStructure()

    def CreateStructure(self):
        MainGroupName = None

        if self.FileNameConv != None:
            if self.FileNameConv.nameInFormat:
                MainGroupName = self.FileNameConv.AssetType + "_" + self.FileNameConv.AssetName + "_rig"
            else:
                MainGroupName = "MainCharacter"
        else:
            MainGroupName = "MainCharacter"

        if cmds.objExists(MainGroupName):
            MainGroup = MainGroupName
        else:
            MainGroup = cmds.group(empty=True, name=MainGroupName)

        for genericGroup in self.groups:
            if cmds.objExists(self.groups[genericGroup]["group"]):
                if not cmds.listRelatives(self.groups[genericGroup]["group"], parent=True)[0] == MainGroupName:
                    cmds.parent(self.groups[genericGroup]["group"], MainGroupName)
            else:
                cmds.group(empty=True, name=self.groups[genericGroup]["group"])
                cmds.parent(self.groups[genericGroup]["group"], MainGroupName)
            if self.groups[genericGroup]["subGroup"]:
                for eachgroup in self.groups[genericGroup]["subGroup"]:
                    if not cmds.objExists(eachgroup):
                        cmds.group(empty=True, name=eachgroup)
                        cmds.parent(eachgroup, self.groups[genericGroup]["group"])
