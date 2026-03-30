import bpy
import os
import importlib

bl_info = {
    "name": "Interactive Modules for Blender",
    "author": "Maui",
    "version": (1, 0),
    "blender": (5, 0, 0),
    "location": "View3D > Sidebar > JKA Tab",
    "description": "Modular lessons for Blender & JKA which teaches you to use Blender in a unique and playful way.",
    "category": "Training",
}

# --- LESSON DISCOVERY ---
def get_lessons_enum(self, context):
    items = []
    folder = os.path.dirname(__file__)
    
    if os.path.exists(folder):
        files = sorted([f for f in os.listdir(folder) if f.startswith("lesson_") and f.endswith(".py")])
        
        for f in files:
            identifier = f.replace(".py", "")
            full_path = os.path.join(folder, f)
            
            # Default name based on filename
            display_name = identifier.replace("_", " ").title()
            
            # Try to extract bl_label from the file content
            try:
                with open(full_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    if 'bl_label' in content:
                        # Extract text between quotes after bl_label = 
                        import re
                        match = re.search(r'bl_label\s*=\s*["\'](.*?)["\']', content)
                        if match:
                            display_name = match.group(1)
            except Exception as e:
                print(f"JKA Error reading label from {f}: {e}")

            items.append((identifier, display_name, f"Start {display_name}"))
    
    if not items:
        return [('NONE', 'No Lessons Found', 'Add lesson_*.py files')]
        
    return items

# --- UI PANEL ---
class JKA_PT_MainPanel(bpy.types.Panel):
    bl_label = "Interactive Modules for Blender"
    bl_idname = "JKA_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Training'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        if not hasattr(scene, "jka_lesson_list"):
            layout.label(text="Initializing...")
            return

        layout.label(text="Welcome Jedi,")
        layout.label(text="Select a module")
        layout.label(text="Select Start Selected Lesson")
        layout.label(text="May Blender be with you!")

        layout.separator()

        layout.label(text="Training Modules:")
        
        row = layout.row(align=True)
        row.prop(scene, "jka_lesson_list", text="")
        
        layout.separator()
        
        try:
            current_selection = scene.jka_lesson_list
        except:
            return

        if current_selection != 'NONE':
            layout.operator("jka.start_lesson", text="Start Selected Lesson", icon='PLAY')
        else:
            layout.label(text="No modules found", icon='ERROR')

        layout.separator()

        layout.label(text="Didn't you learn enough?")
        layout.label(text="More modules available soon.")
        

# --- START OPERATOR ---
class JKA_OT_StartLesson(bpy.types.Operator):
    bl_idname = "jka.start_lesson"
    bl_label = "Start JKA Lesson"
    
    def execute(self, context):
        lesson_id = context.scene.jka_lesson_list
        if lesson_id == 'NONE':
            return {'CANCELLED'}

        operator_name = f"jka_{lesson_id}"
        
        try:
            op_func = getattr(bpy.ops.view3d, operator_name)
            op_func('INVOKE_DEFAULT')
        except AttributeError:
            self.report({'ERROR'}, f"Operator view3d.{operator_name} not found!")
            
        return {'FINISHED'}

# --- REGISTRATION ---
classes = (JKA_PT_MainPanel, JKA_OT_StartLesson)

def register():
    bpy.types.Scene.jka_lesson_list = bpy.props.EnumProperty(
        name="Lessons",
        items=get_lessons_enum
    )

    for cls in classes:
        bpy.utils.register_class(cls)

    folder = os.path.dirname(__file__)
    for f in os.listdir(folder):
        if f.startswith("lesson_") and f.endswith(".py"):
            module_name = f".{f.replace('.py', '')}"
            try:
                mod = importlib.import_module(module_name, package=__package__)
                if hasattr(mod, "register"):
                    mod.register()
            except Exception as e:
                print(f"JKA ERROR: Failed to load {f}: {e}")

def unregister():
    folder = os.path.dirname(__file__)
    for f in os.listdir(folder):
        if f.startswith("lesson_") and f.endswith(".py"):
            module_name = f".{f.replace('.py', '')}"
            try:
                mod = importlib.import_module(module_name, package=__package__)
                if hasattr(mod, "unregister"):
                    mod.unregister()
            except:
                pass

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    if hasattr(bpy.types.Scene, "jka_lesson_list"):
        del bpy.types.Scene.jka_lesson_list

if __name__ == "__main__":
    register()
