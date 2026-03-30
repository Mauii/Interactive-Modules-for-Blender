import bpy
from . import gui

class JKA_Lesson_1_4(bpy.types.Operator):
    bl_idname = "view3d.jka_lesson_1_4"
    bl_label = "1.4 Basic Transformations"
    
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

        obj = context.active_object
        if obj:
            if not self.task_move and (obj.location - self.start_loc).length > 0.5: self.task_move = True
            elif self.task_move and not self.task_rotate:
                diff = sum([abs(a-b) for a,b in zip(obj.rotation_euler, self.start_rot)])
                if diff > 0.1: self.task_rotate = True
            elif self.task_rotate and not self.task_scale:
                diff = sum([abs(a-b) for a,b in zip(obj.scale, self.start_scale)])
                if diff > 0.1: self.task_scale = True
        
        self.update_guide(); return {'PASS_THROUGH'}

    def update_guide(self):
        if not self.task_move: self.guide_text = "Move object [G]"
        elif not self.task_rotate: self.guide_text = "Rotate object [R]"
        elif not self.task_scale: self.guide_text = "Scale object [S]"

    def draw_callback(self, context):
        intro = [(22, (0.2, 0.7, 1.0, 1), "LESSON 1.4: TRANSFORMS"), (16, (1, 1, 1, 1), "Grab, Rotate, Scale. Hold Shift for finetuning the transformations."), (16, (1, 1, 1, 1), "Left Click to confirm transformation.")]
        tasks = [{"done": self.task_move, "label": "Move [G]"}, {"done": self.task_rotate, "label": "Rotate [R]"}, {"done": self.task_scale, "label": "Scale [S]"}]
        gui.draw_lesson_ui(self, context, intro, tasks, self.guide_text)

    def invoke(self, context, event):
        obj = context.active_object
        if not obj: return {'CANCELLED'}
        self.cleanup(context); self.start_loc = obj.location.copy(); self.start_rot = obj.rotation_euler.copy(); self.start_scale = obj.scale.copy()
        self.task_move = self.task_rotate = self.task_scale = False; self.update_guide()
        bpy.types.jka_draw_handler = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback, (context,), 'WINDOW', 'POST_PIXEL')
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

def register(): bpy.utils.register_class(JKA_Lesson_1_4)
def unregister(): bpy.utils.unregister_class(JKA_Lesson_1_4)
