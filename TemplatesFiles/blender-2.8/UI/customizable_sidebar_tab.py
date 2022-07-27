bl_info = {
    "name": "Cuztomizable Sidebar Tab",
    "author": "Your Name Here",
    "version": (1, 0),
    "blender": (3, 2, 0),
    "location": "View3D > Sidebar",
    "description": "Adds a new Mesh Object",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}


import bpy
from bpy.types import Operator, Panel, AddonPreferences
from bpy.props import FloatVectorProperty, StringProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector


class OBJECT_OT_cube(Operator):
    bl_idname = "object.cube"
    bl_label = "Cube"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add()
        
        return {"FINISHED"}

# Interface Panel   
class VIEW3D_PT__test(Panel):
    bl_label = "Panel"
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = "VIEW_3D"
    # Put your default sidebar tab name here
    bl_category = "Tools"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.cube", text="Add Cube", icon='MESH_CUBE')
        
# Add-ons Preferences Update Panel

# Define Panel classes for updating
panels = (
        VIEW3D_PT__test,
        )
def update_panel(self, context):
    message = "Align Tools: Updating Panel locations has failed"
    try:
        for panel in panels:
            if "bl_rna" in panel.__dict__:
                bpy.utils.unregister_class(panel)

        for panel in panels:
            panel.bl_category = context.preferences.addons[__name__].preferences.category
            bpy.utils.register_class(panel)

    except Exception as e:
        print("\n[{}]\n{}\n\nError:\n{}".format(__name__, message, e))
        pass

# Interface Addon Preferences
class MyAddonPreferences(AddonPreferences):
    # this must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__

    category: StringProperty(
            name="Tab Category",
            description="Choose a name for the category of the panel",
            # Put your default sidebar tab name here
            default="Tools",
            update=update_panel
            )

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        col = row.column()
        col.label(text="Tab Category:")
        col.prop(self, "category", text="")


# Registration

classes = (
    OBJECT_OT_cube,
    VIEW3D_PT__test,
    MyAddonPreferences,
    )

register, unregister = bpy.utils.register_classes_factory(classes)


if __name__ == "__main__":
    register()
