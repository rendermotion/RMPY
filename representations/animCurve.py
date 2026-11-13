import pymel.core as pm
from RMPY.core import dataManager


class AnimCurve(object):
    def __init__(self):
        self.node = None
        self.repr_dict = {}
        self.extra_path = '/animCurves'
        self.repr_dict = {}

    @classmethod
    def by_name(cls, anim_node):
        anim_node = pm.ls(anim_node)[0]
        class_instance = cls()
        if type(anim_node) in [pm.nodetypes.AnimCurveUL, pm.nodetypes.AnimCurveUU, pm.nodetypes.AnimCurveTU,
                               pm.nodetypes.AnimCurveUA, pm.nodetypes.AnimCurveUT, pm.nodetypes.AnimCurveTT,
                               pm.nodetypes.AnimCurveTA, pm.nodetypes.AnimCurve]:
            class_instance.node = anim_node
        else:
            print('not correct type of node')
            return None
        return class_instance

    def save(self, *args, **kwargs):
        if len(args) >= 1:
            file_name = args[0]
        else:
            file_name = '%s' % self.node
        data_manager = dataManager.DataManager()
        data_manager.file_path = '{}{}'.format(data_manager.file_path, self.extra_path)
        print(data_manager.file_path)
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

    def set_repr_dict(self):
        connection = pm.listConnections(f'{self.node}.output', plugs=True)[0]
        start_number_of_keys = self.node.numKeys()
        if self.repr_dict:
            if 'type' in self.repr_dict.keys():
                if self.repr_dict['type'] == 'animCurve':
                    # pm.cutKey(self.node, clear=True)
                    self.node.setPostInfinityType(self.repr_dict['data']['PostInfinityType'])
                    self.node.setPreInfinityType(self.repr_dict['data']['PostInfinityType'])
                    for index, (time, value) in enumerate(zip(self.repr_dict['data']['keys']['time'], self.repr_dict['data']['keys']['value'])):
                        if index >= start_number_of_keys:
                            pm.setKeyframe(self.node, insert=True, f=time)

                        pm.keyframe(connection, e=True, floatChange=time, index=(index, index))
                        pm.keyframe(connection, e=True, valueChange=value, index=(index, index))
                        pm.keyTangent(connection, e=True,
                                      inAngle=self.repr_dict['data']['keys']['inTangentAngle'][index],
                                      outAngle=self.repr_dict['data']['keys']['outTangentAngle'][index],
                                      outWeight=self.repr_dict['data']['keys']['outTangentWeight'][index],
                                      inWeight=self.repr_dict['data']['keys']['inTangentWeight'][index],
                                      index=(index, index))
    def get_repr_dict(self):
        self.repr_dict = {'type': 'animCurve',
                          'data': {
                              'PostInfinityType': self.node.getPostInfinityType().key,
                              'PreInfinityType': self.node.getPreInfinityType().key,
                        }}
        connection = pm.listConnections(f'{self.node}.output', plugs=True)[0]
        key_data = {}
        key_data['value'] = pm.keyframe(connection, q=True, valueChange=True)
        key_data['time'] = pm.keyframe(connection, q=True, floatChange=True)
        key_data['outTangentAngle'] = pm.keyTangent(self.node, q=True, outAngle=True)
        key_data['inTangentAngle'] = pm.keyTangent(self.node, q=True, inAngle=True)
        key_data['outTangentWeight'] = pm.keyTangent(self.node, q=True, outWeight=True)
        key_data['inTangentWeight'] = pm.keyTangent(self.node, q=True, inWeight=True)
        self.repr_dict['data']['keys'] = key_data

        return self.repr_dict


if __name__ == '__main__':
    numkeys = pm.keyframe('C_object01_rig_UDF', q=True, keyframeCount=True)

    anim_curve = AnimCurve.by_name('C_object01_rig_UDF')

    from pprint import pprint as pp
    anim_curve.get_repr_dict()
    anim_curve.set_repr_dict()
    pp(anim_curve.repr_dict)
