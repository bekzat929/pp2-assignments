import pygame
import sys

from tools import (
    draw_line,
    draw_pencil,
    flood_fill,
    save_canvas,
    render_text
)

pygame.init()

# ---------------- SCREEN ----------------
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint")

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))

# ---------------- VARIABLES ----------------
current_color = (0, 0, 0)
brush_size = 5

current_tool = "pencil"

drawing = False
prev_pos = None
start_pos = None

text_mode = False
text_input = ""
text_pos = (0, 0)

font = pygame.font.SysFont("Arial", 24)

# ---------------- MAIN LOOP ----------------
running = True

while running:

    screen.blit(canvas, (0, 0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # ---------------- KEYBOARD ----------------
        if event.type == pygame.KEYDOWN:

            # brush sizes
            if event.key == pygame.K_1:
                brush_size = 2
            if event.key == pygame.K_2:
                brush_size = 5
            if event.key == pygame.K_3:
                brush_size = 10

            # tools
            if event.key == pygame.K_p:
                current_tool = "pencil"
            if event.key == pygame.K_l:
                current_tool = "line"
            if event.key == pygame.K_f:
                current_tool = "fill"
            if event.key == pygame.K_t:
                current_tool = "text"

            # SAVE (Ctrl + S)
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_canvas(canvas)

            # TEXT INPUT
            if text_mode:
                if event.key == pygame.K_RETURN:
                    render_text(canvas, text_input, font, current_color, text_pos)
                    text_input = ""
                    text_mode = False

                elif event.key == pygame.K_ESCAPE:
                    text_input = ""
                    text_mode = False

                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]

                else:
                    text_input += event.unicode

        # ---------------- MOUSE DOWN ----------------
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if current_tool == "pencil":
                drawing = True
                prev_pos = (x, y)

            elif current_tool == "line":
                drawing = True
                start_pos = (x, y)

            elif current_tool == "fill":
                flood_fill(canvas, x, y, current_color)

            elif current_tool == "text":
                text_mode = True
                text_pos = (x, y)

        # ---------------- MOUSE UP ----------------
        if event.type == pygame.MOUSEBUTTONUP:

            if current_tool == "pencil":
                drawing = False
                prev_pos = None

            elif current_tool == "line":
                end_pos = event.pos
                draw_line(canvas, current_color, start_pos, end_pos, brush_size)
                drawing = False

    # ---------------- PENCIL DRAW ----------------
    if current_tool == "pencil" and drawing:
        x, y = pygame.mouse.get_pos()
        draw_pencil(canvas, current_color, prev_pos, (x, y), brush_size)
        prev_pos = (x, y)

    # ---------------- LINE PREVIEW ----------------
    if current_tool == "line" and drawing:
        temp = canvas.copy()
        pygame.draw.line(temp, current_color, start_pos, pygame.mouse.get_pos(), brush_size)
        screen.blit(temp, (0, 0))

    # ---------------- TEXT PREVIEW ----------------
    if text_mode:
        preview = font.render(text_input, True, current_color)
        screen.blit(preview, text_pos)

    pygame.display.update()

pygame.quit()
sys.exit()