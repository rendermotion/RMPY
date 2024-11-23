====
Rigs
====
The rig module has a base class called RigBase
This class is the main class where all the rigs inherit.
The idea behind the rigBase class is that all rigs can work as a brick that assembles with other rigs,
with a standardized way of connecting, a standard hierarchy, standard creation functions and a set of tools to aid in rig creation,
all of this under a simplified name convention.

Standard creation functions.
Any rig has something that is used as base to create the rig, most common thing are space locators(points in space),
but you can find rigs that are created based on a curve or geometry.
The standard functions for  rig creation are
    create_point_base: Need to provide input points to create the rig.
    create_curve_base: A curve is the base of the rig.
    create_geometry_base: Some geometry will be the base to create the rig.
While creating rigs with this function you are inheriting some procedures that are in place to name every part of your rig.
In general when you are creating something inside the rig you dont have to worry about the system that it belongs to or
which side of the rig is found, you just provide a simple name without '_' for every object, and the system will take care
of what is the correct full name for your object.
You can find object that takes care of the name convention under self.name_convention.


.. currentmodule:: rig.rigBase
.. autoclass:: RigBase
    :members: create_point_base


.. autoclass:: BaseModel
    :members:
    :undoc-members:

.. autoclass:: RigBase
    :members:
    :undoc-members: