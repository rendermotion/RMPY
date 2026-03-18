================
System structure
================

The system structure is the hierarchy that will contain the rig you are building.

Everytime you create a rig a hierarchy will be created, the basic structure of a rig is expected to consist in 4 groups,
one main system group, called root, and a settings locator, that controls visibility of the rig. Any object that
belongs to the rig should find its place under one of this groups.

    **root**: This folders are the main system group, referred as root.
        **settings**: A locator called settings, where all the settings of to control the rig can be accessed.

        **kinematics**:A group called kinematics, you can place all the nodes that form the rig  that are not joints or controls.

        **joints**:A group called joints, where all the output joints of the rig can be placed.

        **controls**: A group called controls, where all the controls of the rig should live.

        **display**:A group called display, anything you want to be visible to the user but not selectable(reference only).



.. tip::
    None of this groups need to be created, you only need to use them, they are defined as properties and it will be automatically created.
    An instance of this object lives under the self.rig_system name space in every rig that inherits from BigBase.


.. currentmodule:: rig.SystemStructure

.. autoclass:: RigStructureModel
    :members:
    :private-members:
    :undoc-members:

.. autoclass:: SystemStructure
    :members:

