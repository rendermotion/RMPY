================
System structure
================

The system structure is the hierarchy that will contain the rig you are building.

Everytime you create a rig a hierarchy will be created, the basic structure of a rig is expected to consist in 4 folders were everything should be.

    **root**: This folders are the main system folder, referred as root.

        **kinematics**:A group called kinematics, here you can place all the nodes that form the rig  that are not joints or controls.

        **joints**:A group called joints, where all the output joints of the rig can be placed.

        **controls**:A group called controls, where all the controls of the rig should live.

        **display**:A group called display, anything you want to be visible to the user but that might be a reference only(non selectable).

        **settings**: A locator called settings, where all the settings of to control the rig can be accessed.

.. tip::
    None of this groups need to be created, you only need to call it, as a property and it will be automatically created.
    An instance of this class exists inside the any rig instance and can be accessed as self.rig_system


.. currentmodule:: rig.SystemStructure

.. autoclass:: RigStructureModel
    :members:
    :private-members:
    :undoc-members:

.. autoclass:: SystemStructure
    :members:

