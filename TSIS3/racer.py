import pygame
import random

# Константы
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
LANES = [60, 160, 260, 360]

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type="oil"):
        super().__init__()
        self.type = type
        self.image = pygame.Surface((40, 40))
        self.image.fill((100, 100, 100)) # Пятно или преграда
        self.rect = self.image.get_rect()
        self.rect.center = (random.choice(LANES), -50)
        self.speed = 5

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, kind):
        super().__init__()
        self.kind = kind # "nitro", "shield", "repair"
        self.image = pygame.Surface((30, 30))
        colors = {"nitro": (255, 0, 0), "shield": (0, 0, 255), "repair": (0, 255, 0)}
        self.image.fill(colors[kind])
        self.rect = self.image.get_rect()
        self.rect.center = (random.choice(LANES), -50)
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.rect.move_ip(0, 5)
        # Исчезновение по таймауту (5 сек)
        if pygame.time.get_ticks() - self.spawn_time > 5000 or self.rect.top > SCREEN_HEIGHT:
            self.kill()