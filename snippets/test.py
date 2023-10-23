import pymel.core as pm

for each in range(20):
    esfera_transform, esfera_creation = pm.polySphere()
    esfera_transform.translateX.set(each)
    esfera_creation.radius.set(3/each)