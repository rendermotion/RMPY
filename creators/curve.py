import pymel.core as pm
from RMPY.rig import genericRig


class Curve(genericRig.GenericRig):
    def __init__(self, *args, **kwargs):
        super(Curve, self).__init__(*args, **kwargs)

    def create_point_base(self, *pointList, **kwargs):
        super(Curve, self).create_point_base(*pointList, **kwargs)

        periodic = kwargs.pop('periodic', False)
        degree = kwargs.pop('degree', 3)
        ep =kwargs.pop('ep', False)

        listofPoints = [pm.xform('%s' % eachPointList, q=True, ws=True, rp=True) for eachPointList in pointList]

        if ep:
            created_curve = pm.curve(degree=degree, ep=listofPoints, name='line')
        else:
            if not periodic:
                created_curve = pm.curve(degree=degree, p=listofPoints, name='line')
            else:
                fullListPoint = listofPoints + listofPoints[:3]
                numElements = len(fullListPoint)
                knotVector = range(-degree + 1, 0) + range(numElements)
                created_curve = pm.curve(degree=degree, p=fullListPoint, periodic=periodic, name='line', k=knotVector)
        self.name_conv.rename_based_on_base_name(pointList[0], created_curve, name=created_curve)
        return created_curve

if __name__ == '__main__':
    selection = pm.ls(selection=True)
    curve = Curve()
    curve.create_point_base(*pm.ls(selection=True), ep=True)



