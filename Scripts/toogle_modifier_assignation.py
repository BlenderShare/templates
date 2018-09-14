""" by Wazou
    in one click button: add a subsurf modifier it not, delete if exists
"""


for ob in context.selected_objects:
    bpy.context.scene.objects.active=ob
    if ob.modifiers.get('Subsurf'):
        bpy.ops.object.modifier_remove(modifier="Subsurf")
    else:    
        new_subsurf = ob.modifiers.new("Subsurf", "SUBSURF")
        new_subsurf.show_only_control_edges = True
        new_subsurf.levels = 2
        new_subsurf.show_on_cage = True