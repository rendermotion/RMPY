import random
import maya.cmds as cmds
import RMRigTools 

Expresion = '''//{0}
{0}.rotateX=`noise((time+{2})*{1}.frequency)`*{1}.amplitud;
{0}.rotateY=`noise((time+{2}+30)*{1}.frequency)`*{1}.amplitud;
{0}.rotateZ=`noise((time+{2}+60)*{1}.frequency)`*{1}.amplitud;
{0}.ty=`noise((time+{2}+90)*{1}.frequency)`*{1}.movY + {1}.movY;
'''
#ExpressionNode = cmds.expression (name = "NoiseMainExpresion", string = Expresion.format( "pCylinder1" , "nurbsCircle1", random.uniform (0,100)))





def  addAttributes(Object):
	cmds.addAttr( Object , at="float", ln = "movY",   hnv = 1, hxv = 1, h = 0, k = 1, smn = 0, smx = 10)
	cmds.addAttr( Object , at="float", ln = "amplitud",   hnv = 1, hxv = 1, h = 0, k = 1, smn = -10, smx = 10)
	cmds.addAttr( Object , at="float", ln = "frequency",   hnv = 1, hxv = 1, h = 0, k = 1, smn = -10, smx = 10)




bbSphere = RMRigTools.boundingBoxInfo("pSphere1")
print bbSphere.lenX
print bbSphere.lenY
print bbSphere.lenZ