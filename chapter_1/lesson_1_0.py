import bpy
from .. import gui

class JKA_Lesson_1_0(bpy.types.Operator):
    bl_idname = "view3d.jka_lesson_1_0"
    bl_label = "1.0 Camera Basics"
    
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

        if not self.task_orbit:
            if self.sub_state == "WAIT_CLICK" and event.type == 'MIDDLEMOUSE' and event.value == 'PRESS':
                self.sub_state = "WAIT_MOVE"; self.mouse_start_x = event.mouse_x
            elif self.sub_state == "WAIT_MOVE" and abs(event.mouse_x - self.mouse_start_x) > 50:
                self.task_orbit = True; self.sub_state = "PAN_CLICK"
        elif not self.task_pan:
            if self.sub_state == "PAN_CLICK" and event.shift and event.type == 'MIDDLEMOUSE' and event.value == 'PRESS':
                self.sub_state = "PAN_MOVE"; self.mouse_start_x = event.mouse_x
            elif self.sub_state == "PAN_MOVE" and abs(event.mouse_x - self.mouse_start_x) > 50:
                self.task_pan = True
        elif not self.task_zoom:
            if event.type in {'WHEELUPMOUSE', 'WHEELDOWNMOUSE'}:
                self.task_zoom = True
        
        self.update_guide()
        return {'PASS_THROUGH'}

    def update_guide(self):
        if not self.task_orbit: self.guide_text = "Hold [MMB] and Move to Orbit"
        elif not self.task_pan: self.guide_text = "Hold [Shift + MMB] to Pan"
        elif not self.task_zoom: self.guide_text = "Scroll Wheel to Zoom"

    def draw_callback(self, context):
        intro = [(22, (0.2, 0.7, 1.0, 1), "LESSON 1.0: CAMERA BASICS"), (16, (1, 1, 1, 1), "Master the 3D viewport navigation."), (16, (1, 1, 1, 1), "Henceforth experiment with everything I show you.")]
        tasks = [{"done": self.task_orbit, "label": "Orbit [MMB]"}, {"done": self.task_pan, "label": "Pan [Shift + MMB]"}, {"done": self.task_zoom, "label": "Zoom [Scroll wheel]"}]
        gui.draw_lesson_ui(self, context, intro, tasks, self.guide_text)

    def invoke(self, context, event):
        self.cleanup(context)
        self.task_orbit = self.task_pan = self.task_zoom = False
        self.sub_state = "WAIT_CLICK"; self.update_guide()
        bpy.types.jka_draw_handler = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback, (context,), 'WINDOW', 'POST_PIXEL')
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

def register(): bpy.utils.register_class(JKA_Lesson_1_0)
def unregister(): bpy.utils.unregister_class(JKA_Lesson_1_0)
