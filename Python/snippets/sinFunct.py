import math
import maya.cmds as cmds


def AddAttributes (Object, Attribute, SMN = None, SMX = None,keyable = 1 ):
    #print ("Adding Attribute:%s  to Object:%s Min:%s MAx %s"%(Attribute,Object,SMN,SMX))
    AttrList = cmds.listAttr(Object)
    if Attribute not in AttrList:   
        if SMN != None and SMX != None:
            cmds.addAttr(Object, at="float", ln = Attribute ,hnv = 1, hxv = 1, h = 0, k = keyable, smn = SMN, smx = SMX)
        else:
            cmds.addAttr(Object, at="float", ln = Attribute ,hnv = 0, hxv = 0, h = 0, k = keyable)

def sinfunction(control, objectList, axis):
    expression = cmds.expression( name = "SinFunction",unitConversion = "none")
    AddAttributes(control, "Amplitud")
    AddAttributes(control, "phase" )
    AddAttributes(control, "waveLen"       ,SMN =   0   , SMX = 10)
    AddAttributes(control, "DecayHead"     ,SMN =   0   , SMX = 10)
    AddAttributes(control, "DecayHeadLimit",SMN =  .01  , SMX = 10)
    cmds.setAttr('%s.DecayHeadLimit'%control, 10)

    offset = math.pi / (len(objectList) -1)
    script = ''
    count = 0
    for eachObject in objectList:
        script  = script + 'if (%s > %s.DecayHeadLimit/10 * %s)\n'%(offset * count, control , math.pi)
        script  = script + '    %s.translate%s =  %s.Amplitud * sin(%s.phase + %s * %s * %s.waveLen);\n'%(eachObject, axis , control ,control, offset,count ,control)
        #script =  script + '    %s.translateX = %s.Amplitud;\n'%(eachObject, control)
        script  =  script + 'else \n'
        script  = script + '     %s.translate%s =   (1 - %s.DecayHead / 10 * ((cos( %s * %s  / (%s.DecayHeadLimit / 10) ) + 1)/2) ) * %s.Amplitud * sin(%s.phase + %s * %s * %s.waveLen);\n'%(eachObject, axis , control , offset,count ,control, control, control, offset, count , control)
        #script =  script + '    %s.translateX =   (1 - %s.DecayHead * ((cos( %s * %s / %s.DecayHeadLimit ) + 1)/2) ) * %s.Amplitud;\n'                                       %(eachObject , control , offset, count ,control,control)
        count += 1
    cmds.expression(expression ,edit=True, string=script,unitConversion = "none")


