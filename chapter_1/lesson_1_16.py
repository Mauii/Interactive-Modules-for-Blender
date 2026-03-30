import bpy
import mathutils
from .. import gui

class JKA_Lesson_1_16(bpy.types.Operator):
    bl_idname = "view3d.jka_lesson_1_16"
    bl_label = "1.16 Global vs Local"
    
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
        if not obj: return {'PASS_THROUGH'}

        # Step 1: Global Move
        if not self.task_global_test:
            if (obj.location - self.start_loc).length > 1.5:
                self.task_global_test = True
                # Reset start_loc for the next measurement
                self.start_loc = obj.location.copy()
                self.update_guide()

        # Step 2: Local Move (G + X + X)
        elif self.task_global_test and not self.task_move_local:
            move_vec = obj.location - self.start_loc
            if move_vec.length > 1.5:
                # Get Local X axis from the object's world matrix
                # matrix_world.to_quaternion() @ Vector(1,0,0) gives world-space direction of local X
                quat = obj.matrix_world.to_quaternion()
                local_x_axis = (quat @ mathutils.Vector((1.0, 0.0, 0.0))).normalized()
                
                current_move_dir = move_vec.normalized()
                # Check alignment using dot product
                dot = abs(current_move_dir.dot(local_x_axis))
                
                # 0.85 is a bit more forgiving for human movement
                if dot > 0.85:
                    self.task_move_local = True
                    self.update_guide()

        return {'PASS_THROUGH'}

    def update_guide(self):
        if not self.task_global_test: 
            self.guide_text = "Move the cube [G] along the RED axis. Notice it follows the world's grid."
        elif not self.task_move_local: 
            self.guide_text = "Now: Press [G], then [X] TWICE. Slide the cube along its OWN angle!"
        else: 
            self.guide_text = "Mastered! Local (G > X > X) is the fastest way to align parts."

    def draw_callback(self, context):
        intro = [
            (22, (0.2, 0.7, 1.0, 1), "LESSON 1.16: COORDINATE SYSTEMS"),
            (16, (1, 1, 1, 1), "Global: Movement follows the world's fixed grid."),
            (16, (1, 1, 1, 1), "Local: Movement follows the object's own tilted grid."),
            (14, (0.8, 0.8, 0, 1), "Tip: Local allows you to move parts along their natural length.")
        ]
        tasks = [
            {"done": self.task_global_test, "label": "Test Global Move [G]"},
            {"done": self.task_move_local, "label": "Move along Local [G] > [X, X]"}
        ]
        gui.draw_lesson_ui(self, context, intro, tasks, self.guide_text)

    def invoke(self, context, event):
        self.cleanup(context)
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        
        # Create tilted cube
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0), rotation=(0, 0.785, 0.785))
        self.start_loc = context.active_object.location.copy()
        
        self.task_global_test = self.task_move_local = False
        self.update_guide()
        
        bpy.types.jka_draw_handler = bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback, (context,), 'WINDOW', 'POST_PIXEL'
        )
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

def register(): bpy.utils.register_class(JKA_Lesson_1_16)
def unregister(): bpy.utils.unregister_class(JKA_Lesson_1_16)
