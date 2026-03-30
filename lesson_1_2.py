import bpy
from . import gui

class JKA_Lesson_1_2(bpy.types.Operator):
    bl_idname = "view3d.jka_lesson_1_2"
    bl_label = "1.2 Object Selection"
    
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

        active = context.view_layer.objects.active
        if active and active.select_get():
            if "Cube" in active.name: self.task_cube = True
            elif "Light" in active.name: self.task_light = True
            elif "Camera" in active.name: self.task_camera = True
            self.update_guide()
        return {'PASS_THROUGH'}

    def update_guide(self):
        if not self.task_cube: self.guide_text = "Select the Cube"
        elif not self.task_light: self.guide_text = "Select the Light"
        else: self.guide_text = "Select the Camera"

    def draw_callback(self, context):
        intro = [(22, (0.2, 0.7, 1.0, 1), "LESSON 1.2: SELECTION"), (16, (1, 1, 1, 1), "Left-click objects or use the Outliner.")]
        tasks = [{"done": self.task_cube, "label": "Cube"}, {"done": self.task_light, "label": "Light"}, {"done": self.task_camera, "label": "Camera"}]
        gui.draw_lesson_ui(self, context, intro, tasks, self.guide_text)

    def invoke(self, context, event):
        self.cleanup(context); self.task_cube = self.task_light = self.task_camera = False; self.update_guide()
        bpy.types.jka_draw_handler = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback, (context,), 'WINDOW', 'POST_PIXEL')
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

def register(): bpy.utils.register_class(JKA_Lesson_1_2)
def unregister(): bpy.utils.unregister_class(JKA_Lesson_1_2)
