import bpy
from .. import gui

class JKA_Lesson_1_12(bpy.types.Operator):
    bl_idname = "view3d.jka_lesson_1_12"
    bl_label = "1.12 Hierarchy & Parenting"
    
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

        child = bpy.data.objects.get("Child_Object")
        parent = bpy.data.objects.get("Parent_Object")

        if child and parent:
            # Step 1: Establish Parent-Child link
            if not self.task_parent:
                if child.parent == parent:
                    self.task_parent = True
                    self.update_guide()
            
            # Step 2: Unparent (Clear Parent)
            elif self.task_parent and not self.task_clear:
                if child.parent is None:
                    self.task_clear = True
                    self.update_guide()

        return {'PASS_THROUGH'}

    def update_guide(self):
        if not self.task_parent: 
            self.guide_text = "Select Child, then SHIFT-Select Parent. Press [Ctrl + P] > Object"
        elif not self.task_clear: 
            self.guide_text = "Now select the Child and press [Alt + P] > Clear Parent to break the link"
        else: 
            self.guide_text = "Mastered! Parenting is for moving parts, Joining is for merging meshes."

    def draw_callback(self, context):
        intro = [
            (22, (0.2, 0.7, 1.0, 1), "LESSON 1.12: HIERARCHY"),
            (16, (1, 1, 1, 1), "Parenting creates a link without merging the objects."),
            (16, (1, 1, 1, 1), "In the Outliner, the Child will now appear inside the Parent."),
            (16, (1, 1, 1, 1), "In later chapters, you will see the true use of this."),
            (16, (1, 1, 1, 1), "For now, when parenting an object to another, move the parent to see its effect.")
        ]
        tasks = [
            {"done": self.task_parent, "label": "Set Parent [Ctrl + P]"},
            {"done": self.task_clear, "label": "Clear Parent [Alt + P]"}
        ]
        gui.draw_lesson_ui(self, context, intro, tasks, self.guide_text)

    def invoke(self, context, event):
        self.cleanup(context)
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        
        # Parent Object
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        p = context.active_object
        p.name = "Parent_Object"
        
        # Child Object
        bpy.ops.mesh.primitive_cylinder_add(location=(3, 0, 0))
        c = context.active_object
        c.name = "Child_Object"
        c.scale = (0.5, 0.5, 1.5)
        
        bpy.ops.object.select_all(action='DESELECT')
        c.select_set(True) # Start with child selected for the student
        
        self.task_parent = self.task_clear = False
        self.update_guide()
        
        bpy.types.jka_draw_handler = bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback, (context,), 'WINDOW', 'POST_PIXEL'
        )
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

def register(): bpy.utils.register_class(JKA_Lesson_1_12)
def unregister(): bpy.utils.unregister_class(JKA_Lesson_1_12)
