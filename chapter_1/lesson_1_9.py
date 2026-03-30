import bpy
from .. import gui

class JKA_Lesson_1_9(bpy.types.Operator):
    bl_idname = "view3d.jka_lesson_1_9"
    bl_label = "1.9 Adding & Organizing"
    
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

        all_objs = context.scene.objects
        all_cols = bpy.data.collections

        # Step 1: Add Sphere
        if not self.task_add_sphere:
            if any("Sphere" in o.name for o in all_objs):
                self.task_add_sphere = True

        # Step 2: Create a NEW Empty Collection (Manually in Outliner or via M)
        elif self.task_add_sphere and not self.task_collection:
            # Check if a collection exists that is NOT the default 'Scene Collection' 
            # and is currently empty (to force the 'move' step later)
            extra_cols = [c for c in all_cols if c.name != "Collection"]
            if extra_cols:
                self.target_col_name = extra_cols[-1].name
                self.task_collection = True

        # Step 3: Move Sphere to that specific Collection
        elif self.task_collection and not self.task_move_to_col:
            sphere = next((o for o in all_objs if "Sphere" in o.name), None)
            if sphere:
                # Check if the sphere's users_collection contains our new collection
                col = all_cols.get(self.target_col_name)
                if col and sphere.name in col.objects:
                    self.task_move_to_col = True

        self.update_guide()
        return {'PASS_THROUGH'}

    def update_guide(self):
        if not self.task_add_sphere: 
            self.guide_text = "Add a UV Sphere: [Shift + A] > Mesh > UV Sphere"
        elif not self.task_collection: 
            self.guide_text = "Deselect the sphere, then Right-click in Outliner > New Collection"
        elif not self.task_move_to_col: 
            self.guide_text = f"Drag the Sphere into '{self.target_col_name}' in the Outliner"
        else: 
            self.guide_text = "Great! Keeping your Outliner organized is essential for JKA models."

    def draw_callback(self, context):
        intro = [
            (22, (0.2, 0.7, 1.0, 1), "LESSON 1.9: ADDING & ORGANIZING"),
            (16, (1, 1, 1, 1), "Primitives are the building blocks of your model."),
            (16, (1, 1, 1, 1), "When you're getting more accustomed to Blender, you will find uses for collections."),
            (16, (1, 1, 1, 1), "The last step can also be done by selecting an object and press M then Create new Collection."),
            (16, (1, 1, 1, 1), "TIP: To rename anything in Blender, you can select it and press F2.")
        ]
        tasks = [
            {"done": self.task_add_sphere, "label": "Add UV Sphere [Shift + A]"},
            {"done": self.task_collection, "label": "Create New Collection [M]"},
            {"done": self.task_move_to_col, "label": "Move Sphere to Collection"}
        ]
        gui.draw_lesson_ui(self, context, intro, tasks, self.guide_text)

    def invoke(self, context, event):
        self.cleanup(context)
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete()
        
        # Remove extra collections to start fresh
        for col in bpy.data.collections:
            if col.name != "Collection":
                bpy.data.collections.remove(col)

        self.task_add_sphere = self.task_collection = self.task_move_to_col = False
        self.target_col_name = ""
        self.update_guide()
        
        bpy.types.jka_draw_handler = bpy.types.SpaceView3D.draw_handler_add(
            self.draw_callback, (context,), 'WINDOW', 'POST_PIXEL'
        )
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

def register(): bpy.utils.register_class(JKA_Lesson_1_9)
def unregister(): bpy.utils.unregister_class(JKA_Lesson_1_9)
