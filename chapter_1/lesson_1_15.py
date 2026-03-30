import bpy
from .. import gui

class JKA_Lesson_1_15(bpy.types.Operator):
    bl_idname = "view3d.jka_lesson_1_15"
    bl_label = "1.15 Viewport Shading"
    
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

        shading = context.space_data.shading.type
        xray = context.space_data.shading.show_xray
        
        # Step 1: Wireframe (Z > Wireframe)
        if not self.task_wire:
            if shading == 'WIREFRAME': 
                self.task_wire = True
                self.update_guide()
        
        # Step 2: Back to Solid (Z > Solid)
        elif self.task_wire and not self.task_solid:
            if shading == 'SOLID' and not xray:
                self.task_solid = True
                self.update_guide()

        # Step 3: X-Ray (Alt + Z) - Now the contrast is clear!
        elif self.task_solid and not self.task_xray:
            if xray: 
                self.task_xray = True
                self.update_guide()
        
        # Step 4: Material Preview (Z > Material Preview)
        elif self.task_xray and not self.task_mat:
            if shading == 'MATERIAL': 
                self.task_mat = True
                self.update_guide()

        return {'PASS_THROUGH'}

    def update_guide(self):
        if not self.task_wire: 
            self.guide_text = "Switch to Wireframe: Press [Z] > 'Wireframe'"
        elif not self.task_solid: 
            self.guide_text = "Return to Solid: Press [Z] > 'Solid' (Notice you can't see the inner cube)"
        elif not self.task_xray: 
            self.guide_text = "Enable X-Ray: Press [Alt + Z] to see the hidden cube through the walls"
        elif not self.task_mat: 
            self.guide_text = "Switch to Material Preview: Press [Z] > 'Material Preview'"
        else: 
            self.guide_text = "Viewport mastered! You now know how to inspect your models."

    def draw_callback(self, context):
        intro = [
            (22, (0.2, 0.7, 1.0, 1), "LESSON 1.15: VIEWPORT SHADING"),
            (16, (1, 1, 1, 1), "Wireframe: See the skeleton of your mesh."),
            (16, (1, 1, 1, 1), "Solid: The standard work view."),
            (16, (1, 1, 1, 1), "X-Ray: Peek through surfaces to select internal parts."),
            (16, (1, 1, 1, 1), "In later chapters we will use this to edit an object e.g. an arm."),
            (16, (1, 1, 1, 1), "We do this, so we can actually 'sew' the arm on the torso without leaving gaps."),
            (14, (0.8, 0.8, 0.8, 1), "Tip: Use [Alt + Z] to toggle X-Ray quickly.")
        ]
        tasks = [
            {"done": self.task_wire, "label": "Switch to Wireframe [Z]"},
            {"done": self.task_solid, "label": "Return to Solid [Z]"},
            {"done": self.task_xray, "label": "Enable X-Ray [Alt + Z]"},
            {"done": self.task_mat, "label": "Material Preview [Z]"}
        ]
        gui.draw_lesson_ui(self, context, intro, tasks, self.guide_text)

    def invoke(self, context, event):
        self.cleanup(context)
        
        # Setup Demo: A cube inside a cube
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        bpy.data.objects[context.active_object.name].name = "Outer_Shell"
        
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        inner = context.active_object
        inner.name = "Inner_Core"
        inner.scale = (0.5, 0.5, 0.5)
        
        # Add a color to the inner core to make it stand out in Material Preview
        mat = bpy.data.materials.new(name="CoreColor")
        mat.diffuse_color = (1, 0, 0, 1) # Bright Red
        inner.data.materials.append(mat)

        self.task_wire = self.task_solid = self.task_xray = self.task_mat = False
        self.update_guide()
        
        bpy.types.jka_draw_handler = bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback, (context,), 'WINDOW', 'POST_PIXEL'
        )
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

def register(): bpy.utils.register_class(JKA_Lesson_1_15)
def unregister(): bpy.utils.unregister_class(JKA_Lesson_1_15)
