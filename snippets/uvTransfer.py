import maya.cmds as cmds

Uvs = cmds.polyUVSet("pCubeShape1", q=True, allUVSets=True)[0]
print(Uvs)
size = len("pCubeShape1."+Uvs)
for i in range(0, size):
	cmds.polyEditUV("pCubeShape1." + Uvs + "["+str(i) + "]", q=True, uValue=True)


