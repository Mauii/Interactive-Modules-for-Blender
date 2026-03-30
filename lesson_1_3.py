import bpy
from . import gui

class JKA_Lesson_1_3(bpy.types.Operator):
    bl_idname = "view3d.jka_lesson_1_3"
    bl_label = "1.3 Focus & Isolation"
    
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

        if event.value == 'PRESS':
            if event.type in {'NUMPAD_PERIOD', 'PERIOD'}: self.task_frame = True
            if event.type in {'SLASH', 'NUMPAD_SLASH'}: self.task_isolate = True
            self.update_guide()
        return {'PASS_THROUGH'}

    def update_guide(self):
        if not self.task_frame: self.guide_text = "Select an object and press [Numpad .]"
        elif not self.task_isolate: self.guide_text = "Isolate it with [Numpad /]"

    def draw_callback(self, context):
        intro = [(22, (0.2, 0.7, 1.0, 1), "LESSON 1.3: FOCUS & ISOLATION"), (16, (1, 1, 1, 1), "Isolate parts for precision editing.")]
        tasks = [{"done": self.task_frame, "label": "Focus Selected [Numpad .]"}, {"done": self.task_isolate, "label": "Local View [Numpad /]"}]
        gui.draw_lesson_ui(self, context, intro, tasks, self.guide_text)

    def invoke(self, context, event):
        self.cleanup(context); self.task_frame = self.task_isolate = False; self.update_guide()
        bpy.types.jka_draw_handler = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback, (context,), 'WINDOW', 'POST_PIXEL')
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

def register(): bpy.utils.register_class(JKA_Lesson_1_3)
def unregister(): bpy.utils.unregister_class(JKA_Lesson_1_3)
