import bpy
from . import gui

class JKA_Lesson_1_11(bpy.types.Operator):
    bl_idname = "view3d.jka_lesson_1_11"
    bl_label = "1.11 Hiding & Unhiding"
    
    def cleanup(self, context):
        if hasattr(bpy.types, "jka_draw_handler"):
            try: bpy.types.SpaceView3D.draw_handler_remove(bpy.types.jka_draw_handler, 'WINDOW')
            except: pass
            del bpy.types.jka_draw_handler
        if context.area: context.area.tag_redraw()

    def modal(self, context, event):
        if context.area: context.area.tag_redraw()
        if event.type == 'ESC':
            self.cleanup(context)
            return {'CANCELLED'}

        # Get the specific objects we created for this lesson
        target_objs = [o for o in bpy.data.objects if "Hide_Me" in o.name]
        
        if not target_objs:
            return {'PASS_THROUGH'}

        # Step 1: Hide Check
        if not self.task_hide:
            # Check if ANY of our target objects are hidden
            if any(o.hide_get() for o in target_objs):
                self.task_hide = True
                self.update_guide()
        
        # Step 2: Unhide Check
        elif self.task_hide and not self.task_unhide:
            # Check if ALL our target objects are visible again
            if all(not o.hide_get() for o in target_objs):
                self.task_unhide = True
                self.update_guide()

        return {'PASS_THROUGH'}

    def update_guide(self):
        if not self.task_hide: 
            self.guide_text = "Select an object and press [H] to Hide it"
        elif not self.task_unhide: 
            self.guide_text = "Now press [Alt + H] to Unhide everything"
        else: 
            self.guide_text = "Visibility mastered! Use this to manage complex models."

    def draw_callback(self, context):
        intro = [
            (22, (0.2, 0.7, 1.0, 1), "LESSON 1.11: VISIBILITY"),
            (16, (1, 1, 1, 1), "Hide objects to see what's behind them."),
            (16, (1, 1, 1, 1), "[H] to Hide, [Alt + H] to Unhide.")
        ]
        tasks = [
            {"done": self.task_hide, "label": "Hide an object [H]"},
            {"done": self.task_unhide, "label": "Unhide all [Alt + H]"}
        ]
        gui.draw_lesson_ui(self, context, intro, tasks, self.guide_text)

    def invoke(self, context, event):
        self.cleanup(context)
        
        # Clear scene
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        
        # Create 3 cubes to practice with
        for i in range(3):
            bpy.ops.mesh.primitive_cube_add(location=(i*3 - 3, 0, 0))
            context.active_object.name = f"Hide_Me_{i}"
        
        self.task_hide = False
        self.task_unhide = False
        self.update_guide()
        
        bpy.types.jka_draw_handler = bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback, (context,), 'WINDOW', 'POST_PIXEL'
        )
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

def register(): bpy.utils.register_class(JKA_Lesson_1_11)
def unregister(): bpy.utils.unregister_class(JKA_Lesson_1_11)
