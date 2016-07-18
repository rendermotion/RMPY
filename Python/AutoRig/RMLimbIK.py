import maya.cmds as cmds
import RMRigTools
reload (RMRigTools)
import RMRigShapeControls
reload (RMRigShapeControls)
import RMNameConvention
reload (RMNameConvention)


class RMLimbIKFK(object):
    def __init__(self, NameConv = None):
        if not NameConv:
            self.NameConv = RMNameConvention.RMNameConvention()
        else:
            self.NameConv = NameConv

        self.IKjointStructure = None
        self.IKparentGroup = None

        self.FKjointStructure = None
        self.FKparentGroup = None

        self.SknJointStructure = None
        self.SknparentGroup = None

    def RMLimbJointEstructure(self,OriginPoint,ZAxisOrientation = "z", ):
        LimbReferencePonits = RMRigTools.RMCustomPickWalk(OriginPoint,'transform',2)
        return RMRigTools.RMCreateBonesAtPoints(LimbReferencePonits,NameConv = self.NameConv, ZAxisOrientation = ZAxisOrientation)


    def RMMakeIkStretchy(self,ikHandle):
        endJoint = cmds.ikHandle(ikHandle, q = True, endEffector = True)
        parents = RMRigTools.RMCustomPickWalk (endJoint, 'joint', 2, Direction = "up")

    def RMLimbRig(self,RootReferencePoint):

        self.IKparentGroup , self.IKjointStructure = self.RMLimbJointEstructure(RootReferencePoint)
        self.RMCreateIKControls()
        #self.FKparentGroup , self.FKjointStructure = self.RMLimbJointEstructure(RootReferencePoint)        
        #self.RMCreateFKControls()
    
    def RMCreateFKControls(self,AxisFree = "Y"):
        FKFirstLimbControl = RMRigShapeControls.RMCreateBoxCtrl(self.FKjointStructure[0],Xratio=1,Yratio=.3,Zratio=.3)
        ArmParent = RMRigTools.RMCreateGroupOnObj(FKFirstLimbControl)
        RMRigTools.RMLinkHerarchyRotation (self.FKjointStructure[0], self.FKjointStructure[1],FKFirstLimbControl)

        RMRigTools.RMLockAndHideAttributes (FKFirstLimbControl,'0000111000')

        FKSecondLimbControl = RMRigShapeControls.RMCreateBoxCtrl(self.FKjointStructure[1],Xratio=1,Yratio=.3,Zratio=.3)
        SecondLimbParent = RMRigTools.RMCreateGroupOnObj(FKSecondLimbControl)
        cmds.parent(SecondLimbParent, FKFirstLimbControl)

        RMRigTools.RMLinkHerarchyRotation (self.FKjointStructure[1], self.FKjointStructure[2], FKSecondLimbControl)
        if AxisFree == "Y":
            RMRigTools.RMLockAndHideAttributes (FKSecondLimbControl,'0000100000')
        if AxisFree == "Z":
            RMRigTools.RMLockAndHideAttributes (FKSecondLimbControl,'0000010000')

    def RMCreateIKControls(self):
        #joints = RMRigTools.RMCustomPickWalk (IKRootJnt, 'joint', depth)
        ikControl = RMRigShapeControls.RMCreateBoxCtrl(self.IKjointStructure[len(self.IKjointStructure)-1], Xratio = .3, Yratio = .3, Zratio = .3, ParentBaseSize = True)
        IKHandle, effector = cmds.ikHandle (sj = self.IKjointStructure[0], ee = self.IKjointStructure[len(self.IKjointStructure)-1], name = "LimbIKHandle")
        #ikControl = RMRigShapeControls.RMCreateBoxCtrl( joints[len(joints)-1])
        PontConstraint = cmds.pointConstraint (ikControl, IKHandle, name = "LimbCntrlHandleLink")


LimbArmRight = RMLimbIKFK()
LimbArmRight.RMLimbRig("Character01_RH_shoulder_pnt_rfr")
LimbArmLeft = RMLimbIKFK()
LimbArmLeft.RMLimbRig("Character01_LF_shoulder_pnt_rfr")

LimbLegRight = RMLimbIKFK()
LimbLegRight.RMLimbRig("Character01_LF_leg_pnt_rfr")
LimbLegLeft = RMLimbIKFK()
LimbLegLeft.RMLimbRig("Character01_RH_leg_pnt_rfr")
#Limb.RMLimbJointEstructure("Character01_RH_shoulder_pnt_rfr")
#Limb.RMLimbJointEstructure("Character01_LF_leg_pnt_rfr")
#Limb.RMLimbJointEstructure("Character01_RH_leg_pnt_rfr")

