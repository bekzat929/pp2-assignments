import pygame
import random
import json
import time
from db import save_game

CELL = 20
WIDTH, HEIGHT = 600, 400

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class SnakeGame:
    def __init__(self, screen, player_id, username):
        self.screen = screen
        self.player_id = player_id
        self.username = username

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)

        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = RIGHT

        self.food = self.spawn_food()
        self.poison = self.spawn_food()

        self.score = 0
        self.level = 1
        self.speed = 10

        self.game_over_flag = False

    def spawn_food(self):
        return (
            random.randint(0, 29) * CELL,
            random.randint(0, 19) * CELL
        )

    def draw(self):
        self.screen.fill((0, 0, 0))

        for x, y in self.snake:
            pygame.draw.rect(self.screen, (0, 255, 0), (x, y, CELL, CELL))

        pygame.draw.rect(self.screen, (255, 255, 0), (*self.food, CELL, CELL))
        pygame.draw.rect(self.screen, (255, 0, 0), (*self.poison, CELL, CELL))

        txt = self.font.render(f"Score: {self.score} Level: {self.level}", True, (255,255,255))
        self.screen.blit(txt, (10, 10))

    def move(self):
        head = self.snake[0]
        new_head = (head[0] + self.direction[0]*CELL,
                    head[1] + self.direction[1]*CELL)

        self.snake.insert(0, new_head)

        # food
        if new_head == self.food:
            self.score += 10
            self.food = self.spawn_food()
            if self.score % 50 == 0:
                self.level += 1
                self.speed += 2
        else:
            self.snake.pop()

        # poison
        if new_head == self.poison:
            self.snake = self.snake[:-2]
            self.poison = self.spawn_food()

            if len(self.snake) <= 1:
                self.game_over()

        # collision
        if (new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT):
            self.game_over()

        if new_head in self.snake[1:]:
            self.game_over()

    def game_over(self):
        self.game_over_flag = True
        save_game(self.player_id, self.score, self.level)

    def run(self):
        while not self.game_over_flag:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.direction = UP
                    if event.key == pygame.K_DOWN:
                        self.direction = DOWN
                    if event.key == pygame.K_LEFT:
                        self.direction = LEFT
                    if event.key == pygame.K_RIGHT:
                        self.direction = RIGHT

            self.move()
            self.draw()

            pygame.display.update()
            self.clock.tick(self.speed)