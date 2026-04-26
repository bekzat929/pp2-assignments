import pygame
from datetime import datetime

# ---------------- LINE ----------------
def draw_line(surface, color, start, end, thickness):
    pygame.draw.line(surface, color, start, end, thickness)

# ---------------- PENCIL ----------------
def draw_pencil(surface, color, prev_pos, current_pos, thickness):
    if prev_pos is not None:
        pygame.draw.line(surface, color, prev_pos, current_pos, thickness)

# ---------------- FLOOD FILL ----------------
def flood_fill(surface, x, y, new_color):
    width, height = surface.get_size()
    target_color = surface.get_at((x, y))

    if target_color == new_color:
        return

    stack = [(x, y)]

    while stack:
        px, py = stack.pop()

        if px < 0 or py < 0 or px >= width or py >= height:
            continue

        if surface.get_at((px, py)) != target_color:
            continue

        surface.set_at((px, py), new_color)

        stack.append((px + 1, py))
        stack.append((px - 1, py))
        stack.append((px, py + 1))
        stack.append((px, py - 1))

# ---------------- SAVE ----------------
def save_canvas(surface):
    filename = datetime.now().strftime("drawing_%Y-%m-%d_%H-%M-%S.png")
    pygame.image.save(surface, filename)
    print("Saved:", filename)

# ---------------- TEXT ----------------
def render_text(surface, text, font, color, position):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)