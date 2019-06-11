Name Convention
===============
The name convention is based on a token structure that is conformed by several tokens.
Each token can have different types of constraints, for example, lets assume the default example
if you have a 4 token convention that has the following tokens.

    side_name_system_objectType

this is the name convention that I have been using during the last years for all rigs that I create two
tokens have constraints. side, and objectType.
side has the the constraints left, right and center since I use it to differentiate the build side of the object.
and the values that I like to use for each side constraint as are follows.

    for left I like to use  'L'

    for right I like to use  'R'

    and finally
    for center I like to use 'C'

in the case of the objectType the constraints on the name are a little bit open to start I am considering
the type of the object the first thing that matters to me, and the second thing is a custom choise of the token.

For example a orientConstraint type object has the token ORC or a parentConstraint has the token PRC and in the case
of joints the token is JNT.
But there are tokens in this field that can be overwritten, a joint object can also be SKN (in my case I wanted to
differentiate the joints and the ones with this token are joints made to skining)

A second example would be the geometry objects that by default get named MSH but I can override this token with
lets say a BSM to differentiate the meshes from the blendshape Meshes. As I said this token is kind of tricky because
it is asigned a value by default but this value can be easily overwritten by a value on the valid list.



