from RMPY.creators import creatorsBase
from RMPY.core import config
from RMPY.core import dataValidators
import pymel.core as pm
reload(creatorsBase)


class Creator(creatorsBase.Creator):
    def __init__(self, *args, **kwargs):
        super(Creator, self).__init__(*args, **kwargs)
        self.curve = None

    def node_base(self, *nodes, **kwargs):
        super(Creator, self).node_base(*nodes, **kwargs)
        """
        creates a motion path on the provided nodes and attaches them to a curve
        you can control the up vector, and make it one object, or a list of objects one for each Node List
        :param nodes: list of  nodes that will constraint to the path
        :param curve: curve that will have the nodes
        :param UpVectorType: type of UpVector, can be object, array, anything else will be assumed as scene
        :param UpVectorArray: the array of objects that will be the upVector
        :param upVectorObject: the object that will be upVector
        :return:
        """
        motion_path_list = []
        if 'curve' in kwargs.keys():
            self.curve = dataValidators.as_pymel_nodes(kwargs.pop('curve'))

        name = kwargs.pop('name', 'motionPath')

        followAxis = kwargs.pop('followAxis', config.orient_axis[0])
        upAxis = kwargs.pop('upAxis', config.orient_axis[1])

        kwargs['followAxis'] = followAxis
        kwargs['upAxis'] = upAxis

        UpVectorType = kwargs.pop('UpVectorType', 'world')
        UpVectorArray = kwargs.pop('UpVectorArray', None)
        upVectorObject = kwargs.pop('upVectorObject', None)

        if self.curve:
            len_node_list = len(nodes)
            spans = pm.getAttr(self.curve + ".spans")

            min_value = pm.getAttr(self.curve + ".minValue")
            max_value = pm.getAttr(self.curve + ".maxValue")

            form = pm.getAttr(self.curve + ".form")
            step = 0.0
            if len_node_list > 1:
                if form == 0 or form == 1:
                    step = (max_value - min_value) / (len_node_list - 1)
                else:
                    step = (max_value - min_value) / len_node_list
            else:
                step = 0

            node_count = 0

            for each_node in nodes:
                if UpVectorType == 'object':
                    motion_path_node = pm.pathAnimation(each_node, c=self.curve, follow=True,
                                                        worldUpObject=upVectorObject,
                                                        worldUpType="objectrotation", **kwargs)
                elif UpVectorType == 'array':
                    motion_path_node = pm.pathAnimation(each_node, c=self.curve, follow=True,
                                                        worldUpObject=UpVectorArray[node_count],
                                                        worldUpType="object", **kwargs)
                else:
                    motion_path_node = pm.pathAnimation(each_node, c=self.curve, follow=True, worldUpType="scene",
                                                        **kwargs)

                motion_path_node = dataValidators.as_pymel_nodes(motion_path_node)
                motion_path_list.append(motion_path_node)

                list_add_double_linear = each_node.listConnections(type='addDoubleLinear', source=False)
                pm.delete(list_add_double_linear)

                motion_path_node.xCoordinate >> each_node.translateX
                motion_path_node.yCoordinate >> each_node.translateY
                motion_path_node.zCoordinate >> each_node.translateZ

                connection = pm.listConnections(motion_path_node.uValue)
                if connection:
                    pm.delete(connection)
                motion_path_node.uValue.set(step * node_count)
                # pm.setKeyframe(motionPath, v=(step * nodeCount), at="uValue")
                self.name_conv.rename_name_in_format(str(motion_path_node), name=name)
                node_count += 1
            value = pm.currentTime(q=True)
            pm.currentTime(value + 1, e=True)
            pm.currentTime(value, e=True)
        if len(motion_path_list) == 1:
            return motion_path_list[0]
        return motion_path_list


if __name__ == '__main__':

    test_root = pm.ls('C_cubeTest00_pathDeform_GRP')[0]
    motion_path = Creator()
    motion_path.node_base(*test_root.getChildren(), curve='C_curveOnSurface00_twistCable_SHP', name='defo',
                          UpVectorType='object', upVectorObject='C_upVector_path_LOC')