import os
import bpy

"""This helps to import multiple dae files from a specific folder (or fbx with little tweaks).
   Ce script aide à l'import de plusieurs fichiers dae en même temps (ou FBX ou bidouillant un peu).
"""

path = r"C:\\Path\\To\\Folder\\dae"
folder = os.walk(path)

for (dirpath, dirname, filename) in os.walk(path):
    print("path > ", dirpath)
    # print("dir > ", dirname)
    # print("file > ", filename)
    
    for imp in filename:
        file = dirpath + "\\" + imp 
        print(file)
        # bpy.ops.import_scene.fbx(filepath = file)
        bpy.ops.wm.collada_import(filepath = file)