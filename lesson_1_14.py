import bpy
from . import gui

class JKA_Lesson_1_14(bpy.types.Operator):
    bl_idname = "view3d.jka_lesson_1_14"
    bl_label = "1.14 Applying Transforms"
    
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
        if obj and obj.type == 'MESH':
            # Step 1: User must scale the object first
            if not self.task_scale_mod:
                # Check if any axis is significantly different from 1.0
                if any(abs(s - 1.0) > 0.5 for s in obj.scale):
                    self.task_scale_mod = True
                    self.update_guide()
            
            # Step 2: User must Apply the scale (resets scale to 1.0 while keeping size)
            elif self.task_scale_mod and not self.task_apply:
                # We check if the scale is exactly 1.0 (with a tiny margin for float errors)
                # But we only complete if the object is still large (meaning it was APPLIED, not RESET)
                is_scale_one = all(abs(s - 1.0) < 0.0001 for s in obj.scale)
                if is_scale_one:
                    self.task_apply = True
                    self.update_guide()

        return {'PASS_THROUGH'}

    def update_guide(self):
        if not self.task_scale_mod: 
            self.guide_text = "Scale the Cube [S] to make it much larger or smaller"
        elif not self.task_apply: 
            self.guide_text = "Now press [Ctrl + A] and select 'Scale' to freeze it to 1.0"
        else: 
            self.guide_text = "Perfect! The Scale is back to 1.0, keeping your mesh data healthy."

    def draw_callback(self, context):
        intro = [
            (22, (0.2, 0.7, 1.0, 1), "LESSON 1.14: APPLYING TRANSFORMS"),
            (16, (1, 1, 1, 1), "Non-uniform scale causes issues with tools."),
            (16, (1, 1, 1, 1), "Applying [Ctrl + A] 'bakes' the scale into the mesh DNA."),
            (16, (1, 1, 1, 1), "TIP: Did you know, you can also type value and press enter when transforming an object?."),
            (14, (0.8, 0.8, 0.8, 1), "Watch the 'Scale' values in the [N] panel at the Item tab during this lesson.")
        ]
        tasks = [
            {"done": self.task_scale_mod, "label": "Change Scale [S]"},
            {"done": self.task_apply, "label": "Apply Scale [Ctrl + A] > Scale"}
        ]
        gui.draw_lesson_ui(self, context, intro, tasks, self.guide_text)

    def invoke(self, context, event):
        self.cleanup(context)
        
        # Reset Scene
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        
        self.task_scale_mod = False
        self.task_apply = False
        self.update_guide()
        
        bpy.types.jka_draw_handler = bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback, (context,), 'WINDOW', 'POST_PIXEL'
        )
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

def register(): bpy.utils.register_class(JKA_Lesson_1_14)
def unregister(): bpy.utils.unregister_class(JKA_Lesson_1_14)
