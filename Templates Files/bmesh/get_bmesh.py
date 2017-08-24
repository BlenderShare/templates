import bpy
import bmesh
 
def get_bmesh(ob):
    me = ob.data
     
    if ob.mode == 'OBJECT':
        # Get a BMesh representation
        bm = bmesh.new()    # create an empty BMesh
        bm.from_mesh(me)    # fill it in from a Mesh
        return bm
    
    # Get a BMesh representation
    bm = bmesh.from_edit_mesh(me)
    return bm

def finalize_bmesh(bm, ob):
    me = ob.data
 
    if ob.mode == 'OBJECT':
        # Finish up, write the bmesh back to the mesh
        bm.to_mesh(me)
        bm.free()   # free and prevent further access
        del bm
 
    else:
        # Finish up, write the bmesh back to the mesh
        bmesh.update_edit_mesh(me)

C = bpy.context
ob = C.object

bm = get_bmesh(ob)

# Do some stuff
# If the mesh was edited, we need to update it to considerate the changes (like vertex selection/deselection, added/removed verts, edges or faces ects...)

# finalize_bmesh(bm, ob)