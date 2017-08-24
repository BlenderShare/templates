import bpy
import bmesh
 
def get_bmesh(ob):
    me = ob.data
 
    if ob.mode == 'OBJECT':
        bm = bmesh.new()
        bm.from_mesh(me)
        return bm
 
    bm = bmesh.from_edit_mesh(me)
    return bm
 
def finalize_bmesh(bm, ob):
    me = ob.data
 
    if ob.mode == 'OBJECT':
        bm.to_mesh(me)
        bm.free()
        del bm
 
    else:
        bmesh.update_edit_mesh(me)
 
 
C = bpy.context
ob = C.object
 
if ob.mode == 'EDIT':
    bpy.ops.mesh.select_mode(type = 'EDGE')
 
bm = get_bmesh(ob)
 
for e in bm.edges:
    if not e.is_manifold:
        e.select = True
    else:
        e.select = False
 
bm.select_flush(False)  # clean selection
 
finalize_bmesh(bm, ob)  # need to update the mesh to considerate the changes
