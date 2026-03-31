import bpy
from .. import gui

class JKA_Lesson_1_13(bpy.types.Operator):
    bl_idname = "view3d.jka_lesson_1_13"
    bl_label = "1.13 Selection Tools"
    
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

        selected_count = len(context.selected_objects)

        # Step 1: Box Select (B)
        if not self.task_box:
            if event.type == 'B' and event.value == 'PRESS':
                self.task_box = True
        
        # Step 2: Circle Select (C)
        elif self.task_box and not self.task_circle:
            if event.type == 'C' and event.value == 'PRESS':
                self.task_circle = True

        # Step 3: Select Multiple
        elif self.task_circle and not self.task_multi:
            if selected_count >= 5:
                self.task_multi = True

        self.update_guide()
        return {'PASS_THROUGH'}

    def update_guide(self):
        if not self.task_box: self.guide_text = "Press [B] for Box Select and drag over objects"
        elif not self.task_circle: self.guide_text = "Press [C] for Circle Select. Use Left-Click to paint selection"
        elif not self.task_multi: self.guide_text = "Use [B] or [C] to select at least 5 objects at once"
        else: self.guide_text = "Selection tools mastered! Use [ESC] or [Right-Click] to exit Circle mode."

    def draw_callback(self, context):
        intro = [
            (22, (0.2, 0.7, 1.0, 1), "LESSON 1.13: SELECTION TOOLS"),
            (16, (1, 1, 1, 1), "B = Box Select (standard drag)."),
            (16, (1, 1, 1, 1), "C = Circle Select (paint over objects)."),
            (16, (1, 1, 1, 1), "W = Cycle through selection tools in the toolbar.")
        ]
        tasks = [
            {"done": self.task_box, "label": "Activate Box Select [B]"},
            {"done": self.task_circle, "label": "Activate Circle Select [C]"},
            {"done": self.task_multi, "label": "Select 5+ objects at once"}
        ]
        gui.draw_lesson_ui(self, context, intro, tasks, self.guide_text)

    def invoke(self, context, event):
        self.cleanup(context)
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        for i in range(10):
            bpy.ops.mesh.primitive_cube_add(location=(i%4 * 2, i//4 * 2, 0))
            context.active_object.scale = (0.4, 0.4, 0.4)
        
        self.task_box = self.task_circle = self.task_multi = False
        self.update_guide()
        bpy.types.jka_draw_handler = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback, (context,), 'WINDOW', 'POST_PIXEL')
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

def register(): bpy.utils.register_class(JKA_Lesson_1_13)
def unregister(): bpy.utils.unregister_class(JKA_Lesson_1_13)
