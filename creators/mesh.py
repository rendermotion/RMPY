import maya.api as om
from RMPY.core import dataValidators
import pymel.core as pm
geometry = dataValidators.as_pymel_nodes(pm.ls(selection=True))
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
