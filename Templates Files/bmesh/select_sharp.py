import bpy
import bmesh
from math import radians

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
        
def get_sharp_edges(ob, bm, angle, sharp):
    """ Return the sharp edges according the 'sharp' argument
        angle: angle in degrees
        sharp:
            - True = get edges with an angle greater than or equal to angle
            - False = get edges with an angle less than to angle """
    
    edges = set()
    
    for e in bm.edges:
        if e.is_manifold:  #to exclude non manifold edges
            face0, face1 = e.link_faces
            
            if sharp:
                if face0.normal.angle(face1.normal) >= radians(angle):
                    edges.add(e)
                
            else:
                if face0.normal.angle(face1.normal) < radians(angle):
                    edges.add(e)
    
    return edges


C = bpy.context
ob = C.object

if ob.mode == 'EDIT':
    bpy.ops.mesh.select_mode(type = 'EDGE')
    
bm = get_bmesh(ob)

edges = get_sharp_edges(ob, bm, 30, True)

for e in bm.edges:
    if e in edges:
        e.select = True
    
    else:
        e.select = False

bm.select_flush(False)

finalize_bmesh(bm, ob)