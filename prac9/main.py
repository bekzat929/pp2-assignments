import pygame
from player import MusicPlayer

pygame.init()

WIDTH, HEIGHT = 600, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

font = pygame.font.Font(None, 36)

playlist = [
    "music/track1.wav",
    "music/track2.wav"
]

player = MusicPlayer(playlist)

running = True
clock = pygame.time.Clock()

while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()

            if event.key == pygame.K_s:
                player.stop()

            if event.key == pygame.K_n:
                player.next()

            if event.key == pygame.K_b:
                player.previous()

            if event.key == pygame.K_q:
                running = False

    # Текущий трек
    track_text = font.render(f"Track: {player.get_current_track()}", True, (0, 0, 0))
    screen.blit(track_text, (20, 50))

    # Время
    time_text = font.render(f"Time: {player.get_position()} s", True, (0, 0, 0))
    screen.blit(time_text, (20, 100))

    # Подсказки
    controls = font.render("P-Play S-Stop N-Next B-Back Q-Quit", True, (0, 0, 0))
    screen.blit(controls, (20, 200))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()