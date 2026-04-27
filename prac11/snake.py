# ==========================================
# 2. SNAKE GAME (Practice 9)
# ==========================================

import pygame
import random
import sys

pygame.init()

WIDTH = 600
HEIGHT = 600
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 25)

snake = [(100, 100)]
dx = CELL
dy = 0

score = 0

food_x = random.randrange(0, WIDTH, CELL)
food_y = random.randrange(0, HEIGHT, CELL)
food_weight = random.choice([1, 3, 5])
food_timer = pygame.time.get_ticks()

running = True

while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        dx = -CELL
        dy = 0
    if keys[pygame.K_RIGHT]:
        dx = CELL
        dy = 0
    if keys[pygame.K_UP]:
        dx = 0
        dy = -CELL
    if keys[pygame.K_DOWN]:
        dx = 0
        dy = CELL

    head = (snake[0][0] + dx, snake[0][1] + dy)
    snake.insert(0, head)

    # food eaten
    if head == (food_x, food_y):
        score += food_weight
        food_x = random.randrange(0, WIDTH, CELL)
        food_y = random.randrange(0, HEIGHT, CELL)
        food_weight = random.choice([1, 3, 5])
        food_timer = pygame.time.get_ticks()
    else:
        snake.pop()

    # food disappears after 5 sec
    if pygame.time.get_ticks() - food_timer > 5000:
        food_x = random.randrange(0, WIDTH, CELL)
        food_y = random.randrange(0, HEIGHT, CELL)
        food_weight = random.choice([1, 3, 5])
        food_timer = pygame.time.get_ticks()

    # wall collision
    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
        pygame.quit()
        sys.exit()

    # self collision
    if head in snake[1:]:
        pygame.quit()
        sys.exit()

    for part in snake:
        pygame.draw.rect(screen, (0, 255, 0), (part[0], part[1], CELL, CELL))

    pygame.draw.rect(screen, (255, 0, 0), (food_x, food_y, CELL, CELL))

    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    pygame.display.update()
    clock.tick(10)