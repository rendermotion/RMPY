
Group
=====

A group is the most common thing to create when you are doing a rig.
RMPY provides a general group function to create groups.

The group creator allow you to create empty transform nodes. You can provide multiple input transforms at the same time.
The only way to create it is using the point_base function.
Inside a rig class you can create a group based on a point.
the main keyword argument is type, valid types are : 'inserted', 'parent', 'child', 'sibbling'.

In all cases the new group will be aligned to the base point. This options will only change the hierarchy.
**Inserted**: creates a new group as parent of the provided transform but parented to the original parent of the transform, therefore is inserted in the hierarchy between the parent and its child.
**Parent**: The new group will be parent of the selected group but will break the hierarchy it will be parent to the root.
**Child**: The new group will be child of the selected group.
**Sibling**: The new group will be on the same hierarchy as the base point, therefore it will be its sibling since both will share the same parent.




.. currentmodule:: creators.group

.. autoclass:: Group
    :members:
    :undoc-members:
