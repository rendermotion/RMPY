import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel
from RMPY.rig import genericRig
from RMPY.core import config
from RMPY.core import validate
from RMPY.core import transform
from RMPY.creators import curve

reload(genericRig)
reload(transform)


def RebuildWithNCVs(numberOfCvs, curve):
    curve = validate.as_pymel_nodes(curve)
    if curve.form() == 'periodic':
        if numberOfCvs >= 3:
            curve = pm.rebuildCurve(curve, spans=numberOfCvs, keepRange=2)[0]
            return curve
        else:
            return None
    else:
        if numberOfCvs >= 4:
            curve = pm.rebuildCurve(curve, spans=numberOfCvs - 3, keepRange=2)[0]
            return curve
        else:
            return None

class LacesModel(object):
    def __init__(self):
        self.clusters = None
        self.joints = None
        self.upVector = None
        self.controls = None
        self.curve = None
        self.upVectorCurve = None
        self.rig_parent = None
        self.joints_parent = None
        self.upVector_parent = None
        self.controls_parent = None
        self.clusters_parent = None


class Laces(genericRig.GenericRig):
    def __init__(self, *args, **kwargs):
        super(Laces, self).__init__(*args, **kwargs)
        self._model = LacesModel()
        self.create_curve = curve.Curve()

    @property
    def clusters(self):
        return self._model.clusters

    @clusters.setter
    def clusters(self, cluster_list):
        self._model.clusters = cluster_list

    @property
    def joints(self):
        return self._model.joints

    @property
    def upVector(self):
        return self._model.upVector

    @property
    def curve(self):
        return self._model.curve

    @property
    def rootControls(self):
        return self._model.controls_parent

    @property
    def upVectorCurve(self):
        return self._model.upVectorCurve

    @property
    def controls(self):
        return self._model.controls

    @controls.setter
    def controls(self, value):
        self._model.controls = value

    def create_point_base(self, *points, **kwargs):
        super(Laces, self).create_point_base(*points)

        controls_number = kwargs.pop('controls_number', len(points))
        joint_number = kwargs.pop('joint_number', controls_number*2)
        periodic = kwargs.pop('periodic', False)
        print points
        single_orient_object = kwargs.pop('single_orient_object', False)

        curve = self.create_curve.create_point_base(*points, periodic=periodic, ep=True)

        self.name_conv.set_from_name(curve, 'laceCurve', 'name')
        curve.setParent(self.rig_system.kinematics)
        if controls_number:
            kwargs['curve'] = RebuildWithNCVs(controls_number, curve)
        else:
            kwargs['curve'] = curve

        if not single_orient_object:
            self.RMlacesSystemMultipleRotationControls(joint_number, **kwargs)
        else:
            self.RMlacesSystem(joint_number, curve=kwargs['curve'])

    def create_curve_base(self, curve, **kwargs):
        super(Laces, self).create_curve_base(curve)
        joint_number = kwargs.pop('joint_number', 6)
        numCvs = kwargs.pop('numCvs', curve.numCVs())
        if numCvs == curve.numCVs():
            kwargs['curve'] = curve
        else:
            kwargs['curve'] = RebuildWithNCVs(numCvs, curve)
        self.RMlacesSystemMultipleRotationControls(joint_number, **kwargs)

    def RMCreateClustersOnCurve(self, curve=None):
        if type(curve) in [list, tuple]:
            masterCurve = validate.as_pymel_nodes(curve[0])
            mode = "multi"
        else:
            masterCurve = validate.as_pymel_nodes(curve)
            mode = "single"
        degree = pm.getAttr('%s.degree' % masterCurve)
        spans = pm.getAttr('%s.spans' % masterCurve)
        form = pm.getAttr('%s.form' % masterCurve)
        #	Form (open = 0, closed = 1, periodic = 2)
        clusterList = []
        if form == 0 or form == 1:
            # print "Open Line"
            for i in range(0, (degree + spans)):
                cluster_node, cluster_transform = pm.cluster(masterCurve + ".cv[" + str(i) + "]", name='ClusterOnCurve')
                self.name_conv.rename_name_in_format([str(cluster_node), str(cluster_transform)], useName=True)
                if mode == "multi":
                    self.RMAddToCluster(i, curve[1:], cluster_node)
                clusterList.append(cluster_transform)
                pm.setAttr(cluster_transform.visibility, 0)
                ##pm.cluster(cluster,edit=True,geometry = curve + ".["+str(i)+"]")
        if form == 2:
            # print "periodic Line"
            for i in range(0, spans):
                cluster_node, cluster_transform = pm.cluster(masterCurve + ".cv[" + str(i) + "]", name='ClusterOnCurve')
                self.name_conv.rename_name_in_format([str(cluster_node), str(cluster_transform)], useName=True)
                if mode == "multi":
                    self.RMAddToCluster(i, curve[1:], cluster_node)
                clusterList.append(cluster_transform)
                pm.setAttr(cluster_transform.visibility, 0)
                # pm.cluster(cluster,edit=True,geometry = curve + ".["+str(i)+"]")
        self.clusters = clusterList
        return clusterList

    def RMAddToCluster(self, cvIndex, membershipList, cluster):
        clusterSet = pm.listConnections(cluster, type="objectSet")
        for eachShape in membershipList:
            # pm.cluster(cluster, edit=True, geometry = eachShape + ".cv["+str(cvIndex)+"]" )
            pm.sets(clusterSet[0], add="%s.cv[%s]"%(eachShape, str(cvIndex)))

    def RMJointsOnCurve(self, JointNumber, curve=None, UpVectorType="object", UpVectorArray=None, objectType='joint'):

        """
        creates a series of objects and then attaches them to a motion path using the Nodes on curve function,
        the objects it creates can be from joints, groups, or locators this is defined in objectType keyword Arg.
        JointNumber(int): the number of joints that will be created
        curve(nurbsCurve):the curve where the new objects will be attached.

        UpVectorType: the type of up vector it will use, valid values are "object"(New object will be created),
                     "array" an upvectorArray same length that Joint number should be provided, "world"
        objectType: the type of object that will create  valid Values are joint, group,
                    if anything else si written, will assume spaceLocator
        UpVectorArray: The array of locators that will be used for each new created object
                       should be used in conjunction with UpVectorType : array
        """
        # degree = pm.getAttr (curve+".degree")
        # spans = pm.getAttr (curve+".spans")
        # form = pm.getAttr (curve+".form")
        #	Form (open = 0, closed = 1, periodic = 2)
        UpVectorObject = None
        if UpVectorType == "object":
            UpVectorObject = pm.group(empty=True, name='upVector')
            self.name_conv.rename_name_in_format(str(UpVectorObject), useName=True)

        jointArray = []

        for Num in range(0, JointNumber):
            pm.select(cl=True)
            if objectType == 'joint':
                Newjoint = pm.joint(name="laceJoint")
            elif objectType == 'group':
                Newjoint = pm.group(empty=True, name="laceRefGroup")
            else:
                Newjoint = pm.spaceLocator(name="laceRefLocator")

            self.name_conv.rename_name_in_format(str(Newjoint), useName=True)
            jointArray.append(Newjoint)

        self.RMNodesOnCurve(jointArray, curve, UpVectorType=UpVectorType,
                            UpVectorArray=UpVectorArray, upVectorObject=UpVectorObject)
        return {'joints': jointArray, 'UpVector': UpVectorObject}

    def RMNodesOnCurve(self, NodeList, curve, UpVectorType="object", UpVectorArray=None, upVectorObject=None):
        """
        creates a motion path on the provided NodeList and attaches them to a curve
        you can control the up vector, and make it one object, or a list of objects one for each Node List
        :param NodeList: list of  nodes that will constraint to the path
        :param curve: curve that will have the nodes
        :param UpVectorType: type of UpVector, can be object, array, anything else will be assumed as scene
        :param UpVectorArray: the array of objects that will be the upVector
        :param upVectorObject: the object that will be upVector
        :return:
        """
        lenNodeList = len(NodeList)
        spans = pm.getAttr(curve + ".spans")
        form = pm.getAttr(curve + ".form")
        step = 0.0

        if form == 0 or form == 1:
            step = float(spans) / (lenNodeList - 1)
        else:
            step = float(spans) / (lenNodeList)
        nodeCount = 0
        for each_joint in NodeList:
            if UpVectorType == 'object':
                motionPath = pm.pathAnimation(each_joint, c=curve, follow=True, worldUpObject=upVectorObject,
                                                worldUpType="objectrotation")
            elif UpVectorType == 'array':
                motionPath = pm.pathAnimation(each_joint, c=curve, follow=True, worldUpObject=UpVectorArray[nodeCount],
                                                worldUpType="object")
            else:
                motionPath = pm.pathAnimation(each_joint, c=curve, follow=True, worldUpType="scene")

            motionPath = validate.as_pymel_nodes(motionPath)

            listAddDoubleLinear = each_joint.listConnections(type='addDoubleLinear', source=False)
            pm.delete(listAddDoubleLinear)

            motionPath.xCoordinate >> each_joint.translateX
            motionPath.yCoordinate >> each_joint.translateY
            motionPath.zCoordinate >> each_joint.translateZ
            connection = pm.listConnections(motionPath.uValue)
            if connection:
                pm.delete(connection)
            motionPath.uValue.set(step * nodeCount)
            #pm.setKeyframe(motionPath, v=(step * nodeCount), at="uValue")
            self.name_conv.rename_name_in_format(str(motionPath), name=str(motionPath))
            nodeCount += 1
        value = pm.currentTime(q=True)
        pm.currentTime(value + 1, e=True)
        pm.currentTime(value, e=True)

    def RMcreateContolForPnts(self, points, name, **kwargs):
        cubeLineArray = []
        cube_control_reset_list = []
        reset_joints, joint_list = self.rig_tools.RMCreateBonesAtPoints(points)

        useOrientJoint = kwargs.pop('useOrientJoint', False)
        orientJoint = kwargs.pop('orientJoint', config.axis_order)
        secondaryAxisOrient = kwargs.pop('secondaryAxisOrient', '%sup' % config.axis_order[1])
        world_align = kwargs.pop('world_align', True)

        if useOrientJoint:
            pm.joint(joint_list[0], edit=True, orientJoint=orientJoint, secondaryAxisOrient=secondaryAxisOrient,
                     children=True)
            joint_chain_len = len(joint_list)
            transform.align(joint_list[joint_chain_len-2], joint_list[joint_chain_len-1], translate=False)

        for index, each_point in enumerate(points):
            #cubeLine = self.ShapeControls.create_cube_line(5, 5, 5, centered=True,
            #                                         name=self.NameConv.RMSetNameInFormat({'name': name}))
            resetCube, cubeLine = self.rig_controls.create_box_ctrl(each_point, custom_size=1, name=name, centered=True)

            if not world_align:
                transform.align(joint_list[index], resetCube)
            else:
                resetCube.rotate.set([0, 0, 0])
            pm.parentConstraint(cubeLine, each_point, mo=True)
            cubeLineArray.append(cubeLine)
            cube_control_reset_list.append(resetCube)
        pm.delete(reset_joints)
        return cube_control_reset_list, cubeLineArray

    def RMlacesSystem(self, jointNumber, **kwargs):
        curve = kwargs.pop('curve', None)
        clusters = self.RMCreateClustersOnCurve(curve=curve)
        lacesSystem = self.RMJointsOnCurve(jointNumber, curve=curve, UpVectorType="object")

        skinJoints = pm.group(empty=True, name="skinJoints")
        clustersParent = pm.group(empty=True, name='clusters')

        self.name_conv.rename_name_in_format([str(skinJoints), str(clustersParent)], useName=True)
        pm.parent(clustersParent, self.rig_system.kinematics)
        pm.parent(skinJoints, self.rig_system.joints)
        for eachJoint in lacesSystem["joints"]:
            pm.parent(eachJoint, skinJoints)
            self.rig_system.settings.worldScale >> eachJoint.scaleX
            self.rig_system.settings.worldScale >> eachJoint.scaleY
            self.rig_system.settings.worldScale >> eachJoint.scaleZ

        for eachCluster in clusters:
            pm.parent(eachCluster, clustersParent)
        pm.parent(lacesSystem["UpVector"], self.rig_system.kinematics)

        resetPoints, self.controls = self.RMcreateContolForPnts(clusters, "control", **kwargs)
        resetUpVector, UpVector = self.RMcreateContolForPnts([lacesSystem["UpVector"]], "laceUpVector", **kwargs)

        pm.parent(resetUpVector, self.rig_system.kinematics)

        for eachControl in resetPoints:
            pm.parent(eachControl, self.rig_system.controls)

        self.rig_system.settings.worldScale >> self.rig_system.controls.scaleX
        self.rig_system.settings.worldScale >> self.rig_system.controls.scaleY
        self.rig_system.settings.worldScale >> self.rig_system.controls.scaleZ

        self._model.controls_parent = self.rig_system.controls
        self._model.curve = curve
        self._model.upVectorCurve = None
        self._model.rig_parent = self.rig_system.root
        self._model.joints_parent = skinJoints
        self._model.upVector_parent = resetUpVector
        self._model.joints = lacesSystem["joints"]
        self._model.upVector = lacesSystem["UpVector"]

    def RMlacesSystemMultipleRotationControls(self, jointNumber, **kwargs):
        curve = kwargs.pop('curve', None)
        curve_distance = kwargs.pop('curve_distance', 1)
        offset_axis = kwargs.pop('offset_axis', 'Z')
        fk_controls = kwargs.pop('fk_controls', False)

        OrientationCurve = pm.duplicate(curve)[0]

        if self.name_conv.is_name_in_format(OrientationCurve):
            self.name_conv.set_from_name(OrientationCurve, 'upVectorCurve', 'name')
        else:
            self.name_conv.rename_name_in_format(OrientationCurve, name='upVectorCurve',
                                                 system=self.name_conv.get_a_short_name(OrientationCurve))

        OrientationCurve.setParent(self.rig_system.kinematics)

        #pm.move(curve_distance, OrientationCurve, moveY=True)
        if offset_axis in ['z','Z']:
            OrientationCurve.translateZ.set(OrientationCurve.translateZ.get()+curve_distance)
        if offset_axis in ['y','Y']:
            OrientationCurve.translateY.set(OrientationCurve.translateZ.get()+curve_distance)
        if offset_axis in ['x','X']:
            OrientationCurve.translateX.set(OrientationCurve.translateZ.get()+curve_distance)

        # clusterObjects =
        self.RMCreateClustersOnCurve(curve=[curve, OrientationCurve])
        clusters = pm.group(empty=True, name='clusters')
        self.rig_system.settings.worldScale >> clusters.scaleX
        self.rig_system.settings.worldScale >> clusters.scaleY
        self.rig_system.settings.worldScale >> clusters.scaleZ
        # for i in clusterObjects:
        for i in self.clusters:
            pm.parent(i, clusters)

        cntrls = pm.group(empty=True, name='LaceCntrls')
        resetPoints, self.controls = self.RMcreateContolForPnts(self.clusters, "laceControl", **kwargs)

        cntrls.setParent(self.rig_system.controls)
        self.name_conv.rename_name_in_format([str(cntrls), str(clusters)], useName=True)
        for index, eachControl in enumerate(resetPoints):
            if not fk_controls:
                pm.parent(eachControl, cntrls)
            else:
                if index == 0:
                    pm.parent(eachControl, cntrls)
                else:
                    pm.parent(eachControl, self.controls[index - 1])


        self.RMLacesSystemBasedOnTwoCurves(jointNumber, curve, OrientationCurve)
        pm.parent(clusters, self.rig_system.kinematics)
        self._model.controls_parent = cntrls

    def RMLacesSystemBasedOnTwoCurves(self, jointNumber, curveRig, curveOrient, objectsType='joint'):

        UpVectorArray = self.RMJointsOnCurve(jointNumber, curve=curveOrient, UpVectorType="world",
                                             objectType='spaceLocator')
        lacesSystem = self.RMJointsOnCurve(jointNumber, curve=curveRig, UpVectorArray=UpVectorArray["joints"],
                                           UpVectorType="array", objectType=objectsType)

        #rig = pm.group(empty=True, name="LaceRig")
        skinJoints = pm.group(empty=True, name='LaceSkinJoints')
        UpVectorNodes = pm.group(empty=True, name='LaceUpVector')

        pm.parent(skinJoints, self.rig_system.joints)
        pm.parent(UpVectorNodes, self.rig_system.kinematics)
        self.name_conv.rename_name_in_format([str(UpVectorNodes), str(skinJoints)], useName=True)

        index = 0
        for each_joint in lacesSystem["joints"]:
            pm.parent(each_joint, skinJoints)
            self.rig_system.settings.worldScale >> each_joint.scaleX
            self.rig_system.settings.worldScale >> each_joint.scaleY
            self.rig_system.settings.worldScale >> each_joint.scaleZ
            self.name_conv.rename_set_from_name(each_joint, "skinjoint", Token="objectType")
            index += 1

        for i in UpVectorArray["joints"]:
            pm.parent(i, UpVectorNodes)

        self.rig_system.settings.worldScale >> self.rig_system.controls.scaleX
        self.rig_system.settings.worldScale >> self.rig_system.controls.scaleY
        self.rig_system.settings.worldScale >> self.rig_system.controls.scaleZ

        self._model.curve = curveRig
        self._model.upVectorCurve = curveOrient
        self._model.rig_parent = self.rig_system.root
        self._model.joints_parent = skinJoints
        self._model.upVector_parent = UpVectorNodes
        self._model.joints = lacesSystem["joints"]
        self._model.upVector = UpVectorArray["joints"]

        return {'main': self.rig_system.root, 'parentSkinJoints': skinJoints, 'parentUpVector': UpVectorNodes,
                'UpVectorSystem': UpVectorArray, 'pathFollowObjects': lacesSystem}

if __name__ == '__main__':
    rope_root = pm.ls('C_rope00_reference_grp')[0]
    laces_rig = Laces()
    print rope_root.getChildren()
    laces_rig.create_point_base(*rope_root.getChildren(),
                                offset_axis='y', centered=True)