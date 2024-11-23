

skinCluster
===========
The SkinCluster class provides a simple interface to deal with skin clusters, also contains tools to save, and load skin clusters.
Currently there are some known issues on the skin cluster.

    #. The save tool will fail if the indices of the skin cluster are not consecutive.
       This means if a joint has been removed from the skin cluster, and the indices no longer.
    #. The tool currently doesn't save blend weights.
    #. Tool is not written currently with the API so it might not be the fastest option for loading.

.. currentmodule:: creators.skinCluster

.. autoclass:: SkinCluster
    :members: