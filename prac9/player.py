import pygame

class MusicPlayer:
    def __init__(self, playlist):
        pygame.mixer.init()
        self.playlist = playlist
        self.current = 0

    def load(self):
        pygame.mixer.music.load(self.playlist[self.current])

    def play(self):
        self.load()
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()

    def next(self):
        self.current += 1
        if self.current >= len(self.playlist):
            self.current = 0
        self.play()

    def previous(self):
        self.current -= 1
        if self.current < 0:
            self.current = len(self.playlist) - 1
        self.play()

    def get_current_track(self):
        return self.playlist[self.current]

    def get_position(self):
        return pygame.mixer.music.get_pos() // 1000  # секунды