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
    ui_scale = context.preferences.system.ui_scale
    
    white, gold, gray = (1, 1, 1, 1), (1, 0.8, 0, 1), (0.4, 0.4, 0.4, 1)
    bg_color = (0.02, 0.02, 0.02, 0.8)
    
    margin_left = 30 * ui_scale
    margin_bottom = 30 * ui_scale
    padding = 20 * ui_scale
    line_h_intro = 25 * ui_scale
    line_h_task = 30 * ui_scale

    # Check completion state
    is_done = all([t["done"] for t in tasks])

    # --- 1. INTRO PANEL SIZE ---
    max_w_intro = 0
    for size, color, text in intro_text:
        blf.size(font_id, int(size * ui_scale))
        width, height = blf.dimensions(font_id, text)
        if width > max_w_intro: max_w_intro = width
            
    c1_w = max_w_intro + (padding * 2)
    c1_h = (len(intro_text) * line_h_intro) + padding

    # --- 2. GOALS PANEL SIZE ---
    goal_label = f"GOAL: {guide_text}"
    blf.size(font_id, int(18 * ui_scale))
    max_w_goal, _ = blf.dimensions(font_id, goal_label)
    
    blf.size(font_id, int(16 * ui_scale))
    for t in tasks:
        task_str = f"[DONE] {t['label']}"
        tw, _ = blf.dimensions(font_id, task_str)
        if tw > max_w_goal: max_w_goal = tw
            
    c2_w = max_w_goal + (padding * 2)
    
    # Base height: Header + Tasks + Footer
    # If is_done, we add extra space (40px) for the "MODULE COMPLETE" message
    extra_space = 40 * ui_scale if is_done else 0
    c2_h = (len(tasks) * line_h_task) + (70 * ui_scale) + extra_space

    # --- 3. POSITIONING ---
    goals_y = margin_bottom
    intro_y = goals_y + c2_h + (15 * ui_scale)

    # --- 4. DRAW PANEL 2 (GOALS) ---
    draw_rect_clean(margin_left, goals_y, c2_w, c2_h, bg_color)
    
    # Goal title
    blf.size(font_id, int(18 * ui_scale))
    blf.color(font_id, *gold)
    blf.position(font_id, margin_left + padding, goals_y + c2_h - (35 * ui_scale), 0)
    blf.draw(font_id, goal_label)

    # Task list
    curr_y = goals_y + c2_h - (70 * ui_scale)
    blf.size(font_id, int(16 * ui_scale))
    for t in tasks:
        blf.color(font_id, *(gray if t["done"] else white))
        blf.position(font_id, margin_left + padding, curr_y, 0)
        status = "[DONE]" if t["done"] else "[    ]"
        blf.draw(font_id, f"{status} {t['label']}")
        curr_y -= line_h_task

    # Completion Message (Inserted between tasks and footer)
    if is_done:
        blf.size(font_id, int(20 * ui_scale))
        blf.color(font_id, 0.2, 1, 0.2, 1)
        blf.position(font_id, margin_left + padding, curr_y - (5 * ui_scale), 0)
        blf.draw(font_id, "MODULE COMPLETE!")

    # Footer (Always at the very bottom of the box)
    blf.size(font_id, int(12 * ui_scale))
    blf.color(font_id, 0.6, 0.6, 0.6, 1)
    blf.position(font_id, margin_left + padding, goals_y + (12 * ui_scale), 0)
    blf.draw(font_id, "Press [ESC] to quit.")

    # --- 5. DRAW PANEL 1 (INTRO) ---
    draw_rect_clean(margin_left, intro_y, c1_w, c1_h, bg_color)
    
    curr_y = intro_y + c1_h - (padding + 5 * ui_scale)
    for size, color, text in intro_text:
        blf.size(font_id, int(size * ui_scale))
        blf.color(font_id, *color)
        blf.position(font_id, margin_left + padding, curr_y, 0)
        blf.draw(font_id, text)
        curr_y -= line_h_intro
