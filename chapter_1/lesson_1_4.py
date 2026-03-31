import bpy
from .. import gui

class JKA_Lesson_1_4(bpy.types.Operator):
    bl_idname = "view3d.jka_lesson_1_4"
    bl_label = "1.4 Basic Transformations"
    
    def cleanup(self, context):
        if hasattr(bpy.types, "jka_draw_handler"):
            try: bpy.types.SpaceView3D.draw_handler_remove(bpy.types.jka_draw_handler, 'WINDOW')
            except: pass
            del bpy.types.jka_draw_handler
        for n in ["Practice_Cube", "Pivot_Reference"]:
            if n in bpy.data.objects:
                bpy.data.objects.remove(bpy.data.objects[n], do_unlink=True)
        if context.area: context.area.tag_redraw()

    def modal(self, context, event):
        if context.area: context.area.tag_redraw()
        if event.type == 'ESC':
            self.cleanup(context)
            return {'CANCELLED'}

        obj = bpy.data.objects.get("Practice_Cube")
        if obj:
            # 1. Transform Tasks
            if not self.task_move:
                if (obj.location - self.start_loc).length > 0.5: self.task_move = True
            elif not self.task_rotate:
                diff = sum([abs(a-b) for a,b in zip(obj.rotation_euler, self.start_rot)])
                if diff > 0.1: self.task_rotate = True
            elif not self.task_scale:
                diff = sum([abs(a-b) for a,b in zip(obj.scale, self.start_scale)])
                if diff > 0.1: self.task_scale = True
            
            # 2. Multi-Selection Task
            elif not self.task_select_all:
                if len(context.selected_objects) >= 2:
                    self.task_select_all = True

            # 3. Pivot Point Tasks
            elif not self.task_pivot_cursor:
                if context.scene.tool_settings.transform_pivot_point == 'CURSOR':
                    self.task_pivot_cursor = True
            elif not self.task_pivot_median:
                if context.scene.tool_settings.transform_pivot_point == 'MEDIAN_POINT':
                    self.task_pivot_median = True

        self.update_guide(); return {'PASS_THROUGH'}

    def update_guide(self):
        if not self.task_move: self.guide_text = "Move object [G]"
        elif not self.task_rotate: self.guide_text = "Rotate object [R]"
        elif not self.task_scale: self.guide_text = "Scale object [S]"
        elif not self.task_select_all: self.guide_text = "Select BOTH objects (Hold [Shift] + Click both)"
        elif not self.task_pivot_cursor: self.guide_text = "Set Pivot to '3D Cursor' [period .]"
        elif not self.task_pivot_median: self.guide_text = "Set Pivot back to 'Median Point'"
        else: self.guide_text = "Transformations and Pivots mastered! Press ESC."

    def draw_callback(self, context):
        intro = [
            (22, (0.2, 0.7, 1.0, 1), "LESSON 1.4: TRANSFORMS & PIVOTS"),
            (16, (1, 1, 1, 1), "Grab [G], Rotate [R], and Scale [S] are your core tools."),
            (16, (1, 1, 1, 1), "Pivot Points determine the center of your transformation."),
            (16, (1, 1, 1, 1), "Find the Pivot menu at the TOP CENTER of the viewport."),
            (16, (1, 1, 1, 1), "Median Point = Center of selection | 3D Cursor = Center of the red/white ring."),
            (16, (1, 1, 1, 1), "Make sure to try all of the options to see their functionality."),
            (16, (1, 1, 1, 1), "These functionalities can vary depending on amount of selected objects.")
        ]
        tasks = [
            {"done": self.task_move, "label": "Move [G]"},
            {"done": self.task_rotate, "label": "Rotate [R]"},
            {"done": self.task_scale, "label": "Scale [S]"},
            {"done": self.task_select_all, "label": "Select Multiple [Shift + Click]"},
            {"done": self.task_pivot_cursor, "label": "Switch Pivot to 3D Cursor"},
            {"done": self.task_pivot_median, "label": "Switch Pivot to Median Point"}
        ]
        gui.draw_lesson_ui(self, context, intro, tasks, self.guide_text)

    def invoke(self, context, event):
        self.cleanup(context)
        bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()
        
        # Create first object
        bpy.ops.mesh.primitive_cube_add(size=2, location=(-2, 0, 0))
        obj = context.active_object; obj.name = "Practice_Cube"
        
        # Create second object for pivot experimentation
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(2, 0, 0))
        ref = context.active_object; ref.name = "Pivot_Reference"
        
        # Deselect to force user to select
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        context.view_layer.objects.active = obj
        
        # Cursor for pivot exercise
        context.scene.cursor.location = (0, 3, 0)
        
        self.start_loc, self.start_rot, self.start_scale = obj.location.copy(), obj.rotation_euler.copy(), obj.scale.copy()
        self.task_move = self.task_rotate = self.task_scale = self.task_select_all = False
        self.task_pivot_cursor = self.task_pivot_median = False
        
        self.update_guide()
        bpy.types.jka_draw_handler = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback, (context,), 'WINDOW', 'POST_PIXEL')
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

def register(): bpy.utils.register_class(JKA_Lesson_1_4)
def unregister(): bpy.utils.unregister_class(JKA_Lesson_1_4)
