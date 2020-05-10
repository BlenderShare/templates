import bpy
import rna_keymap_ui

from bpy.types import Operator, Menu, AddonPreferences
from bpy.props import StringProperty


bl_info = {
    "name": "custom_keymaps_template",
    "description": "Single Line Explanation",
    "author": "Legigan Jeremy AKA Pistiwique$",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "View3D",
    "warning": "This is an unstable version",
    "wiki_url": "",
    "category": "Object"}


class TEST_OT_operator_cube_add(Operator):
    ''' Simple test operator '''
    bl_idname = 'object.cube_add'
    bl_label = "Add Cube"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        bpy.ops.mesh.primitive_cube_add()

        return {'FINISHED'}

class TEST_MT_menu_cube_add(Menu):
    ''' Simple test menu '''
    bl_label = "Menu Cube Add"

    def draw(self, context):
        layout = self.layout
        layout.operator('mesh.primitive_cube_add', text = "Add Cube",
                        icon = 'MESH_CUBE')


class TEST_MT_pie_menu_cube_add(Menu):
    ''' Simple test pie menu '''
    bl_label = "Pie Cube Add"

    def draw(self, context):
        pie = self.layout.menu_pie()
        pie.operator('mesh.primitive_cube_add', text = "Add Cube",
                        icon = 'MESH_CUBE')

class AddonKeymaps:
    _addon_keymaps = []
    _keymaps = {}

    @classmethod
    def new_keymap(cls, name, kmi_name, kmi_value=None, km_name='3D View',
                   space_type="VIEW_3D", region_type="WINDOW",
                   event_type=None, event_value=None, ctrl=False, shift=False,
                   alt=False, key_modifier="NONE"):
        """
        Adds a new keymap
        :param name: str, Name that will be displayed in the panel preferences
        :param kmi_name: str
                - bl_idname for the operators (exemple: 'object.cube_add')
                - 'wm.call_menu' for menu
                - 'wm.call_menu_pie' for pie menu
        :param kmi_value: str
                - class name for Menu or Pie Menu
                - None for operators
        :param km_name: str, keymap name (exemple: '3D View Generic')
        :param space_type: str, space type keymap is associated with, see:
                https://docs.blender.org/api/current/bpy.types.KeyMap.html?highlight=space_type#bpy.types.KeyMap.space_type
        :param region_type: str, region type keymap is associated with, see:
                https://docs.blender.org/api/current/bpy.types.KeyMap.html?highlight=region_type#bpy.types.KeyMap.region_type
        :param event_type: str, see:
                https://docs.blender.org/api/current/bpy.types.Event.html?highlight=event#bpy.types.Event.type
        :param event_value: str, type of the event, see:
                https://docs.blender.org/api/current/bpy.types.Event.html?highlight=event#bpy.types.Event.value
        :param ctrl: bool
        :param shift: bool
        :param alt: bool
        :param key_modifier: str, regular key pressed as a modifier
                https://docs.blender.org/api/current/bpy.types.KeyMapItem.html?highlight=modifier#bpy.types.KeyMapItem.key_modifier
        :return:
        """
        cls._keymaps.update({name: [kmi_name, kmi_value, km_name, space_type,
                                    region_type, event_type, event_value,
                                    ctrl, shift, alt, key_modifier]
                             })

    @classmethod
    def add_hotkey(cls, kc, keymap_name):

        items = cls._keymaps.get(keymap_name)
        if not items:
            return

        kmi_name, kmi_value, km_name, space_type, region_type = items[:5]
        event_type, event_value, ctrl, shift, alt, key_modifier = items[5:]
        km = kc.keymaps.new(name=km_name, space_type=space_type,
                            region_type=region_type)

        kmi = km.keymap_items.new(kmi_name, event_type, event_value,
                                  ctrl=ctrl,
                                  shift=shift, alt=alt,
                                  key_modifier=key_modifier
                                  )
        if kmi_value:
            kmi.properties.name = kmi_value

        kmi.active = True

        cls._addon_keymaps.append((km, kmi))

    @staticmethod
    def register_keymaps():
        wm = bpy.context.window_manager
        kc = wm.keyconfigs.addon
        # In background mode, there's no such thing has keyconfigs.user,
        # because headless mode doesn't need key combos.
        # So, to avoid error message in background mode, we need to check if
        # keyconfigs is loaded.
        if not kc:
            return

        for keymap_name in AddonKeymaps._keymaps.keys():
            AddonKeymaps.add_hotkey(kc, keymap_name)

    @classmethod
    def unregister_keymaps(cls):
        kmi_values = [item[1] for item in cls._keymaps.values() if item]
        kmi_names = [item[0] for item in cls._keymaps.values() if
                     item not in ['wm.call_menu', 'wm.call_menu_pie']]

        for km, kmi in cls._addon_keymaps:
            # remove addon keymap for menu and pie menu
            if hasattr(kmi.properties, 'name'):
                if kmi_values:
                    if kmi.properties.name in kmi_values:
                        km.keymap_items.remove(kmi)

            # remove addon_keymap for operators
            else:
                if kmi_names:
                    if kmi.idname in kmi_names:
                        km.keymap_items.remove(kmi)

        cls._addon_keymaps.clear()

    @staticmethod
    def get_hotkey_entry_item(name, kc, km, kmi_name, kmi_value, col):

        # for menus and pie_menu
        if kmi_value:
            for km_item in km.keymap_items:
                if km_item.idname == kmi_name and km_item.properties.name == kmi_value:
                    col.context_pointer_set('keymap', km)
                    rna_keymap_ui.draw_kmi([], kc, km, km_item, col, 0)
                    return

            col.label(text=f"No hotkey entry found for {name}")
            col.operator(TEMPLATE_OT_restore_hotkey.bl_idname,
                         text="Restore keymap",
                         icon='ADD').km_name = km.name

        # for operators
        else:
            if km.keymap_items.get(kmi_name):
                col.context_pointer_set('keymap', km)
                rna_keymap_ui.draw_kmi([], kc, km, km.keymap_items[kmi_name],
                                       col, 0)

            else:
                col.label(text=f"No hotkey entry found for {name}")
                col.operator(TEMPLATE_OT_restore_hotkey.bl_idname,
                             text="Restore keymap",
                             icon='ADD').km_name = km.name

    @staticmethod
    def draw_keymap_items(wm, layout):
        kc = wm.keyconfigs.user

        for name, items in AddonKeymaps._keymaps.items():
            kmi_name, kmi_value, km_name = items[:3]
            box = layout.box()
            split = box.split()
            col = split.column()
            col.label(text=name)
            col.separator()
            km = kc.keymaps[km_name]
            AddonKeymaps.get_hotkey_entry_item(name, kc, km, kmi_name,
                                             kmi_value, col)


