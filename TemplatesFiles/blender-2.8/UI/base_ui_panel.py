import bpy
from bpy.types import Operator

class CODE_OT_cube(Operator):
    bl_idname = "object.cube"
    bl_label = "Cube"
    bl_description = ""
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add()
        
        return {"FINISHED"}

class PANEL_PT__test(bpy.types.Panel):
    bl_label = "Panel"
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = "VIEW_3D"
    bl_category = "Test"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.cube", text="Add Cube", icon='MESH_CUBE')


classes = ( CODE_OT_cube, PANEL_PT__test )

register, unregister = bpy.utils.register_classes_factory(classes)
    
if __name__ == "__main__":
    register()

