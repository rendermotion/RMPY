.. toctree::
    :maxdepth: 1
    :hidden:
    :caption: Understanding creators

========
Creators
========

All creators inherit from a base class called creator. Which provides similar creation functions for the creators class.
In general, creators should return pymel nodes directly of the object created.

The creators are the classes used to create all the nodes on a rig, is an easy way to create the maya nodes.
You can use your custom code(pymel or cmds) to create the maya nodes, but using the creators can provide you of
a rig point of view creator thinking, that will simplify your code.
These are some of the creators that RMPY currently has,  many more could be added,
but so far this are the more common that I have needed through my rig creation process.

.. note::
    Many maya nodes don't have a way to be created through the creators, this nodes can be created with the regular cmds.createNode() function
    and then they could be renamed using the self.name_convention.rename_name_in_format() function on your rig.
    There are other nodes like constraints or matrix nodes that are created automatically when you use the self.connect object inside the rig.
    Notice that another advantage of creating the nodes through the creators, is that they are created with the correct name based on context.


Here you can find a list of creators with their documentation and some examples of how to use them.

    :doc:`/creators/group`

    :doc:`/creators/spaceLocator`

    :doc:`/creators/skinCluster`








