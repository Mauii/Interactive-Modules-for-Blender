import bpy
from .. import gui

class JKA_Lesson_1_17(bpy.types.Operator):
    bl_idname = "view3d.jka_lesson_1_17"
    bl_label = "1.17 Undo & History"
    
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

        # Step 1: Undo (Ctrl + Z)
        if not self.task_undo:
            if event.ctrl and event.type == 'Z' and event.value == 'PRESS':
                self.task_undo = True
                self.update_guide()
        
        # Step 2: Redo (Ctrl + Shift + Z)
        elif self.task_undo and not self.task_redo:
            if event.ctrl and event.shift and event.type == 'Z' and event.value == 'PRESS':
                self.task_redo = True
                self.update_guide()

        return {'PASS_THROUGH'}

    def update_guide(self):
        if not self.task_undo: 
            self.guide_text = "First, move the cube [G]. Then press [Ctrl + Z] to Undo"
        elif not self.task_redo: 
            self.guide_text = "Now press [Ctrl + Shift + Z] to Redo (bring the move back)"
        else: 
            self.guide_text = "Mistakes are part of the process. Undo is your best friend!"

    def draw_callback(self, context):
        intro = [
            (22, (0.2, 0.7, 1.0, 1), "LESSON 1.17: UNDO & REDO"),
            (16, (1, 1, 1, 1), "Ctrl + Z: Go back one step."),
            (16, (1, 1, 1, 1), "Ctrl + Shift + Z: Go forward one step (Redo)."),
            (14, (0.8, 0.8, 0, 1), "Tip: Look at 'Edit > Undo History' to see all recent actions.")
        ]
        tasks = [
            {"done": self.task_undo, "label": "Undo Action [Ctrl + Z]"},
            {"done": self.task_redo, "label": "Redo Action [Ctrl + Shift + Z]"}
        ]
        gui.draw_lesson_ui(self, context, intro, tasks, self.guide_text)

    def invoke(self, context, event):
        self.cleanup(context)
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        
        self.task_undo = self.task_redo = False
        self.update_guide()
        bpy.types.jka_draw_handler = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback, (context,), 'WINDOW', 'POST_PIXEL')
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

def register(): bpy.utils.register_class(JKA_Lesson_1_17)
def unregister(): bpy.utils.unregister_class(JKA_Lesson_1_17)
