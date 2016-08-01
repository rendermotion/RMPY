import maya.cmds
import maya.api.OpenMaya as om
import RMNameConvention
reload (RMNameConvention)
import RMRigTools

class RMTwistJoints(object):
    def __init__(self, NameConv = None):
        if not NameConv:
            self.NameConv = RMNameConvention.RMNameConvention()
        else:
            self.NameConv = NameConv

        self.TwistJoints = None
        self.TwistResetPoint = None
    def RMCreateTwistJoints(self, TwistJoint, LookAtObject,  NumberOfTB = 5):
        LookAtObject = cmds.listRelatives(TwistJoint,type = "transform",children=True)

    

        positionA = cmds.xform(TwistJoint ,q=True,ws=True,rp=True)
        positionB = cmds.xform(LookAtObject ,q=True,ws=True,rp=True)

        vectorA = om.MVector(positionA)
        vectorB = om.MVector(positionB)
        
        self.RMCreateBonesBetweenPoints(vectorA,vectorB,NumberOfTB, AlignObject = TwistJoint)

        control = cmds.RMRigShapeControls.RMCreateBoxCtrl('')
        xform(control, ls=True, relative=True,  t = [0,1,0])
        cmds.lookAtConstraint(self.TwistJoints[0], aim = [1,0,0], upVector = [0,0,0], wut = control)

        TwistJointDivide = cmds.shadingNode( asUtility = "MultiplyDivide",name = "TwistJoint" + self.NameConv.RMGetAShortName(TwistJoint))
        TwistJointDivide = self.NameConv.RMRenameNameInFormat(TwistJointDivide)
        









            '''
            TwistPoint=RMCreateChildPoint #(TwistBone)
            TwistPoint.name=uniquename("TwistPoint")
            TwistBoneArray[1].parent=TwistPoint
            
            TwistCntrlPntOrig=RMCreateChildPoint #(TwistBone)
            TwistCntrlPntOrig.name=uniquename("TwistControlOrigin")
            
            TwistCntrlPntEnd=RMCreateChildPoint #(TwistBone)
            TwistCntrlPntEnd.name=uniquename("TwistControlEnd")
            in coordsys local move TwistCntrlPntEnd [((distance PuntoInicial PuntoFinal)*(NumberOfTB-1)/NumberOfTB),0,0]
            
            for n=2 to  TwistBoneArray.count do
                paramWire.connect TwistBone.children[1].position.controller[#X_Position]   TwistBoneArray[n].position.controller[#X_Position] "X_Position/3"
            
            --RMAttachToPoints TwistBoneArray[1] TwistBoneArray[3] TwistBoneArray[2] flag:2
            upNode1=RMLookAtConstraint TwistCntrlPntOrig TwistBone.children[1] Axis:"Y" UpNodeValue:-1
            upNode2=RMLookAtConstraint TwistCntrlPntEnd TwistBone.children[1] Axis:"Y" UpNodeValue:-1
            for n=1 to NumberOfTB do
                (
                  RMAttachToPoints   TwistCntrlPntOrig TwistCntrlPntEnd  TwistBoneArray[n] flag:2 weightNeg:(1.0-(n-1.0)/(NumberOfTB-1.0)) weightPos:((n-1.0)/(NumberOfTB-1.0)) wireWeight:False
                )
            if TwistBone.parent != undefined do 
                upNode1.parent=TwistBone.parent
            upNode2.parent=TwistBone
            --Regresa 
                -- Los Punos que controlan el Twist
                --Los Upnodes de Los puntos que controlan el Twist
                -- El origen de los twistBones
            return #(#(TwistCntrlPntOrig,TwistCntrlPntEnd),#(upNode1,upNode2),TwistCntrlPntOrig)'''

    def RMCreateBonesBetweenPoints(self,InitialPoint, FinalPoint, NumberOfTB,AlignObject = None):
        DirectionVector  = FinalPoint-InitialPoint
        TotalLength = DirectionVector.length()
        Step = TotalLength / NumberOfTB
        StepVector = DirectionVector.normal() * Step
        locatorsList = []

        for count in range(0,NumberOfTB + 1):
            Locator = cmds.spaceLocator()
            if AlignObject:
                if self.NameConv.RMIsNameInFormat (AlignObject):
                    Locator[0] = self.NameConv.RMRenameBasedOnBaseName(AlignObject,Locator[0], NewName= 'TwistJoint' + self.NameConv.RMGetFromName(AlignObject,"Name").capitalize())
            locatorsList.append(Locator[0])
            cmds.xform(Locator[0], translation = list(InitialPoint + (StepVector * count)), worldSpace=True)
            RMRigTools.RMAlign(AlignObject,Locator[0],2)
        self.TwistResetPoint , self.TwistJoints = RMRigTools.RMCreateBonesAtPoints(locatorsList)
        return self.TwistJoints



TJ = RMTwistJoints()
TJ.RMCreateTwistJoints("Character01_LF_shoulder_pnt_rfr")








