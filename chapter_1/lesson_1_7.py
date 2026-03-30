import bpy
from .. import gui

class JKA_Lesson_1_7(bpy.types.Operator):
    bl_idname = "view3d.jka_lesson_1_7"
    bl_label = "1.7 The 3D Cursor"
    
    def cleanup(self, context):
        if hasattr(bpy.types, "jka_draw_handler"):
            try: bpy.types.SpaceView3D.draw_handler_remove(bpy.types.jka_draw_handler, 'WINDOW')
            except: pass
            del bpy.types.jka_draw_handler
        for n in ["UC", "TC"]:
            if n in bpy.data.objects: bpy.data.objects.remove(bpy.data.objects[n], do_unlink=True)
        if context.area: context.area.tag_redraw()

    def modal(self, context, event):
        if context.area: context.area.tag_redraw()
        if event.type == 'ESC':
            self.cleanup(context)
            return {'CANCELLED'}

        cur = context.scene.cursor
        u, t = bpy.data.objects.get("UC"), bpy.data.objects.get("TC")
        if t and not self.task_cursor_move and (cur.location - t.location).length < 0.01: self.task_cursor_move = True
        elif self.task_cursor_move and u and not self.task_teleport and (u.location - cur.location).length < 0.01: self.task_teleport = True
        elif self.task_teleport and not self.task_reset and cur.location.length < 0.01: self.task_reset = True
        
        self.update_guide(); return {'PASS_THROUGH'}

    def update_guide(self):
        if not self.task_cursor_move: self.guide_text = "Snap Cursor to Target [Shift + S]"
        elif not self.task_teleport: self.guide_text = "Snap Cube to Cursor [Shift + S]"
        elif not self.task_reset: self.guide_text = "Reset Cursor [Shift + C]"

    def draw_callback(self, context):
        intro = [(22, (0.2, 0.7, 1.0, 1), "LESSON 1.7: 3D CURSOR"), (16, (1, 1, 1, 1), "Precise pivot management.")]
        tasks = [{"done": self.task_cursor_move, "label": "Cursor to Selection"}, {"done": self.task_teleport, "label": "Selection to Cursor"}, {"done": self.task_reset, "label": "Reset Cursor"}]
        gui.draw_lesson_ui(self, context, intro, tasks, self.guide_text)

    def invoke(self, context, event):
        self.cleanup(context); bpy.ops.mesh.primitive_cube_add(location=(-3,-3,0)); context.active_object.name="UC"
        bpy.ops.mesh.primitive_cube_add(location=(2,2,2)); t=context.active_object; t.name="TC"
        m=bpy.data.materials.new(name="G"); m.diffuse_color=(1,.8,0,1); t.data.materials.append(m)
        self.task_cursor_move = self.task_teleport = self.task_reset = False; self.update_guide()
        bpy.types.jka_draw_handler = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback, (context,), 'WINDOW', 'POST_PIXEL')
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

def register(): bpy.utils.register_class(JKA_Lesson_1_7)
def unregister(): bpy.utils.unregister_class(JKA_Lesson_1_7)
