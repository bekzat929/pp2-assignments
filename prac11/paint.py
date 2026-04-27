# ==========================================
# 3. PAINT GAME (Practice 9)
# ==========================================

import pygame
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

screen.fill((255, 255, 255))

clock = pygame.time.Clock()

color = (0, 0, 0)
shape = "square"

running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                shape = "square"
            if event.key == pygame.K_2:
                shape = "right"
            if event.key == pygame.K_3:
                shape = "equal"
            if event.key == pygame.K_4:
                shape = "rhombus"

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if shape == "square":
                pygame.draw.rect(screen, color, (x, y, 60, 60), 2)

            elif shape == "right":
                points = [(x, y), (x, y+60), (x+60, y+60)]
                pygame.draw.polygon(screen, color, points, 2)

            elif shape == "equal":
                points = [(x, y), (x-30, y+60), (x+30, y+60)]
                pygame.draw.polygon(screen, color, points, 2)

            elif shape == "rhombus":
                points = [(x, y-40), (x-40, y), (x, y+40), (x+40, y)]
                pygame.draw.polygon(screen, color, points, 2)

    pygame.display.update()
    clock.tick(60)