import bpy
from .. import gui

class JKA_Lesson_1_8(bpy.types.Operator):
    bl_idname = "view3d.jka_lesson_1_8"
    bl_label = "1.8 Duplicate & Instance"
    
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

        objs = [o for o in context.scene.objects if o.type == 'MESH']
        
        # Step 1: Normal Duplicate (Check for 2 objects with 2 unique meshes)
        if not self.task_duplicate:
            if len(objs) >= 2:
                unique_meshes = {o.data.name for o in objs}
                if len(unique_meshes) >= 2:
                    self.task_duplicate = True

        # Step 2: Linked Duplicate (Check for 3+ objects but fewer unique meshes)
        elif self.task_duplicate and not self.task_instance:
            if len(objs) >= 3:
                unique_meshes = {o.data.name for o in objs}
                # If we have 3 objects but only 2 mesh data blocks, an Alt+D was used
                if len(objs) > len(unique_meshes):
                    self.task_instance = True
                    # Store the name of the shared mesh to track changes
                    shared_mesh_names = [o.data.name for o in objs]
                    self.target_mesh_name = max(set(shared_mesh_names), key=shared_mesh_names.count)

        # Step 3: Verify link by renaming the shared Mesh Data
        elif self.task_instance and not self.task_check:
            # Check if the shared mesh data name has been changed by the user
            shared_data = bpy.data.meshes.get(self.target_mesh_name)
            if not shared_data:
                # If the original name is gone, it means it was renamed
                self.task_check = True

        self.update_guide()
        return {'PASS_THROUGH'}

    def update_guide(self):
        if not self.task_duplicate: 
            self.guide_text = "Select Cube and press [Shift + D] (Unique Copy)"
        elif not self.task_instance: 
            self.guide_text = "Select a Cube and press [Alt + D] (Linked Instance)"
        elif not self.task_check: 
            self.guide_text = "Go to 'Data' tab (Green Triangle) and Rename the Mesh"
        else: 
            self.guide_text = "Instances share everything except Object-level transforms!"

    def draw_callback(self, context):
        intro = [
            (22, (0.2, 0.7, 1.0, 1), "LESSON 1.8: DUPLICATION"),
            (16, (1, 1, 1, 1), "Shift+D = Full Copy."),
            (16, (1, 1, 1, 1), "Alt+D = Linked Data (Geometry stays synced)."),
            (16, (1, 1, 1, 1), "In the Outline, collapse the arrow on the left of the copy."),
            (16, (1, 1, 1, 1), "Now click on the JKA_Shared_Mesh and press F2, rename and press enter."),
            (16, (1, 1, 1, 1), "If you look at the copied object in the same place, you see the name changed there aswell.")
        ]
        tasks = [
            {"done": self.task_duplicate, "label": "Normal Duplicate [Shift+D]"},
            {"done": self.task_instance, "label": "Linked Duplicate [Alt+D]"},
            {"done": self.task_check, "label": "Rename Shared Mesh Data"}
        ]
        gui.draw_lesson_ui(self, context, intro, tasks, self.guide_text)

    def invoke(self, context, event):
        self.cleanup(context)
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        
        bpy.ops.mesh.primitive_cube_add(location=(0,0,0))
        # Give mesh a predictable name to track renaming
        context.active_object.data.name = "JKA_Shared_Mesh"
        
        self.task_duplicate = self.task_instance = self.task_check = False
        self.target_mesh_name = "JKA_Shared_Mesh"
        self.update_guide()
        
        bpy.types.jka_draw_handler = bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback, (context,), 'WINDOW', 'POST_PIXEL'
        )
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

def register(): bpy.utils.register_class(JKA_Lesson_1_8)
def unregister(): bpy.utils.unregister_class(JKA_Lesson_1_8)