class TEMPLATE_OT_restore_hotkey(Operator):
    bl_idname = "template.restore_hotkey"
    bl_label = "Restore hotkeys"
    bl_options = {'REGISTER', 'INTERNAL'}

    km_name: StringProperty()

    def execute(self, context):
        context.preferences.active_section = 'KEYMAP'
        wm = context.window_manager
        kc = wm.keyconfigs.addon
        km = kc.keymaps.get(self.km_name)
        if km:
            km.restore_to_default()
            context.preferences.is_dirty = True
        context.preferences.active_section = 'ADDONS'
        return {'FINISHED'}


class TestAddonPreferences(AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        wm = context.window_manager
        layout = self.layout

        AddonKeymaps.draw_keymap_items(wm, layout)

CLASSES = [TEST_OT_operator_cube_add,
           TEST_MT_menu_cube_add,
           TEST_MT_pie_menu_cube_add,
           TestAddonPreferences,
           TEMPLATE_OT_restore_hotkey]

def register():
    for cls in CLASSES:
       bpy.utils.register_class(cls)

    AddonKeymaps.new_keymap('Cube Operator', 'object.cube_add', None,
                            '3D View Generic', 'VIEW_3D', 'WINDOW', 'RIGHTMOUSE',
                            'PRESS', True, False, False, 'NONE'
                            )
    AddonKeymaps.new_keymap('Cube Menu', 'wm.call_menu', 'TEST_MT_menu_cube_add',
                            '3D View Generic', 'VIEW_3D', 'WINDOW', 'RIGHTMOUSE',
                            'PRESS', True, True, False, 'NONE'
                            )
    AddonKeymaps.new_keymap('Cube Pie Menu', 'wm.call_menu_pie',
                            'TEST_MT_pie_menu_cube_add', '3D View Generic',
                            'VIEW_3D', 'WINDOW', 'RIGHTMOUSE', 'PRESS', True,
                            True, True, 'NONE'
                            )

    AddonKeymaps.register_keymaps()

def unregister():
    AddonKeymaps.unregister_keymaps()
    for cls in CLASSES:
       bpy.utils.unregister_class(cls)