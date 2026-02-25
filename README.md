RMPY
=====

This is a rigging framework intended to help you create rigs in an easy and fast way.
Each rig you create has exposed all the properties and maya objects that you define, for easy access, the encapsulation of the rig provides an easy way to assemble multiple rigs, together to increase complexity.
It has standardized methods for creation and connection of the rigs.
You can access the [documentation here](https://rmpy.readthedocs.io).
or check out this [AI generated doc](https://deepwiki.com/rendermotion/RMPY).


RMPY by default is linked to other repository which is called [builder](https://github.com/rendermotion/builder).
This repo provides RMPY of a way to builds rigs fast, and run python scripts in a specific order, and gives pipeline context to RMPY data management functions.

To create your first rig you can test the following code.

**default**
```python
from RMPY.rig import rigWorld
rigWorld.RigWorld()
```
Thought RMPY started as a cmds repository things evolved and many new rigs are done using pymel for simplicity, and now most of the rigs return pymel objects, and I encourage this. 
I have heard many riggers complaining about the speed of pymel, but in my experience it has proven to not be slow if used in the right context. Things where PYMEL starts loosing speed where writen using maya API2.
