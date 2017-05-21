import maya.cmds as cmds
import maya.mel as mel
from RMPY import RMRigTools
from RMPY import RMNameConvention
from RMPY import RMRigShapeControls

reload(RMNameConvention)


class RMlaces(object):
    def __init__(self, NameConv=None):
        self.curve = None
        if not NameConv:
            self.NameConv = RMNameConvention.RMNameConvention()
        else:
            self.NameConv = NameConv
        self.shpCtrl = RMRigShapeControls.RMRigShapeControls(NameConv=self.NameConv)

    def RMCreateClustersOnCurve(self, curve=None):
        if curve.__class__ in [str, unicode]:
            masterCurve = curve
            mode = "single"
            # print ("degree:%s",degree)
            # print ("spans:%s",spans)
            # print ("form:%s",form)
        elif curve.__class__ == list:
            masterCurve = curve[0]
            mode = "multi"
        degree = cmds.getAttr(masterCurve + ".degree")
        spans = cmds.getAttr(masterCurve + ".spans")
        form = cmds.getAttr(masterCurve + ".form")
        #	Form (open = 0, closed = 1, periodic = 2)
        clusterList = []
        if form == 0 or form == 1:
            # print "Open Line"
            for i in range(0, (degree + spans)):
                cluster = cmds.cluster(masterCurve + ".cv[" + str(i) + "]", name='ClusterOnCurve')
                cluster = self.NameConv.RMRenameNameInFormat(cluster, {}, useName=True)
                if mode == "multi":
                    self.RMAddToCluster(i, curve[1:], cluster)
                clusterList.append(cluster[1])
                cmds.setAttr(cluster[1] + ".visibility", 0)
                ##cmds.cluster(cluster,edit=True,geometry = curve + ".["+str(i)+"]")
        if form == 2:
            # print "periodic Line"
            for i in range(0, spans):
                cluster = cmds.cluster(masterCurve + ".cv[" + str(i) + "]", name='ClusterOnCurve')
                cluster = self.NameConv.RMRenameNameInFormat(cluster, {}, useName=True)
                if mode == "multi":
                    self.RMAddToCluster(i, curve[1:], cluster)
                clusterList.append(cluster[1])
                cmds.setAttr(cluster[1] + ".visibility", 0)
                # cmds.cluster(cluster,edit=True,geometry = curve + ".["+str(i)+"]")
        return clusterList

    def RMAddToCluster(self, cvIndex, membershipList, cluster):
        clusterSet = cmds.listConnections(cluster, type="objectSet")
        for eachShape in membershipList:
            # cmds.cluster(cluster, edit=True, geometry = eachShape + ".cv["+str(cvIndex)+"]" )
            cmds.sets(eachShape + ".cv[" + str(cvIndex) + "]", add=clusterSet[0])

    def RMJointsOnCurve(self, JointNumber, curve=None, UpVectorType="object", UpVectorArray=None, objectType='joint'):
        '''
        UpVectorType    : valid values are "object","array","world"
        objectType: valid Values are joint, group, if anithing else si written, will asume spaceLocator
        '''
        # degree = cmds.getAttr (curve+".degree")
        # spans = cmds.getAttr (curve+".spans")
        # form = cmds.getAttr (curve+".form")
        #	Form (open = 0, closed = 1, periodic = 2)
        UpVectorObject = None
        if UpVectorType == "object":
            UpVectorObject = cmds.group(empty=True, name='upVector')
            UpVectorObject = self.NameConv.RMRenameNameInFormat(UpVectorObject, {}, useName=True)

        jointArray = []

        for Num in range(0, JointNumber):
            cmds.select(cl=True)
            if objectType == 'joint':
                Newjoint = cmds.joint(name="LaceJoint")
            elif objectType == 'group':
                Newjoint = cmds.group(empty=True, name="LaceRefGroup")
            else:
                Newjoint = cmds.spaceLocator(name="LaceRefLocator")

            Newjoint = self.NameConv.RMRenameNameInFormat(Newjoint, {}, useName=True)
            jointArray.append(Newjoint)

        self.RMNodesOnCurve(jointArray, curve, UpVectorType=UpVectorType, UpVectorArray=UpVectorArray,
                            upVectorObject=UpVectorObject)
        return {'joints': jointArray, 'UpVector': UpVectorObject}

    def RMNodesOnCurve(self, NodeList, curve, UpVectorType="object", UpVectorArray=None, upVectorObject=None):

        lenNodeList = len(NodeList)
        spans = cmds.getAttr(curve + ".spans")
        form = cmds.getAttr(curve + ".form")
        step = 0.0

        if form == 0 or form == 1:
            step = float(spans) / (lenNodeList - 1)
        else:
            step = float(spans) / (lenNodeList)
        nodeCount = 0
        for eachJoint in NodeList:
            if UpVectorType == 'object':
                motionPath = cmds.pathAnimation(eachJoint, c=curve, follow=True, worldUpObject=upVectorObject,
                                                worldUpType="objectrotation")
            elif UpVectorType == 'array':
                motionPath = cmds.pathAnimation(eachJoint, c=curve, follow=True, worldUpObject=UpVectorArray[nodeCount],
                                                worldUpType="object")
            else:
                motionPath = cmds.pathAnimation(eachJoint, c=curve, follow=True, worldUpType="scene")
            cmds.setKeyframe(motionPath, v=(step * nodeCount), at="uValue")
            self.NameConv.RMRenameNameInFormat(motionPath, {'name': motionPath})
            nodeCount += 1
        value = cmds.currentTime(q=True)
        cmds.currentTime(value + 1, e=True)
        cmds.currentTime(value, e=True)

    def RMcreateContolForPnts(self, points, name):
        cubeLineArray = []
        for obj in points:
            cubeLine = self.shpCtrl.RMCreateCubeLine(5, 5, 5, centered=True,
                                                     name=self.NameConv.RMSetNameInFormat({'name': name}))

            RMRigTools.RMAlign(obj, cubeLine, 1)
            cmds.makeIdentity(cubeLine, apply=True, t=True, r=True, s=True)
            cmds.parentConstraint(cubeLine, obj)
            cubeLineArray.append(cubeLine)
        return cubeLineArray

    def RMlacesSystem(self, jointNumber, curve=None):
        clusters = self.RMCreateClustersOnCurve(curve=curve)
        lacesSystem = self.RMJointsOnCurve(jointNumber, curve=curve, UpVectorType="object")

        rig = cmds.group(empty=True, name='LaceRig')
        cntrls = cmds.group(empty=True, name="LaceCntrls")
        skinJoints = cmds.group(empty=True, name="LaceSkinJoints")

        rig, cntrls, skinJoints = self.NameConv.RMRenameNameInFormat([rig, cntrls, skinJoints], {}, useName=True)

        cmds.parent(skinJoints, rig)
        for i in lacesSystem["joints"]:
            cmds.parent(i, skinJoints)
        for i in clusters:
            cmds.parent(i, rig)
        cmds.parent(lacesSystem["UpVector"], rig)
        controls = self.RMcreateContolForPnts(clusters, "laceControl")
        UpVector = self.RMcreateContolForPnts([lacesSystem["UpVector"]], "laceUpVector")
        cmds.parent(UpVector[0], cntrls)
        for eachControl in controls:
            cmds.parent(eachControl, cntrls)

    def RMlacesSystemMultipleRotationControls(self, jointNumber, curve=None):
        OrientationCurve = cmds.duplicate(curve)[0]
        cmds.move(5, OrientationCurve, moveY=True)

        clusterObjects = self.RMCreateClustersOnCurve(curve=[curve, OrientationCurve])

        clusters = cmds.group(empty=True, name='clusters')
        for i in clusterObjects:
            cmds.parent(i, clusters)

        cntrls = cmds.group(empty=True, name='LaceCntrls')
        controls = self.RMcreateContolForPnts(clusterObjects, "laceControl")
        cntrls, clusters = self.NameConv.RMRenameNameInFormat([cntrls, clusters], {}, useName=True)

        for eachControl in controls:
            cmds.parent(eachControl, cntrls)
        LacesSystem = self.RMLacesSystemBasedOnTwoCurves(jointNumber, curve, OrientationCurve)
        cmds.parent(clusters, LacesSystem['parent'])

    def RMLacesSystemBasedOnTwoCurves(self, jointNumber, curveRig, curveOrient, objectsType='joint'):
        UpVectorArray = self.RMJointsOnCurve(jointNumber, curve=curveOrient, UpVectorType="world",
                                             objectType='spaceLocator')
        lacesSystem = self.RMJointsOnCurve(jointNumber, curve=curveRig, UpVectorArray=UpVectorArray["Joints"],
                                           UpVectorType="array", objectType=objectsType)

        rig = cmds.group(empty=True, name="LaceRig")
        skinJoints = cmds.group(empty=True, name='LaceSkinJoints')
        UpVectorNodes = cmds.group(empty=True, name='LaceUpVector')

        cmds.parent(skinJoints, rig)
        cmds.parent(UpVectorNodes, rig)
        rig, UpVectorNodes, skinJoints = self.NameConv.RMRenameNameInFormat([rig, UpVectorNodes, skinJoints], {},
                                                                            useName=True)

        index = 0
        for i in lacesSystem["joints"]:
            cmds.parent(i, skinJoints)
            lacesSystem["joints"][index] = self.NameConv.RMRenameSetFromName(i, "skinjoint", Token="objectType")
            index += 1

        for i in UpVectorArray["joints"]:
            cmds.parent(i, UpVectorNodes)

        return {'main': rig, 'parentSkinJoints': skinJoints, 'parentUpVector': UpVectorNodes,
                'UpVectorSystem': UpVectorArray, 'pathFollowObjects': lacesSystem}

    def RebuildWithNCVs(self, numberOfCvs, curve):
        if cmds.getAttr(curve + ".form") == 2:
            if numberOfCvs >= 3:
                curve = cmds.rebuildCurve(curve, spans=numberOfCvs, keepRange=2)[0]
                return curve
            else:
                return None
        else:
            if numberOfCvs >= 4:
                curve = cmds.rebuildCurve(curve, spans=numberOfCvs - 3, keepRange=2)[0]
                return curve
            else:
                return None
