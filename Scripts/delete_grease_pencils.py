import bpy

""" by stephen-l
    delete all scenes grease pencil
"""
scene = bpy.context.scene
if scene.grease_pencil :
    scene.grease_pencil.clear()
    scene.grease_pencil = None

# nettoye les datablocks
gps = bpy.data.grease_pencil[:]
for gp in gps:
    if gp.users < 1:
        bpy.data.grease_pencil.remove(gp)
                
""" by Wazou
    you can also use, rough mode:
"""
gps = bpy.data.grease_pencil[:]
for gp in gps:
    bpy.data.grease_pencil.remove(gp, do_unlink=True)