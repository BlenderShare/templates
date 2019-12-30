import bpy

"""

by using modulo and integer division, it allows you to easily align things on grid

index | index % 4 | index // 4
  0   |     0     |   0
  1   |     1     |   0
  2   |     2     |   0
  3   |     3     |   0
  4   |     0     |   1
  5   |     1     |   1
  6   |     2     |   1
  7   |     3     |   1
  
(seen on blender cloud : scripting for Artists tutorial)

"""


grid_size = 8
object_amount = 64

for i in range(object_amount):
    x = i % grid_size
    y = i // grid_size
    bpy.ops.mesh.primitive_cube_add(size=.1, location=(x,y,1))