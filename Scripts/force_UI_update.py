""" by Wazou
        force redraw the UI
"""

for window in bpy.context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'VIEW_3D': # le type d'area que tu veux taguer
                    area.tag_redraw() 
            
            for region in area.regions:
               region.tag_redraw()