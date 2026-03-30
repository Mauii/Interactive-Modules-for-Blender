import bpy
from . import gui

class JKA_Lesson_1_6(bpy.types.Operator):
    bl_idname = "view3d.jka_lesson_1_6"
    bl_label = "1.6 Join & Separate"
    
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

        # Step 1: Join Check (Automatic)
        mesh_count = len([o for o in context.scene.objects if o.type == 'MESH'])
        if not self.task_join and mesh_count == 1:
            self.task_join = True
            self.update_guide()
        
        if event.value == 'PRESS':
            # Step 2: Enter Edit Mode
            if self.task_join and not self.task_edit_in:
                if event.type == 'TAB' and context.mode == 'OBJECT':
                    self.task_edit_in = True
            
            # Step 3: Selection Logic
            elif self.task_edit_in and not self.task_select:
                if event.type == 'A':
                    if event.alt: self.has_deselected = True
                    elif self.has_deselected: self.task_select = True
            
            # Step 4: Separate
            elif self.task_select and not self.task_separate:
                if event.type == 'P':
                    self.task_separate = True
            
            # Step 5: Back to Object Mode
            elif self.task_separate and not self.task_obj_mode:
                if event.type == 'TAB' and context.mode.startswith('EDIT'):
                    self.task_obj_mode = True
        
        self.update_guide()
        return {'PASS_THROUGH'}

    def update_guide(self):
        if not self.task_join: self.guide_text = "Join the two cubes with [Ctrl + J]"
        elif not self.task_edit_in: self.guide_text = "Enter Edit Mode with [TAB]"
        elif not self.task_select: self.guide_text = "Deselect [Alt + A], then Select All [A]"
        elif not self.task_separate: self.guide_text = "Separate the part with [P] > Selection"
        elif not self.task_obj_mode: self.guide_text = "Return to Object Mode with [TAB]"

    def draw_callback(self, context):
        intro = [
            (22, (0.2, 0.7, 1.0, 1), "LESSON 1.6: JOIN & SEPARATE"),
            (16, (1, 1, 1, 1), "Merging and splitting meshes for kitbashing.")
        ]
        tasks = [
            {"done": self.task_join, "label": "Join [Ctrl + J]"},
            {"done": self.task_edit_in, "label": "Edit Mode [TAB]"},
            {"done": self.task_select, "label": "Deselect All [Alt + A], Select All [A]"},
            {"done": self.task_separate, "label": "Separate [P]"},
            {"done": self.task_obj_mode, "label": "Object Mode [TAB]"}
        ]
        gui.draw_lesson_ui(self, context, intro, tasks, self.guide_text)

    def invoke(self, context, event):
        self.cleanup(context)
        
        # Scene Setup
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        bpy.ops.mesh.primitive_cube_add(location=(0,0,0))
        bpy.ops.mesh.primitive_cube_add(location=(2.5,0,0))
        
        # Selection for Join
        for o in context.scene.objects: o.select_set(True)
        context.view_layer.objects.active = context.scene.objects[0]

        self.task_join = self.task_edit_in = self.task_select = False
        self.task_separate = self.task_obj_mode = self.has_deselected = False
        self.update_guide()
        
        bpy.types.jka_draw_handler = bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback, (context,), 'WINDOW', 'POST_PIXEL'
        )
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

def register(): bpy.utils.register_class(JKA_Lesson_1_6)
def unregister(): bpy.utils.unregister_class(JKA_Lesson_1_6)
