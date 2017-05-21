import maya.cmds as cmds


def progressiveConstraint(startObject, endObject, objectList, constraintType="parent", mo=True):
    constraintValue = float(0.0)
    NumElements = len(objectList)
    deltaConstValue = 1.0 / (float(NumElements) + 1)
    print deltaConstValue

    for eachObject in objectList:
        constraintValue = constraintValue + deltaConstValue
        print "ConstValue = %s" % constraintValue

        if constraintType == 'parent':
            cmds.parentConstraint(startObject, eachObject, w=1.0 - constraintValue, mo=mo)
            cmds.parentConstraint(endObject, eachObject, w=constraintValue, mo=mo)

        elif constraintType == 'orient':
            cmds.orientConstraint(startObject, eachObject, w=1.0 - constraintValue, mo=mo)
            cmds.orientConstraint(endObject, eachObject, w=constraintValue, mo=mo)

        elif constraintType == 'point':
            cmds.pointConstraint(startObject, eachObject, w=float(1) - constraintValue, mo=mo)
            cmds.pointConstraint(endObject, eachObject, w=constraintValue, mo=mo)


def deepthProgressiveconstraint(depth, objectList, constraintType="orient", mo=True):
    childGroup = []
    if depth > 1:
        for eachGroup in objectList:
            eachChild = cmds.listRelatives(eachGroup, children=True, type="transform")
            childGroup.append(eachChild[0])
        deepthProgressiveconstraint(depth - 1, childGroup)

    progressiveConstraint(objectList[0], objectList[len(objectList) - 1], objectList[1:-1],
                          constraintType=constraintType, mo=mo)


if __name__ == '__main__':
    selection = cmds.ls(selection=True)
    deepthProgressiveconstraint(4, selection, constraintType="orient", mo=True)
# progressiveConstraint(selection[0],selection[len(selection)-1], selection[1:-1],constraintType="orient",mo = True)
