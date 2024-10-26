====
Rigs
====
The rigs module has a base class called RigBase
This class is the main layout to all the rigs.
The idea behind the rigBase class is that all rigs can work as a brick that assembles with other rigs,
with similar creation functions, a standard way of connecting, a standard hierarchy, and a set of tools to aid in rig creation.

The creation functions.
Any rig has something that is used a s a base to create the rig, most common thing are transforms in space, or space locators.
The function that acomplishes this is the create_point_base function.

.. currentmodule:: rig.rigBase
.. autoclass:: RigBase
    :members: create_point_base





.. autoclass:: BaseModel
    :members:
    :undoc-members:

.. autoclass:: RigBase
    :members:
    :undoc-members: