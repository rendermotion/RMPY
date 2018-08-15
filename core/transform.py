import pymel.core as pm
from RMPY.core import validate
from RMPY.core import config


def align(obj1, obj2, translate=True, rotation=True):
    obj1 = validate.as_pymel_nodes(obj1)
    obj2 = validate.as_pymel_nodes(obj2)
    if translate:
        Obj1position = pm.xform(obj1, q=True, ws=True, rp=True)
        pm.xform(obj2, ws=True, t=Obj1position)
    if rotation:
        rotate_order_obj1 = pm.xform(obj1, q=True, rotateOrder=True)
        rotate_order_obj2 = pm.xform(obj2, q=True, rotateOrder=True)
        if rotate_order_obj1 != rotate_order_obj2:
            Null = pm.group(em=True)
            pm.xform(Null, rotateOrder=rotate_order_obj1)
            Obj1rotacion = pm.xform(obj1, q=True, ws=True, ro=True)
            pm.xform(Null, ws=True, ro=Obj1rotacion)
            pm.xform(Null, p=True, rotateOrder=rotate_order_obj2)
            Obj1rotacion = pm.xform(Null, q=1, ws=1, ro=True)
            pm.xform(obj2, ws=True, ro=Obj1rotacion)
            #print "Warning : Obj Rotation Order Mismatch on obj "
            #print  (obj2 + " Aligning to " + obj1 + "\n")
            pm.delete(Null)
        else:
            Obj1rotacion = pm.xform(obj1, q=True, ws=True, ro=True)
            pm.xform(obj2, ws=True, ro=Obj1rotacion)


def joint_length(scene_joint):
    children = pm.listRelatives(scene_joint, children=True)
    if children:
        if len(children) > 0 and pm.objectType(children[0]) != "locator":
            return pm.getAttr('{}.translate{}'.format(children[0], config.axis_order[0].upper()))
        else:
            return joint_size(scene_joint)
    else:
        return joint_size(scene_joint)


def joint_size(scene_joint):
    if pm.objectType(scene_joint) == "joint":
        radius = pm.getAttr(scene_joint + ".radius")
        return (radius * 2)
    else:
        return 1.0