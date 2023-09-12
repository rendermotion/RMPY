import pymel.core as pm
from RMPY.core import dataManager


class Curve(object):
    def __init__(self):
        self.node = None
        self.repr_dict = {}
        self.extra_path = '/nurbsCurves'

    @classmethod
    def by_name(cls, curve_node):
        curve_node = pm.ls(curve_node)[0]
        class_instance = cls()
        if type(curve_node) == pm.nodetypes.NurbsCurve:
            class_instance.node = curve_node.getParent()
        else:
            if type(curve_node.getShapes()[0]) == pm.nodetypes.NurbsCurve:
                class_instance.node = curve_node
        return class_instance

    def save(self, *args, **kwargs):
        if len(args) >= 1:
            file_name = args[0]
        else:
            file_name = '%s' % self.node
        data_manager = dataManager.DataManager()
        data_manager.file_path = '{}{}'.format(data_manager.file_path, self.extra_path)
        data_manager.save(file_name, self.get_repr_dict(), **kwargs)

    def load(self, *args, **kwargs):
        try:
            if len(args) >= 1:
                file_name = args[0]
            else:
                file_name = '%s' % self.node
            data_manager = dataManager.DataManager()
            data_manager.file_path = '{}{}'.format(data_manager.file_path, self.extra_path)
            self.repr_dict = data_manager.load(file_name, **kwargs)
            return self.repr_dict

        except IOError:
            if len(args) >= 1:
                file_name = args[0]
            else:
                file_name = '%s' % self.node

            print ("couldn't load file name: {}".format(file_name))

    def get_repr_dict(self):
        self.repr_dict = {'type': 'curve',
        'data': {'transform': str(self.node),
        'shapes': {}}}
        shapes = self.node.getShapes()
        for each_shape in shapes:
            self.repr_dict['data']['shapes'][str(each_shape)] = {}
            self.repr_dict['data']['shapes'][str(each_shape)]['degree'] = each_shape.degree()
            self.repr_dict['data']['shapes'][str(each_shape)]['spans'] = each_shape.spans.get()
            self.repr_dict['data']['shapes'][str(each_shape)]['form'] = each_shape.form().index - 1
            self.repr_dict['data']['shapes'][str(each_shape)]['rational'] = False
            self.repr_dict['data']['shapes'][str(each_shape)]['dimension'] = 3# no 2d curves supported
            self.repr_dict['data']['shapes'][str(each_shape)]['knots'] = list(each_shape.getKnots())
            self.repr_dict['data']['shapes'][str(each_shape)]['cps'] =[[each.x, each.y, each.z]
                                                                       for each in each_shape.getCVs(space='object')]
            self.repr_dict['data']['shapes'][str(each_shape)]['type'] = 'nurbsCurve'
        return self.repr_dict

    def set_repr_dict(self):
        if self.repr_dict:
            if 'type' in self.repr_dict.keys():
                if self.repr_dict['type'] == 'curve':
                    # if not self.node:
                    #     self.node = pm.ls(self.repr_dict)
                    for each_shape_name, shape_node in zip(self.repr_dict['data']['shapes'], self.node.getShapes()):
                        if str(shape_node) in self.repr_dict['data']['shapes'].keys():
                            current_key = str(shape_node)
                        else:
                            current_key = each_shape_name
                        connections = pm.listConnections('{}.create'.format(self.node), source=True, destination=False)
                        if connections:
                            print ('forcing curve: {} the following node was deleted: {}'.format(self.node, connections))
                            pm.delete(connections)
                        pm.setAttr('{}.cc'.format(shape_node),
                                   self.repr_dict['data']['shapes'][current_key]['degree'],
                                   self.repr_dict['data']['shapes'][current_key]['spans'],
                                   self.repr_dict['data']['shapes'][current_key]['form'],
                                   self.repr_dict['data']['shapes'][current_key]['rational'],
                                   self.repr_dict['data']['shapes'][current_key]['dimension'],
                                   self.repr_dict['data']['shapes'][current_key]['knots'],
                                   len(self.repr_dict['data']['shapes'][current_key]['knots']),
                                   len(self.repr_dict['data']['shapes'][current_key]['cps']),
                                   *self.repr_dict['data']['shapes'][current_key]['cps'], type='nurbsCurve')

                else:
                    print ('not valid curve type found in '
                           'representation dictionary load, check source {}'.format(self.repr_dict))
            else:
                print ('not valid type key on curve representation '
                       'dictionary load, check source {}'.format(self.repr_dict))
        else:
            print ('no representation dictionary for {}'.format(self.node))


if __name__ == '__main__':
    control_curve = Curve.by_name('C_cog00_Hip_ctr')
    from pprint import pprint as pp
    control_curve.load()
    # pp(control_curve.repr_dict)
    control_curve.set_repr_dict()
    # pp(control_curve.get_repr_dict())