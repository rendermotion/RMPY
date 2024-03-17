Name Convention
===============
All RMPY works with the name_convention class, the creators, rigs and tools that require a name of a new element on the rig(any maya node), will pick it based on the context of the creation of the object.

The name convention is based on a token structure that is formed by a fixed number of tokens.
Each token can have different types of constraints.
The default convention that ships with RMPY is made of 4 tokens.

    side_name_system_objectType

On this convention there are two tokens that have constraints. side, and objectType.
side has the the constraints left, right and center. And it is used to differentiate the build side of the object.
The values that are use for each side constraints, are follows.

    'L' for left
    'R' for right
    'C' for center

For the **objectType** the constraint is some characters that define the type of the object, this characters are predefined on a dictionary and are automatically added to a name, based on the type of the object. You can overwrite this behaviour using the combination of characters as long as they are predefined on the dictionary.

For example a orientConstraint type object has the token ORC or a parentConstraint has the token PRC and in the case
of joints the token is JNT.
But there are tokens in this field that can be forced and overwritten, a joint object can also be SKN (in my case I wanted to
differentiate the joints and the ones with this token are joints made for skining)

A second example would be the geometry objects that by default get the prefix MSH but I can override this token with
lets say a BSM to differentiate the meshes from the blendshape Meshes. As I said this token is auto assigned, but can be
overwritten by any value on the valid list.


<paragraph>
    Main functions to
<block_quote>






