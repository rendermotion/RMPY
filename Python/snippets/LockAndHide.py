import RMRigTools
selection = cmds.ls(selection = True)
if selection:
    if (cmds.getAttr("%s.visibility"%selection[0])):
        for eachObject in selection :
            RMRigTools.RMLockAndHideAttributes( eachObject, "xxxxxxxxx1" )
            cmds.setAttr("%s.visibility"%eachObject,False)
            RMRigTools.RMLockAndHideAttributes( eachObject, "xxxxxxxxxl" )
    else:
        for eachObject in selection :
            RMRigTools.RMLockAndHideAttributes( eachObject, "xxxxxxxxx1" )
            cmds.setAttr("%s.visibility"%eachObject,True)
        
    