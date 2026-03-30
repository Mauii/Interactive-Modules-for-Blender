import bpy
from .. import gui

class JKA_Lesson_1_1(bpy.types.Operator):
    bl_idname = "view3d.jka_lesson_1_1"
    bl_label = "1.1 Standard Views"
    
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
            if event.type == 'NUMPAD_1':
                if event.ctrl: self.task_back = True
                else: self.task_front = True
            elif event.type == 'NUMPAD_3':
                if event.ctrl: self.task_left = True
                else: self.task_right = True
            elif event.type == 'NUMPAD_7':
                if event.ctrl: self.task_bottom = True
                else: self.task_top = True
            self.update_guide()
        return {'PASS_THROUGH'}

    def update_guide(self):
        self.guide_text = "Use Numpad keys for Orthographic views"

    def draw_callback(self, context):
        intro = [(22, (0.2, 0.7, 1.0, 1), "LESSON 1.1: STANDARD VIEWS"), (16, (1, 1, 1, 1), "Fixed camera directions.")]
        tasks = [{"done": self.task_front, "label": "Front [1]"}, {"done": self.task_back, "label": "Back [Ctrl+1]"}, 
                 {"done": self.task_right, "label": "Right [3]"}, {"done": self.task_left, "label": "Left [Ctrl+3]"}, 
                 {"done": self.task_top, "label": "Top [7]"}, {"done": self.task_bottom, "label": "Bottom [Ctrl+7]"}]
        gui.draw_lesson_ui(self, context, intro, tasks, self.guide_text)

    def invoke(self, context, event):
        self.cleanup(context); self.task_front = self.task_back = self.task_right = self.task_left = self.task_top = self.task_bottom = False
        self.update_guide()
        bpy.types.jka_draw_handler = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback, (context,), 'WINDOW', 'POST_PIXEL')
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

def register(): bpy.utils.register_class(JKA_Lesson_1_1)
def unregister(): bpy.utils.unregister_class(JKA_Lesson_1_1)
