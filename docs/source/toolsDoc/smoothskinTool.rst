====================
The smooth skin tool
====================

The smooth skin tool provides an easy way to interpolate the weights between a list of joints that are part of a continuos chain.
The simplest example that can occur to me are the joints of the spine.

Launching the tool
__________________

To launch the tool execute the following code on your script editor.

.. code-block:: python
   :caption: Testing that RMPY was correctly installed.
   :emphasize-lines: 6

    from RMPY.Tools import RMINTSmoothSkinCluster
    RMINTSmoothSkinCluster.Main().show()


.. image:: toolsDoc/img/smooth_skin_base00.png
   :alt: smooth skin tool image