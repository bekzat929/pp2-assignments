import pygame
import sys
from db import init_db, get_or_create_player, get_leaderboard
from game import SnakeGame

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("Arial", 28)

init_db()

username = ""


def draw_text(text, x, y):
    img = font.render(text, True, (255,255,255))
    screen.blit(img, (x, y))


def menu():
    global username

    while True:
        screen.fill((0,0,0))

        draw_text("SNAKE GAME", 220, 50)
        draw_text("Type name:", 50, 120)
        draw_text(username, 200, 120)

        draw_text("Press ENTER to play", 180, 200)
        draw_text("L - Leaderboard", 180, 250)
        draw_text("ESC - Quit", 180, 300)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    if username != "":
                        return "play"

                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]

                elif event.key == pygame.K_l:
                    return "leaderboard"

                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                else:
                    username += event.unicode

        pygame.display.update()


def leaderboard():
    data = get_leaderboard()

    while True:
        screen.fill((0,0,0))

        draw_text("TOP 10", 250, 30)

        y = 80
        for row in data:
            draw_text(f"{row[0]} | {row[1]} | L{row[2]}", 100, y)
            y += 30

        draw_text("ESC - Back", 200, 350)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.update()


while True:
    action = menu()

    if action == "play":
        player_id = get_or_create_player(username)
        game = SnakeGame(screen, player_id, username)
        game.run()

    elif action == "leaderboard":
        leaderboard()