import pymel.core as pm


def create_static_geo():
    static_geo = [u'venom_eye_goo_left_geo', u'venom_eye_left_geo',  u'venom_body_geo', u'venom_eye_goo_right_geo', u'venom_eye_right_geo']
    match_name = [u'L_eyeGoo_static_geo', u'L_eye_static_geo',  u'C_body_static_geo', u'R_eyeGoo_static_geo', u'R_eye_static_geo']
    static_geo_root = pm.ls('static_geo')
    if static_geo_root:
        static_geo_root = static_geo[0]
    else:
        static_geo_root = pm.group(empty=True, name='static_geo')

    for each_geo, static_geo in zip(static_geo, match_name):
        static_geo_duplicate = pm.duplicate(each_geo, name=static_geo)[0]
        static_geo_duplicate.setParent(static_geo_root)
        blend_shape_node = pm.blendShape(each_geo)[0]
        pm.blendShape(str(blend_shape_node), edit=True, target=[str(each_geo), 0, str(static_geo_duplicate),  1.0])
        blend_shape_node.setWeight(0, 1.0)


if __name__ == '__main__':
    create_static_geo()
