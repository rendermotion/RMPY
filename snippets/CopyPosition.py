import maya.cmds as cmds

sel=cmds.ls(sl=True)
print sel

position =(cmds.getAttr(sel[0]+".t"))
rotation = (cmds.getAttr(sel[0]+".r"))
scale = (cmds.getAttr(sel[0]+".s"))

print position[0][0]
print position[0][1]
print position[0][2]
print rotation
print scale

#cmds.setAttr(sel[1]+".t",position[0][0],position[0][1],position[0][2])
cmds.setAttr(sel[1]+".r",rotation[0][0],rotation[0][1],rotation[0][2])
#cmds.setAttr(sel[1]+".s",scale[0][0],scale[0][1],scale[0][2])
