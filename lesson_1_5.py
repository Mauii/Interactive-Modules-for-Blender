import bpy
from . import gui

class JKA_Lesson_1_5(bpy.types.Operator):
    bl_idname = "view3d.jka_lesson_1_5"
    bl_label = "1.5 Snapping Basics"
    
    def cleanup(self, context):
        if hasattr(bpy.types, "jka_draw_handler"):
            try: bpy.types.SpaceView3D.draw_handler_remove(bpy.types.jka_draw_handler, 'WINDOW')
            except: pass
            del bpy.types.jka_draw_handler
        for n in ["User_Cube", "TARGET_CUBE"]:
            if n in bpy.data.objects: bpy.data.objects.remove(bpy.data.objects[n], do_unlink=True)
        if context.area: context.area.tag_redraw()

    def modal(self, context, event):
        if context.area: context.area.tag_redraw()
        if event.type == 'ESC':
            self.cleanup(context)
            return {'CANCELLED'}

        if not self.task_snap_on:
            if context.scene.tool_settings.use_snap: self.task_snap_on = True
        elif not self.task_aligned:
            u, t = bpy.data.objects.get("User_Cube"), bpy.data.objects.get("TARGET_CUBE")
            if u and t and 1.99 < (u.location - t.location).length < 2.01: self.task_aligned = True
        
        self.update_guide(); return {'PASS_THROUGH'}

    def update_guide(self):
        if not self.task_snap_on: self.guide_text = "Enable Snapping [Shift + Tab]"
        elif not self.task_aligned: self.guide_text = "Align cube against target"

    def draw_callback(self, context):
        intro = [(22, (0.2, 0.7, 1.0, 1), "LESSON 1.5: SNAPPING"), (16, (1, 1, 1, 1), "Stick objects together perfectly.")]
        tasks = [{"done": self.task_snap_on, "label": "Enable Snap"}, {"done": self.task_aligned, "label": "Align"}]
        gui.draw_lesson_ui(self, context, intro, tasks, self.guide_text)

    def invoke(self, context, event):
        self.cleanup(context); bpy.ops.mesh.primitive_cube_add(location=(0,0,0)); u = context.active_object; u.name = "User_Cube"
        bpy.ops.mesh.primitive_cube_add(location=(4,0,0)); t = context.active_object; t.name = "TARGET_CUBE"
        m = bpy.data.materials.new(name="G"); m.diffuse_color=(1,.8,0,1); t.data.materials.append(m)
        self.task_snap_on = self.task_aligned = False; self.update_guide()
        bpy.types.jka_draw_handler = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback, (context,), 'WINDOW', 'POST_PIXEL')
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

def register(): bpy.utils.register_class(JKA_Lesson_1_5)
def unregister(): bpy.utils.unregister_class(JKA_Lesson_1_5)
