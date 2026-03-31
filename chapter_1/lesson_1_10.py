import bpy
from .. import gui

class JKA_Lesson_1_10(bpy.types.Operator):
    bl_idname = "view3d.jka_lesson_1_10"
    bl_label = "1.10 Origin Points"
    
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

        obj = bpy.data.objects.get("Origin_Cube")
        if obj:
            # Step 1: Cursor to Corner (Already learned in 1.7, but applied here)
            if not self.task_cursor:
                if (context.scene.cursor.location - obj.location).length > 0.5:
                    self.task_cursor = True

            # Step 2: Set Origin to Cursor
            elif self.task_cursor and not self.task_set_origin:
                # Check if origin is no longer at (0,0,0) relative to geometry
                if (obj.location - context.scene.cursor.location).length < 0.01:
                    self.task_set_origin = True

            # Step 3: Test Rotation
            elif self.task_set_origin and not self.task_rotate:
                if sum([abs(r) for r in obj.rotation_euler]) > 0.2:
                    self.task_rotate = True

        self.update_guide()
        return {'PASS_THROUGH'}

    def update_guide(self):
        if not self.task_cursor: self.guide_text = "Move the 3D Cursor to a corner of the Cube [Shift + Right-Click]"
        elif not self.task_set_origin: self.guide_text = "Right-Click Cube > Set Origin > Origin to 3D Cursor"
        elif not self.task_rotate: self.guide_text = "Now Rotate [R] to see it pivot around the new point"
        else: self.guide_text = "Origins are the pivots of your model. Mastered!"

    def draw_callback(self, context):
        intro = [
            (22, (0.2, 0.7, 1.0, 1), "LESSON 1.10: ORIGIN POINTS"),
            (16, (1, 1, 1, 1), "The 'Origin' (orange dot) is the pivot point."),
            (16, (1, 1, 1, 1), "Essential for proper rotation of body parts.")
        ]
        tasks = [
            {"done": self.task_cursor, "label": "Position 3D Cursor"},
            {"done": self.task_set_origin, "label": "Set Origin to Cursor"},
            {"done": self.task_rotate, "label": "Test New Pivot Rotation"}
        ]
        gui.draw_lesson_ui(self, context, intro, tasks, self.guide_text)

    def invoke(self, context, event):
        self.cleanup(context)
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        bpy.ops.mesh.primitive_cube_add(location=(0,0,0))
        context.active_object.name = "Origin_Cube"
        context.scene.cursor.location = (0,0,0)
        
        self.task_cursor = self.task_set_origin = self.task_rotate = False
        self.update_guide()
        bpy.types.jka_draw_handler = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback, (context,), 'WINDOW', 'POST_PIXEL')
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

def register(): bpy.utils.register_class(JKA_Lesson_1_10)
def unregister(): bpy.utils.unregister_class(JKA_Lesson_1_10)
