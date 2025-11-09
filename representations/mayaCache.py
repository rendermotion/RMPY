import pymel.core as pm
from RMPY.core import dataManager
from maya import mel


class MayaCache(object):
    def __init__(self):
        self.extra_path = 'mayaCache'

    def save(self, *geometry_nodes, extra_folder=''):
        shapes = [each.getShape() for each in geometry_nodes]
        dataManager.DataManager()
        data_manager = dataManager.DataManager()
        data_manager.file_path = f'{data_manager.file_path}/{self.extra_path}/{extra_folder}'
        # pm.cacheFile(geometry=geometry_nodes)
        print(data_manager.file_path)
        pm.cacheFile(f='shapeCache', directory=data_manager.file_path, staticCache=True,
                     worldSpace=True, st=1, et=100, points=shapes, singleCache=True)

    def load(self, *geometry_nodes):
        shapes = [each.getShape() for each in geometry_nodes]
        shapes_switch = [mel.eval(f'createHistorySwitch("{each}",false)') for each in shapes]
        dataManager.DataManager()
        data_manager = dataManager.DataManager()
        data_manager.file_path = '{}/{}'.format(data_manager.file_path, self.extra_path)
        pm.cacheFile(f='shapeCache', directory=data_manager.file_path,
                     # worldSpace=True, st=1, et=100,
                     points=shapes,
                     ia=[f'{each}.inp[0]' for each in shapes_switch],
                     # ia=[f'{each}.inMesh' for each in shapes],
                     singleCache=True,
                     createCacheNode=True)

        [pm.setAttr(f'{each}.playFromCache', 1) for each in shapes_switch]


if __name__ == '__main__':
    geometry_list = pm.ls('geo')[0].getChildren()
    # MayaCache().save(*geometry_list)
    MayaCache().load(*geometry_list)


