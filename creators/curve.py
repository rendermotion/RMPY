import pymel.core as pm
from RMPY.rig import genericRig


class Creator(genericRig.GenericRig):
    def __init__(self, *args, **kwargs):
        super(Creator, self).__init__(*args, **kwargs)

    def create_point_base(self, *pointList, **kwargs):
        super(Creator, self).create_point_base(*pointList, **kwargs)

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

'''
class Creator(RigBase.RigBase):
    def __init__(self, *args, **kwargs):
        super(Creator, self).__init__(*args,**kwargs)

    def curve_base(self, curve, number_of_cvs=4):
        curve = dataValidators.as_pymel_nodes(curve)

        if curve.form() == 'periodic':
            if number_of_cvs >= 3:
                curve = pm.rebuildCurve(curve, spans=number_of_cvs, keepRange=2)[0]
                return curve
            else:
                return None
        else:
            if number_of_cvs >= 4:
                curve = pm.rebuildCurve(curve, spans=number_of_cvs - 3, keepRange=2)[0]
                return curve
            else:
                return None

    def animation_base(self, animated_node):
        end_play_back = pm.playbackOptions(q=True, maxTime=True)
        start_play_back = pm.playbackOptions(q=True, minTime=True)
        positions = []
        for each_frame_index in range(int(start_play_back), int(end_play_back)):
            pm.currentTime(each_frame_index, edit=True)
            positions.append(dataValidators.as_vector_position(animated_node))
        return self.point_base(positions)

    def point_base(self, *listofPoints, **kwargs):
        periodic = kwargs.pop('periodic', False)
        degree = kwargs.pop('degree', 3)
        ep = kwargs.pop('ep', False)

        listofPoints = [dataValidators.as_vector_position(each_point) for each_point in listofPoints]

        if not periodic:
            if ep:
                Curve = pm.curve(degree=degree, ep=listofPoints, name='line')
            else:
                Curve = pm.curve(degree=degree, p=listofPoints, name='line')
        else:
            fullListPoint = listofPoints + listofPoints[:3]
            if ep:
                fullListPoint = listofPoints + listofPoints[:3]
                numElements = len(fullListPoint)
                knotVector = range(-degree + 1, 0) + range(numElements)
                # knotVector = (-2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0)
                Curve = pm.curve(degree=degree, ep=fullListPoint, periodic=periodic, name='line', k=knotVector)
                # for each in fullListPoint:
                #    new_locator = pm.spaceLocator()
                #    new_locator.translate.set(each)
            else:
                fullListPoint = listofPoints + listofPoints[:3]
                numElements = len(fullListPoint)
                knotVector = range(-degree + 1, 0) + range(numElements)
                Curve = pm.curve(degree=degree, p=fullListPoint, periodic=periodic, name='line', k=knotVector)
        self.name_conv.rename_name_in_format(Curve, name = str(Curve))
        return Curve
        '''
if __name__ == '__main__':
    shape = Creator()
    selection = pm.ls(selection=True)
    new_shape = shape.animation_base(selection[0])
    the_final_shape = shape.curve_base(new_shape, number_of_cvs=6)


