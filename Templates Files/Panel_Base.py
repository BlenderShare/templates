import bpy


class Test_Code(bpy.types.Operator):
    bl_idname = "object.test_code"
    bl_label = "Test Code"
    bl_description = ""
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        return {"FINISHED"}


class Panel_Test_Code(bpy.types.Panel):
    '''Use this docstring to add a documentation or an information avaible
    inside blender API.'''
    bl_idname = "panel_test_code"
    bl_label = "Panel Test Code"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "category"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.test_code", text="Test Code", icon='TEXT')


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
