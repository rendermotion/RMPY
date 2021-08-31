##############
# GET FnMesh
##############
from maya.api import OpenMaya

def getMfnMesh(name):
    sel = OpenMaya.MSelectionList()
    try:
        sel.add(str(name))
    except RuntimeError as e:
        return e

    dagPath = sel.getDagPath(0)
    return OpenMaya.MFnMesh(dagPath)

###############
# Get UV Data
###############

def getUvData(name):
    from collections import namedtuple
    uvDataTuple = namedtuple('uvDataTuple', 'uvCounts uvIds uvs')
    uvData = dict()
    mesh = getMfnMesh(name)
    for uvSet in mesh.getUVSetNames():
        uvCounts, uvIds = mesh.getAssignedUVs(uvSet)
        uvData[uvSet] = uvDataTuple(uvCounts, uvIds, getMfnMesh(name).getUVs(uvSet))
        print uvCounts
        print uvIds
        print mesh.getUVs(uvSet)
    return uvData


def build():
    ####################
    # poly Cube test
    ####################

    pCube1 = getMfnMesh("pCube1")
    toCopyUvData = getUvData("toCopy")

    ### Uv data from the source mesh to copy
    uvCounts = toCopyUvData.values()[0].uvCounts
    polyCounts = len(uvCounts)
    uvIds = toCopyUvData.values()[0].uvIds
    u, v = toCopyUvData.values()[0].uvs
    print 'after function'
    print u
    print v
    print uvIds
    ##############
    # Clear Uvs
    # Set Uvs
    # Assign Uvs
    ##############

    uvSetName = pCube1.createUVSet("mapTest")
    # uvSetName = "map1"
    pCube1.setCurrentUVSetName(uvSetName)
    # pCube1.clearUVs()
    pCube1.setUVs(u, v, uvSetName)
    # pCube1.assignUVs(uvCounts, uvIds, uvSetName)
    assign_uvs('pCube1', uvCounts, uvIds,  uvSetName)

    print pCube1.numUVs(pCube1.getUVSetNames()[0])
    print pCube1.numUVs(pCube1.getUVSetNames()[1])


def assign_uvs(mesh_name, uvCounts, uvIds, uvSetName):
    geo_object =getMfnMesh(mesh_name)
    index_uvIds = 0
    index_polygon = 0
    for each_uv_face_vertex_number in uvCounts:
        for each_uv_index in range(each_uv_face_vertex_number):
            print index_polygon, each_uv_index, uvIds[index_uvIds], uvSetName
            geo_object.assignUV(index_polygon, each_uv_index, uvIds[index_uvIds], uvSetName)
            index_uvIds += 1
        index_polygon += 1




    # Try Assigning Uvs
if __name__=='__main__':
    build()
    # pCube1 = getMfnMesh("pCube1")
    # print pCube1.numUVs(pCube1.getUVSetNames()[0])
    # print pCube1.numUVs(pCube1.getUVSetNames()[1])