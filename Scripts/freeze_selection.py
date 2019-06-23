'''
Copyright (C) 2018 cedric lepiller
pitiwazou@hotmail.com

Created by cedric lepiller, tweaked by stephen-l

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import bpy
from bpy.types import (
    PropertyGroup, Operator, Panel, Menu, WindowManager
    )

    
class Freezer:
    
    freeze_list = []
    
    def freeze(self, context):
        _freeze = [o for o in context.selected_objects if not o.hide_select]
        for o in _freeze:
            o.hide_select = True
        self.freeze_list = _freeze
    
    def unfreeze(self):
        for o in self.freeze_list:
            o.hide_select = False
        self.freeze_list.clear()
        

# Freeze Selection
class TEST_CODE_OT_make_non_selectable(Freezer, Operator):
    bl_idname = "test_code.make_non_selectable"
    bl_label = "Make Selection Non Selectable"
    bl_description = ""
    bl_options = {"REGISTER"}

    def execute(self, context):
        self.freeze(context)
        return {"FINISHED"}

# Unfreeze Selection    
class TEST_CODE_OT_make_selectable(Freezer, Operator):
    bl_idname = "test_code.make_selectable"
    bl_label = "Make Selection Selectable"
    bl_description = "Make Selection Selectable"
    bl_options = {"REGISTER"}

    def execute(self, context):
        self.unfreeze() 
        return {"FINISHED"}

        
class PANEL_PT_easyref(Panel):
    bl_idname = "test_code"
    bl_label = "Test Code"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "TEST CODE"

    def draw(self, context):
        layout = self.layout
        split = layout.split()
        col = split.column(align=True)
        row = col.row(align=True)
        row.scale_y=1.5
        row.operator("test_code.make_non_selectable", text="Freeze Selection", icon='FREEZE')
        row = col.row(align=True)
        row.scale_y=1.5
        row.operator("test_code.make_selectable", text="Make Selectable", icon='FILE_TICK')

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