#RMCreateIKControls("Character01_MD_Leg_jnt_FK",2)
#RMMakeIkStretchy('ikHandle1')
'''
global proc RMMakeIkStretchy (string $ikHandle)
{
    //Find the end joint where the ikHandle is located.
    string $endJoint[];
    $endJoint[0] = `eval ("ikHandle -q -endEffector " + $ikHandle)`;
    select $endJoint[0];
    $endJoint = `pickWalk -d up`;
    $endJoint = `pickWalk -d down`;
    //Find the start joint being affected by the ik handle.
    string $startJoint[];
    $startJoint[0] = `eval ("ikHandle -q -startJoint " + $ikHandle)`;
    //Now that we know the start and end joints for the ik handle,
    //we need to find the world space of these joints so that we can,
    //calculate the total length of the chain.
    //Create a vector array to store the world space coordinates of the joints.
    vector $jointPos[];
    //Vector between two points
    vector $btwPointsVector = <<0,0,0>>;
    //Create a float to store the distance between the current joint and the last one.
    float $distBtwJoints = 0;
    //This will store the total distance along the length of the chain.
    float $totalDistance = 0;
    //String variable to house current joint being queried in the while loop.
    string $currentJoint = $startJoint[0];
    //Counter integer used in the while loop to determine the proper index in the vector array.
    int $counter = 0;
    //Initial selection going into the while loop/
    select $startJoint;
    //Exit loop boolean
    int $exitLoop = 0;
    //Will loop through all the joints between the base and end by pickwalking through them.
    //The loop stores the world space of each joint into $jointPos as it iterates over them.
    //The while loop keeps going until the current joint equals the end joint.
    while ($exitLoop == 0)
    {
        //Exit loop condition
        if ($currentJoint == $endJoint[0])
        {
            $exitLoop = 1;
        }
        //Query the world space of the current joint.
        $jointPos[$counter] = `joint -q -p -a $currentJoint`;
        if ($counter != 0)
        {
            //Calulate the distance between this joint and the last.
            //First compute the vector between the two points
            $btwPointsVector = ($jointPos[$counter-1]) - ($jointPos[($counter)]);
            //Now compute the length of the vector (the distance)
            $distBtwJoints = mag ($btwPointsVector);
            //Add the distance onto our total
            $totalDistance = ($totalDistance + $distBtwJoints);
        }
        pickWalk -d down;
        $sel = `ls -sl`;
        $currentJoint = $sel[0];
        $counter++;
    }
    //Now that we have the distance along the length of the chain ($totalDistance),
    //we can use this to make the chain stretch when that distance
    //is exceeded by the IK handle.
    //To measure the distance from the ik handle to the start joint.
    //Create two empty group nodes and use there translates to
    //calculate the distance using a distanceBetween render node.
    string $startPoint = `group -em`;
    string $endPoint = `group -em`;
    $startPoint = `rename $startPoint ($ikHandle + "startPoint")`;
    $endPoint = `rename $endPoint ($ikHandle + "endPoint")`;
    pointConstraint -offset 0 0 0 -weight 1 $startJoint[0] $startPoint;
    pointConstraint -offset 0 0 0 -weight 1 $ikHandle $endPoint;
    //Create a distance between render node.
    string $distanceNode = `shadingNode -asUtility distanceBetween`;
    //Connect the translates of the point constrained grp nodes
    //to the point1 and point2 inputs on the distance node.
    connectAttr -f ($startPoint + ".translate") ($distanceNode + ".point1");
    connectAttr -f ($endPoint + ".translate") ($distanceNode + ".point2");
    //Create a condition render node.
    string $conditionNode = `shadingNode -asUtility condition`;
    connectAttr -f ($distanceNode + ".distance") ($conditionNode + ".colorIfFalseR");
    connectAttr -f ($distanceNode + ".distance") ($conditionNode + ".secondTerm");
    //Set the condition node operation to 'greater or equal' ie, (>=)
    setAttr ($conditionNode + ".operation") 3;
    //Set the condition node's first term equal to the $totalDistance
    setAttr ($conditionNode + ".firstTerm") $totalDistance;
    //Set the condition node's colorIfTrueR equal to the $totalDistance
    setAttr ($conditionNode + ".colorIfTrueR") $totalDistance;
    //Create a multiply/Divide render node.
    string $muliDivNode = `shadingNode -asUtility multiplyDivide`;
    //Set the dividend to be the distance btw the ik handle and the start joint.
    connectAttr -f ($conditionNode + ".outColorR") ($muliDivNode + ".input1X");
    //Set the divisor to the total distance along the chain
    setAttr ($muliDivNode + ".input2X") $totalDistance;
    //Set the node operation to 'divide'
    setAttr ($muliDivNode + ".operation") 2;
    //Now that we have the normalized scale factor, lets plug this into the
    //scaleX of each joint in the chain.
    $exitLoop = 0;
    $currentJoint = $startJoint[0];
    select $currentJoint;
    //The while loop keeps going until the current joint equals the end joint.
    while ($exitLoop == 0)
    {
        //Connect the output of the multiply/divide node to the
        //scale 'X' of the joints. This will cause them to stretch
        //along their length as the distance expands.
        connectAttr -f ($muliDivNode + ".outputX") ($currentJoint + ".scaleX");
        //Pickwalk down to move down through the joint heirarchy.
        pickWalk -d down;
        $sel = `ls -sl`;
        $currentJoint = $sel[0];
        //Exit loop condition
        if ($currentJoint == $endJoint[0])
        {
            $exitLoop = 1;
        }
    }
    if (`objExists ("*MD_Mover2_ctr_rig")`)
    {
        parent $startPoint ScaledData;
        parent $endPoint ScaledData;
    }
    
    select $ikHandle;
}
'''