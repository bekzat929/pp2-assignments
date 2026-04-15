import pygame
import sys
from clock import MickeyClock

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
def main():
    pygame.init()

    background_path = "images/clock.png"
    right_hand_path = "images/right_hand.png"
    left_hand_path = "images/left_hand.png"

    temp_bg = pygame.image.load(background_path)
    width, height = temp_bg.get_size()

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Mickey's Clock")

    game_clock = pygame.time.Clock()
    mickey_clock = MickeyClock(screen, background_path, right_hand_path, left_hand_path)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        mickey_clock.draw()

        pygame.display.flip()
        game_clock.tick(1)  # update once per second

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()