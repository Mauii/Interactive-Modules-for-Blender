import bpy
import os
import re
import importlib

bl_info = {
    "name": "Interactive Lessons for Blender",
    "author": "Maui",
    "version": (1, 1),
    "blender": (5, 0, 0),
    "location": "View3D > Sidebar > Training Tab",
    "description": "Modular lessons for Blender & JKA which teaches you to use Blender in a unique and playful way.",
    "category": "Training",
}

# --- DISCOVERY LOGIC ---

def get_chapters_enum(self, context):
    items = []
    folder = os.path.dirname(__file__)
    if os.path.exists(folder):
        subdirs = sorted([d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d)) and d.startswith("chapter_")])
        for d in subdirs:
            name = d.replace("_", " ").title()
            items.append((d, name, f"Open {name}"))
    return items if items else [('NONE', 'No Chapters Found', '')]

def get_lessons_enum(self, context):
    items = []
    chapter = context.scene.jka_chapter_list
    if chapter == 'NONE':
        return [('NONE', 'Select a Chapter first', '')]
    
    chapter_folder = os.path.join(os.path.dirname(__file__), chapter)
    if os.path.exists(chapter_folder):
        files = [f for f in os.listdir(chapter_folder) if f.startswith("lesson_") and f.endswith(".py")]
        
        def natural_key(string_):
            return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]
        
        files.sort(key=natural_key)
        
        for f in files:
            identifier = f.replace(".py", "")
            full_path = os.path.join(chapter_folder, f)
            display_name = identifier.replace("_", " ").title()
            
            try:
                with open(full_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    match = re.search(r'bl_label\s*=\s*["\'](.*?)["\']', content)
                    if match:
                        display_name = match.group(1)
            except:
                pass
            items.append((identifier, display_name, ""))
            
    return items if items else [('NONE', 'No Lessons Found', '')]

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
        layout.label(text="Select a Chapter and Module")
        layout.label(text="May Blender be with you!")

        layout.separator()

        # Chapter Selection
        layout.label(text="1. Choose Chapter:")
        layout.prop(scene, "jka_chapter_list", text="")

        layout.separator()

        # Lesson Selection
        layout.label(text="2. Choose Lesson:")
        layout.prop(scene, "jka_lesson_list", text="")
        
        layout.separator()
        
        if scene.jka_lesson_list != 'NONE' and scene.jka_chapter_list != 'NONE':
            layout.operator("jka.start_lesson", text="Start Selected Lesson", icon='PLAY')
        else:
            layout.label(text="Please select a module", icon='INFO')

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
    bpy.types.Scene.jka_chapter_list = bpy.props.EnumProperty(
        name="Chapters", items=get_chapters_enum)
    
    bpy.types.Scene.jka_lesson_list = bpy.props.EnumProperty(
        name="Lessons", items=get_lessons_enum)

    for cls in classes:
        bpy.utils.register_class(cls)

    main_folder = os.path.dirname(__file__)
    for d in os.listdir(main_folder):
        if d.startswith("chapter_") and os.path.isdir(os.path.join(main_folder, d)):
            chapter_path = os.path.join(main_folder, d)
            for f in os.listdir(chapter_path):
                if f.startswith("lesson_") and f.endswith(".py"):
                    module_name = f"{__package__}.{d}.{f.replace('.py', '')}"
                    try:
                        mod = importlib.import_module(module_name)
                        if hasattr(mod, "register"):
                            mod.register()
                    except Exception as e:
                        print(f"JKA ERROR: Failed to load {f}: {e}")


def unregister():
    main_folder = os.path.dirname(__file__)
    for d in os.listdir(main_folder):
        if d.startswith("chapter_") and os.path.isdir(os.path.join(main_folder, d)):
            chapter_path = os.path.join(main_folder, d)
            for f in os.listdir(chapter_path):
                if f.startswith("lesson_") and f.endswith(".py"):
                    module_name = f".{d}.{f.replace('.py', '')}"
                    try:
                        mod = importlib.import_module(module_name, package=__package__)
                        if hasattr(mod, "unregister"):
                            mod.unregister()
                    except:
                        pass

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.jka_chapter_list
    del bpy.types.Scene.jka_lesson_list

if __name__ == "__main__":
    register()
