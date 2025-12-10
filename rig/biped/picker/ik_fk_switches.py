import pymel.core as pm
from RMPY.core import rig_core


def fk_to_ik(namespace, side, system, set_key=False, switch=True):
    fk_arm = ['{}:{}_fk00_{}_ctr'.format(namespace, side, system), '{}:{}_fk01_{}_ctr'.format(namespace, side, system)]
    ik_joints_arm = ['{}:{}_ik01_{}_jnt'.format(namespace, side, system), '{}:{}_ik02_{}_jnt'.format(namespace, side, system)]
    ik_pole_vector = '{}:{}_ikPoleVectorIK00_{}_ctr'.format(namespace, side, system)

    for destination, source in zip(fk_arm, ik_joints_arm):
        rig_core.aim_point_based(destination, destination, source, ik_pole_vector)
        pm.setAttr(f'{destination}.scale', [1, 1, 1])
        # rig_core.align(destination.format(namespace, side, system), source.format(namespace, side, system), rotate=True, translate=False)
        # pm.matchTransform(destination.format(namespace, side, system), source.format(namespace, side, system), rotation=True)
    if switch:
        pm.setAttr(f'{namespace}:{side}_root00_{system}_ctr.IkFkSwitch', 0)
    if set_key:
        pm.setKeyframe(fk_arm[0])
        pm.setKeyframe(fk_arm[1])
        pm.setKeyframe(f'{namespace}:{side}_root00_{system}_ctr.IkFkSwitch')


def ik_to_fk(namespace, side, system, set_key=False,  switch=True):
    fk_joints = ['{}:{}_fk00_{}_jnt', '{}:{}_fk01_{}_jnt', '{}:{}_fk02_{}_jnt']
    fk_tip = '{}:{}_fk02_{}_jnt'
    ik_controls = ['{}:{}_ikIK00_{}_ctr', '{}:{}_ikPoleVectorIK00_{}_ctr']
    side_joints = []
    for each in fk_joints:
        side_joints.append(each.format(namespace, side, system))
    pole_vector = rig_core.space_locator.pole_vector(*side_joints)
    pm.matchTransform(ik_controls[0].format(namespace, side, system), fk_tip.format(namespace, side, system),
                      position=True)
    pm.matchTransform(ik_controls[1].format(namespace, side, system), pole_vector, position=True)
    pm.delete(pole_vector)
    if switch:
        pm.setAttr(f'{namespace}:{side}_root00_{system}_ctr.IkFkSwitch', 10)
    if set_key:
        pm.setKeyframe(ik_controls[0].format(namespace, side, system))
        pm.setKeyframe(ik_controls[1].format(namespace, side, system))
        pm.setKeyframe(f'{namespace}:{side}_root00_{system}_ctr.IkFkSwitch')


def ik_fk_switch_animation():
    namespace, side, system = identify_limb()
    start_time = pm.playbackOptions(q=True, minTime=True)
    end_time = pm.playbackOptions(q=True, maxTime=True)
    original_time = pm.currentTime(q=True)
    if pm.getAttr('{}:{}_root00_{}_ctr.IkFkSwitch'.format(namespace, side, system)) > 5:
        for each in range(int(start_time), int(end_time + 1)):
            pm.currentTime(each, e=True)
            fk_to_ik(namespace, side, system, set_key=True, switch=True)
    else:
        for each in range(int(start_time), int(end_time + 1)):
            pm.currentTime(each, e=True)
            ik_to_fk(namespace, side, system, set_key=True, switch=True)
    pm.currentTime(original_time, e=True)


def ik_fk_switch():
    namespace, side, system = identify_limb()

    if pm.getAttr(f'{namespace}:{side}_root00_{system}_ctr.IkFkSwitch') > 5:
        fk_to_ik(namespace, side, system)
    else:
        ik_to_fk(namespace, side, system)


def identify_limb():
    selection = pm.ls(selection=True)[0]
    namespace_split = selection.split(':')
    if len(namespace_split) > 1:
        namespace = namespace_split[0]
        object_name = namespace_split[-1]
    else:
        namespace = ''
        object_name = namespace_split[0]

    object_split = object_name.split('_')
    side = object_split[0]
    system = object_split[2]
    return namespace, side, system


if __name__ == '__main__':
    ik_fk_switch_animation()
    ik_fk_switch()




