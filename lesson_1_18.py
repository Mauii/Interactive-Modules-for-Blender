import bpy
from . import gui

class JKA_Lesson_1_18(bpy.types.Operator):
    bl_idname = "view3d.jka_lesson_1_18"
    bl_label = "1.18 Annotations & Measuring"
    
    def cleanup(self, context):
        if hasattr(bpy.types, "jka_draw_handler"):
            try: bpy.types.SpaceView3D.draw_handler_remove(bpy.types.jka_draw_handler, 'WINDOW')
            except: pass
            del bpy.types.jka_draw_handler
            
        # Proper way to clear all annotation layers
        if context.annotation_data:
            while context.annotation_data.layers:
                context.annotation_data.layers.remove(context.annotation_data.layers[0])
        if context.area: context.area.tag_redraw()

    def modal(self, context, event):
        if context.area: context.area.tag_redraw()
        if event.type == 'ESC':
            self.cleanup(context)
            return {'CANCELLED'}

        # Get active tool info safely
        try:
            active_tool_id = context.workspace.tools.from_space_view3d_mode('OBJECT').idname.lower()
        except:
            active_tool_id = ""

        # Step 1: Activate Measure Tool
        if not self.task_tool:
            if "measure" in active_tool_id:
                self.task_tool = True
                self.update_guide()
        
        # Step 2: Snap-Measure (Detect CTRL + Mouse movement)
        elif self.task_tool and not self.task_measure:
            if event.ctrl and event.type == 'MOUSEMOVE':
                self.task_measure = True
                self.update_guide()

        # Step 3: Switch back to Selection Tool
        elif self.task_measure and not self.task_switch_back:
            if "select" in active_tool_id or "tweak" in active_tool_id:
                # Clear ruler-remnants by removing layers
                if context.annotation_data:
                    while context.annotation_data.layers:
                        context.annotation_data.layers.remove(context.annotation_data.layers[0])
                self.task_switch_back = True
                self.update_guide()

        # Step 4: Draw Annotation
        elif self.task_switch_back and not self.task_annotate:
            anno = context.annotation_data
            if anno and anno.layers:
                for layer in anno.layers:
                    for frame in layer.frames:
                        if len(frame.strokes) > 0:
                            self.task_annotate = True
                            self.update_guide()
                            return {'PASS_THROUGH'}

        return {'PASS_THROUGH'}

    def update_guide(self):
        if not self.task_tool: 
            self.guide_text = "Select the Ruler tool (bottom icon in toolbar)"
        elif not self.task_measure: 
            self.guide_text = "Hold [CTRL] and drag to Snap-Measure the Cylinder height"
        elif not self.task_switch_back: 
            self.guide_text = "Now select the 'Select Box' tool (top icon) or press [W]"
        elif not self.task_annotate: 
            self.guide_text = "Hold [D] and Left-Click to draw a note around the floating Cube"
        else: 
            self.guide_text = "Visual aids mastered! Chapter 1 is officially complete."

    def draw_callback(self, context):
        intro = [
            (22, (0.2, 0.7, 1.0, 1), "LESSON 1.18: VISUAL AIDS"),
            (16, (1, 1, 1, 1), "Measuring: Vital to ensure limbs have JKA proportions."),
            (16, (1, 1, 1, 1), "Annotations: Use [D] to draw notes for yourself or others."),
            (16, (1, 1, 1, 1), "TIP: Hover over a button to see if it has hotkeys which you can learn."),
            (16, (0.8, 0.8, 0, 1), "This lesson is considered the final of Chapter 1."),
            (16, (0.8, 0.8, 0, 1), "Great job for getting this far and thank you for your future work!")
        ]
        tasks = [
            {"done": self.task_tool, "label": "Activate Measure Tool"},
            {"done": self.task_measure, "label": "Snap-Measure [CTRL]"},
            {"done": self.task_switch_back, "label": "Switch back to Select"},
            {"done": self.task_annotate, "label": "Draw Annotation [D]"}
        ]
        gui.draw_lesson_ui(self, context, intro, tasks, self.guide_text)

    def invoke(self, context, event):
        self.cleanup(context)
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        
        bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, 2))
        context.active_object.dimensions = (0.5, 0.5, 4.0)
        bpy.ops.mesh.primitive_cube_add(location=(3, 0, 5))
        context.active_object.scale = (0.3, 0.3, 0.3)
        
        self.task_tool = self.task_measure = self.task_switch_back = self.task_annotate = False
        self.update_guide()
        
        bpy.types.jka_draw_handler = bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback, (context,), 'WINDOW', 'POST_PIXEL'
        )
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

def register(): bpy.utils.register_class(JKA_Lesson_1_18)
def unregister(): bpy.utils.unregister_class(JKA_Lesson_1_18)
