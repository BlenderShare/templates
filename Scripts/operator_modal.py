import bpy
from bpy.props import IntProperty, FloatProperty
from bpy_extras import view3d_utils

"""
    From Tricotou via Blenderlounge Discord
"""

def pick(context, event):
    # get the context arguments
    scene = context.scene
    region = context.region
    rv3d = context.space_data.region_3d
    coord = event.mouse_region_x, event.mouse_region_y
    viewlayer = bpy.context.view_layer

    # get the ray from the viewport and mouse
    view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
    ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)
    ray_target = ray_origin + (view_vector *-10)
    ray_goal = ray_origin + (view_vector *10000)

    # get and select object
    result, location, normal, index, obj, matrix = scene.ray_cast(viewlayer, ray_target, ray_goal)
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    
class ModalOperator(bpy.types.Operator):
    """Move an object with the mouse, example"""
    bl_idname = "object.modal_operator"
    bl_label = "Simple Modal Operator"

    first_mouse_x: IntProperty()
    first_value: FloatProperty()

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':
            delta = self.first_mouse_x - event.mouse_x
            context.object.location.x = self.first_value + delta * 0.01

        elif event.type == 'LEFTMOUSE':
            pick(context, event)
            return {'RUNNING_MODAL'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            context.object.location.x = self.first_value
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.object:
            self.first_mouse_x = event.mouse_x
            self.first_value = context.object.location.x

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "No active object, could not finish")
            return {'CANCELLED'}


def register():
    bpy.utils.register_class(ModalOperator)


def unregister():
    bpy.utils.unregister_class(ModalOperator)


if __name__ == "__main__":
    register()

    # test call
    #bpy.ops.object.modal_operator('INVOKE_DEFAULT')
