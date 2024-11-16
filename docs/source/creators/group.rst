
Group creator
=============

A group is the most common thing to create when you are doing a rig.
RMPY provides a general group function to create groups.

The group creator allow you to create empty transform nodes. You can provide multiple input transforms at the same time.
The only way to create it is using the point_base function.
Inside a rig class you can create a group based on a point.
the main keyword argument is type, valid types are : 'inserted', 'parent', 'child', 'sibbling'.
    inserted: creates a new group as parent of the provided transform but parented to the original parent of the transform,
              therefore is inserted in the hierarchy between the parent and its child




.. currentmodule:: creators.group

.. autoclass:: Group
    :members:
    :undoc-members:
