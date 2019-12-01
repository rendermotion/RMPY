import maya.cmds as cmds


def RenameHierarchyShapes(SceneObject):
	shapes = cmds.listRelatives(SceneObject, path=True, children=True, shapes=True)
	print shapes
	if shapes:
		cmds.rename(shapes, "%sShape"%SceneObject)
	childList = cmds.listRelatives(SceneObject, children = True)
	if childList:
		for eachChild in childList:
			RenameHierarchyShapes(eachChild)

if __name__=="__main__":
	RenameHierarchyShapes("Face")
