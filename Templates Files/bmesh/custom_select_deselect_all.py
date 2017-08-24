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
        
def custom_select_deselect_all(bm, select = False):
    """ Select or deselect all
        select:
            - True = select all
            - False = deselect all """
            
    for v in bm.verts:
        
        v.select = select
    
        bm.select_flush(select)


C = bpy.context
ob = C.object

bm = get_bmesh(ob)

custom_select_deselect_all(bm, select = False)

finalize_bmesh(bm, ob)