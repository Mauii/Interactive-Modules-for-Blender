import bpy, blf, gpu
from gpu_extras.batch import batch_for_shader

def draw_rect_clean(x, y, w, h, color):
    shader = gpu.shader.from_builtin('UNIFORM_COLOR')
    vertices = ((x, y), (x + w, y), (x + w, y + h), (x, y + h))
    indices = ((0, 1, 2), (0, 2, 3))
    batch = batch_for_shader(shader, 'TRIS', {"pos": vertices}, indices=indices)
    gpu.state.blend_set('ALPHA')
    shader.bind()
    shader.uniform_float("color", color)
    batch.draw(shader)

def draw_lesson_ui(self, context, intro_text, tasks, guide_text):
    font_id = 0
    # Screen dimensions
    render_w = context.region.width
    render_h = context.region.height

    white, gold, gray = (1, 1, 1, 1), (1, 0.8, 0, 1), (0.4, 0.4, 0.4, 1)
    bg_color = (0.02, 0.02, 0.02, 0.8)

    # --- PANEL 1: INTRO (Centered Top) ---
    line_height_intro = 25
    max_w_intro = 0
    for size, color, text in intro_text:
        blf.size(font_id, size)
        max_w_intro = max(max_w_intro, blf.dimensions(font_id, text))
    
    c1_w = max_w_intro + 40
    c1_h = (len(intro_text) * line_height_intro) + 20
    
    # Calculate Center-Top position
    c1_x = (render_w / 2) - (c1_w / 2)
    c1_y = render_h - 50 # 50 pixels from top border
    
    draw_rect_clean(c1_x - 15, c1_y - c1_h + 20, c1_w, c1_h, bg_color)
    
    curr_y = c1_y - 5
    for size, color, text in intro_text:
        blf.size(font_id, size)
        blf.color(font_id, *color)
        blf.position(font_id, c1_x, curr_y, 0)
        blf.draw(font_id, text)
        curr_y -= line_height_intro

    # --- PANEL 2: GOALS (Bottom Left) ---
    line_height_task = 30
    goal_label = f"GOAL: {guide_text}"
    
    blf.size(font_id, 18)
    max_w_goal = blf.dimensions(font_id, goal_label)
    
    blf.size(font_id, 16)
    for t in tasks:
        task_text = f"[DONE] {t['label']}"
        max_w_goal = max(max_w_goal, blf.dimensions(font_id, task_text))
    
    c2_w = max_w_goal + 40
    c2_h = 60 + (len(tasks) * line_height_task) + 40
    
    # Position: Bottom Left with 30px padding
    c2_x = 30 
    c2_y = 30 + c2_h - 55 # Dynamic bottom-up position
    
    draw_rect_clean(c2_x - 15, c2_y - c2_h + 55, c2_w, c2_h, bg_color)
    
    blf.color(font_id, *gold)
    blf.size(font_id, 18)
    blf.position(font_id, c2_x, c2_y + 20, 0)
    blf.draw(font_id, goal_label)

    curr_task_y = c2_y - 15
    for task in tasks:
        blf.color(font_id, *(gray if task["done"] else white))
        blf.size(font_id, 16)
        blf.position(font_id, c2_x + 10, curr_task_y, 0)
        status = "[DONE]" if task["done"] else "[    ]"
        blf.draw(font_id, f"{status} {task['label']}")
        curr_task_y -= line_height_task

    blf.color(font_id, 0.6, 0.6, 0.6, 1)
    blf.size(font_id, 13)
    footer_y = c2_y - c2_h + 65
    blf.position(font_id, c2_x + 10, footer_y, 0)
    blf.draw(font_id, "Press [ESC] to quit.")

    if all([t["done"] for t in tasks]):
        blf.color(font_id, 0.2, 1, 0.2, 1)
        blf.size(font_id, 20)
        blf.position(font_id, c2_x + 10, footer_y + 25, 0)
        blf.draw(font_id, "CHAPTER 1 COMPLETE!")
