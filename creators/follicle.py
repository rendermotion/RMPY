import pymel.core as pm
from RMPY import RMRigTools


class Follicle(object):
    def __init__(self):
        self.Hys = None
        self.hair_system()

    def surface_based(self, nurbs_surface, **kwargs):
        nurbs_surface = RMRigTools.validate_pymel_nodes(nurbs_surface)
        surface = None
        if nurbs_surface == pm.nodetypes.NurbsSurface:
            surface = nurbs_surface
        else:
            shapes = nurbs_surface.getShapes()
            if shapes:
                surface = shapes[0]
        if surface:
            u_value = kwargs.pop('u_value', .5)
            v_value = kwargs.pop('v_value', .5)
            pm.language.Mel.eval('createHairCurveNode("%s", "%s" ,%s ,.5 , 1 ,0 ,0 ,0 ,0 ,"" ,1.0 ,{%s} ,"" ,"" ,2 );' %
                                 (self.Hys, surface, u_value, v_value))
            new_follicle = pm.ls('follicle1')[0]
            return new_follicle
        else:
            print 'not valid surface provided'
            raise AttributeError

    def hair_system(self):
        pm.language.Mel.eval('createNode hairSystem')
        self.Hys = pm.ls("hairSystem1")[0]

    def cleanup(self):
        #pm.delete(pm.listRelatives(self.Hys, p=True))
        pm.delete(self.Hys)
        self.Hys = None

if __name__ == '__main__':
    new_fol = Follicle()
    new_fol.surface_based('C_basePlane00_suspension_GRP')