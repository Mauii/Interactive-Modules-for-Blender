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
    
    # Get current window dimensions
    region_w = context.region.width
    region_h = context.region.height
    
    white, gold, gray = (1, 1, 1, 1), (1, 0.8, 0, 1), (0.4, 0.4, 0.4, 1)
    bg_color = (0.02, 0.02, 0.02, 0.8)
    margin = 40 # Padding from the screen edges

    # --- PANEL 1: INTRO (Top Center) ---
    line_height_intro = 25
    max_w_intro = 0
    for size, color, text in intro_text:
        blf.size(font_id, size)
        max_w_intro = max(max_w_intro, blf.dimensions(font_id, text)[0])
    
    c1_w = max_w_intro + 40
    c1_h = (len(intro_text) * line_height_intro) + 30
    
    # Calculate horizontal center and position near the top
    c1_x = (region_w / 2) - (c1_w / 2)
    c1_y = region_h - margin
    
    draw_rect_clean(c1_x, c1_y - c1_h, c1_w, c1_h, bg_color)
    
    curr_y = c1_y - 35
    for size, color, text in intro_text:
        blf.size(font_id, size)
        blf.color(font_id, *color)
        blf.position(font_id, c1_x + 20, curr_y, 0)
        blf.draw(font_id, text)
        curr_y -= line_height_intro

    # --- PANEL 2: GOALS (Bottom Left) ---
    line_height_task = 30
    goal_label = f"GOAL: {guide_text}"
    
    blf.size(font_id, 18)
    max_w_goal = blf.dimensions(font_id, goal_label)[0]
    
    blf.size(font_id, 16)
    for t in tasks:
        task_text = f"[DONE] {t['label']}"
        max_w_goal = max(max_w_goal, blf.dimensions(font_id, task_text)[0])
    
    c2_w = max_w_goal + 50
    c2_h = 80 + (len(tasks) * line_height_task) + 40
    
    # Position fixed at bottom left with margin
    c2_x = margin
    c2_y = margin + c2_h
    
    draw_rect_clean(c2_x, c2_y - c2_h, c2_w, c2_h, bg_color)
    
    # Draw Goal Header
    blf.color(font_id, *gold)
    blf.size(font_id, 18)
    blf.position(font_id, c2_x + 20, c2_y - 40, 0)
    blf.draw(font_id, goal_label)

    # Draw Tasks
    curr_task_y = c2_y - 80
    for task in tasks:
        blf.color(font_id, *(gray if task["done"] else white))
        blf.size(font_id, 16)
        blf.position(font_id, c2_x + 20, curr_task_y, 0)
        status = "[DONE]" if task["done"] else "[    ]"
        blf.draw(font_id, f"{status} {task['label']}")
        curr_task_y -= line_height_task

    # Footer (ESC info)
    blf.color(font_id, 0.6, 0.6, 0.6, 1)
    blf.size(font_id, 13)
    blf.position(font_id, c2_x + 20, c2_y - c2_h + 20, 0)
    blf.draw(font_id, "Press [ESC] to quit.")

    # Success Message
    if all([t["done"] for t in tasks]):
        blf.color(font_id, 0.2, 1, 0.2, 1)
        blf.size(font_id, 20)
        blf.position(font_id, c2_x + 20, c2_y - c2_h + 45, 0)
        blf.draw(font_id, "Module complete!")
