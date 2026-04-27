# ==========================================
# 1. RACER GAME (Practice 9)
# ==========================================

import pygame
import random
import sys

pygame.init()

WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 25)

player = pygame.Rect(180, 500, 50, 80)
enemy = pygame.Rect(random.randint(50, 300), 0, 50, 80)

coin = pygame.Rect(random.randint(50, 350), -50, 30, 30)
coin_value = random.choice([1, 2, 5])

player_speed = 5
enemy_speed = 5
coins = 0

running = True

while running:
    screen.fill((100, 100, 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.x < WIDTH - 50:
        player.x += player_speed

    # enemy move
    enemy.y += enemy_speed
    if enemy.y > HEIGHT:
        enemy.y = 0
        enemy.x = random.randint(50, 300)

    # coin move
    coin.y += 4
    if coin.y > HEIGHT:
        coin.x = random.randint(50, 350)
        coin.y = -50
        coin_value = random.choice([1, 2, 5])

    # collision with coin
    if player.colliderect(coin):
        coins += coin_value
        coin.x = random.randint(50, 350)
        coin.y = -50
        coin_value = random.choice([1, 2, 5])

    # every 5 coins enemy faster
    if coins % 5 == 0 and coins != 0:
        enemy_speed = 5 + coins // 5

    # collision with enemy
    if player.colliderect(enemy):
        print("Game Over")
        pygame.quit()
        sys.exit()

    pygame.draw.rect(screen, (0, 0, 255), player)
    pygame.draw.rect(screen, (255, 0, 0), enemy)
    pygame.draw.circle(screen, (255, 255, 0), coin.center, 15)

    text = font.render(f"Coins: {coins}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    pygame.display.update()
    clock.tick(60)