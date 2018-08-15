import maya.api as om

geometry = RMRigTools.validate_pymel_nodes(geometry)
# vertex_destination_list = destination.vtx
result = {}

selection_list = om.MSelectionList()
selection_list.add(geometry.fullPath())
selObj = selection_list.getDagPath(0)
mfnSourceObject = om.MFnMesh(selObj)

mfnSourceObject.getPoints()
selObj = selection_list.getDagPath(1)
mfnDestinationObject = om.MFnMesh(selObj)
vertex_in_source = mfnSourceObject.getPoints(space=om.MSpace.kWorld)
